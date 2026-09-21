"""Collect RoboFAC-confirmed failures from training tasks into one bank file.

This intentionally uses ``training_tasks.py`` and its randomized training
layouts.  It never runs the official evaluation task grid.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from uuid import uuid4
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
from vla.failure_diagnosis import RoboFACDiagnosisError


def _write_episode_json(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(record, indent=2) + "\n")
    temporary.replace(path)


def _write_episode_video(path: Path, frames: list[np.ndarray], fps: int = 5) -> None:
    """Write RGB observations without overlays, preserving one frame per label."""
    import cv2

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.stem + ".tmp.mp4")
    height, width = frames[0].shape[:2]
    writer = cv2.VideoWriter(
        str(temporary), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )
    try:
        if not writer.isOpened():
            raise RuntimeError(f"Cannot open MP4 writer for {path}")
        for frame in frames:
            if frame.shape[:2] != (height, width):
                raise ValueError("Episode frames have inconsistent dimensions")
            writer.write(cv2.cvtColor(np.asarray(frame, dtype=np.uint8), cv2.COLOR_RGB2BGR))
    finally:
        writer.release()
    if not temporary.exists() or temporary.stat().st_size == 0:
        raise RuntimeError(f"MP4 writer produced no video for {path}")
    temporary.replace(path)


def collect_attempt(
    policy, task_name: str, seed: int, max_episode_steps: int,
    *, episode_path: Path | None = None, checkpoint: str | None = None,
    bank_path: Path | None = None,
) -> bool:
    """Collect a rollout and preserve video/diagnosis even if RoboFAC rejects it."""
    spec = TRAINING_TASKS[task_name]
    frames: list[np.ndarray] = []
    terminal_frame = None
    video_saved = False
    env = None
    record = {
        "format": "memoryvla_collection_episode_v1",
        "task": task_name, "seed": seed, "task_instruction": None,
        "checkpoint": str(Path(checkpoint).resolve()) if checkpoint else None,
        "failure_bank": str(bank_path.resolve()) if bank_path else None,
        "bank_episode_id": None, "failure_memory_stored": False,
        "status": "running", "success": None, "terminated": False,
        "truncated": False, "max_episode_steps": max_episode_steps,
        "actions": [], "diagnosis": None, "diagnosis_error": None,
        "video": None, "video_fps": 5, "video_frame_count": 0,
        "policy_frame_count": 0, "terminal_video_frame_index": None,
        "frame_mapping": "Video frames 0..policy_frame_count-1 are pre-action policy timesteps. "
                         "The optional final frame shows the observation after the last action "
                         "and was not sent to RoboFAC.",
    }

    def save_artifacts():
        nonlocal video_saved
        if episode_path is None:
            return
        record["policy_frame_count"] = len(frames)
        video_frames = frames + ([terminal_frame] if terminal_frame is not None else [])
        if video_frames and not video_saved:
            video_path = episode_path.with_suffix(".mp4")
            _write_episode_video(video_path, video_frames, fps=record["video_fps"])
            video_saved = True
            record["video"] = video_path.name
            record["video_frame_count"] = len(video_frames)
            record["terminal_video_frame_index"] = len(frames) if terminal_frame is not None else None
        _write_episode_json(episode_path.with_suffix(".json"), record)

    try:
        if episode_path is not None:
            save_artifacts()
        env = _make_env(spec)
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
        record["task_instruction"] = instruction
        policy.reset(instruction)
        image, depth, intrinsic, extrinsic = _get_policy_observation(
            env, obs, "3rd_view_camera", policy.use_spatial
        )
        done = False
        truncated = False
        first_frame = "True"
        for timestep in range(max_episode_steps):
            frame = np.asarray(image).copy()
            raw_action, action = policy.step(
                image, depth, intrinsic, extrinsic, instruction,
                current_position=np.asarray(base_env.tcp.pose.p, dtype=np.float32),
                episode_first_frame=first_frame,
            )
            del raw_action
            frames.append(frame)
            terminal_frame = None
            first_frame = "False"
            command = np.concatenate(
                [action["world_vector"], action["rot_axangle"], action["gripper"]]
            )
            record["actions"].append({"policy_timestep": timestep, "command": command.tolist()})
            obs, _, done, truncated, _ = env.step(command)
            image, depth, intrinsic, extrinsic = _get_policy_observation(
                env, obs, "3rd_view_camera", policy.use_spatial
            )
            terminal_frame = np.asarray(image).copy()
            if done or truncated:
                break

        success = bool(done)
        record.update(success=success, terminated=bool(done), truncated=bool(truncated),
                      status="diagnosis_pending" if not success else "success")
        context = policy.vla.active_ep_contexts.get(policy.vla.active_ep_id, {})
        record["bank_episode_id"] = context.get("fail_episode_id")
        # Persist the complete video before the potentially slow/failing API request.
        save_artifacts()
        record["diagnosis"] = policy.finish_episode(success=success, frames=frames)
        unit = policy.vla.fail_episodic_bank.bank.get(record["bank_episode_id"])
        record["failure_memory_stored"] = bool(
            unit is not None and unit.cog_mem_bank is not None and unit.per_mem_bank is not None
        )
        if not success:
            if record["failure_memory_stored"]:
                record["status"] = "failure_stored"
            elif record["diagnosis"] and record["diagnosis"].get("failed"):
                record["status"] = "failure_not_stored"
            else:
                record["status"] = "failure_unconfirmed"
        return success
    except UnstableLayoutError as exc:
        record.update(status="skipped_layout", error=str(exc))
        raise
    except RoboFACDiagnosisError as exc:
        record.update(status="diagnosis_error", diagnosis_error=str(exc),
                      diagnosis_raw_responses=getattr(exc, "raw_responses", []))
        raise
    except BaseException as exc:
        record.update(status="interrupted" if isinstance(exc, (KeyboardInterrupt, SystemExit)) else "error",
                      error=f"{type(exc).__name__}: {exc}")
        raise
    finally:
        try:
            save_artifacts()
        finally:
            if env is not None:
                env.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True, help="VLA .pt checkpoint")
    parser.add_argument("--output", type=Path, required=True, help="Output .pt failure bank")
    parser.add_argument(
        "--episodes-dir", type=Path,
        help="Parent directory for per-run episode JSON/MP4 pairs; defaults to <output_stem>_episodes.",
    )
    parser.add_argument("--episodes-per-task", type=int, default=10)
    parser.add_argument("--max-episode-steps", type=int, default=80)
    parser.add_argument(
        "--max-failure-memories",
        type=int,
        default=512,
        help="Maximum diagnosed failures retained in the output bank.",
    )
    parser.add_argument("--seed", type=int, default=100_000)
    parser.add_argument("--task", choices=("all", *TRAINING_TASKS), default="all")
    parser.add_argument("--experiment-mode", default="full")
    return parser.parse_args()


def main() -> None:
    os.environ.setdefault("DISPLAY", "")
    args = parse_args()
    if min(args.episodes_per_task, args.max_episode_steps, args.max_failure_memories) < 1:
        raise ValueError("episode and failure-bank limits must be positive")

    episodes_root = args.episodes_dir or args.output.parent / f"{args.output.stem}_episodes"
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid4().hex[:8]
    episodes_dir = episodes_root / run_id
    episodes_dir.mkdir(parents=True, exist_ok=False)
    print(f"episode_artifacts={episodes_dir}", flush=True)

    policy = VLAInference(
        saved_model_path=args.checkpoint,
        policy_setup="widowx_bridge",
        experiment_mode=args.experiment_mode,
        failure_bank_max_entries=args.max_failure_memories,
    )
    # Collection starts with an empty failure bank.  This prevents a bank from
    # a previous run from silently contaminating this training-only artifact.
    policy.vla.fail_episodic_bank.bank.clear()
    policy.vla.fail_episodic_bank.episode_id = 1

    task_names = list(TRAINING_TASKS) if args.task == "all" else [args.task]
    attempts = 0
    rollout_failures = 0
    diagnosis_errors = 0
    skipped_layouts = 0
    args.output.parent.mkdir(parents=True, exist_ok=True)

    def save_progress() -> dict:
        summary = {
            "scope": "training_tasks.py only",
            "episode_artifacts": str(episodes_dir.resolve()),
            "tasks": task_names,
            "attempted_rollouts": attempts,
            "environment_failures": rollout_failures,
            "diagnosis_errors": diagnosis_errors,
            "skipped_layouts": skipped_layouts,
            "robofac_confirmed_memories": len(policy.vla.fail_episodic_bank.bank),
        }
        # Replace only after a complete write, preserving the last good bank.
        bank_tmp = args.output.with_suffix(args.output.suffix + ".tmp")
        policy.vla.fail_episodic_bank.save_bank(bank_tmp)
        bank_tmp.replace(args.output)
        summary_path = args.output.with_suffix(".json")
        summary_tmp = summary_path.with_suffix(".json.tmp")
        summary_tmp.write_text(json.dumps(summary, indent=2) + "\n")
        summary_tmp.replace(summary_path)
        return summary

    try:
        for task_index, task_name in enumerate(task_names):
            for attempt in range(args.episodes_per_task):
                seed = args.seed + task_index * args.episodes_per_task + attempt
                try:
                    success = collect_attempt(
                        policy, task_name, seed, args.max_episode_steps,
                        episode_path=episodes_dir / task_name / f"seed_{seed}",
                        checkpoint=args.checkpoint, bank_path=args.output,
                    )
                except UnstableLayoutError as exc:
                    skipped_layouts += 1
                    print(f"task={task_name} seed={seed} skipped_layout={exc}", flush=True)
                    save_progress()
                    continue
                except RoboFACDiagnosisError as exc:
                    # finish_episode already discards this episode's unfinished memory.
                    attempts += 1
                    rollout_failures += 1
                    diagnosis_errors += 1
                    print(f"task={task_name} seed={seed} skipped_diagnosis={exc}", flush=True)
                    save_progress()
                    continue
                attempts += 1
                rollout_failures += int(not success)
                print(f"task={task_name} seed={seed} success={success}", flush=True)
                save_progress()
    finally:
        summary = save_progress()
        print(json.dumps(summary, indent=2), flush=True)
        print(f"saved_failure_bank={args.output}", flush=True)


if __name__ == "__main__":
    main()
