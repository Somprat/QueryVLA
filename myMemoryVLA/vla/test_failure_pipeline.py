from types import SimpleNamespace

import numpy as np
import torch
import torch.nn as nn

from vla.failure_diagnosis import parse_failure_diagnosis, sample_episode_frames
from vla.episodic.failfusion import FailAwareFusion
from vla.memory_vla import BankEntry, MemoryVLA


def _entry(timestep: int) -> BankEntry:
    return BankEntry(
        timestep=torch.tensor(timestep),
        feat=torch.full((1, 2), float(timestep)),
        image_embedding=None,
        task_tags=("test",),
    )


class _FailedBank:
    def __init__(self):
        self.bank = {12: object()}
        self.max_steps = 10
        self.completed = None

    def end_episode(self, **kwargs):
        self.completed = kwargs

    def kick_memory(self):
        raise AssertionError("capacity should not be exceeded")


class _CaptureFailureFusion(nn.Module):
    def __init__(self):
        super().__init__()
        self.seen_memory = None

    def forward(self, current, failure_memory):
        self.seen_memory = failure_memory
        risk = current.new_ones((*current.shape[:-1], 1))
        return current + 1, risk


def test_frame_sampling_preserves_policy_timestep_indices() -> None:
    frames = [np.zeros((2, 2, 3), dtype=np.uint8) for _ in range(120)]

    sampled = sample_episode_frames(frames, max_frames=20)

    assert len(sampled) == 20
    assert sampled[0][0] == 0
    assert sampled[-1][0] == 119


def test_diagnosis_parser_accepts_json_code_fences() -> None:
    diagnosis = parse_failure_diagnosis(
        '```json\n{"failed": true, "failure_start_timestep": 3, '
        '"failure_end_timestep": 5}\n```'
    )

    assert diagnosis["failure_start_timestep"] == 3
    assert diagnosis["failure_end_timestep"] == 5


def test_failure_aware_fusion_preserves_input_at_initialization() -> None:
    fusion = FailAwareFusion(dim=4)
    current = torch.randn(1, 1, 4)
    failure_memory = torch.randn(1, 3, 4)

    output, risk = fusion(current, failure_memory)

    assert output.shape == current.shape
    assert risk.shape == (1, 1, 1)
    assert torch.allclose(output, current)


def test_episodic_fusion_uses_failure_bank_internal_episode_id() -> None:
    model = MemoryVLA.__new__(MemoryVLA)
    nn.Module.__init__(model)
    model.active_ep_contexts = {
        7: {
            "cog": None,
            "per": None,
            "fail_episode_id": 12,
        }
    }
    failure_cog = torch.randn(1, 2, 4)
    failure_per = torch.randn(1, 2, 3)
    model.fail_active_ep_contexts = {
        12: {"cog": failure_cog, "per": failure_per}
    }
    model.cog_fail_fusion = _CaptureFailureFusion()
    model.per_fail_fusion = _CaptureFailureFusion()

    cog = torch.randn(1, 1, 4)
    per = torch.randn(1, 2, 3)
    fused_cog, fused_per = model._fuse_episodic_tokens(cog, per, [7])

    assert torch.equal(model.cog_fail_fusion.seen_memory, failure_cog)
    assert torch.equal(model.per_fail_fusion.seen_memory, failure_per)
    assert torch.allclose(fused_cog, cog + 1)
    assert torch.allclose(fused_per, per + 1)


def test_failed_episode_stores_only_timestep_aligned_window() -> None:
    model = MemoryVLA.__new__(MemoryVLA)
    nn.Module.__init__(model)
    model.use_episodic = True
    model.active_ep_id = 7
    model.active_ep_contexts = {
        7: {"bank_episode_id": 11, "fail_episode_id": 12, "instruction": "put carrot in sink"}
    }
    model.episode_recordings = {7: {"cog": [], "per": []}}
    model.fail_active_ep_contexts = {12: {"cog": None, "per": None}}
    entries = [_entry(timestep) for timestep in range(10)]
    model.fail_episode_recordings = {
        7: {"cog": entries, "per": list(entries)}
    }
    model.cog_mem_bank = SimpleNamespace(bank={})
    model.per_mem_bank = SimpleNamespace(bank={})
    model.success_episodic_bank = SimpleNamespace(
        bank={11: object()}, max_steps=10, kick_memory=lambda: None
    )
    model.fail_episodic_bank = _FailedBank()
    def diagnose(frames, task_instruction=None):
        assert task_instruction == "put carrot in sink"
        return {
            "failed": True,
            "failure_start_timestep": 3,
            "failure_end_timestep": 5,
        }

    model._diagnose_failed_episode = diagnose

    frames = [np.zeros((2, 2, 3), dtype=np.uint8) for _ in range(10)]
    returned_diagnosis = model.finish_episode(False, frames=frames)

    completed = model.fail_episodic_bank.completed
    assert completed is not None
    assert returned_diagnosis is completed["failure_diagnosis"]
    stored_timesteps = [
        int(entry.timestep) for entry in completed["episode_cog_banks"]
    ]
    assert stored_timesteps == list(range(1, 8))
    assert completed["failure_start_timestep"] == 3
    assert completed["failure_end_timestep"] == 5
    assert completed["failure_diagnosis"]["stored_start_timestep"] == 1
    assert completed["failure_diagnosis"]["stored_end_timestep"] == 7
    assert model.success_episodic_bank.bank == {}
