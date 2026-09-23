# Bridge collection: 50 attempts per task

## Sources and interpretation

Source: datasets/failure_banks/bridge_5k.pt and its JSON summary; outcomes reconstructed from the latest 50-attempt run in tmux train. This report covers 200 scheduled attempts, 177 executed rollouts, 116 environment failures and 102 saved diagnoses. The 23 unstable layouts were skipped without retry.

Categories below summarize the saved RoboFAC failure_type text; they are not independently verified physical failure causes. Bank episode IDs are not rollout seeds. No episode-to-seed join is assumed. The 14 failures without saved diagnoses remain unclassified; the run logged no observable failure for these and zero diagnosis errors.

## Per-task breakdown

| Task | Success | Environment failure | Skipped | Reach/grasp misalignment | Stacking misalignment | Placement misalignment | Saved but missing type | No saved diagnosis |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| green_cube_in_sink | 0 | 50 | 0 | 50 | 0 | 0 | 0 | 0 |
| carrot_in_sink | 0 | 27 | 23 | 25 | 0 | 0 | 1 | 1 |
| yellow_cube_on_green_cube | 22 | 28 | 0 | 15 | 1 | 0 | 0 | 12 |
| put_spoon_on_plate | 39 | 11 | 0 | 9 | 0 | 1 | 0 | 1 |

## Diagnosis quality limitations

- All 102 diagnoses locate the failure at timestep 0–0; stored context is 0–2. These windows do not establish when the actual failure occurred.
- Model-reported confidence ranges from 0 to 0.012578 and is not a calibrated probability.
- Descriptions repeatedly misidentify objects: cup/orange for carrot, knife for spoon, and the green cube as the object to lift in the yellow-on-green stacking task.
- Failure labels and explanations are repetitive and often incomplete. One saved carrot diagnosis has an empty failure type.
- The bank contains feature summaries, not replayable rollout videos. The saved labels alone cannot support a trustworthy physical root-cause breakdown.

## Exact labels by task

### green_cube_in_sink

- 29: Position deviation, misalignment during the reach for the green cube. The robot,
- 12: Position deviation, misalignment during the reach for the cube. The robot arm's
- 4: Position deviation, misalignment during the reach for the long block. The robot,
- 2: Position deviation, alignment error during the grasping stage. The robot arm did
- 1: Position deviation, alignment error during the reach for the cube. The robot arm
- 1: Position deviation, alignment error during the grasping stage. The robot arm's L
- 1: Position deviation, alignment with the target position of the green cube. The L-
### carrot_in_sink

- 9: Position deviation, misalignment during the reach for the cup. The robot arm did
- 9: Position deviation, misalignment during the reach for the orange. The robot arm,
- 6: Position deviation, misalignment during the reach for the cup stage. The robot's
- 1: [empty failure type]
- 1: Position deviation, misalignment during the grasping stage. The robot arm's grip
### yellow_cube_on_green_cube

- 6: Position deviation, misalignment during the grasping stage. The robot arm's grip
- 4: Position deviation, grasp failure, misalignment, insufficient grasping force, or
- 2: Position deviation, misalignment during the grasping stage. The robot arm's end-
- 2: Position deviation, grasp failure, misalignment, insufficient force applied by a
- 1: Position deviation, misalignment during the stacking phase. The robot arm did a
- 1: Position deviation, grasp failure, alignment error, grasping error, misalignment
### put_spoon_on_plate

- 4: Position deviation, misalignment during the grasping stage. The robot arm's end-
- 3: Position deviation, misalignment during the grasping stage. The robot arm was in
- 1: Position deviation, misalignment during the grasping stage. The robot arm didnot
- 1: Position deviation, grasping error, misalignment, or insufficient alignment of a
- 1: Position deviation, misalignment during the final stage of placing the knife on.

## Saved episode details

### Bank episode 1: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cube. The robot arm's 
- Model-reported confidence: 0.012578
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 2: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cube. The robot arm's 
- Model-reported confidence: 0.012578
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 3: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cube. The robot arm's 
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 4: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cube. The robot arm's 
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 5: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 6: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.012578
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube and continue with the subsequent steps of placing it in the safe. The position deviation in 

### Bank episode 7: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cube. The robot arm's 
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 8: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cube. The robot arm's 
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 9: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube and continue with the subsequent steps of placing it in the box. The position deviation in X

### Bank episode 10: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 11: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube and continue with the subsequent steps of the task. The position deviation in the X-axis, Y,

