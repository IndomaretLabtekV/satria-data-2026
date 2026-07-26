# Artifact Inventory

## Notebook

- `dinov3.ipynb`
- `dinov3-fullrun.ipynb`
- `convnext-full-raw.ipynb`
- `satdat.ipynb`
- `satdat_fixed_cleaned_dinov3.ipynb`

## Prompt perbaikan

- `PROMPT_REVISE_V5_DINOV3.md`
- `PROMPT_FIX_V5_DINOV3_FP32.md`

## DINO raw artifacts

Folder:

- `DINOv3/v5_dinov3_frozen_raw/`

Isi utama:

- OOF metrics/predictions
- per-fold metrics
- classification report
- high-confidence errors
- selected-view policy
- TTA comparison
- fold assignments
- run manifest
- test prediction audit
- 10 head checkpoints
- train/test feature caches
- submission

## ConvNeXt artifacts

Folder:

- `ConvNeXt2/experiments/v3_convnext_clean/`

Nama folder tetap berasal dari konteks notebook v3, tetapi artifact yang dianalisis adalah raw-data run pengguna.

Isi utama:

- 5 fold checkpoints
- folds
- fold summary
- history
- OOF predictions
- top errors
- train/test scans
- duplicate review
- submission

## Test probability export

- `export_test_probs_dinov3.py`
- `export_test_probs_convnext.py`
- `README_TEST_PROBS.md`
- `test_probs_dinov3.csv`
- `test_probs_convnext.csv`

## Manual review

- `manual_review_queue_consensus_174.csv`
- `manual_review_queue_all_oof_errors_729.csv`
- `copy_manual_review_images.py`
- `MANUAL_REVIEW_QUEUE_README.md`

Status:

- disimpan untuk kemungkinan cleaning di masa depan;
- relabeling sedang dipause.
