You are Claude Opus 5 operating at Max effort. Act as a principal computer vision research engineer, Kaggle notebook architect, and rigorous codebase investigator.

Your task is to inspect the existing project thoroughly, reason about the strongest feasible next experiment, and then create one production-quality Kaggle notebook for BDC Satria Data 2026.

Use your full reasoning capability internally. Do not expose private chain-of-thought. Record only concise, decision-relevant rationale in the notebook Markdown and in your final response.

<repository_documents>
The repository contains the full history of a waste image classification project. Before creating anything, inspect the actual files and artifacts. Do not rely only on filenames or summaries.

Read these sources first, preferably in parallel when there are no dependencies:

<document index="1">
<source>howtoprompt.md</source>
<purpose>
Prompting guidance for Claude models. Follow its principles while carrying out this task, especially clear instructions, context grounding, XML organization, proactive action, long-context handling, investigation before answering, parallel file reading, minimal overengineering, and self-verification.
</purpose>
</document>

<document index="2">
<source>Petunjuk_Teknis_BDC_Satria_Data_2026.md</source>
<purpose>
Official competition problem, dataset contract, class mapping, Macro F1 metric, submission rules, test isolation requirements, and disqualification constraints.
</purpose>
</document>

<document index="3">
<source>sum/satdat_chat_handoff_full/00_MASTER_HANDOFF.md</source>
</document>

<document index="4">
<source>sum/satdat_chat_handoff_full/01_CHRONOLOGY.md</source>
</document>

<document index="5">
<source>sum/satdat_chat_handoff_full/02_CURRENT_GROUNDING.md</source>
</document>

<document index="6">
<source>sum/satdat_chat_handoff_full/03_PATHS_AND_ARTIFACTS.md</source>
</document>

<document index="7">
<source>sum/satdat_chat_handoff_full/04_NEXT_ACTIONS.md</source>
</document>

<document index="8">
<source>scripts/v7-dinov3-vit7b-frozen-raw.ipynb</source>
<purpose>
Current adopted DINOv3 ViT-7B implementation. Reuse its proven data discovery, raw-data contract, fold construction, safe image loading, two-T4 requirements, final LayerNorm handling, cache integrity, metrics, head training protocol, reproducibility, and leakage guards where applicable.
</purpose>
</document>

<document index="9">
<source>scripts/cari-task-head.ipynb</source>
<purpose>
Most recent V9A cached head-zoo experiment. Study every attempted readout, classifier, blend, specialist, development result, assessment result, and final rejection decision.
</purpose>
</document>

<document index="10">
<source>results/v9a_v7_cached_head_zoo/</source>
<purpose>
Actual V9A result artifacts. Treat these results as more authoritative than stale summaries. Inspect data_contract.json, development leaderboards, locked recipes, assessment metrics, and final_train_only_decision.json.
</purpose>
</document>

<document index="11">
<source>ref/code/ver34_clean_end_to_end.ipynb</source>
<purpose>
Use this only as a reference for polished one-notebook end-to-end organization, artifact packaging, reproducibility documentation, full-train retraining, test inference, submission generation, and saved-checkpoint inference. Do not copy its face-classification-specific logic.
</purpose>
</document>

<document index="12">
<source>ref/paper/</source>
<purpose>
Review only papers that are directly relevant to DINOv3 frozen features, feature readout, spatial or patch pooling, waste classification, and efficient transfer learning. Use them as supporting context, not as permission to add external labeled data.
</purpose>
</document>
</repository_documents>

<project_context>
Competition: Big Data Challenge Satria Data 2026.

Task: classify each waste image into exactly one of:

* 0 = Recyclable
* 1 = Electronic
* 2 = Organic

Official raw training set:

* Recyclable: 9,999
* Electronic: 3,961
* Organic: 12,567
* Total: 26,527 images

Official test set:

* 1,458 unlabeled images
* Submission order must exactly follow the official template
* Evaluation metric is Macro F1

Current date: July 28, 2026.

Official submission deadline: July 30, 2026 at 16:00 WIB.

The user intends to run the new notebook on Kaggle today using exactly two Tesla T4 GPUs.

The user is currently around leaderboard rank 101. The approximate target scores are:

* Minimum desired: 99.6179
* Stretch target: 99.9462

These leaderboard values are only motivational context. Never tune using test images, leaderboard behavior, previous test predictions, manual test inspection, or hidden-label assumptions.
</project_context>

