# Hasil Eksperimen

## DINO one-fold screen

- `mlp_concat_weighted_ce`: **0.985483**
- `mlp_concat_ce`: sekitar **0.984730**
- `linear_concat_ce`: sekitar **0.981580**
- `linear_mean_ce`: sekitar **0.980728**
- `linear_cls_ce`: sekitar **0.979409**

Recipe terkunci:

- MLP head
- concat CLS + patch mean
- weighted cross-entropy

## DINO raw full 5-fold

Overall:

- Fold 0: **0.985022**
- Assessment folds 1–4: **0.986432**
- Full OOF original: **0.986149**
- Full OOF orig+hflip: **0.986239**
- Fold mean: **0.986152**
- Fold std: **0.001358**
- Accuracy: **0.984846**
- Log loss: **0.066029**
- Total rows: **26.527**

Per fold:

- Fold 0: 0.985022
- Fold 1: 0.987244
- Fold 2: 0.988146
- Fold 3: 0.985827
- Fold 4: 0.984520

Per class:

- Recyclable F1: 0.981044
- Electronic F1: 0.991683
- Organic F1: 0.985721

Confusion utama:

- Recyclable → Organic: 141
- Organic → Recyclable: 195

OOF prediction distribution:

- 0: 10.047
- 1: 3.975
- 2: 12.505

Test counts:

- 0: 521
- 1: 199
- 2: 738

TTA:

- orig+hflip naik hanya sekitar 0.000089;
- threshold minimum 0.0002;
- final policy tetap orig-only.

## ConvNeXt raw vs DINO

Pada 26.464 aligned rows:

- ConvNeXt macro F1: sekitar **0.982327**
- ConvNeXt errors: **519**
- DINO errors: **400**

Overlap:

- both correct: 25.735
- Conv wrong, DINO correct: 329
- Conv correct, DINO wrong: 210
- both wrong: 190
- both wrong, same alternative prediction: 174

## Diagnostic blend

Blend hanya untuk mengukur diversity:

- sekitar 38% DINO + 62% ConvNeXt;
- macro F1 sekitar **0.989407**;
- errors: **321**;
- theoretical oracle sekitar **0.993813**.

Tidak boleh dipakai sebagai final ensemble.

## Leaderboard context

- ConvNeXt relabel submission sebelumnya: sekitar **98.0473**.
- Benchmark eksternal raw DINO: **99.7311**.
- Target pengguna: **99.8925+**.