### Bank episode 12: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 13: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 14: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube and continue with the subsequent steps of placing it in the box. The position deviation in X

### Bank episode 15: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, alignment error during the reach for the cube. The robot arm
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, alignment error during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind

### Bank episode 16: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 17: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cube. The robot arm's 
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 18: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube and continue with the subsequent steps of placing it in the box. The position deviation in X

### Bank episode 19: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 20: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 21: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 22: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the long block. The robot,
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the long block. The robot arm did not properly align itself over the light green long block, leading to an inability to grasp it accurately. This misalignment indicates that the end-effector was not positioned correctly in relation to the target object, resulting in a failure to complete the subsequent steps of lifting and stacking the block on

### Bank episode 23: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 24: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cube. The robot arm's 
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 25: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 26: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cube. The robot arm's 
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 27: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 28: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, alignment error during the grasping stage. The robot arm's L
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, alignment error during the grasping stage. The robot arm's end-effector was not properly aligned with the green cube, leading to an unsuccessful grasp. This misalignment indicates that the robot's approach trajectory did not accurately position itself over the green cube, resulting in a failure to securely grasp it. The position deviation in the X and Y axes indicates that theL

### Bank episode 29: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 30: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 31: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 32: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.012578
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube and continue with the subsequent steps of placing it in the safe. The position deviation in 

### Bank episode 33: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cube. The robot arm's 
- Model-reported confidence: 0.012578
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 34: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube and continue with the subsequent steps of the task. The position deviation in the X-axis, Y,

### Bank episode 35: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the long block. The robot,
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the long block. The robot arm did not properly align itself over the long block, leading to an inability to grasp it accurately. This misalignment indicates that the end-effector was not positioned correctly in relation to the target object, resulting in a suboptimal grip that could lead to dropping the block in subsequent steps. Such position,

### Bank episode 36: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, alignment error during the grasping stage. The robot arm did
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, alignment error during the grasping stage. The robot arm did not reach the correct position to successfully grasp the green cube. This misalignment resulted in the end-effector being off-target, preventing it from securely holding the cube and leading to the failure of the task. The position deviation indicates that the end-effector was not properly aligned with the green cube,

### Bank episode 37: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the long block. The robot,
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the long block. The robot arm did not properly align itself over the long block, leading to an inability to grasp it accurately. This misalignment indicates that the end-effector was not positioned correctly in relation to the target object, resulting in a failure to complete the subsequent steps of the task. The robot's inability to accurately

### Bank episode 38: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 39: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cube. The robot arm's 
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 40: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 41: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cube. The robot arm's 
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 42: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, alignment error during the grasping stage. The robot arm did
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, alignment error during the grasping stage. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned above the target object, resulting in a failure to securely grasp it. The position deviation in the X and Y axes indicates that the end-effector was a

### Bank episode 43: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube and continue with the subsequent steps of placing it in the box. The position deviation in X

### Bank episode 44: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 45: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 46: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the long block. The robot,
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the long block. The robot arm did not properly align itself over the light green long block, leading to an inability to grasp it accurately. This misalignment indicates that the end-effector was not positioned correctly in relation to the target object, resulting in a failure to complete the subsequent steps of lifting and stacking the block on

### Bank episode 47: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 48: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, alignment with the target position of the green cube. The L-
- Model-reported confidence: 0.0
- Failure timestep range: 0–0



### Bank episode 49: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 50: green_cube_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Model-reported confidence: 0.012578
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube and continue with the subsequent steps of placing it in the safe. The position deviation in 

### Bank episode 51: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cup. The robot arm did
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cup. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not grasp the cup securely, preventing it from completing the subsequent 'L

### Bank episode 52: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cup. The robot arm did
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cup. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not grasp the cup securely, preventing it from completing the subsequent 'L

### Bank episode 53: carrot_in_sink

- Report category: Missing failure type
- Raw failure type: [empty]
- Model-reported confidence: 0.0
- Failure timestep range: 0–0



### Bank episode 54: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cup. The robot arm did
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cup. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not grasp the cup securely, preventing it from completing the subsequent 'L

### Bank episode 55: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cup. The robot arm did
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cup. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not grasp the cup securely, preventing it from completing the subsequent 'L

### Bank episode 56: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cup stage. The robot's
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cup stage. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not securely grasp the cup, preventing it from completing the task of

### Bank episode 57: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cup stage. The robot's
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cup stage. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not securely grasp the cup, preventing it from completing the task of

