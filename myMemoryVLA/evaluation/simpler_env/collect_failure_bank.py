"""Collect RoboFAC-confirmed failures from training tasks into one bank file.

This intentionally uses ``training_tasks.py`` and its randomized training
layouts.  It never runs the official evaluation task grid.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import numpy as np

from collect_widowx_demos import (
    ROBOT_XY,
    UnstableLayoutError,
    _make_env,
    _randomize_training_layout,
)
from maniskill2_evaluator import _get_policy_observation
from training_tasks import TRAINING_TASKS
from vla_policy import VLAInference


def collect_attempt(policy, task_name: str, seed: int, max_episode_steps: int) -> bool:
    """Run one policy rollout and let MemoryVLA/RoboFAC store failed windows."""
    spec = TRAINING_TASKS[task_name]
    env = _make_env(spec)
    try:
        obs, _ = env.reset(
            seed=seed,
            options={
                "obj_init_options": {"episode_id": 0},
                "robot_init_options": {
                    "init_xy": np.asarray(ROBOT_XY),
                    "init_rot_quat": np.array([0.0, 0.0, 0.0, 1.0]),
                },
            },
        )
        base_env = env.unwrapped
        _randomize_training_layout(base_env, spec, np.random.default_rng(seed))
        obs = env.get_wrapper_attr("observation")(base_env.get_obs())
        instruction = base_env.get_language_instruction()
        policy.reset(instruction)

        image, depth, intrinsic, extrinsic = _get_policy_observation(
            env, obs, "3rd_view_camera", policy.use_spatial
        )
        frames: list[np.ndarray] = []
        done = False
        truncated = False
        first_frame = "True"
        for _ in range(max_episode_steps):
            raw_action, action = policy.step(
                image,
                depth,
                intrinsic,
                extrinsic,
                instruction,
                current_position=np.asarray(base_env.tcp.pose.p, dtype=np.float32),
                episode_first_frame=first_frame,
            )
            del raw_action
            frames.append(np.asarray(image).copy())
            first_frame = "False"

            obs, _, done, truncated, _ = env.step(
                np.concatenate(
                    [action["world_vector"], action["rot_axangle"], action["gripper"]]
                )
            )
            if done or truncated:
                break
            image, depth, intrinsic, extrinsic = _get_policy_observation(
                env, obs, "3rd_view_camera", policy.use_spatial
            )

        success = bool(done)
        # ``finish_episode`` runs RoboFAC only when this is a failed rollout,
        # then keeps the diagnosed timestep window in the failure bank.
        policy.finish_episode(success=success, frames=frames)
        return success
    finally:
        env.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True, help="VLA .pt checkpoint")
    parser.add_argument("--output", type=Path, required=True, help="Output .pt failure bank")
    parser.add_argument("--episodes-per-task", type=int, default=10)
    parser.add_argument("--max-episode-steps", type=int, default=80)
    parser.add_argument("--seed", type=int, default=100_000)
    parser.add_argument("--task", choices=("all", *TRAINING_TASKS), default="all")
    parser.add_argument("--experiment-mode", default="full")
    return parser.parse_args()


def main() -> None:
    os.environ.setdefault("DISPLAY", "")
    args = parse_args()
    if args.episodes_per_task < 1 or args.max_episode_steps < 1:
        raise ValueError("--episodes-per-task and --max-episode-steps must be positive")

    policy = VLAInference(
        saved_model_path=args.checkpoint,
        policy_setup="widowx_bridge",
        experiment_mode=args.experiment_mode,
    )
    # Collection starts with an empty failure bank.  This prevents a bank from
    # a previous run from silently contaminating this training-only artifact.
    policy.vla.fail_episodic_bank.bank.clear()
    policy.vla.fail_episodic_bank.episode_id = 1

    task_names = list(TRAINING_TASKS) if args.task == "all" else [args.task]
    attempts = 0
    rollout_failures = 0
    for task_index, task_name in enumerate(task_names):
        for attempt in range(args.episodes_per_task):
            seed = args.seed + task_index * args.episodes_per_task + attempt
            try:
                success = collect_attempt(
                    policy, task_name, seed, args.max_episode_steps
                )
            except UnstableLayoutError as exc:
                print(f"task={task_name} seed={seed} skipped_layout={exc}")
                continue
            attempts += 1
            rollout_failures += int(not success)
            print(f"task={task_name} seed={seed} success={success}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    policy.vla.fail_episodic_bank.save_bank(args.output)
    summary = {
        "scope": "training_tasks.py only",
        "tasks": task_names,
        "attempted_rollouts": attempts,
        "environment_failures": rollout_failures,
        "robofac_confirmed_memories": len(policy.vla.fail_episodic_bank.bank),
    }
    args.output.with_suffix(".json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(f"saved_failure_bank={args.output}")


if __name__ == "__main__":
    main()
