#!/bin/bash
# Train only the existing cog/per FailAwareFusion modules from a frozen bank.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "${repo_root}"
python_bin="${repo_root}/.venv/bin/python"

: "${PRETRAINED_CKPT:?Set PRETRAINED_CKPT to the VLA checkpoint to adapt}"
: "${FAILURE_BANK:?Set FAILURE_BANK to collect_failure_bank.py output}"

data_root_dir="${DATA_ROOT_DIR:-./data/bridge-rlds}"
run_root_dir="${RUN_ROOT_DIR:-./log/bridge_generated}"
run_id="${RUN_ID:-memvla_failure_fusion}"
n_gpu="${N_GPU:-1}"
batch_size="${BATCH_SIZE:-1}"
global_batch_size="${GLOBAL_BATCH_SIZE:-8}"
max_steps="${MAX_STEPS:-20000}"
save_interval="${SAVE_INTERVAL:-2500}"
hf_token="${HF_TOKEN:-YOUR_HF_TOKEN}"

if [[ ! -x "${python_bin}" ]]; then
  echo "Missing virtual environment: ${python_bin}" >&2
  exit 1
fi
if (( global_batch_size % (n_gpu * batch_size) != 0 )); then
  echo "GLOBAL_BATCH_SIZE must be divisible by N_GPU * BATCH_SIZE." >&2
  exit 1
fi

"${python_bin}" -m torch.distributed.run --nproc_per_node="${n_gpu}" train.py \
  --pretrained_checkpoint "${PRETRAINED_CKPT}" \
  --is_resume false \
  --resume_step 0 \
  --resume_epoch 0 \
  --vla.type prism-dinosiglip-224px+oxe+diffusion \
  --vla.data_mix bridge_widowx_simpler_rgbd \
  --vla.expected_world_size "${n_gpu}" \
  --vla.per_device_batch_size "${batch_size}" \
  --vla.global_batch_size "${global_batch_size}" \
  --vla.learning_rate 2e-5 \
  --vla.max_steps "${max_steps}" \
  --data_root_dir "${data_root_dir}" \
  --run_root_dir "${run_root_dir}" \
  --run_id "${run_id}" \
  --save_interval "${save_interval}" \
  --trackers '[jsonl]' \
  --hf_token "${hf_token}" \
  --dataloader_type stream \
  --experiment_mode full \
  --freeze_vlm true \
  --freeze_action_model true \
  --failure_bank_path "${FAILURE_BANK}" \
  --failure_fusion_only true
