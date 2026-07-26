# MASTER HANDOFF — BDC SATRIA DATA 2026

Tanggal grounding: **26 Juli 2026**

---


# Current Grounding dan Keputusan Terbaru

## Tujuan

- Kompetisi: BDC Satria Data 2026, klasifikasi gambar sampah tiga kelas.
- Target leaderboard pengguna: minimal **99.8925**.
- Hanya ada **dua submission tersisa untuk bulan ini**.
- Leaderboard tidak boleh dipakai sebagai alat debugging.

## Dataset resmi

Raw official class counts:

- Label 0 / Recyclable: **9.999**
- Label 1 / Electronic: **3.961**
- Label 2 / Organic: **12.567**
- Total: **26.527**

Keputusan terbaru:

- **Raw official labels menjadi canonical development dataset.**
- **Pause relabeling lanjutan untuk saat ini.**
- Dataset hasil review manual tetap disimpan sebagai ablation/cadangan.
- Cleaning tidak dibuang, tetapi bukan jalur utama berikutnya.
- Jika cleaning dibuka lagi, semua relabel tetap manual setelah inspeksi visual.

## Model utama

- Keluarga utama: **DINOv3**, bukan ConvNeXt.
- DINOv3 raw lebih kuat, lebih stabil, dan lebih cepat daripada ConvNeXt pengguna.
- Baseline saat ini: DINOv3 ViT-L/16 frozen, head `mlp_concat_weighted_ce`.
- Notebook final wajib **satu model**, tanpa ensemble.

## Ensemble

Ensemble hanya boleh dipakai untuk:

- diagnosis;
- mengukur diversity;
- mengurutkan manual review;
- membandingkan error ConvNeXt dan DINO.

Ensemble tidak boleh menjadi final notebook atau final submission.

## Relabeling

- Tidak ada auto-relabel.
- Model hanya memberi kandidat review.
- Semua gambar harus dicek manual.
- Jika yakin, pengguna memindahkan gambar sendiri.
- Jika ambigu/tidak yakin, label dibiarkan.
- `manual_labeling.csv` tidak boleh dibuka atau digunakan.
- Test probabilities tidak boleh digunakan untuk cleaning.

## Strategi eksperimen berikutnya

Urutan prioritas:

1. DINOv3 public checkpoint yang lebih kuat tetapi masih muat/stabil.
2. Satu fold dahulu untuk setiap perubahan backbone, resolusi, atau fine-tuning.
3. Partial fine-tuning ViT-L bila model lebih besar tidak memberi gain atau tidak muat.
4. Uji resolusi lebih tinggi setelah arsitektur/fine-tuning stabil.
5. Full 5-fold hanya untuk kandidat yang jelas lebih kuat.

Baseline fold 0:

- DINOv3 ViT-L frozen raw: **0.985022**

Ambang praktis untuk layak full:

- Sekitar **0.988+** pada fold 0, atau bukti kuat bahwa pola error membaik.

## Submission

- Raw DINO yang sudah selesai **belum disubmit**.
- Submission kedua harus kandidat high-confidence.
- Submission ketiga disimpan untuk refinement final.
- Skor peserta lain 99.7311 hanya benchmark eksternal.
- Tidak boleh meminta notebook, kode, konfigurasi privat, atau artifact peserta lain.


---


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


---


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


---


# Rules dan Hard Constraints

## Integritas kompetisi

- Pengembangan mandiri.
- Jangan meminta/memakai notebook, kode, checkpoint, atau config privat peserta lain.
- Public pretrained model boleh digunakan dan harus dapat didokumentasikan.
- Hanya official train dan informasi visual gambar.
- Test tidak boleh digunakan untuk training, validation, model selection, tuning, thresholding, pseudo-labeling, atau adaptation.
- Tidak ada upload Kaggle otomatis.

## Data

- Raw counts:
  - 0: 9.999
  - 1: 3.961
  - 2: 12.567
- `manual_labeling.csv` tidak boleh digunakan.
- Semua relabel manual.
- Tidak ada auto-relabel.
- Tidak ada external labels.
- Gambar ambigu lebih aman dipertahankan raw.
- Test probabilities tidak boleh memengaruhi cleaning.

## Model

- Final notebook satu model.
- Tidak ada final ensemble.
- Ensemble hanya diagnostic.
- Satu perubahan besar per eksperimen.
- Backbone/resolusi/fine-tuning baru diuji satu fold dulu.
- Full 5-fold hanya jika gain jelas.
- Jangan mengejar 7B secara buta; gunakan model terbesar yang benar-benar muat/stabil pada dua T4.

## Submission

- Total tiga submission per bulan.
- Satu sudah digunakan.
- Dua tersisa.
- Raw DINO baseline belum disubmit.
- Submission kedua harus kandidat high-confidence.


---


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


---


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
