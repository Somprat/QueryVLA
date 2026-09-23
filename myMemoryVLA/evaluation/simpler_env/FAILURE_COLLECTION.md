# Failure collection artifacts

`collect_failure_bank.py` automatically saves episode JSON and MP4 pairs on every new run. No additional flags are required. With `--output datasets/failure_banks/bridge_5k.pt`, the layout is:

```text
datasets/failure_banks/
  bridge_5k.pt
  bridge_5k.json
  bridge_5k_episodes/
    <UTC timestamp>_<unique run ID>/
      green_cube_in_sink/
        seed_100000.json
        seed_100000.mp4
      ...
```

The aggregate JSON includes `episode_artifacts`, the absolute path to this run's directory. `--episodes-dir PATH` changes the parent directory; each run still gets a unique subdirectory. The existing bank output is replaced as before, but prior episode artifacts are preserved. Bank episode IDs are scoped to the corresponding collection run, not globally unique across reruns.

Each episode JSON records the task, seed, instruction, checkpoint and bank paths, environment outcome, action commands, failure-bank episode ID, whether a memory was retained at completion, and the full diagnosis dictionary returned by MemoryVLA (including raw response, sampled labels, failure bounds, and stored-context bounds where available). Learned feature tensors remain in the `.pt` bank; they are not duplicated into JSON. Later bank-capacity eviction can remove an entry that was retained at episode completion.

Successful episodes have no RoboFAC diagnosis. Failed episodes retain their diagnosis even when RoboFAC returns `failed: false`. Diagnosis errors retain their error and available raw model responses. Unstable layouts have an explanatory JSON but no MP4, because no rollout ran. Interrupted or unexpectedly failed rollouts preserve available frames when normal exception handling can run; forced process termination cannot guarantee finalization.

The MP4 is RGB camera observations encoded at 5 FPS. Video frames `0..policy_frame_count-1` correspond exactly to the pre-action policy timesteps passed to RoboFAC. One additional frame shows the observation after the last action; `terminal_video_frame_index` identifies it. This final frame is for review and is not sent to RoboFAC or used as a memory timestep. `actions` lists each command as world translation (3), rotation axis-angle (3), and gripper (1).

The completed video and a JSON with status `diagnosis_pending` are saved before the RoboFAC request, then JSON is updated after the result. All normal JSON/video writes use temporary files and rename. A hard crash during diagnosis therefore leaves a reviewable video and pending record. These artifacts are generated prospectively; they do not reconstruct recordings for older banks.

CPU checks:

```bash
.venv/bin/python script/test_collection_artifacts.py
.venv/bin/python script/test_robofac_recovery.py
```
