# Current Grounding

## Current best
- DINOv3 ViT-7B LVD-1689M
- Frozen 100%
- Native 256
- Official final LayerNorm
- Final CLS + true-patch mean
- V7 regularized_mlp_final
- Five-fold OOF Macro F1: 0.9901360067264733

## Current status
- V7: adopted
- V8 specialist: rejected
- V9 drop/relabel cleaning: rejected
- V10 multi-seed original-data ensemble: next active experiment
- Final end-to-end notebook: not yet built

## Current safe submission
- Submission 1 = V7 five-fold probability average

## Candidate submission 2
- V10 three-seed regularized-head ensemble, only if OOF gate passes

## Canonical data policy
- Raw official train remains canonical
- No global cleaning of validation
- No test use during development
- No pseudo-label