### Bank episode 58: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the orange. The robot arm,
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the orange. The robot arm did not properly align itself over the orange, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the object. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 60: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cup. The robot arm did
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cup. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not grasp the cup securely, preventing it from completing the subsequent 'L

### Bank episode 61: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the orange. The robot arm,
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the orange. The robot arm did not properly align itself over the orange, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the object. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 62: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the orange. The robot arm,
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the orange. The robot arm did not properly align itself over the orange, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a position deviation that prevented the robot from successfully completing the task. The robot's inability to correctly reach the target,

### Bank episode 63: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the orange. The robot arm,
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the orange. The robot arm did not properly align itself over the orange, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a position deviation that prevented the robot from successfully completing the task. The robot's inability to correctly reach the target,

### Bank episode 64: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the orange. The robot arm,
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the orange. The robot arm did not properly align itself over the orange, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not grasp the orange effectively, preventing it from completing the '

### Bank episode 65: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cup. The robot arm did
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cup. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not grasp the cup securely, preventing it from completing the subsequent 'L

### Bank episode 66: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cup stage. The robot's
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cup stage. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not securely grasp the cup, preventing it from completing the task of

### Bank episode 67: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the orange. The robot arm,
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the orange. The robot arm did not properly align itself over the orange, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a position deviation that prevented the robot from successfully completing the task. The robot's inability to correctly reach the target,

### Bank episode 68: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cup stage. The robot's
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cup stage. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not securely grasp the cup, preventing it from completing the task of

### Bank episode 69: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the orange. The robot arm,
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the orange. The robot arm did not properly align itself over the orange, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a position deviation that prevented the robot from successfully completing the task. The robot's inability to correctly reach the target,

### Bank episode 70: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the grasping stage. The robot arm's grip
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the grasping stage. The robot arm's gripper did not properly align with the center of the cup, leading to an unsuccessful grasp. This misalignment indicates that the end-effector was not accurately positioned over the cup, which is crucial for a successful grasp. As a result, the robot could not lift the cup and continue with the subsequent steps of placing,

### Bank episode 71: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the orange. The robot arm,
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the orange. The robot arm did not properly align itself over the orange, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a position deviation that prevented the robot from successfully completing the task. The robot's inability to correctly reach the target,

### Bank episode 72: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cup stage. The robot's
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cup stage. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not securely grasp the cup, preventing it from completing the task of

### Bank episode 73: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cup stage. The robot's
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cup stage. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not grasp the cup securely, preventing it from completing the task of

### Bank episode 74: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cup. The robot arm did
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cup. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not grasp the cup securely, preventing it from completing the subsequent 'L

### Bank episode 75: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the orange. The robot arm,
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the orange. The robot arm did not accurately position itself over the orange, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not properly oriented and positioned relative to the target object, resulting in a failure to grasp it securely. The position deviation in the X-axis indicates that the end

### Bank episode 76: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cup. The robot arm did
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cup. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not grasp the cup securely, preventing it from completing the subsequent 'L

### Bank episode 77: carrot_in_sink

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the reach for the cup. The robot arm did
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

Position deviation, misalignment during the reach for the cup. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not securely grasp the cup, preventing it from completing the subsequent 'L

### Bank episode 81: yellow_cube_on_green_cube

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the grasping stage. The robot arm's grip
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the grasping stage. The robot arm's gripper did not properly align with the center of the green cube, leading to an unsuccessful grasp. This misalignment indicates that the end-effector was not accurately positioned over the target object, which is crucial for successful manipulation. As a result, the robot arm could not lift the green cube and stack it on a

### Bank episode 82: yellow_cube_on_green_cube

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the grasping stage. The robot arm's end-
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the grasping stage. The robot arm's end-effector was not properly aligned with the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the robot's approach trajectory did not accurately position itself over the green cube, resulting in a failure to securely grasp it. Consequently, the robot could not complete the subsequent

### Bank episode 85: yellow_cube_on_green_cube

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, grasp failure, misalignment, insufficient grasping force, or
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, grasp failure, misalignment, insufficient grasping force, or position deviation during the grasping stage. The robot arm's gripper did not properly align with the center of the green cube, leading to an unsuccessful grasp. This misalignment indicates that the end-effector was not positioned accurately over the green cube, which is crucial for a successful grasp. As a result, it

### Bank episode 88: yellow_cube_on_green_cube

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the grasping stage. The robot arm's grip
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the grasping stage. The robot arm's gripper did not properly align with the center of the green cube, leading to an unsuccessful grasp. This misalignment indicates that the end-effector was not accurately positioned over the target object, which is crucial for successful manipulation. As a result, the robot arm could not lift the green cube and stack it on a

