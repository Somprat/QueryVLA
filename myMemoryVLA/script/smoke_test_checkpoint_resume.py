"""Verify a tiny FSDP model takes the same next update after checkpoint resume.

Run from the repo root: .venv/bin/python -m script.smoke_test_checkpoint_resume
Requires one CUDA GPU; creates only temporary checkpoint files.
"""
from pathlib import Path
from tempfile import TemporaryDirectory

import torch
import torch.distributed as dist
from torch.distributed.fsdp import (
    FullyShardedDataParallel as FSDP,
    FullStateDictConfig,
    FullOptimStateDictConfig,
    StateDictType,
)

from training.strategies.fsdp import FSDPStrategy


def strategy():
    result = FSDPStrategy.__new__(FSDPStrategy)
    result.vlm = FSDP(torch.nn.Sequential(torch.nn.Linear(4, 2)).cuda(),
                      device_id=0, use_orig_params=True)
    result.optimizer = torch.optim.AdamW(result.vlm.parameters(), lr=0.01)
    result.lr_scheduler = torch.optim.lr_scheduler.StepLR(result.optimizer, 1, gamma=0.8)
    result.all_module_keys = result.trainable_module_keys = ["0"]
    result.fsdp_state_dict_type = StateDictType.FULL_STATE_DICT
    result.fsdp_save_policy = FullStateDictConfig(offload_to_cpu=True, rank0_only=True)
    result.fsdp_save_optimizer_policy = FullOptimStateDictConfig(offload_to_cpu=True, rank0_only=True)
    return result


def step(s, x):
    s.optimizer.zero_grad()
    loss = s.vlm(x).square().mean()
    loss.backward()
    s.optimizer.step()
    s.lr_scheduler.step()


def main():
    torch.cuda.set_device(0)
    with TemporaryDirectory() as tmp:
        dist.init_process_group("nccl", init_method=f"file://{tmp}/rendezvous", rank=0, world_size=1)
        try:
            original = strategy()
            x = torch.randn(3, 4, device="cuda")
            step(original, x)
            original.save_checkpoint(Path(tmp), 1, 0)
            checkpoint = next(Path(tmp).glob("checkpoints/*.pt"))
            metadata = torch.load(str(checkpoint.with_suffix(".optimizer")), mmap=True)
            assert (metadata["global_step"], metadata["epoch"]) == (1, 0)
            resumed = strategy()
            model = torch.load(checkpoint, map_location="cpu")["model"]
            resumed.vlm.module[0].load_state_dict(model["0"])
            resumed.load_optimizer_and_scheduler(str(checkpoint))
            assert resumed.lr_scheduler.state_dict() == original.lr_scheduler.state_dict()
            step(original, x)
            step(resumed, x)
            for a, b in zip(original.vlm.parameters(), resumed.vlm.parameters()):
                torch.testing.assert_close(a, b, rtol=0, atol=0)
            for state in resumed.optimizer.state.values():
                assert state["step"].item() == 2
            try:
                resumed.load_optimizer_and_scheduler(str(Path(tmp) / "missing.pt"))
            except FileNotFoundError:
                pass
            else:
                raise AssertionError("Missing optimizer state must fail")
            assert not list(Path(tmp).rglob("*.tmp"))
            print("PASS: resumed FSDP update matches uninterrupted update exactly; counters, scheduler, and missing-state checks pass")
        finally:
            dist.destroy_process_group()


if __name__ == "__main__":
    main()
