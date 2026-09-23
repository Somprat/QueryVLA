"""CPU checks of collection artifacts, including real MP4 encoding/decoding."""
import json
from pathlib import Path
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

import cv2
import numpy as np

from test_robofac_recovery import diagnosis, load_module


def load_collector():
    stubs = {}
    for name, attrs in {
        "collect_widowx_demos": dict(ROBOT_XY=[0, 0], UnstableLayoutError=type("UnstableLayoutError", (RuntimeError,), {}), _make_env=None, _randomize_training_layout=None),
        "maniskill2_evaluator": dict(_get_policy_observation=None),
        "training_tasks": dict(TRAINING_TASKS={"test_task": {}}),
        "vla_policy": dict(VLAInference=None),
    }.items():
        stubs[name] = ModuleType(name)
        stubs[name].__dict__.update(attrs)
    stubs["vla.failure_diagnosis"] = diagnosis
    with patch.dict("sys.modules", stubs):
        return load_module("collector_artifacts", "evaluation/simpler_env/collect_failure_bank.py")


class ArtifactTests(unittest.TestCase):
    def check_episode(self, outcome):
        collector = load_collector()
        env = SimpleNamespace(closed=False, frame=0)
        env.unwrapped = env
        env.tcp = SimpleNamespace(pose=SimpleNamespace(p=[0, 0, 0]))
        env.reset = lambda **kw: ({}, {})
        env.get_obs = lambda: {}
        env.get_wrapper_attr = lambda name: lambda obs: obs
        env.get_language_instruction = lambda: "put the test object in the sink"
        env.close = lambda: setattr(env, "closed", True)
        def step(command):
            env.frame += 1
            return {}, 0, outcome == "success" and env.frame == 3, env.frame == 3, {}
        env.step = step
        def observation(*args):
            return np.full((32, 32, 3), env.frame * 60, np.uint8), None, None, None
        bank = SimpleNamespace(bank={})
        model = SimpleNamespace(active_ep_contexts={7: {"fail_episode_id": 12}}, active_ep_id=7, fail_episodic_bank=bank)
        policy = SimpleNamespace(vla=model, use_spatial=False, reset=lambda instruction: None)
        action = dict(world_vector=np.zeros(3), rot_axangle=np.zeros(3), gripper=np.zeros(1))
        policy.step = lambda *args, **kw: ({}, action)
        expected = dict(failed=outcome == "stored", failure_start_timestep=1,
                        failure_end_timestep=2, explanation="The object slips.",
                        failure_type="slip", confidence=0.8, raw_response="original response")
        with tempfile.TemporaryDirectory() as temporary:
            stem = Path(temporary) / "test_task" / "seed_100"
            def finish(**kwargs):
                # Video and pending metadata must survive an API failure.
                self.assertTrue(stem.with_suffix('.mp4').exists())
                pending = json.loads(stem.with_suffix('.json').read_text())
                self.assertEqual(pending['policy_frame_count'], 3)
                self.assertEqual(len(kwargs['frames']), 3)
                if outcome == "diagnosis_error":
                    exc = diagnosis.RoboFACDiagnosisError("invalid bounds")
                    exc.raw_responses = ["raw invalid answer"]
                    raise exc
                if outcome == "unexpected_error":
                    raise RuntimeError("connection handler broke")
                if outcome == "stored":
                    bank.bank[12] = SimpleNamespace(cog_mem_bank=object(), per_mem_bank=object())
                return None if outcome == "success" else expected
            policy.finish_episode = finish
            randomize = lambda *args: None
            if outcome == "skipped_layout":
                def randomize(*args):
                    raise collector.UnstableLayoutError("unstable")
            with patch.object(collector, '_make_env', return_value=env), patch.object(collector, '_randomize_training_layout', side_effect=randomize), patch.object(collector, '_get_policy_observation', side_effect=observation):
                kwargs = dict(episode_path=stem, checkpoint='checkpoint.pt', bank_path=Path(temporary) / 'bank.pt')
                if outcome in {"diagnosis_error", "skipped_layout", "unexpected_error"}:
                    with self.assertRaises(RuntimeError):
                        collector.collect_attempt(policy, 'test_task', 100, 3, **kwargs)
                else:
                    self.assertEqual(collector.collect_attempt(policy, 'test_task', 100, 3, **kwargs), outcome == 'success')
            self.assertTrue(env.closed)
            record = json.loads(stem.with_suffix('.json').read_text())
            if outcome == "skipped_layout":
                self.assertIsNone(record['video'])
                self.assertFalse(stem.with_suffix('.mp4').exists())
                self.assertEqual(record['status'], 'skipped_layout')
                return
            cap = cv2.VideoCapture(str(stem.with_suffix('.mp4')))
            decoded = []
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                decoded.append(frame)
            cap.release()
            self.assertEqual(len(decoded), 4)
            self.assertEqual(record['video_frame_count'], 4)
            self.assertEqual(record['terminal_video_frame_index'], 3)
            self.assertEqual([a['policy_timestep'] for a in record['actions']], [0, 1, 2])
            self.assertEqual(record['video'], 'seed_100.mp4')
            self.assertEqual(record['bank_episode_id'], 12)
            for index, frame in enumerate(decoded):
                self.assertLess(abs(float(frame.mean()) - index * 60), 8)
            statuses = dict(success='success', stored='failure_stored', unconfirmed='failure_unconfirmed', diagnosis_error='diagnosis_error', unexpected_error='error')
            self.assertEqual(record['status'], statuses[outcome])
            self.assertEqual(record['failure_memory_stored'], outcome == 'stored')
            if outcome in {'stored', 'unconfirmed'}:
                self.assertEqual(record['diagnosis'], expected)
            if outcome == 'diagnosis_error':
                self.assertEqual(record['diagnosis_raw_responses'], ['raw invalid answer'])

    def test_stored_failure(self):
        self.check_episode('stored')

    def test_success(self):
        self.check_episode('success')

    def test_unconfirmed_failure(self):
        self.check_episode('unconfirmed')

    def test_diagnosis_error_keeps_video(self):
        self.check_episode('diagnosis_error')

    def test_unexpected_error_keeps_video(self):
        self.check_episode('unexpected_error')

    def test_skipped_layout_has_json_without_video(self):
        self.check_episode('skipped_layout')


if __name__ == '__main__':
    unittest.main()