### Bank episode 89: yellow_cube_on_green_cube

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, grasp failure, misalignment, insufficient force applied by a
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

The robot arm's gripper did not properly align with the green cube during the grasping stage. This misalignment resulted in the gripper being unable to securely grasp the cube, leading to a failure in completing the task of stacking it on the yellow cube. The position deviation indicates that the end-effector was not positioned correctly over the green cube, which is crucial for a successful grasp

### Bank episode 90: yellow_cube_on_green_cube

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, grasp failure, misalignment, insufficient grasping force, or
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, grasp failure, misalignment, insufficient grasping force, or position deviation during the grasping stage. The robot arm's gripper did not properly align with the center of the green cube, leading to an unsuccessful grasp. This misalignment indicates that the end-effector was not accurately positioned over the target object, which is crucial for successful manipulation. As a re

### Bank episode 92: yellow_cube_on_green_cube

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, grasp failure, misalignment, insufficient grasping force, or
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, grasp failure, misalignment, insufficient grasping force, or position deviation during the grasping stage. The robot arm's gripper did not properly align with the center of the green cube, leading to an unsuccessful grasp. This misalignment indicates that the end-effector was not positioned accurately over the target object, which is crucial for successful manipulation. As a re

### Bank episode 94: yellow_cube_on_green_cube

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, grasp failure, misalignment, insufficient force applied by a
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

The robot arm's gripper did not properly align with the center of the green cube during the grasping attempt. This misalignment resulted in the gripper being unable to securely grasp the cube, leading to a failure in completing the stacking task. The position deviation indicates that the end-effector was off course, causing it to miss the target object entirely. Such deviations can result from a m

### Bank episode 98: yellow_cube_on_green_cube

- Report category: Stacking misalignment
- Raw failure type: Position deviation, misalignment during the stacking phase. The robot arm did a 
- Model-reported confidence: 0.012562
- Failure timestep range: 0–0

Position deviation, misalignment during the stacking phase. The robot arm did not properly align the light green long block directly above the red cube before attempting to stack it. This misalignment resulted in the inability to successfully place the block on the cube, leading to a failure in completing the task. The position deviation indicates that the end-effector was off course, causing the 

### Bank episode 100: yellow_cube_on_green_cube

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the grasping stage. The robot arm's grip
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the grasping stage. The robot arm's gripper did not properly align with the center of the light green long block, leading to an unsuccessful grasp. This misalignment indicates that the end-effector was not positioned accurately over the object, which is crucial for a successful grasp. As a result, the robot arm could not lift the block and continue with the 

### Bank episode 102: yellow_cube_on_green_cube

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, grasp failure, misalignment, insufficient grasping force, or
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, grasp failure, misalignment, insufficient grasping force, or position deviation during the grasping stage. The robot arm's gripper did not properly align with the center of the green cube, leading to an unsuccessful grasp. This misalignment indicates that the end-effector was not positioned accurately over the green cube, which is crucial for a successful grasp. As a result, it

### Bank episode 106: yellow_cube_on_green_cube

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the grasping stage. The robot arm's grip
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the grasping stage. The robot arm's gripper did not properly align with the center of the green cube, leading to an unsuccessful grasp. This misalignment indicates that the end-effector was not accurately positioned over the target object, which is crucial for successful manipulation. As a result, the robot arm could not lift the green cube and stack it on a

### Bank episode 108: yellow_cube_on_green_cube

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the grasping stage. The robot arm's end-
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

The robot arm was unable to properly align itself over the light green long block, resulting in a position deviation that hindered its ability to grasp the object. This misalignment indicates that the end-effector was not accurately positioned above the target object, leading to an unsuccessful attempt to lift it. The failure occurred specifically during the grasping stage, where precise alignment

### Bank episode 120: yellow_cube_on_green_cube

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, grasp failure, alignment error, grasping error, misalignment
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, grasp failure, alignment error, grasping error, misalignment during the grasping stage. The robot arm's gripper did not properly align with the center of the green cube, leading to an unsuccessful grasp. This misalignment indicates that the end-effector was not positioned accurately over the target object, which is crucial for successful manipulation. As a result, the robot arm

### Bank episode 126: yellow_cube_on_green_cube

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the grasping stage. The robot arm's grip
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the grasping stage. The robot arm's gripper did not properly align with the center of the green cube, leading to an unsuccessful grasp. This misalignment indicates that the end-effector was not accurately positioned over the target object, which is crucial for successful manipulation. As a result, the robot could not lift the green cube and stack it on the y