<current_grounding>
The current adopted model is V7:

* Backbone: `facebook/dinov3-vit7b16-pretrain-lvd1689m`
* DINOv3 ViT-7B trained on LVD-1689M
* Backbone fully frozen
* Input size 256×256
* Original view only
* Direct-square resize
* Bilinear interpolation with antialiasing
* RGB conversion after EXIF transpose
* ImageNet normalization
* FP16 frozen backbone
* Backbone sharded across exactly two Tesla T4 GPUs
* No DataParallel
* No CPU or disk offload
* Official pretrained final LayerNorm applied per token before pooling
* Four final transformer blocks cached
* Register tokens excluded from patch pooling
* Cached information per block:

  * CLS token
  * mean of true patch tokens
* Feature pooling computed in FP32
* Cache stored in FP16
* Seed 42
* Five stratified folds
* Fold 0 used for development
* Folds 1–4 kept untouched until the candidate recipe was locked

V7 selected head:

* Final block only
* Concatenated final CLS and final true-patch mean
* LayerNorm
* Linear 8192 → 512
* GELU
* Dropout 0.40
* Linear 512 → 3
* Balanced class weights calculated from each training partition
* Cross entropy with label smoothing 0.05
* AdamW
* Learning rate 8e-4
* Weight decay 1e-4
* Cosine scheduler
* Maximum 15 epochs
* Early stopping patience 5
* Gradient clipping at 1.0

V7 five-fold OOF Macro F1:

`0.9901360067264733`

The dominant remaining error is Recyclable versus Organic. Electronic is nearly saturated.

V8 R/O specialist was rejected.

V9 drop and relabel cleaning was rejected.

V9A tried many readouts and heads using the old V7 cache. Its strongest development-fold candidate did not produce a sufficiently stable assessment gain.

V9A final assessment:

* Best recipe was a blend, but this project must not use it in the new notebook
* Best assessment Macro F1: approximately 0.9904393
* Control assessment Macro F1: approximately 0.9903008
* Gain over control: approximately +0.0001385
* Both had 225 errors
* Best recipe won only two of four assessment folds
* Adoption recommendation: false

The main conclusion is that further head search over the old cache has reached diminishing returns. A new richer embedding cache is now the highest-value experiment.
</current_grounding>

<primary_hypothesis>
The old V7 cache irreversibly discarded most patch-level spatial and distributional information.

Averaging all 256 patch tokens removes signals such as:

* texture distribution,
* foreground area,
* localized material cues,
* strongest semantic regions,
* spatial object layout,
* variation between image regions,
* whether a material occupies the main object or only the background.

These signals may matter specifically for Recyclable versus Organic classification.

The new experiment should therefore focus on patch-aware DINOv3 ViT-7B embeddings, not on another broad classifier-head zoo.
</primary_hypothesis>

<required_backbone>
Use the timm model:

* Hugging Face repository: `timm/vit_7b_patch16_dinov3.lvd1689m`
* timm model name: `vit_7b_patch16_dinov3.lvd1689m`
* Pretrained on LVD-1689M
* Input size: 256×256
* Hidden dimension expected from the official model output: 4096
* Unpooled output expected to contain:

  * one CLS token,
  * four register tokens,
  * 256 spatial patch tokens

Important implementation notes from the model card:

* The original QKV projection biases were all zero.
* timm disables QKV bias for this model rather than loading unnecessary zero-valued parameters.
* The original model stores RoPE periods through bfloat16, while timm initializes them in float32.
* Keep timm's default float32 RoPE-period behavior unless code-grounded evidence shows it must be changed.
* Record this implementation difference in the notebook manifest.
* Do not claim that changing from Transformers to timm alone should create a major gain.
* The primary source of potentially new signal is richer patch-aware pooling.
  </required_backbone>

<non_negotiable_authoring_constraints>
During this authoring task:

1. Do not execute the notebook.
2. Do not execute Python locally.
3. Do not load or download the model locally.
4. Do not install packages locally.
5. Do not run training, inference, tests, benchmarks, imports, or syntax checks locally.
6. Do not use a local GPU or CPU to validate project code.
7. Do not run any project script.
8. Read-only filesystem inspection is allowed.
9. Writing or editing the target notebook file is allowed.
10. Create exactly one new project file:
    `scripts/v10-dinov3-vit7b-timm-rich-spatial-end-to-end.ipynb`
