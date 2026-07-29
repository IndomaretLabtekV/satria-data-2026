# Next Actions

1. Create V10 prompt/notebook.
2. Use V7 cache only.
3. Reproduce fold-0 V7 seed-42 control exactly.
4. Train same regularized head with seeds 2026 and 3407.
5. Evaluate each seed and three-seed probability average.
6. Require stable Macro F1 gain, lower error, and no Electronic degradation.
7. Only after fold-0 pass, run all five folds.
8. Decide whether V10 standalone or V7+V10 is Submission 2.
9. Stop research after V10.
10. Build one end-to-end notebook:
   - optional train-cache rebuild
   - five-fold training
   - one-time test feature extraction
   - two submission outputs
   - reproducibility/audit artifacts
