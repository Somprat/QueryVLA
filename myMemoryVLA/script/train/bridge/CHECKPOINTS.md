# Saving and resuming Bridge training

New runs save model weights (`step-....pt`) and a matching `.optimizer` file
at every `SAVE_INTERVAL` optimizer updates (default 2500) and at `MAX_STEPS`.
Keep both files together. The optimizer file contains Adam state, the learning-rate
scheduler state, global optimizer step, and epoch. A checkpoint is ready when the
log reports `Saved resumable checkpoint` after both writes finish.

Resume with the same experiment, architecture, freeze settings, batch sizes, and
dataset settings as the original run:

```bash
DATA_ROOT_DIR=datasets/widowx_simpler_rlds_v2 \
EXPERIMENT_MODE=full \
ACTIVATE_SPATIAL_PATH=true \
FREEZE_ACTION_MODEL=true \
RESUME_CHECKPOINT=/absolute/path/to/step-005000-epoch-00-loss=0.XXXX.pt \
MAX_STEPS=20000 \
bash script/train/bridge/train_mixture.sh
```

Replace the checkpoint path with its actual filename. Step and epoch are read
from the optimizer file automatically. `MAX_STEPS=20000` means 20,000 total
optimizer updates, so resuming at 5,000 performs 15,000 further updates.

This resumes model and optimization state, not the exact RLDS iterator,
random-number sequence, or in-memory episode history. The data stream restarts.

Processes started before this change still use the old saving code and will not
write optimizer files. Old weights-only checkpoints cannot recover missing Adam
state. To initialize a new optimizer from such weights, use `PRETRAINED_CKPT=...`
instead of `RESUME_CHECKPOINT`; the new run starts its step counter at zero.

Saving optimizer state adds disk usage and temporary CPU memory, rather than
permanent GPU memory. For approximately 322 million trainable FP32 parameters,
Adam's two moment tensors add roughly 2.4 GiB per checkpoint, on top of the model
weights. Full FSDP model-state gathering also requires CPU memory during saving.
