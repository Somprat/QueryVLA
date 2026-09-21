# Bridge 5k collection report

Sources: saved failure bank and latest completed run in tmux train. Rollout seeds/statuses are reconstructed from scrollback; bank episode IDs are separate identifiers and are not joined to seeds.

## Task outcomes

| Task | Success | Failure | Skipped |
|---|---:|---:|---:|
| green_cube_in_sink | 0 | 10 | 0 |
| carrot_in_sink | 0 | 6 | 4 |
| yellow_cube_on_green_cube | 6 | 4 | 0 |
| put_spoon_on_plate | 7 | 3 | 0 |

## Diagnosis quality

Saved diagnoses: 21. Reported confidence range: 0.0–0.012578. Failure window counts: {(0, 0): 21}.

Diagnoses are model-generated and unverified. Text includes repetitive and incomplete explanations and object mismatches (for example, knife in spoon tasks). Confidence is a model-reported value, not a calibrated probability. Successful episodes and the two unconfirmed failures have no diagnosis in this bank. Raw videos/frames are not included in the bank.

## Saved failure episodes

### Bank episode 1: put the green cube in the sink

- Failure type: Position deviation, misalignment during the reach for the cube. The robot arm's 
- Confidence: 0.012578
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, misalignment during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 2: put the green cube in the sink

- Failure type: Position deviation, misalignment during the reach for the cube. The robot arm's 
- Confidence: 0.012562
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, misalignment during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 3: put the green cube in the sink

- Failure type: Position deviation, misalignment during the reach for the cube. The robot arm's 
- Confidence: 0.012578
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, misalignment during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 4: put the green cube in the sink

- Failure type: Position deviation, misalignment during the reach for the cube. The robot arm's 
- Confidence: 0.012562
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, misalignment during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 5: put the green cube in the sink

- Failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Confidence: 0.0
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 6: put the green cube in the sink

- Failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Confidence: 0.012578
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube and continue with the subsequent steps of placing it in the safe. The position deviation in 

### Bank episode 7: put the green cube in the sink

- Failure type: Position deviation, misalignment during the reach for the cube. The robot arm's 
- Confidence: 0.012578
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, misalignment during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 8: put the green cube in the sink

- Failure type: Position deviation, misalignment during the reach for the cube. The robot arm's 
- Confidence: 0.012562
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, misalignment during the reach for the cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly behind (X

### Bank episode 9: put the green cube in the sink

- Failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Confidence: 0.012562
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube and continue with the subsequent steps of placing it in the box. The position deviation in X

### Bank episode 10: put the green cube in the sink

- Failure type: Position deviation, misalignment during the reach for the green cube. The robot,
- Confidence: 0.0
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, misalignment during the reach for the green cube. The robot arm did not properly align itself over the green cube, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a failure to securely grasp the cube. The position deviation in the X and Y axes indicates that the end-effector was slightly off

### Bank episode 11: put the carrot in the sink

- Failure type: Position deviation, misalignment during the reach for the orange. The robot arm,
- Confidence: 0.012345
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, misalignment during the reach for the orange. The robot arm did not properly align itself over the orange, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, resulting in a position deviation that prevented the robot from successfully completing the task. The robot's inability to reach the correct position,

### Bank episode 12: put the carrot in the sink

- Failure type: Position deviation, misalignment during the reach for the orange. The robot arm,
- Confidence: 0.012345
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, misalignment during the reach for the orange. The robot arm did not properly align itself over the orange, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not grasp the orange effectively, preventing it from completing the '

### Bank episode 13: put the carrot in the sink

- Failure type: Position deviation, misalignment during the reach for the cup. The robot arm did
- Confidence: 0.012345
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, misalignment during the reach for the cup. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not grasp the cup securely, preventing it from completing the subsequent 'L

### Bank episode 14: put the carrot in the sink

- Failure type: Position deviation, misalignment during the reach for the cup. The robot arm did
- Confidence: 0.012345
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, misalignment during the reach for the cup. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not grasp the cup securely, preventing it from completing the subsequent 'L

### Bank episode 15: put the carrot in the sink

- Failure type: Position deviation, misalignment during the reach for the cup stage. The robot's
- Confidence: 0.0
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, misalignment during the reach for the cup stage. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not securely grasp the cup, preventing it from completing the task of

### Bank episode 16: put the carrot in the sink

- Failure type: Position deviation, misalignment during the reach for the cup. The robot arm did
- Confidence: 0.012345
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, misalignment during the reach for the cup. The robot arm did not properly align itself over the cup, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not accurately positioned, which is crucial for successful manipulation tasks. As a result, the robot could not grasp the cup securely, preventing it from completing the subsequent 'L

### Bank episode 19: stack the yellow cube on the green cube

- Failure type: Position deviation, grasp failure, alignment error, grasping error, misalignment
- Confidence: 0.012345
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, grasp failure, alignment error, grasping error, misalignment, The robot arm's gripper did not reach the correct position to successfully grasp the green cube. This resulted in an inability for the robot to lift and move the cube to the target position, leading to a failure in completing the task. The position deviation indicates that the end-effector was slightly off in both X-

### Bank episode 22: stack the yellow cube on the green cube

- Failure type: Position deviation, grasp failure, misalignment, insufficient grasping force, or
- Confidence: 0.0
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, grasp failure, misalignment, insufficient grasping force, or position deviation during the grasping stage. The robot arm's gripper did not properly align with the center of the green cube, leading to an unsuccessful grasp. This misalignment indicates that the end-effector was not accurately positioned over the target object, which is crucial for successful manipulation. As a re

### Bank episode 28: put the spoon on the plate

- Failure type: Position deviation, misalignment during the grasping stage. The robot arm didnot
- Confidence: 0.0
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, misalignment during the grasping stage. The robot arm did not reach the correct position to successfully grasp the knife, leading to an inability to complete the subsequent steps of lifting and moving the knife to the plate. This misalignment indicates that the end-effector was not properly oriented towards the knife, resulting in a failure to execute the grasp effectively. The

### Bank episode 32: put the spoon on the plate

- Failure type: Position deviation, misalignment during the grasping stage. The robot arm was in
- Confidence: 0.0
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, misalignment during the grasping stage. The robot arm was unable to accurately position itself over the knife, leading to an unsuccessful grasp attempt. This misalignment indicates that the end-effector was not properly oriented towards the knife, resulting in a failure to grasp it securely. The position deviation in the X and Y axes indicates that the end-effector was slightly

### Bank episode 34: put the spoon on the plate

- Failure type: Position deviation, grasping error, alignment error, or orientation deviation.Gr
- Confidence: 0.012345
- Failure timesteps: 0–0; stored context: 0–2

Position deviation, grasping error, alignment error, or orientation deviation.Gr, the robot arm was unable to grasp the knife due to an incorrect positioning of the end-effector relative to the knife. The end-effector was misaligned and did not reach the optimal position necessary for a successful grasp, leading to a failure in completing the task. This misalignment indicates that the robot's path

