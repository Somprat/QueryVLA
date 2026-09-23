"""CPU-only checks: python script/test_robofac_recovery.py."""
import importlib.util
import json
from pathlib import Path
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


diagnosis = load_module("diagnosis", "vla/failure_diagnosis.py")


def response(text, reason="stop"):
    body = {"choices": [{"message": {"content": text}, "finish_reason": reason}]}
    from io import BytesIO
    return BytesIO(json.dumps(body).encode())


class RecoveryTests(unittest.TestCase):
    def test_invalid_then_valid_response_retries(self):
        good = '{"failed":true,"failure_start_timestep":0,"failure_end_timestep":1,"failure_type":"slip","explanation":"The object falls from the gripper.","confidence":0.7}'
        with patch.object(diagnosis.request, "urlopen", side_effect=[response('{\r\n' * 100), response(good)]) as send, patch.object(diagnosis.time, "sleep"):
            result = diagnosis.diagnose_failure_with_robofac([np.zeros((2, 2, 3), dtype=np.uint8)] * 2)
        self.assertTrue(result["failed"])
        self.assertEqual(send.call_count, 2)
        payloads = [json.loads(call.args[0].data) for call in send.call_args_list]
        self.assertEqual([p["temperature"] for p in payloads], [0, 0.2])

    def test_exhausted_retries_have_short_error(self):
        with patch.object(diagnosis.request, "urlopen", side_effect=lambda *a, **kw: response('{\r\n' * 1000)) as send, patch.object(diagnosis.time, "sleep"):
            with self.assertRaises(diagnosis.RoboFACDiagnosisError) as caught:
                diagnosis.diagnose_failure_with_robofac([np.zeros((2, 2, 3), dtype=np.uint8)])
        self.assertEqual(send.call_count, 3)
        self.assertLess(len(str(caught.exception)), 300)
        self.assertEqual(len(caught.exception.raw_responses), 3)

    def test_length_limited_response_is_not_accepted(self):
        with patch.object(diagnosis.request, "urlopen", return_value=response('{"failed":false}', "length")):
            with self.assertRaises(diagnosis.RoboFACDiagnosisError):
                diagnosis.diagnose_failure_with_robofac([np.zeros((2, 2, 3), dtype=np.uint8)], max_attempts=1)

    def test_unsampled_bounds_retry_without_rounding(self):
        def answer(start, end):
            return response(json.dumps(dict(failed=True, failure_start_timestep=start,
                failure_end_timestep=end, failure_type="slip",
                explanation="The object falls after lifting.", confidence=0.7)))
        frames = [np.zeros((2, 2, 3), dtype=np.uint8)] * 80
        with patch.object(diagnosis.request, "urlopen", side_effect=[answer(0, 1), answer(33, 37)]) as send, patch.object(diagnosis.time, "sleep"):
            result = diagnosis.diagnose_failure_with_robofac(frames, task_instruction="put carrot in sink")
        self.assertEqual((result["failure_start_timestep"], result["failure_end_timestep"]), (33, 37))
        payload = json.loads(send.call_args_list[0].args[0].data)
        props = payload["response_format"]["json_schema"]["schema"]["properties"]
        self.assertEqual(props["failure_start_timestep"]["enum"], result["sampled_timesteps"])
        self.assertIn("put carrot in sink", payload["messages"][0]["content"][-1]["text"])
        self.assertEqual(len(result["raw_responses"]), 2)

    def test_repeated_initial_window_is_diagnosis_error(self):
        text = json.dumps(dict(failed=True, failure_start_timestep=0,
            failure_end_timestep=0, failure_type="misalignment",
            explanation="The gripper approaches the object.", confidence=0.1))
        with patch.object(diagnosis.request, "urlopen", side_effect=lambda *a, **kw: response(text)) as send, patch.object(diagnosis.time, "sleep"):
            with self.assertRaisesRegex(diagnosis.RoboFACDiagnosisError, "Initial-only"):
                diagnosis.diagnose_failure_with_robofac([np.zeros((2, 2, 3), dtype=np.uint8)] * 80)
        self.assertEqual(send.call_count, 3)

    def test_malformed_diagnoses_are_not_saved_as_unconfirmed(self):
        base = dict(failed=True, failure_start_timestep=1, failure_end_timestep=2,
                    failure_type="slip", explanation="The object falls.", confidence=0.7)
        cases = [dict(failure_start_timestep=2, failure_end_timestep=1),
                 dict(failure_start_timestep=1.5), dict(failure_start_timestep=True),
                 dict(failure_type=""), dict(explanation=" "), dict(failed="unknown"),
                 dict(confidence=float("nan")), dict(failure_start_timestep=-1)]
        for change in cases:
            with self.subTest(change=change), patch.object(diagnosis.request, "urlopen", side_effect=lambda *a, **kw: response(json.dumps({**base, **change}))):
                with self.assertRaises(diagnosis.RoboFACDiagnosisError):
                    diagnosis.diagnose_failure_with_robofac([np.zeros((2, 2, 3), dtype=np.uint8)] * 3, max_attempts=1)

    def test_unconfirmed_failure_does_not_need_bounds(self):
        with patch.object(diagnosis.request, "urlopen", return_value=response('{"failed":false}')) as send:
            result = diagnosis.diagnose_failure_with_robofac([np.zeros((2, 2, 3), dtype=np.uint8)])
        self.assertFalse(result["failed"])
        self.assertEqual(send.call_count, 1)

    def test_collection_saves_and_skips_diagnosis_failure(self):
        self.check_collection(False)

    def test_collection_saves_before_unexpected_error_propagates(self):
        self.check_collection(True)

    def check_collection(self, fatal):
        stubs = {}
        for name, attrs in {
            "collect_widowx_demos": dict(ROBOT_XY=None, UnstableLayoutError=type("UnstableLayoutError", (RuntimeError,), {}), _make_env=None, _randomize_training_layout=None),
            "maniskill2_evaluator": dict(_get_policy_observation=None),
            "training_tasks": dict(TRAINING_TASKS={"test_task": {}}),
            "vla_policy": dict(VLAInference=None),
        }.items():
            stubs[name] = ModuleType(name)
            stubs[name].__dict__.update(attrs)
        stubs["vla.failure_diagnosis"] = diagnosis
        with patch.dict("sys.modules", stubs):
            collector = load_module("collector", "evaluation/simpler_env/collect_failure_bank.py")
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "bank.pt"
            bank = SimpleNamespace(bank={}, episode_id=1)
            bank.save_bank = lambda path: Path(path).write_text(json.dumps(bank.bank))
            policy = SimpleNamespace(vla=SimpleNamespace(fail_episodic_bank=bank))
            args = SimpleNamespace(episodes_dir=None, output=output, checkpoint="unused", experiment_mode="full", max_failure_memories=512, episodes_per_task=3, max_episode_steps=80, task="all", seed=10)
            calls = []
            def collect(*unused, **kwargs):
                calls.append(1)
                if len(calls) == 1:
                    bank.bank[1] = "confirmed"
                    return False
                self.assertEqual(json.loads(output.read_text()), {"1": "confirmed"})
                if len(calls) == 2:
                    if fatal:
                        raise RuntimeError("unexpected")
                    raise diagnosis.RoboFACDiagnosisError("invalid diagnosis")
                return True
            with patch.object(collector, "parse_args", return_value=args), patch.object(collector, "VLAInference", return_value=policy), patch.object(collector, "collect_attempt", side_effect=collect):
                if fatal:
                    with self.assertRaisesRegex(RuntimeError, "unexpected"):
                        collector.main()
                else:
                    collector.main()
            self.assertEqual(json.loads(output.read_text()), {"1": "confirmed"})
            summary = json.loads(output.with_suffix('.json').read_text())
            self.assertEqual(summary["diagnosis_errors"], 0 if fatal else 1)
            self.assertEqual(summary["attempted_rollouts"], 1 if fatal else 3)
            self.assertFalse(output.with_suffix('.pt.tmp').exists())


if __name__ == "__main__":
    unittest.main()