11. Do not modify existing notebooks, results, summaries, papers, or scripts.
12. Do not create temporary scripts, helper modules, progress files, alternate notebooks, Markdown reports, or generated datasets during authoring.
13. The notebook itself may create caches, checkpoints, metrics, plots, submissions, and ZIP artifacts only when the user later runs it on Kaggle.
14. Do not merely recommend code. Implement the complete notebook.
    </non_negotiable_authoring_constraints>

<competition_constraints>
The notebook must enforce all of the following:

* Use only images supplied by the competition.
* Use official raw training labels as the canonical labels.
* Do not add external labeled images.
* Do not use metadata as predictive features.
* Do not use image dimensions, filenames, paths, IDs, or EXIF metadata as predictive features.
* Do not use official test images for training, validation, model selection, calibration, threshold tuning, or hyperparameter tuning.
* Do not use pseudo-labeling on test.
* Do not inspect test images manually for model decisions.
* Do not load external test labels.
* Do not load previous submissions for blending or decision correction.
* Do not use leaderboard feedback as a training signal.
* Test images may be discovered and processed only after the train-only recipe selection is cryptographically and programmatically locked.
* Preserve the exact official submission row order.
* Output class codes 0, 1, and 2.
  </competition_constraints>

<single_model_constraint>
The final prediction pipeline must be one model only:

* One DINOv3 ViT-7B frozen backbone
* One selected classifier head
* One original image view
* One deterministic inference pass
* One final full-training head checkpoint
* One probability matrix
* Argmax classification

Forbidden:

* Fold-model ensembling
* Seed ensembling
* Probability blending
* Model soups
* Specialist blending
* V7/V10 blending
* Prior-submission blending
* Test-time augmentation
* Multi-crop inference
* Horizontal-flip inference
* Multiple backbone families
* Manual prediction correction

Cross-validation models may be trained temporarily for train-only evaluation, but they must not be combined for the final test prediction. After selection, retrain one head from scratch on all official raw training rows.
</single_model_constraint>

<brainstorming_requirement>
Before implementing, investigate the project and evaluate the proposed approach critically.

Internally consider at least these hypotheses:

1. The main gain can come from richer spatial and distributional pooling of DINOv3 patch tokens.
2. A timm implementation difference alone is unlikely to provide a large gain.
3. Richer embeddings may overfit or introduce noisy background cues.
4. A simpler subset of the proposed statistics may generalize better than using every branch.
5. The bottleneck may partly be label ambiguity that no frozen readout can fully solve.
6. A technically different approach may have higher expected value under the two-day deadline.

You are allowed to propose and implement a better approach only when it satisfies every condition below:

* It is grounded in the inspected project artifacts or relevant included papers.
* It can run on Kaggle T4×2.
* It remains fully train-only during selection.
* It uses no external labeled data.
* It keeps the DINOv3 ViT-7B backbone frozen.
* It creates one end-to-end notebook.
* It produces one final single model.
* It does not require a broad new head zoo.
* It is realistic to run today.
* It has a clearer expected benefit than patch-aware pooling.

Do not stop after brainstorming and do not return a list of ideas. Choose the strongest feasible design and implement it.

If no alternative clearly dominates, use the patch-aware design specified below.

Document a concise design decision in the notebook's opening Markdown:

* what approach was chosen,
* what alternatives were considered,
* why the final approach was chosen,
* what information is genuinely new relative to V7 and V9A,
* what risks remain.
  </brainstorming_requirement>

<preprocessing_contract>
For the primary experiment, preserve V7 image preprocessing exactly to avoid confounding representation changes with geometry changes:

1. Open the image safely with PIL.
2. Apply `ImageOps.exif_transpose`.
3. Convert to RGB.
4. Resize directly to 256×256.
5. Use bilinear interpolation with antialiasing.
6. Convert to tensor.
7. Normalize with ImageNet mean and standard deviation.
8. Use original view only.
9. Use no random image augmentation during frozen feature extraction.
10. Do not use center crop.
11. Do not preserve aspect ratio through letterboxing in this experiment.
12. Do not silently replace this with timm's resolved default transform.

The notebook must explicitly explain that 256×256 is the native model resolution, while retaining V7's exact resize pipeline makes the comparison cleaner.

Keep model-native bicubic preprocessing as a documented future ablation only. Do not implement it as an additional candidate in this notebook unless your repository-grounded brainstorming demonstrates an overwhelming reason and it does not expand the experiment materially.
</preprocessing_contract>

