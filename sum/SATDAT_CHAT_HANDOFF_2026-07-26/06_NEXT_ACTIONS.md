# Next Actions

## 1. Bekukan semua artifact

Simpan:

- raw dataset;
- cleaned dataset yang sudah ada;
- raw DINO full artifacts;
- ConvNeXt checkpoints;
- OOF kedua model;
- test probability exports;
- manual-review queues;
- semua submission files.

## 2. Eksperimen DINO lebih kuat

Prioritas:

- public DINOv3 checkpoint lebih besar dari ViT-L;
- raw official labels;
- satu fold;
- satu seed untuk screening;
- preprocessing standar;
- satu variabel berubah.

Baseline:

- fold 0 = 0.985022.

Layak full jika:

- sekitar 0.988+;
- atau ada improvement error pattern yang jelas.

## 3. Jika model lebih besar tidak cocok

Partial fine-tuning ViT-L:

- unfreeze 1–2 block terakhir;
- backbone LR sangat kecil;
- head LR lebih besar;
- satu fold dahulu;
- pantau VRAM, log loss, per-class F1, dan R/O confusion.

## 4. Resolusi

Setelah model stabil:

- uji 448 atau 512;
- satu fold;
- jangan dicampur dengan perubahan besar lain.

## 5. Full run

Full 5-fold hanya ketika:

- fold 0 naik jelas;
- tidak ada leakage;
- error distribution membaik;
- biaya GPU layak;
- pipeline tetap single model.

## 6. Submission

- Jangan submit raw baseline.
- Submission kedua hanya kandidat yang jelas unggul dan stabil.
- Submission ketiga untuk refinement final.

## 7. Cleaning bila model mentok

- buka kembali cleaned dataset/queue 174;
- review manual saja;
- jalankan cleaned DINO sebagai ablation;
- jangan menganggap OOF cleaned otomatis lebih dekat ke LB.