### Bank episode 127: yellow_cube_on_green_cube

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the grasping stage. The robot arm's grip
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the grasping stage. The robot arm's gripper did not properly align with the center of the green cube, leading to an unsuccessful grasp. This misalignment indicates that the end-effector was not accurately positioned over the target object, which is crucial for successful manipulation. As a result, the robot arm could not lift the green cube and stack it on a

### Bank episode 134: put_spoon_on_plate

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the grasping stage. The robot arm's end-
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

The robot arm was unable to properly grasp the knife due to a position deviation that occurred during the grasping stage. Specifically, the end-effector was not aligned correctly with the knife, leading to an unsuccessful attempt to pick it up. This misalignment indicates that the robot's approach trajectory did not adequately account for the spatial relationship between the end-effector and the L

### Bank episode 136: put_spoon_on_plate

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the grasping stage. The robot arm was in
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the grasping stage. The robot arm was unable to accurately position itself over the knife, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not properly oriented towards the knife, resulting in a failure to grasp it securely. The position deviation in the X and Y axes indicates that the end-effector was slightly

### Bank episode 159: put_spoon_on_plate

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the grasping stage. The robot arm's end-
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the grasping stage. The robot arm's end-effector was not properly aligned with the knife, leading to an unsuccessful grasp. This misalignment indicates that the robot's approach trajectory did not accurately position itself over the knife, resulting in a failure to securely grasp it. The position deviation in the X and Y axes indicates that the end-effector,

### Bank episode 161: put_spoon_on_plate

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the grasping stage. The robot arm was in
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the grasping stage. The robot arm was unable to accurately position itself over the knife, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not properly oriented towards the knife, resulting in a failure to grasp it securely. The position deviation in the X and Y axes indicates that the end-effector was slightly

### Bank episode 162: put_spoon_on_plate

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the grasping stage. The robot arm's end-
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the grasping stage. The robot arm's end-effector was not properly aligned with the knife, leading to an unsuccessful grasp. This misalignment indicates that the robot's approach trajectory did not accurately position itself over the knife, resulting in a failure to securely grasp it. The position deviation in the X and Y axes indicates that the end-effector,

### Bank episode 164: put_spoon_on_plate

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the grasping stage. The robot arm was in
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the grasping stage. The robot arm was unable to accurately position itself over the knife, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not properly oriented towards the knife, resulting in a failure to securely grasp it. The position deviation in the X and Y axes indicates that the end-effector was slightly

### Bank episode 168: put_spoon_on_plate

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the grasping stage. The robot arm didnot
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the grasping stage. The robot arm did not reach the correct position to successfully grasp the knife. This misalignment indicates that the end-effector was not properly oriented towards the knife, leading to an inability to complete the task effectively. As a result, the robot could not proceed with the subsequent steps of lifting and moving the knife to the

### Bank episode 169: put_spoon_on_plate

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, grasping error, misalignment, or insufficient alignment of a
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, grasping error, misalignment, or insufficient alignment of a knife relative to the cup during the grasping stage. The robot arm was unable to properly grasp the knife due to a misalignment, which resulted in the end-effector being positioned incorrectly and not being able to securely hold the knife. This misalignment indicates that the robot's approach trajectory did not take a

### Bank episode 175: put_spoon_on_plate

- Report category: Placement misalignment
- Raw failure type: Position deviation, misalignment during the final stage of placing the knife on.
- Model-reported confidence: 0.012345
- Failure timestep range: 0–0

The robot arm did not accurately position the knife directly above the plate before attempting to lower it down for placement. This misalignment resulted in the knife being positioned incorrectly, preventing it from being successfully placed on the plate. The position deviation indicates that the end-effector was off course, leading to an inability to complete the task as intended. Such deviations

### Bank episode 177: put_spoon_on_plate

- Report category: Reach/grasp misalignment
- Raw failure type: Position deviation, misalignment during the grasping stage. The robot arm's end-
- Model-reported confidence: 0.0
- Failure timestep range: 0–0

Position deviation, misalignment during the grasping stage. The robot arm's end-effector was not properly aligned with the knife, leading to an unsuccessful grasp. This misalignment indicates that the robot's approach trajectory did not accurately position itself over the knife, resulting in a failure to securely grasp it. The position deviation in the X and Y axes indicates that the end-effector,