<token_extraction_contract>
Implement robust extraction of the final four transformer blocks.

Requirements:

1. Use the actual timm model structure. Do not assume API details without inspecting the model implementation patterns available in the repository or official timm conventions.
2. Obtain the raw token sequence from each of the final four blocks.
3. Apply the official pretrained final normalization layer per token before any pooling.
4. Do not apply final normalization twice.
5. Add a preflight equivalence check showing that the normalized final-block tokens match the model's normal `forward_features` final-token output within a justified FP16 tolerance.
6. Derive prefix-token and register-token counts from model attributes or verified configuration whenever possible.
7. Assert the expected contract:

   * total token count 261,
   * prefix token count 5,
   * register token count 4,
   * true patch token count 256,
   * hidden size 4096.
8. Treat prefix token 0 as CLS.
9. Exclude all four register tokens from every patch statistic.
10. Reshape true patch tokens from `[B, 256, 4096]` to `[B, 16, 16, 4096]` only after validating token ordering and grid size.
11. Compute pooling in FP32.
12. Store cached features in FP16.
13. Reject NaN or Inf values immediately.
14. Never use `forward_head()` for feature extraction because timm's default classifier pooling may differ from the desired manual readout.
15. Keep the backbone in evaluation mode with all parameters frozen.
    </token_extraction_contract>

<rich_embedding_contract>
The cache must preserve branch identity explicitly.

Preferred full representation per image:

From each of the final four normalized blocks:

1. CLS token
2. Mean of the 256 true patch tokens

This creates eight cross-layer branches.

From the normalized final block only:

3. Patch standard deviation, using `unbiased=False`
4. Patch maximum, calculated independently for each feature dimension
5. Mean of the top 10 percent salient patches
6. Mean of the top 25 percent salient patches
7. Mean of the top 50 percent salient patches
8. Top-left quadrant patch mean
9. Top-right quadrant patch mean
10. Bottom-left quadrant patch mean
11. Bottom-right quadrant patch mean

Across all four blocks, this produces 17 named branches in total:

* 8 cross-layer CLS/patch-mean branches
* 9 final-block spatial or distributional branches

Do not select salient patches using raw token L2 norm after LayerNorm because token norms may become nearly uniform.

Use final CLS-to-patch cosine similarity:

```python
cls_unit = F.normalize(final_cls.float(), dim=-1, eps=1e-6)
patch_unit = F.normalize(final_patches.float(), dim=-1, eps=1e-6)
saliency = torch.einsum("bd,bnd->bn", cls_unit, patch_unit)
```

Then:

* top 10 percent: use a deterministic integer `k`, approximately 26 of 256 patches
* top 25 percent: 64 patches
* top 50 percent: 128 patches

Use `torch.topk`, gather the selected true patch tokens, and average in FP32.

For quadrant pooling:

* reshape to a 16×16 grid,
* split it into four non-overlapping 8×8 quadrants,
* average all 64 patch tokens in each quadrant.

Store features as a tensor shaped conceptually like:

`[N, 17, 4096]`

Also store an ordered branch-name list and include it in every cache signature.

If your investigation identifies a strong reason to remove one noisy branch such as patch max, you may do so only before implementation and must document the decision. Do not perform a broad combinatorial branch search.
</rich_embedding_contract>

<feature_cache_contract>
The frozen backbone is expensive and should run only once per image.

Implement:

* Resumable sharded cache extraction
* Atomic writes
* Per-shard completion metadata
* Deterministic row order
* Cache integrity checks
* Cache schema version
* Ordered image-ID signature
* Label signature
* Fold signature
* Preprocessing signature
* Model repository and immutable revision
* timm version
* PyTorch version
* CUDA version
* GPU names
* Backbone dtype
* Pooling dtype
* Storage dtype
* Branch names
* Branch count
* Hidden size
* Token contract
* RoPE-period dtype behavior
* QKV-bias behavior
* Extraction timing and throughput
* Test-access flag
* Manual-test-label-access flag

Recommended train cache storage:

* FP16 shards
* approximately 128 or 256 rows per shard
* each shard contains feature tensor, labels, global indices, and image IDs
* manifest written only after validation
* corrupted or incomplete shards must be recomputed safely

Do not store raw `[N, 256, 4096]` patch-token tensors.

Do not delete a completed valid cache.

The notebook must be restartable after Kaggle interruption without recomputing valid shards.
</feature_cache_contract>

