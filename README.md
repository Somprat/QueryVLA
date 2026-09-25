# QueryVLA

QueryVLA is a research extension of [MemoryVLA](https://arxiv.org/abs/2508.19236) for selective and cross-episode memory retrieval in vision-language-action (VLA) models. It adds instruction-conditioned top-k retrieval, successful-episode summaries, and an optional point-cloud spatial memory while retaining MemoryVLA's perceptual/cognitive memory and diffusion action policy.

This repository contains the QueryVLA implementation, training and evaluation launchers, a vendored SimplerEnv integration, and reproducibility notes for the Bridge WidowX experiments.

> **Status:** Experimental research code. The reported results are preliminary and should not be interpreted as a statistically established improvement over MemoryVLA.

## Main Components

- **Query-based retrieval:** ranks within-episode memories using semantic similarity, end-effector distance, and temporal recency, then retrieves a bounded top-k set.
- **Task-conditioned weighting:** maps instructions to `spatial`, `object_state`, `temporal`, or `default` retrieval modes.
- **Cross-episode memory:** stores compact summaries of successful episodes and retrieves related summaries using the current instruction and initial scene.
- **Spatial memory:** converts depth and camera calibration into a point cloud and encodes it as spatial tokens.
- **Controlled ablations:** supports baseline, query-only, episodic-only, query-plus-episodic, and full-model evaluation modes.

## Preliminary Results

The matched SimplerEnv-Bridge comparison uses the same pretrained checkpoint and 24 trials for each of four tasks.

| Task | Full history | Query top-4 |
|---|---:|---:|
| Stack green cube on yellow cube | 9/24 | 8/24 |
| Put carrot on plate | 18/24 | 19/24 |
| Put spoon on tablecloth | 18/24 | 19/24 |
| Put eggplant in basket | 24/24 | 24/24 |
| **Overall** | **69/96 (71.9%)** | **70/96 (72.9%)** |

Query top-4 retained approximately the same task success while reducing the maximum retrieved within-episode history from 16 entries to four. The net difference is one successful episode and varies by task, so it is evidence of a memory-budget trade-off rather than a reliable accuracy gain. See [`myMemoryVLA/reports/query_vs_full_history.md`](myMemoryVLA/reports/query_vs_full_history.md) for the evaluation details.

## Repository Layout

```text
multimodal/
├── myMemoryVLA/
│   ├── vla/                    # QueryVLA model and memory implementations
│   ├── evaluation/             # SimplerEnv and LIBERO evaluation code
│   ├── script/setup/           # Environment and checkpoint setup
│   ├── script/eval/            # Evaluation launchers
│   ├── script/train/           # Training launchers
│   ├── reports/                # Experiment reports
│   └── third_libs/SimplerEnv/  # Vendored simulation integration
├── models/                     # Model metadata and local checkpoint locations
├── artifacts/                  # Small smoke-test artifacts
└── FRESH_RUNPOD_SETUP.md       # Full setup and troubleshooting guide
```

Large checkpoints, datasets, virtual environments, caches, and generated rollouts are excluded from Git.

## Tested Environment

The reproducible setup targets a Linux GPU machine or RunPod with:

- Python 3.10
- PyTorch 2.2.0 and CUDA 12.1
- An NVIDIA GPU with sufficient memory for the 7B VLA checkpoint
- SAPIEN 2.2.2 and a working Vulkan driver for SimplerEnv rendering
- Approximately 40 GiB of free storage for the Bridge checkpoint and download cache

The original evaluation setup was tested on an NVIDIA L40S. See [`FRESH_RUNPOD_SETUP.md`](FRESH_RUNPOD_SETUP.md) for system packages, simulator validation, LIBERO setup, and troubleshooting.

## Quick Start

Clone the repository and create the tested evaluation environment:

```bash
git clone https://github.com/Somprat/multimodal.git
cd multimodal/myMemoryVLA
bash script/setup/bootstrap_runpod_eval.sh
source script/setup/env.sh
```

### Llama configuration and tokenizer

The MemoryVLA checkpoint already contains the complete trained Llama parameter state. The loader only needs a compatible local Llama 2 configuration and tokenizer; it does not need to download a second copy of the gated base-model weights.

```bash
mkdir -p ../models/llama2-7b-public
.venv/bin/huggingface-cli download NousResearch/Llama-2-7b-hf \
  config.json generation_config.json \
  tokenizer.json tokenizer.model tokenizer_config.json special_tokens_map.json \
  --local-dir ../models/llama2-7b-public
source script/setup/env.sh
```

`script/setup/env.sh` selects this directory automatically when its configuration and tokenizer files are present.

### Download the Bridge checkpoint

```bash
.venv/bin/python script/setup/download_memvla_bridge.py
```

The downloader retrieves the official `shihao1895/memvla-bridge` checkpoint and metadata into:

```text
models/model_b/checkpoints/memvla-bridge.pt
```

The checkpoint is approximately 33.5 GB. Hugging Face credentials, if needed, should be supplied through the Hugging Face CLI or environment and must not be committed.

## Evaluation

Run the complete four-task Bridge evaluation from `myMemoryVLA/`:

```bash
source script/setup/env.sh
EXPERIMENT_MODE=query QUERY_RETRIEVAL_TOP_K=4 \
  bash script/eval/bridge/eval_bridge.sh
```

To reproduce the full-history comparison:

```bash
EXPERIMENT_MODE=baseline bash script/eval/bridge/eval_bridge.sh
```

To evaluate another compatible checkpoint:

```bash
CKPT_PATH=/absolute/path/to/checkpoint.pt \
EXPERIMENT_MODE=full \
  bash script/eval/bridge/eval_bridge.sh
```

The launcher evaluates cube, carrot, spoon, and eggplant manipulation with 24 object variations each. Logs, rollout videos, and action plots are written below the selected model directory under `eval_simpler/`.

### Experiment modes

| Mode | Query retrieval | Episodic memory | Spatial memory |
|---|:---:|:---:|:---:|
| `baseline` | No | No | No |
| `query` | Yes | No | No |
| `episodic` | No | Yes | No |
| `query_episodic` | Yes | Yes | No |
| `full` | Yes | Yes | Yes |
| `spatial` | No | No | Yes (direct action conditioning) |

## Training

Training expects an RLDS dataset beneath `DATA_ROOT_DIR`. The ManiSkill launcher defaults to the full QueryVLA configuration while freezing the pretrained VLM and action policy so the new memory pathways can be trained.

```bash
source script/setup/env.sh

DATA_ROOT_DIR=/absolute/path/to/datasets \
PRETRAINED_CKPT=../models/model_b/checkpoints/memvla-bridge.pt \
EXPERIMENT_MODE=full \
MAX_STEPS=10000 \
SAVE_INTERVAL=2500 \
  bash script/train/maniskill/train_maniskill.sh
```

Use a dry run to inspect the generated training command without starting a job:

```bash
DRY_RUN=true EXPERIMENT_MODE=full \
  bash script/train/maniskill/train_maniskill.sh
```

`baseline` and `query` are evaluation-only configurations when both the pretrained VLM and action model are frozen.

## Tests

Focused retrieval and training-scope checks can be run from `myMemoryVLA/`:

```bash
.venv/bin/python -m pip install pytest
.venv/bin/python -m pytest \
  vla/spatial/test_retrieval.py \
  vla/test_ablation_safety.py \
  vla/test_training_scope.py
```

## Reproducibility Notes

- Report the checkpoint, experiment mode, random seed, task-level successes, and number of episodes for every evaluation.
- Do not compare results from different checkpoints or protocols as if they were a matched ablation.
- A one-episode difference across 96 trials is not sufficient evidence of a reliable accuracy improvement.
- The Bridge checkpoint includes the complete Llama state. The local `llama2-7b-public` directory supplies architecture and tokenizer files only.

## Acknowledgments

QueryVLA builds on MemoryVLA and uses SimplerEnv/ManiSkill2-real2sim for simulated robot evaluation. Third-party source and assets remain subject to their respective licenses and citation requirements.
