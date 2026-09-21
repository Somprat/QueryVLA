#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
export PATH="$PWD/.venv-robofac/bin:$PATH"
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}"
export VLLM_USE_FLASHINFER_SAMPLER=0
exec vllm serve MINT-SJTU/RoboFAC-7B \
  --host 127.0.0.1 \
  --port 8000 \
  --gpu-memory-utilization 0.35 \
  --max-model-len 16384 \
  --max-num-seqs 1 \
  --limit-mm-per-prompt '{"image":20}' \
  --structured-outputs-config '{"backend":"xgrammar","disable_any_whitespace":true}'