<kaggle_runtime_contract>
The notebook will be run only on Kaggle.

Require:

* `/kaggle/working`
* exactly two visible CUDA GPUs
* both GPUs must identify as Tesla T4
* FP16 model weights
* no DataParallel
* no DistributedDataParallel
* no CPU offload
* no disk offload
* no model layer left on CPU
* no model parameter left on `meta`
* fail closed when the device map is invalid
* use both T4 GPUs through explicit model sharding
* prevent individual transformer blocks from being split across devices
* use Accelerate or another appropriate official mechanism for dispatching a timm model
* audit the final device map
* print parameter counts and device allocation
* include a small preflight batch before full extraction
* fail before full extraction if shapes, dtypes, devices, normalization, or token counts are wrong

The notebook author must not assume that `timm.create_model(..., pretrained=True)` supports a Transformers-style `device_map` argument.

Implement a technically sound loading and dispatch strategy for the large timm checkpoint. Prefer an immutable Hugging Face revision and a memory-efficient loading path. Resolve and record the exact 40-character commit SHA at Kaggle runtime.

Use the Kaggle secret `HF_TOKEN`. Provide a clear actionable error when:

* the token is absent,
* the DINOv3 license was not accepted,
* the repository cannot be downloaded,
* the revision cannot be resolved,
* the model cannot be distributed entirely across the two GPUs.

Do not silently downgrade to a smaller model.

A fallback to the existing Transformers ViT-7B backend may be included only as an explicit configuration option if you determine that a reliable timm dispatch path cannot be guaranteed. It must never activate silently. The default and primary implementation must remain timm.
</kaggle_runtime_contract>

<data_contract>
Reuse or improve V7's strict raw-data discovery.

Requirements:

* Search expected Kaggle input roots safely.
* Resolve exactly one official raw train directory.
* The immediate train subdirectories must be exactly:

  * `0_Recyclable`
  * `1_Electronic`
  * `2_Organic`
* Verify official counts exactly.
* Reject symlinks and unsupported entries.
* Sort rows deterministically by official relative image ID.
* Assign labels only from official class folders.
* Build five stratified folds with:

  * `n_splits=5`
  * `shuffle=True`
  * `random_state=42`
* Preserve exact fold reproducibility.
* Save fold assignments and signatures.
* Validation always uses official original labels.
* Do not drop or relabel any training image.
* Do not use old cleaned datasets.
* Do not use previous feature caches unless their complete new V10 cache signature matches exactly.

The official test and template should be resolved separately but not indexed or opened until the train-only selection decision is locked.
</data_contract>

<model_comparison_contract>
Do not create another head zoo.

Implement exactly two main train-only candidates.

<candidate name="timm_control">
Purpose: establish the timm equivalent of V7 using the new cache.

Input:

* normalized final-block CLS branch
* normalized final-block true-patch mean branch
* concatenate to 8192 dimensions

Architecture:

* LayerNorm(8192)
* Linear(8192, 512)
* GELU
* Dropout(0.40)
* Linear(512, 3)

Training protocol must match V7 as closely as possible. </candidate>

<candidate name="rich_spatial_fusion">
Purpose: consume all selected rich embedding branches in one regularized head.

Preferred architecture:

For each branch:

* its own LayerNorm(4096)

Then use one shared projection across branches:

* shared Linear(4096, 256)
* GELU
* modest projection dropout, such as 0.10

Concatenate all projected branches:

* 17 × 256 = 4352 dimensions when all preferred branches are kept

Fusion:

* LayerNorm(fused dimension)
* Linear(fused dimension, 512)
* GELU
* Dropout(0.40)
* Linear(512, 3)

The projection weights should be shared across branch types because all branches live in the same DINO feature space, while branch-specific LayerNorm allows separate scaling.

Do not add branch attention, residual towers, experts, transformers, graph layers, specialist heads, cosine classifiers, tree models, or extra classifier families unless a specific inspected artifact proves the preferred architecture is invalid.

Use the same optimizer and training protocol for the control and rich candidate so the comparison isolates representation quality. </candidate>
</model_comparison_contract>

<head_training_contract>
Use a deterministic and auditable training loop.

Default protocol:

* Seed: 42
* PyTorch deterministic setup where practical
* Balanced class weights computed from the current training partition:
  `total / (num_classes * class_count)`
