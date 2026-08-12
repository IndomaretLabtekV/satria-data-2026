# Experiment Log

This file summarizes the experiment trail that led to the final BDC Satria Data 2026 submission. It is intentionally compact; bulky generated artifacts and full research notes are not part of the public repository.

## Validation Baseline

The locked final control recipe used a frozen DINOv3 ViT-7B representation and reached **0.9901662324 five-fold OOF Macro F1** with **287 total OOF errors**. Of those errors, **242** were between Recyclable and Organic, making that class boundary the main bottleneck.

Approximate per-class OOF F1:

| Class | OOF F1 |
| --- | ---: |
| Recyclable | 0.98638 |
| Electronic | 0.99433 |
| Organic | 0.98979 |

## Curated Experiment Trail

| Stage | Notebook | Purpose | Outcome |
| --- | --- | --- | --- |
| Baseline | `01_convnext_baseline.ipynb` | Establish a strong supervised CNN baseline | Useful reference baseline |
| Frozen foundation model | `02_dinov3_vitl_frozen.ipynb` | Test frozen DINOv3 ViT-L embeddings | Promising; motivated scaling |
| Scale-up | `03_dinov3_vit7b_frozen.ipynb` | Frozen DINOv3 ViT-7B with regularized head | Adopted as core representation |
| Patch attention | `04_material_patch_attention.ipynb` | Test material-aware patch aggregation | Rejected; lower validation score |
| Resampling | `05_model_native_resampling.ipynb` | Compare preprocessing interpolation while holding the model fixed | Rejected; no robust gain |
| Texture readout | `06_second_order_texture.ipynb` | Add second-order Gram/texture statistics | Rejected; no robust gain |
| Seed ensemble | `07_seed_ensemble_diagnostics.ipynb` | Measure head-seed variance and mean-softmax ensemble | Rejected; ensemble underperformed the locked control |
| PEFT screen | `08_final_block_lora_screen.ipynb` | Low-cost LoRA on final-block Q/V projections | Rejected at fold-0 gate |

## Final Selection Logic

The final notebook evaluates a richer spatial readout against a strict control using train-only validation. A candidate is adopted only when gains are sufficiently large, repeat across folds, reduce total and Recyclable/Organic errors, and do not degrade the already-strong Electronic class.

The richer variants did not clear those robustness gates, so the final submission retained the simpler frozen ViT-7B control. This was deliberate: the submission was chosen from reproducible validation evidence rather than from post-hoc test manipulation.

## Files Not Included

The original workspace also contained exploratory prompts, external reference notebooks and papers, chat/session handoffs, feature caches, checkpoints, OOF probability matrices, plots, and submission bundles. They were excluded from this public version because they are either non-source working material or unnecessarily large for a GitHub portfolio repository.
