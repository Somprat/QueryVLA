# Training commands found in historical documentation

These are verbatim documented blocks. They may be examples or proposed work, not executed commands. Distinct blocks appear once; dates identify commits, not executions. Vendor documentation is excluded.

## 1. 2026-07-10T10:31:51+07:00 — 769fa0a

Source: `myMemoryVLA/README.md`

```bash
# Train on the Bridge dataset
   bash script/train/bridge/train_bridge.sh
   # Train on the LIBERO-Spatial dataset
   bash script/train/libero/train_libero_spatial.sh
   # Train on the LIBERO-Object dataset
   bash script/train/libero/train_libero_object.sh
   # Train on the LIBERO-Goal dataset
   bash script/train/libero/train_libero_goal.sh
   # Train on the LIBERO-100 dataset
   bash script/train/libero/train_libero_100.sh
   # Train on the Fractal dataset
   bash script/train/fractal/train_fractal.sh
   # Train on real-world data
   bash script/train/real_world/train_real.sh
```

## 2. 2026-08-20T16:05:36Z — f4291a3

Source: `TRAINING_PROGRESS.md`

```bash
WANDB_MODE=disabled \
DATA_ROOT_DIR=/workspace/datasets \
PRETRAINED_CKPT=/workspace/multimodal/models/model_b/checkpoints/memvla-bridge.pt \
EXPERIMENT_MODE=full \
MAX_STEPS=1 \
SAVE_INTERVAL=9999 \
BATCH_SIZE=1 \
N_GPU=1 \
RUN_ID=maniskill_one_step_smoke \
bash myMemoryVLA/script/train/maniskill/train_maniskill.sh
```

## 3. 2026-09-08T21:10:34+07:00 — 662e38c

Source: `README.md`

```bash
source script/setup/env.sh

DATA_ROOT_DIR=/absolute/path/to/datasets \
PRETRAINED_CKPT=../models/model_b/checkpoints/memvla-bridge.pt \
EXPERIMENT_MODE=full \
MAX_STEPS=10000 \
SAVE_INTERVAL=2500 \
  bash script/train/maniskill/train_maniskill.sh
```

## 4. 2026-09-08T21:10:34+07:00 — 662e38c

Source: `README.md`

```bash
DRY_RUN=true EXPERIMENT_MODE=full \
  bash script/train/maniskill/train_maniskill.sh
```

## 5. 2026-09-23T04:34:29Z — 61e2afc

Source: `myMemoryVLA/script/train/bridge/CHECKPOINTS.md`

```bash
DATA_ROOT_DIR=datasets/widowx_simpler_rlds_v2 \
EXPERIMENT_MODE=full \
ACTIVATE_SPATIAL_PATH=true \
FREEZE_ACTION_MODEL=true \
RESUME_CHECKPOINT=/absolute/path/to/step-005000-epoch-00-loss=0.XXXX.pt \
MAX_STEPS=20000 \
bash script/train/bridge/train_mixture.sh
```