* CrossEntropyLoss
* Label smoothing: 0.05
* AdamW
* Learning rate: 8e-4
* Weight decay: 1e-4
* Maximum epochs: 15
* Early stopping patience: 5
* CosineAnnealingLR
* Gradient clipping: 1.0
* Head batch size: 256, reduced only if necessary
* Prediction batch size: 512
* Best checkpoint selected by validation Macro F1
* Log loss recorded as a secondary diagnostic
* No threshold tuning
* Final class prediction from argmax

For each evaluation, save:

* Macro F1
* accuracy
* log loss
* per-class precision, recall, and F1
* confusion matrix
* total errors
* Recyclable → Organic errors
* Organic → Recyclable errors
* total R/O errors
* Electronic errors
* confidence summary
* margin summary
* training history
* best epoch
* parameter count
* runtime
  </head_training_contract>

<selection_protocol>
Follow strict staged train-only evaluation.

Phase 1: development fold 0

Train and evaluate:

* `timm_control`
* `rich_spatial_fusion`

The rich candidate passes the development gate only when all are true:

1. Macro F1 gain over control is at least `0.0015`.
2. Total errors decrease.
3. Total Recyclable/Organic errors decrease.
4. Electronic F1 decreases by no more than `0.0005`.
5. Predictions and probabilities are finite.
6. The gain is not caused by row-order or fold mismatch.
7. The rich model does not violate the single-model contract.

Phase 2: locked assessment folds 1–4

Only run the rich candidate on assessment folds if it passes the fold-0 gate.

Before evaluating folds 1–4:

* serialize the selected architecture,
* serialize all hyperparameters,
* serialize branch order,
* serialize the fold-0 decision,
* calculate a recipe signature,
* do not change the recipe after assessment begins.

Adopt the rich candidate only when all are true:

1. Aggregate Macro F1 gain over control is at least `0.0015`.
2. The rich candidate beats control on at least three of four assessment folds.
3. Aggregate total errors decrease.
4. Aggregate R/O errors decrease.
5. Electronic F1 remains stable within `0.0005`.
6. Improvement is not concentrated in only one fold.
7. No leakage or test access occurred.

If the rich candidate fails the gate:

* mark it rejected,
* select `timm_control` as the notebook's train-only fallback recipe,
* do not blend the two,
* do not tune another architecture,
* continue only if the notebook is configured to generate a control submission.

Make this policy explicit through a configuration field such as:

`GENERATE_CONTROL_SUBMISSION_IF_RICH_REJECTED = True`

The final decision must be written to `selection_decision.json` before any test image is opened.
</selection_protocol>

<final_training_contract>
After a recipe is selected using train-only evidence:

1. Determine the full-training epoch count from the selected recipe's cross-validation best epochs.
2. Prefer a robust statistic such as the median rounded to an integer.
3. Reinitialize the selected head from scratch.
4. Train that one head on all 26,527 official raw training rows.
5. Use the exact selected architecture and hyperparameters.
6. Do not early-stop using test information.
7. Save one final checkpoint.
8. Record the full-training history.
9. Do not average fold checkpoints.
10. Do not initialize from a fold checkpoint.
11. Do not combine control and rich heads.
    </final_training_contract>

<test_and_submission_contract>
The notebook may access test only after verifying:

* `selection_decision.json` exists,
* the decision signature matches the current config,
* train cache is complete,
* fold evaluation is complete,
* selected recipe is immutable,
* `test_images_accessed` was false during model selection.

Then:

1. Resolve the official test directory and official submission template.
2. Verify there are exactly 1,458 test images.
3. Preserve the official template's row order.
4. Extract test embeddings using the same:

   * timm model revision,
   * preprocessing,
   * token extraction,
   * branch definitions,
   * dtypes,
   * cache schema.
5. Run one deterministic inference pass with the one final full-training head.
6. Save the probability matrix.
7. Use argmax.
8. Map predictions to numeric codes 0, 1, and 2.
9. Preserve exactly the required columns:

   * `id`
   * `predicted`
10. Validate:

* 1,458 rows,
* no missing values,
* no duplicate IDs,
* all predictions in `{0, 1, 2}`,
* order identical to the template.

11. Save the filename through a clearly editable config:
    `TEAM_NAME = "CHANGE_ME"`
12. Produce:
    `submission_<TEAM_NAME>.csv`

Do not read the submission after generation for manual decision changes. Automated format validation is allowed.
</test_and_submission_contract>

<notebook_structure>
Create a polished, readable, top-to-bottom Kaggle notebook with Markdown explanations and code cells.

