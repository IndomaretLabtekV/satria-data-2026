# Kronologi Sesi

## 1. Audit notebook DINOv3 awal

Pipeline awal adalah DINOv3 ViT-L/16 frozen pada raw official train.

Masalah yang ditemukan:

- Dataset sempat bukan raw official karena class counts berbeda.
- Hugging Face token/gated access sempat gagal.
- Forward FP16 DINOv3 pada T4 menghasilkan feature non-finite.
- Cache dan processor perlu dibuat fail-closed.

Solusi final:

- raw counts dikembalikan ke 9.999 / 3.961 / 12.567;
- backbone compute FP32;
- feature storage FP16 hanya setelah finite checks;
- dua T4 melalui DataParallel;
- feature cache berbentuk shards;
- processor/resolusi dikunci;
- test tidak disentuh saat screen.

## 2. Smoke test

Smoke test berhasil pada 300 gambar.

Hasil:

- raw counts benar;
- orig dan hflip feature extraction berhasil;
- lima recipe head berhasil dibandingkan;
- MLP concat menjadi kandidat terbaik;
- smoke score tidak dipakai sebagai keputusan karena validation sangat kecil.

## 3. Full-data one-fold screen

Seluruh 26.527 train dipakai, tetapi hanya fold 0 untuk recipe selection.

Hasil:

- best recipe: `mlp_concat_weighted_ce`;
- fold 0 macro F1: **0.985483**;
- original view lebih baik daripada orig+hflip pada screen;
- confusion terbesar tetap Recyclable vs Organic.

Recipe kemudian dikunci.

## 4. Full 5-fold DINO raw

Full run selesai:

- 5 folds;
- 2 seeds per fold: 42 dan 314;
- 10 head checkpoints;
- test feature dan submission berhasil dibuat;
- tidak ada upload otomatis.

File screen tidak muncul pada full run karena memang hanya dibuat di screen mode.

## 5. Evaluasi DINO raw

Full run menunjukkan:

- folds 1–4 lebih tinggi daripada fold 0;
- variasi fold rendah;
- orig-only tetap dipilih karena gain hflip di bawah threshold;
- submission berhasil dibuat tetapi tidak digunakan.

## 6. Target OOF 0.999 dan submission

Pengguna menargetkan LB 99.8925.

Kesimpulan:

- OOF 0.999 bukan syarat mendapatkan LB 99.8925.
- Hubungan OOF dan LB tidak stabil pada proyek ini.
- Mengurangi sekitar 402 error menjadi 20–30 tidak realistis hanya dengan mengganti head.
- Setelah pengguna menjelaskan submission hanya tiga per bulan dan tersisa dua, keputusan final menjadi:
  - jangan submit raw DINO sekarang;
  - raw DINO hanya baseline diagnostik.

## 7. Koreksi terkait peserta lain

Assistant sempat salah menyarankan mencari detail notebook peserta lain.

Keputusan final setelah koreksi pengguna:

- jangan meminta atau memakai notebook/kode/checkpoint/config privat peserta lain;
- skor peserta lain hanya benchmark eksternal;
- semua eksperimen memakai data, kode, dan artifact tim sendiri.

## 8. Analisis ConvNeXt raw

ConvNeXt full milik pengguna memakan sekitar **9 jam 4 menit**, sehingga tidak ingin diulang.

Artifact OOF dan checkpoint dianalisis tanpa retrain.

Kesimpulan:

- DINO lebih kuat sebagai single model;
- ConvNeXt tetap complementary untuk diagnosis;
- ConvNeXt tidak perlu dilatih ulang.

## 9. Export test probabilities

Dibuat dua script inference-only.

DINO:

- memakai `test_prediction_audit.csv`;
- cocok persis dengan submission lama;
- menghasilkan `test_probs_dinov3.csv`;
- counts: 521 / 199 / 738.

ConvNeXt:

- inference lima checkpoint pada CPU;
- 97 exact train-test SHA256 matches;
- cocok persis dengan dua submission lama;
- menghasilkan `test_probs_convnext.csv`;
- counts: 523 / 201 / 734.

Keputusan:

- kedua file hanya artifact audit;
- tidak boleh dipakai untuk tuning/cleaning.

## 10. Manual-review queue

OOF ConvNeXt dan DINO disejajarkan.

Dibuat:

- `manual_review_queue_consensus_174.csv`
- `manual_review_queue_all_oof_errors_729.csv`
- `copy_manual_review_images.py`
- `MANUAL_REVIEW_QUEUE_README.md`

Kelompok:

- P1: kedua model salah, prediksi sama — 174.
- P2: kedua model salah, prediksi berbeda — 16.
- P3: DINO salah, ConvNeXt benar — 210.
- P4: ConvNeXt salah, DINO benar — 329.

Tidak ada auto-relabel.

## 11. Constraint final satu model

Pengguna menegaskan final Satdat harus mengikuti pendekatan single-model seperti proyek terdahulu.

Hard constraint final:

- tidak ada ensemble pada training/inference final;
- ensemble hanya diagnostic/manual review.

## 12. Notebook cleaned

Pengguna sempat ingin full-run DINO pada dataset manual-cleaned.

Notebook awal cleaned memiliki bug:

- `train_df` dipakai sebelum dibuat;
- expected constants hilang;
- raw-count references masih tersisa;
- artifact path berisiko menimpa raw run.

Dibuat `satdat_fixed_cleaned_dinov3.ipynb`.

Yang diubah hanya layer dataset/audit:

- counts cleaned dinamis;
- total tetap 26.527;
- fold baru berdasarkan cleaned labels;
- artifact dipisahkan;
- model, optimizer, loss, preprocessing, TTA, seeds, dan inference tidak diubah.

Namun cleaned run kemudian tidak lagi menjadi prioritas utama.

## 13. Informasi eksternal raw DINO

Peserta dengan LB 99.7311 menyarankan:

- jangan terlalu agresif relabel;
- preprocessing standar;
- fokus pada model DINO lebih besar.

Kesimpulan akhir sesi:

- pernyataan bahwa cleaning selalu tidak berguna pada 26k tidak sepenuhnya universal;
- tetapi pada kondisi proyek ini, expected gain lebih besar dari model improvement;
- raw official labels terbukti mampu menghasilkan LB tinggi;
- raw menjadi canonical development dataset;
- pause relabeling;
- fokus pada model DINOv3.