Use Indonesian for explanatory Markdown intended for the user and competition judges.

Use clear English names for code identifiers, functions, classes, comments, filenames, and artifact fields.

Recommended sections:

1. Title and executive experiment summary
2. Competition constraints and leakage policy
3. Why V7/V9A plateaued
4. Chosen V10 hypothesis and alternatives considered
5. Runtime instructions
6. Kaggle package installation
7. Imports and global configuration
8. Reproducibility utilities
9. Atomic artifact utilities
10. Environment and dual-T4 preflight
11. HF token and immutable model revision
12. Strict raw-train resolver
13. Safe image loader and preprocessing
14. Dataset indexing and class-count audit
15. Stable five-fold construction
16. Train-only data and fold signatures
17. timm ViT-7B construction and two-GPU dispatch
18. Model/device/token preflight
19. Final-LayerNorm equivalence test
20. Rich pooling implementation
21. Resumable train feature extraction
22. Cache consolidation and integrity audit
23. Dataset classes for cached features
24. Control head
25. Rich spatial-fusion head
26. Shared training and evaluation utilities
27. Fold-0 development comparison
28. Locked recipe decision
29. Folds 1–4 assessment when eligible
30. Final train-only adoption decision
31. Full-training epoch selection
32. Full-training single-head retraining
33. Test-isolation unlock
34. Official test and template resolver
35. Resumable test feature extraction
36. Single-model inference
37. Submission creation and validation
38. Metrics, plots, and error analysis
39. Reproducibility manifest
40. Artifact packaging
41. Final run summary
42. Saved-checkpoint inference shortcut for verification

Keep the notebook focused. Do not add unrelated EDA, decorative animations, external dashboards, or generic tutorial content.
</notebook_structure>

<artifact_contract>
When the notebook is run, place outputs under:

`/kaggle/working/v10_dinov3_vit7b_timm_rich_spatial/`

Expected artifacts include:

* `environment.json`
* `config.json`
* `locked_contract.json`
* `data_contract.json`
* `fold_assignments.csv`
* `fold_signature.json`
* `model_manifest.json`
* `device_map.json`
* `preflight_report.json`
* `feature_cache/train/`
* `feature_cache/test/`
* `cache_manifest_train.json`
* `cache_manifest_test.json`
* `development_metrics.csv`
* `development_metrics.json`
* `locked_recipe_before_assessment.json`
* `assessment_per_fold.csv`
* `assessment_aggregate.csv`
* `selection_decision.json`
* train-only OOF probabilities and predictions
* confusion-matrix figures
* training-history files
* `final_head.pt`
* `final_training_history.csv`
* `test_probabilities.npy`
* `submission_<TEAM_NAME>.csv`
* `final_run_summary.json`
* `artifact_bundle.zip`

The ZIP should contain essential proof and reproducibility artifacts but should not duplicate multi-gigabyte feature caches unless explicitly configured.
</artifact_contract>

<robustness_requirements>
The generated notebook must:

* run from top to bottom on Kaggle,
* use pathlib instead of hard-coded Windows paths,
* avoid stale state between reruns,
* use atomic JSON, CSV, NPY, and checkpoint writes,
* detect incompatible existing caches,
* never reuse an incomplete cache silently,
* show informative progress bars,
* print elapsed time and throughput,
* release the large backbone before head training when safe,
* run garbage collection and CUDA cache cleanup at sensible phase boundaries,
* avoid unnecessary host-memory copies,
* use pinned memory appropriately,
* keep feature extraction under inference mode,
* avoid silent exception swallowing,
* fail with actionable messages,
* avoid arbitrary magic constants without configuration,
* avoid hard-coding specific test predictions,
* avoid excessive abstraction,
* avoid helper classes that are not needed,
* avoid dead code and commented-out experiments,
* avoid unfinished TODO markers except clearly editable user configuration such as `TEAM_NAME`.
  </robustness_requirements>

<examples>
<example>
Situation: The V9A summary says a new head is promising, but `final_train_only_decision.json` says adoption is false.

Correct behavior:
Trust the actual final decision artifact, explain that the assessment gain was too small and unstable, and do not carry the V9A blend into V10. </example>

<example>
Situation: The timm model emits 261 tokens.

Correct behavior:
Verify one CLS token and four register tokens, exclude the four register tokens, and calculate patch statistics from exactly 256 true patch tokens.

Incorrect behavior:
Average tokens 1 through 260 and accidentally include register tokens. </example>

<example>
Situation: The rich head wins fold 0 by 0.0003.

Correct behavior:
Reject it under the locked 0.0015 development gate and avoid opening assessment folds for additional tuning.

Incorrect behavior:
Lower the gate after seeing the result or create more heads until one wins. </example>

<example>
Situation: timm uses a default model transform that differs from V7.

Correct behavior:
Keep V7's direct-square 256×256 bilinear preprocessing for the primary comparison and document the reason.

Incorrect behavior:
Change resize geometry, interpolation, pooling, head, and backend simultaneously without acknowledging the confounds. </example>

<example>
Situation: The model cannot be dispatched fully across two T4 GPUs.

Correct behavior:
Fail with a clear device-map report, or use an explicitly configured and documented non-silent Transformers backend only when that fallback was intentionally enabled.

Incorrect behavior:
Silently offload layers to CPU or disk, silently use one GPU, or silently switch to a smaller model. </example>

<example>
Situation: The notebook author wants to verify syntax locally.

Correct behavior:
Perform a static manual review of the notebook structure and code without executing Python or notebook cells.

Incorrect behavior:
Run Python, nbconvert, pytest, imports, model loading, or any notebook cell locally. </example> </examples>

<tool_use_policy>
Use read-only repository inspection proactively before making claims about the codebase.

When reading multiple independent files, inspect them in parallel where the available tools permit it.

Do not speculate about files you have not opened.

Do not stop at suggestions. After investigation and design selection, write the requested notebook.

Do not perform destructive operations.

Do not delete, rename, or overwrite existing project files.

Do not create a Git commit unless explicitly requested.

Do not use tools to execute project code during authoring.
</tool_use_policy>

<implementation_quality>
Write a high-quality general implementation rather than code designed merely to satisfy superficial checks.

Do not hard-code expected predictions, metrics, or best epochs.

Do not fabricate successful runtime output in notebook cells.

All newly created notebook cells must have empty execution counts and empty outputs.

The notebook must clearly distinguish:

* known historical results,
* hypotheses,
* runtime assertions,
* results that will only exist after the user executes it.

Do not claim that V10 improves V7 before it has been run.

Use the included sources to preserve the project's established conventions wherever they remain correct.
</implementation_quality>

<static_self_review>
After writing the notebook, inspect the complete generated file statically without executing it.

Verify all of the following:

1. Only the requested notebook was created.
2. Existing files were not changed.
3. The notebook uses nbformat 4-compatible structure.
4. Every code cell has empty outputs and no execution count.
5. Imports are internally consistent.
6. All referenced functions and classes are defined before use.
7. Config names are consistent.
8. Artifact paths are Kaggle-safe.
9. No Windows-specific path remains.
10. No local project execution occurred.
11. The official class mapping is correct.
12. Official train counts are correct.
13. The test set is not accessed before selection lock.
14. Register tokens are excluded.
15. Final normalization is applied exactly once.
16. Patch saliency uses CLS-to-patch cosine similarity.
17. Cache branch order is deterministic.
18. Control and rich heads use comparable training settings.
19. No ensemble or TTA exists.
20. Final training creates one head.
21. Submission format is `id,predicted`.
22. Submission order follows the template.
23. Numeric labels are restricted to 0, 1, and 2.
24. The notebook has an actionable HF token error.
25. The notebook audits both Tesla T4 GPUs.
26. No CPU or disk model offload is accepted.
27. Test-access flags are recorded.
28. All major artifacts have signatures.
29. The final checkpoint inference shortcut uses the same selected architecture and preprocessing.
30. No fabricated notebook output is present.

Fix any statically detectable inconsistency before finishing.
</static_self_review>

<final_response_format>
After creating and reviewing the notebook, respond concisely with:

* the exact notebook path,
* confirmation that it was not executed,
* the final chosen approach,
* whether you kept the proposed 17-branch embedding or made a justified adjustment,
* the main runtime assumptions that the user must satisfy on Kaggle,
* any material uncertainty that cannot be verified without running the notebook.

Do not paste the notebook's full JSON or all of its code into the response.
</final_response_format>

<task>
Now inspect the repository thoroughly, choose the strongest feasible design under these constraints, and create exactly:

`scripts/v10-dinov3-vit7b-timm-rich-spatial-end-to-end.ipynb`

Do not execute it locally. Complete the notebook implementation rather than returning only recommendations. </task>