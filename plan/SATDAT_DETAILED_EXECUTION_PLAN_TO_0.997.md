# SATDAT Part 2

# Detailed Execution Plan dari V11A.2 sampai Kandidat Final

**Kompetisi:** BDC Satria Data 2026 Problem 1  
**Task:** Klasifikasi citra sampah 3 kelas  
**Metric utama:** Macro-averaged F1-Score  
**Target aspiratif:** 0.997  
**Deadline resmi:** 30 Juli 2026 pukul 16.00 WIB  
**Tanggal penyusunan:** 29 Juli 2026, Asia/Jakarta  
**Status dokumen:** Execution SSOT  
**State aktif:** V10 champion, V11A.2 belum memiliki hasil final, V11B wajib sebagai data and evaluation checkpoint

---

## 0. Cara Menggunakan Dokumen Ini

Dokumen ini adalah rencana eksekusi, bukan daftar ide. Setiap fase memiliki:

1. tujuan;
2. hipotesis;
3. input yang wajib tersedia;
4. langkah implementasi;
5. artifact yang harus dihasilkan;
6. metrik yang harus dicatat;
7. acceptance gate;
8. stop condition;
9. keputusan lanjutan.

Gunakan aturan berikut selama eksperimen:

- Jangan menjalankan eksperimen berikutnya sebelum artifact fase sebelumnya lolos validasi.
- Jangan memilih kandidat hanya berdasarkan satu angka Macro F1.
- Jangan menambah eksperimen baru ketika kandidat aktif belum memiliki keputusan tertulis.
- Setiap perubahan besar harus dibandingkan dengan control yang memakai split, seed, data, dan preprocessing yang sama.
- Semua hasil negatif tetap dicatat.
- Test hanya dibuka saat inferensi kandidat final.
- Leaderboard tidak dipakai sebagai debugger.

Urutan baca yang disarankan:

1. Section 1 sampai 6 untuk keputusan utama dan deadline path.
2. Section 7 untuk V11A.2.
3. Section 8 sampai 14 untuk V11B.
4. Section 15 untuk V12A.
5. Section 16 sampai 17 untuk geometry dan LoRA.
6. Section 18 sampai 22 untuk final training, submission, recovery, dan checklist.

---

## 1. Executive Decision

### 1.1 Keputusan utama

Target 0.997 tidak realistis jika jalurnya hanya:

```text
cache DINOv3 ViT-7B lama
→ tambah head
→ sweep learning rate
→ pilih skor fold 0 tertinggi
```

Evidence project menunjukkan frozen head path sudah memasuki diminishing returns:

| Model atau eksperimen | Full OOF Macro F1 | Total error | R/O error | Status |
|---|---:|---:|---:|---|
| V5 frozen DINOv3 ViT-L | 0.986149 | sekitar 402 | dominan R/O | baseline lama |
| V7 frozen DINOv3 ViT-7B | sekitar 0.9901 | 287 | 241 | strong baseline |
| V10 frozen ViT-7B upgrade | 0.990166 | belum tersedia di arsip lokal | belum tersedia di arsip lokal | champion historis |
| V11A.1 material branch | 0.990275 | 285 | 242 | signal ada, gain kecil |
| V11A.2 stabilization | belum final | belum final | belum final | fase aktif |

Untuk mendekati 0.997, project membutuhkan tiga jenis perbaikan:

1. **Data and evaluation repair** melalui V11B.
2. **Material-aware representation** melalui spatial statistics dan geometry.
3. **Backbone adaptation** melalui LoRA jika masih ada waktu dan compute.

### 1.2 Posisi V11B

V11B tetap wajib. Fungsinya bukan mengejar skor langsung. V11B harus menghasilkan:

- review queue train-only;
- keputusan review manual;
- duplicate cluster map;
- cleaned manifest;
- duplicate-grouped fold assignments;
- protocol-matched V10 control;
- measurement baseline yang lebih jujur.

Tanpa V11B:

- model dapat mempelajari label salah;
- near-duplicate dapat menyeberang fold;
- gain kecil dapat berasal dari leakage;
- LoRA dapat menghafal noise;
- skor antarversi tidak dapat dibandingkan secara bersih.

### 1.3 Realitas target 0.997

V11A.1 masih memiliki 285 error. OOF 0.997 kira-kira membutuhkan 60 sampai 100 error, tergantung confusion direction dan distribusi kelas. Artinya sekitar 185 sampai 225 error harus diselesaikan.

Implikasinya:

- memperbaiki 16 sampai 26 label issue kuat akan membantu objective dan evaluasi;
- label repair saja tidak cukup;
- head-only gain sebesar 0.0001 sampai 0.0003 tidak cukup;
- adapted representation adalah kandidat upside terbesar;
- leaderboard 0.997 tetap mungkin berbeda dari OOF 0.997 karena test hanya berisi 1.458 gambar.

Tidak ada langkah dalam plan ini yang menjamin 0.997. Tujuannya adalah memaksimalkan probabilitas mendapatkan single model terbaik dengan validasi yang dapat dipertanggungjawabkan.

---

## 2. Hard Constraints

### 2.1 Kompetisi

- Train resmi: 26.527 gambar.
- Test resmi: 1.458 gambar.
- Kelas:
  - `0 = Recyclable`
  - `1 = Electronic`
  - `2 = Organic`
- Metric: Macro F1.
- Maksimal tiga submission.
- Submission terakhir diterima sampai 30 Juli 2026 pukul 16.00 WIB.
- Prediksi test harus dibuat otomatis.
- Urutan test harus sama dengan template resmi.

### 2.2 Data

- Canonical raw counts:
  - Recyclable: 9.999
  - Electronic: 3.961
  - Organic: 12.567
  - Total: 26.527
- Tidak boleh memakai external labeled images.
- Tidak boleh memakai metadata nonvisual sebagai predictive feature.
- Tidak boleh memakai test untuk training, validation, model selection, thresholding, adaptation, pseudo-labeling, atau relabeling.
- `manual-labeling.csv` dan seluruh manual test labels harus tetap dikarantina.
- Tidak ada auto-relabel.
- Relabel train hanya dilakukan setelah inspeksi visual manusia.
- Gambar ambigu tidak boleh dipaksa mengikuti prediksi model.

### 2.3 Model

- Final submission harus berasal dari satu model.
- Final prediction tidak boleh berupa ensemble antar-backbone, antar-fold, antar-seed, atau antar-checkpoint.
- Ensemble hanya boleh dipakai untuk diagnosis dan ranking review queue.
- Public pretrained backbone diperbolehkan dan wajib didokumentasikan.
- Satu perubahan besar per eksperimen.
- Kandidat mahal harus lolos one-fold causal screen sebelum full confirmation.

### 2.4 Reproducibility

- Setiap run memiliki manifest.
- Setiap artifact memiliki checksum.
- Fold assignments tidak dibuat ulang setelah melihat skor.
- Seed dikunci.
- Config disimpan bersama output.
- Failure tidak boleh diam-diam dilanjutkan.
- Non-finite feature atau logit menyebabkan run berhenti.

---

## 3. Known State dan Missing Artifact

### 3.1 Artifact yang tersedia di arsip

Arsip historis memuat:

- notebook V1 sampai V8;
- handoff sampai 26 Juli 2026;
- full V7 analysis bundle;
- V7 fold assignments;
- V7 OOF predictions;
- V7 per-fold metrics;
- V7 high-confidence errors;
- V7 R/O error gallery;
- feature cache manifest;
- model and preprocessing audit;
- reference code;
- 11 paper dan technical notes;
- juknis resmi.

### 3.2 State terbaru yang diketahui dari chat

- V10 adalah historical champion dengan full OOF sekitar 0.990166.
- V11A.1 `material_frozen_global` mencapai 0.990275.
- V11A.1 memiliki 285 total error dan 242 R/O error.
- V11A cache meliputi representasi:
  - global `[26.527, 8.192]`;
  - spatial `[26.527, 64, 512]`.
- V11A.2 memiliki empat kandidat:
  - `lr4e4_plain`
  - `lr2e4_plain`
  - `lr4e4_roaux`
  - `lr4e4_roaux_reg`

### 3.3 Artifact yang belum tersedia di arsip lokal

Sebelum implementasi V11B, wajib impor:

- exact V10 config;
- V10 fold assignments;
- V10 full OOF probabilities;
- V10 per-fold predictions;
- V10 classification report;
- V10 run manifest;
- V11A.1 full OOF probabilities;
- V11A.2 notebook;
- V11A.2 output seluruh seed yang selesai;
- V11 global cache;
- V11 spatial cache;
- cache index atau sample-to-row mapping;
- duplicate analysis artifact terbaru jika threshold atau cluster pernah diperbarui.

### 3.4 Aturan jika artifact terbaru tidak dapat dipulihkan

Jangan menebak struktur V10 atau V11.

Gunakan fallback berikut:

| Artifact hilang | Fallback |
|---|---|
| V10 OOF probabilities | gunakan V7 sebagai ranking signal, tandai V10 signal unavailable |
| V10 exact config | jangan menyebut rerun sebagai exact V10 control |
| V11A.2 output | jalankan V11A.2 terlebih dahulu |
| V11 spatial cache | V12A ditunda |
| duplicate group artifact | rebuild dari raw train dengan threshold yang dikunci sebelum scoring |
| cache row map | fail closed, jangan menyelaraskan berdasarkan row order |

---

## 4. North-Star Metrics dan Decision Metrics

### 4.1 Headline metric

```text
Macro F1 = mean(F1_Recyclable, F1_Electronic, F1_Organic)
```

### 4.2 Metrik wajib setiap run

Setiap run harus melaporkan:

- full OOF Macro F1;
- accuracy;
- log loss;
- per-class precision;
- per-class recall;
- per-class F1;
- confusion matrix;
- total error;
- R/O error;
- Recyclable to Organic error;
- Organic to Recyclable error;
- Electronic error;
- per-fold Macro F1;
- fold mean;
- fold standard deviation;
- per-seed Macro F1;
- seed standard deviation;
- confidence distribution;
- error confidence distribution;
- prediction class counts.

### 4.3 Metrik khusus grouped validation

- duplicate cluster overlap antar-fold, target `0`;
- number of singleton groups;
- number of multi-sample groups;
- fold class counts;
- fold sample counts;
- fold group counts;
- largest group size per fold;
- mixed-label groups unresolved;
- reviewed-sample coverage per fold.

### 4.4 Metrik khusus label audit

- jumlah kandidat per tier;
- jumlah gambar direview;
- jumlah `confirmed_keep`;
- jumlah `corrected_label`;
- jumlah `ambiguous`;
- jumlah `corrupted_or_unusable`;
- confirmation rate per signal;
- correction rate per signal;
- reviewer agreement jika ada dua reviewer;
- correction matrix;
- perubahan class counts;
- perubahan R/O boundary samples.

### 4.5 Decision hierarchy

Urutan keputusan:

1. Integrity gate.
2. Data alignment gate.
3. Leakage gate.
4. Full OOF Macro F1.
5. R/O error.
6. Per-class stability.
7. Per-fold consistency.
8. Per-seed consistency.
9. Log loss and calibration health.
10. Runtime and submission feasibility.

Kandidat dengan Macro F1 lebih tinggi tetap ditolak jika:

- duplicate leakage ditemukan;
- gain hanya muncul pada satu fold;
- Electronic F1 rusak;
- config tidak dapat direproduksi;
- output bergantung pada test-derived decision;
- final inference membutuhkan ensemble.

---

## 5. Master Dependency Flow

```text
Artifact recovery and integrity audit
→ V11A.2 completion
→ Multi-model OOF alignment
→ Duplicate map
→ V11B review queue
→ Blind manual review
→ Cleaned manifest
→ StratifiedGroupKFold
→ Raw grouped V10 control
→ Cleaned grouped V10 control
→ V12A cache-only spatial screen
→ Optional V12B geometry screen
→ Optional V13 LoRA screen
→ Champion selection
→ Single final model retraining
→ Test inference
→ Submission QA
```

### 5.1 Dependency rules

- V11B queue dapat mulai dari V7 dan V10 sebelum V11A.2 selesai.
- Final V11B priority tier baru dikunci setelah V11A.2 probabilities masuk.
- Grouped V10 control baru boleh mulai setelah duplicate groups dan cleaned manifest dikunci.
- V12A dapat berjalan setelah grouped folds terkunci karena memakai cache.
- V12B tidak boleh mengubah split.
- V13 tidak boleh mengubah data policy dan geometry secara bersamaan pada causal screen.
- Final training baru dimulai setelah champion decision ditulis.

---

## 6. Deadline-Constrained Execution Path

### 6.1 Waktu tersedia

Pada saat dokumen ini disusun, sisa waktu menuju deadline sekitar 37 jam. Seluruh roadmap penuh tidak dapat dijalankan serial dengan aman.

Prioritas deadline:

1. pulihkan artifact;
2. selesaikan V11A.2;
3. bangun V11B high-risk queue;
4. review kandidat paling informatif;
5. lock duplicate-grouped split;
6. rerun cache-only control;
7. jalankan V12A jika cache tersedia;
8. train satu final model;
9. sisakan buffer untuk inference dan submission.

### 6.2 Jadwal berbasis jam

`H+0` adalah waktu plan mulai dieksekusi.

| Window | Aktivitas utama | Output wajib | Stop time |
|---|---|---|---|
| H+0 sampai H+1.5 | recovery, checksums, schema audit | artifact registry | H+1.5 |
| H+1 sampai H+5 | V11A.2 selected candidate completion | OOF per seed | H+5 |
| H+1.5 sampai H+4 | build initial V11B queue | review queue v0 | H+4 |
| H+4 sampai H+9 | manual review P0, P1, high-risk P2 | review decisions | H+9 |
| H+8 sampai H+11 | duplicate grouping and fold lock | grouped folds | H+11 |
| H+11 sampai H+16 | protocol-matched V10 controls | raw and cleaned metrics | H+16 |
| H+16 sampai H+21 | V12A cache-only screen and confirmation | V12A decision | H+21 |
| H+21 sampai H+27 | final single-model training | final checkpoint | H+27 |
| H+27 sampai H+30 | test inference and QA | candidate submission | H+30 |
| H+30 sampai deadline | reserve and one permitted refinement | verified final upload | deadline |

### 6.3 Minimum viable V11B jika waktu ketat

Jika manual review 300 sampai 500 gambar tidak selesai, minimum viable V11B adalah:

- review seluruh 19 file dari mixed-label near-duplicate groups;
- review seluruh consensus high-confidence errors;
- review seluruh P0;
- review P1 sampai batas waktu;
- lock status gambar yang belum direview sebagai `unreviewed`;
- jangan auto-relabel sisa queue;
- tetap buat group id untuk seluruh train;
- tetap jalankan grouped control.

Target minimum:

- 100 sampai 200 gambar dengan risk tertinggi direview benar;
- seluruh mixed-label duplicate diperiksa;
- seluruh confirmed correction memiliki evidence;
- grouped split zero overlap.

### 6.4 Cutoff rules

| Kondisi pada cutoff | Keputusan |
|---|---|
| V11A.2 belum selesai H+5 | pakai output seed yang valid untuk audit, jangan tunggu sweep |
| review belum 300 gambar H+9 | stop pada tier boundary, lock keputusan yang sudah ada |
| grouped control gagal H+16 | gunakan V10/V11A champion lama untuk final, jangan memaksa cleaned candidate |
| V12A belum menang jelas H+21 | hentikan V12A |
| final checkpoint belum ada H+27 | retrain champion paling stabil dengan fixed epochs |
| inference gagal setelah H+30 | gunakan checkpoint dan inference path terakhir yang sudah tervalidasi |

### 6.5 Compute allocation

| Workload | Preferred runtime | Alasan |
|---|---|---|
| V11A.2 head-only | P100, T4, atau CPU dengan RAM cukup | tidak ada backbone forward |
| V11B queue and grouping | CPU high-RAM | hash, dataframe, nearest-neighbor |
| V10 grouped head control | single P100 atau T4 | cache-only |
| V12A Gram/prototype | single P100 atau T4 | cache-only |
| V12B ViT-7B extraction | T4 x2 jika pipeline DataParallel sudah stabil | throughput extraction |
| ViT-L LoRA | P100 atau T4 dengan AMP and checkpointing | PEFT screen |

Catatan:

- VRAM dua GPU tidak otomatis menjadi satu memory pool.
- T4 x2 membantu throughput jika model muat pada masing-masing GPU.
- Jangan mengganti runtime hanya karena GPU utilization pada cell awal nol. Tahap setup, unzip, hashing, dataframe build, dan dataloader warmup memang dapat berjalan di CPU.

---

## 7. Phase A: V11A.2 Frozen Material Stabilization

### 7.1 Tujuan

Menentukan apakah signal material dari V11A.1 dapat dibuat stabil tanpa mengubah backbone atau mengekstrak ulang feature.

### 7.2 Hipotesis

Material branch memiliki signal, tetapi V11A.1 terlalu sensitif terhadap:

- learning rate;
- seed;
- R/O auxiliary objective;
- regularization.

Jika signal benar, satu konfigurasi harus:

- mengalahkan continued control;
- menurunkan R/O error;
- stabil lintas seed;
- menang di mayoritas confirmation folds.

### 7.3 Kandidat terkunci

| Candidate ID | Learning rate | R/O auxiliary | Regularization |
|---|---:|---|---|
| `lr4e4_plain` | 4e-4 | tidak | baseline |
| `lr2e4_plain` | 2e-4 | tidak | baseline |
| `lr4e4_roaux` | 4e-4 | ya | tanpa reg tambahan |
| `lr4e4_roaux_reg` | 4e-4 | ya | ya |

Jangan menambah kandidat baru sebelum empat kandidat ini memiliki keputusan.

### 7.4 Input wajib

- canonical train manifest;
- cache global `[N, 8192]`;
- cache spatial `[N, 64, 512]`;
- cache row map;
- fold assignments yang dipakai V11A.1;
- continued control config;
- class index mapping;
- seeds `42`, `314`, `2026`;
- V10 atau V11A.1 OOF untuk paired comparison.

### 7.5 Preflight

Checklist:

- [ ] `N == 26.527`
- [ ] tidak ada duplicate `sample_id`
- [ ] semua `sample_id` pada cache cocok dengan manifest
- [ ] cache shape sesuai manifest
- [ ] seluruh feature finite
- [ ] dtype feature tercatat
- [ ] class order tepat `[0, 1, 2]`
- [ ] fold values tepat `[0, 1, 2, 3, 4]`
- [ ] train dan validation index tidak overlap
- [ ] test cache tidak dimuat
- [ ] config hash disimpan

### 7.6 Execution sequence

#### Stage A1: Smoke test

- fold 0;
- seed 42;
- maksimal 500 train dan 200 valid;
- dua epoch;
- seluruh empat kandidat.

Pass jika:

- loss finite;
- gradient finite;
- probability row sum mendekati 1;
- checkpoint tersimpan;
- inference deterministik dalam tolerance.

#### Stage A2: Fold-0 candidate screen

- seluruh fold-0 train and validation;
- seed 42;
- empat kandidat;
- early stopping rule sama;
- epoch budget sama.

Urutkan berdasarkan:

1. Macro F1;
2. R/O error;
3. log loss;
4. Electronic F1;
5. training stability.

Eliminasi kandidat jika:

- Macro F1 di bawah continued control lebih dari 0.0002;
- R/O error naik lebih dari 2%;
- Electronic F1 turun lebih dari 0.0005;
- run non-finite;
- best epoch terlalu tidak stabil.

#### Stage A3: Seed stability

Ambil maksimal dua kandidat terbaik.

Jalankan fold 0 untuk:

- seed 314;
- seed 2026.

Kandidat lolos jika:

- median gain positif;
- tidak ada seed yang collapse;
- seed standard deviation tidak lebih buruk signifikan dari control;
- R/O error membaik pada minimal dua dari tiga seed.

#### Stage A4: Confirmation folds

Ambil satu kandidat terbaik.

Jalankan folds 1 sampai 4 dengan protocol yang sama. Jika waktu cukup, gunakan tiga seed. Jika waktu terbatas, gunakan seed 42 untuk seluruh confirmation folds dan dua seed tambahan hanya pada fold 0.

#### Stage A5: Full OOF assembly

OOF wajib dirakit berdasarkan `sample_id`, bukan concatenation order.

Validasi:

- setiap sample tepat satu prediction;
- tidak ada missing row;
- tidak ada duplicate row;
- probability finite;
- probability sum valid;
- OOF label cocok dengan manifest.

### 7.7 Output schema

`v11a2_oof_predictions.csv`

| Column | Type | Description |
|---|---|---|
| `sample_id` | string | stable train identifier |
| `image_sha256` | string | exact content hash |
| `filepath` | string | relative train path |
| `label` | int | official train label |
| `fold` | int | validation fold |
| `seed` | int | run seed |
| `candidate_id` | string | V11A.2 candidate |
| `prob_0` | float | Recyclable probability |
| `prob_1` | float | Electronic probability |
| `prob_2` | float | Organic probability |
| `predicted` | int | argmax |
| `confidence` | float | max probability |
| `margin` | float | top1 minus top2 |
| `is_correct` | bool | prediction equals label |

Output lain:

- `v11a2_candidate_summary.csv`
- `v11a2_per_fold_metrics.csv`
- `v11a2_per_seed_metrics.csv`
- `v11a2_confusion_matrices.json`
- `v11a2_run_manifest.json`
- `v11a2_decision.md`

### 7.8 Adoption gate

Adopt V11A.2 sebagai champion hanya jika:

- full OOF gain minimal `+0.0003`;
- total error turun;
- R/O error turun;
- menang minimal 3 dari 4 confirmation folds;
- stabil pada seed 42, 314, dan 2026;
- Electronic F1 tidak turun lebih dari 0.0005;
- tidak ada leakage atau alignment issue.

### 7.9 Stop condition

Jika gagal gate:

- tandai `material_head_stabilization = exhausted`;
- jangan sweep LR baru;
- jangan menambah dropout variant;
- jangan mengubah loss lagi pada cache yang sama;
- tetap gunakan probabilities untuk V11B label audit.

---

## 8. Phase B0: Canonical Artifact Registry

### 8.1 Tujuan

Membuat satu registry yang menjelaskan artifact mana yang valid, berasal dari run apa, memakai data apa, dan dapat dipakai untuk V11B.

### 8.2 Registry schema

`artifact_registry.csv`

| Column | Description |
|---|---|
| `artifact_id` | stable artifact identifier |
| `version` | V7, V10, V11A.1, V11A.2 |
| `artifact_type` | OOF, cache, config, fold, checkpoint, report |
| `path` | absolute or portable relative path |
| `sha256` | file checksum |
| `size_bytes` | file size |
| `row_count` | row count if tabular |
| `schema_hash` | normalized schema fingerprint |
| `data_signature` | train manifest signature |
| `fold_signature` | fold assignment signature |
| `model_signature` | backbone and head signature |
| `created_at` | artifact creation time |
| `status` | valid, stale, missing, incompatible |
| `notes` | issue or provenance |

### 8.3 Required checks

- OOF row count.
- Unique sample count.
- Missing probability.
- Probability range.
- Class order.
- Path normalization.
- Filename collision.
- Data signature consistency.
- Fold signature consistency.
- Whether artifact includes test information.

### 8.4 Fail-closed rules

- Artifact tanpa sample identifier tidak boleh digabung hanya berdasarkan row order.
- Artifact dengan data signature berbeda tidak boleh dipakai tanpa explicit reconciliation.
- Artifact dengan unknown class order tidak boleh dipakai.
- Artifact test tidak boleh masuk ke V11B workspace.

---

## 9. Phase B1: Canonical Sample Identity and Alignment

### 9.1 Stable identity

Gunakan:

```text
sample_id = image_sha256
```

Jika exact duplicate menghasilkan SHA yang sama untuk beberapa file, gunakan:

```text
row_id = image_sha256 + "::" + normalized_relative_path
```

Definisi:

- `sample_id` mewakili content identity.
- `row_id` mewakili satu record dataset.
- `duplicate_group_id` mewakili exact atau near-duplicate cluster.

### 9.2 Canonical manifest

`train_manifest_raw.csv`

| Column | Description |
|---|---|
| `row_id` | unique record identifier |
| `sample_id` | content identifier |
| `image_sha256` | exact hash |
| `relative_path` | portable image path |
| `filename` | basename |
| `original_label` | official label |
| `class_name` | class text |
| `width` | decoded width |
| `height` | decoded height |
| `aspect_ratio` | width divided by height |
| `file_size_bytes` | file size |
| `decode_ok` | decode status |
| `exact_duplicate_count` | exact duplicate size |
| `duplicate_group_id` | assigned later |

### 9.3 OOF alignment procedure

Untuk setiap source model:

1. normalize path separators;
2. derive or import image SHA256;
3. join to canonical manifest;
4. verify one-to-one or documented one-to-many relation;
5. retain source-specific fold;
6. rename probabilities with source prefix;
7. audit missing rows;
8. audit conflicting labels;
9. audit duplicate predictions;
10. save alignment report.

### 9.4 Source prefixes

- `v7_prob_0`, `v7_prob_1`, `v7_prob_2`
- `v10_prob_0`, `v10_prob_1`, `v10_prob_2`
- `v11a1_prob_0`, `v11a1_prob_1`, `v11a1_prob_2`
- `v11a2_s42_prob_0`, and so on
- `convnext_prob_0`, and so on, diagnostic only

### 9.5 Alignment gate

- 100% canonical rows accounted for or missingness explicitly documented.
- Zero silent duplicate joins.
- Zero label mismatch after path normalization.
- Model probability rows sum to 1 within tolerance.
- Missing source predictions do not become zero.

---

## 10. Phase B2: Duplicate Group Construction

### 10.1 Tujuan

Mencegah exact dan near-duplicate images menyeberang validation folds.

### 10.2 Known evidence

Audit sebelumnya menemukan:

- 436 near-duplicate groups;
- 910 files dalam groups;
- sekitar 742 OOF rows memiliki near-duplicate di fold lain;
- 7 mixed-label groups;
- 19 files di mixed-label groups.

Angka tersebut harus diverifikasi terhadap canonical manifest terbaru.

### 10.3 Detection layers

#### Layer 1: Exact duplicate

- SHA256 sama.
- Semua record dengan SHA yang sama masuk satu group.

#### Layer 2: Near-duplicate visual

Gunakan threshold yang dikunci sebelum melihat OOF gain. Candidate signals:

- perceptual hash distance;
- difference hash distance;
- image dimensions;
- normalized DINO embedding cosine similarity;
- optional structural similarity for candidate pairs.

### 10.4 Pair generation

Jangan menghitung seluruh pair `N x N`.

Gunakan:

1. exact hash buckets;
2. perceptual hash index;
3. approximate nearest neighbor pada frozen embedding;
4. union-find untuk membentuk connected components.

### 10.5 Threshold policy

Threshold dipilih berdasarkan visual inspection terhadap sampled candidate pairs, bukan berdasarkan Macro F1.

Simpan:

- threshold;
- jumlah pair;
- sampled true duplicate rate;
- false merge examples;
- false split examples.

### 10.6 Mixed-label duplicate policy

Semua mixed-label group masuk P0 review.

Setelah review:

- label jelas sama: corrected labels dibuat konsisten;
- object berbeda walau visual mirip: group boleh dipisahkan jika evidence kuat;
- ambiguous: seluruh group tetap satu duplicate group dan ditandai ambiguous;
- corrupted image: exclude record setelah evidence disimpan.

### 10.7 Output

`duplicate_groups.csv`

| Column | Description |
|---|---|
| `row_id` | dataset record |
| `duplicate_group_id` | stable group id |
| `group_size` | number of records |
| `group_type` | singleton, exact, near, mixed |
| `original_label_count` | label distribution |
| `mixed_label_flag` | whether labels conflict |
| `detection_reason` | SHA, pHash, embedding, combined |
| `review_required` | manual review flag |

### 10.8 Gate

- setiap train row memiliki satu `duplicate_group_id`;
- singleton memiliki unique group;
- no row belongs to two groups;
- mixed-label groups masuk queue;
- cluster construction deterministic;
- group file memiliki checksum.

---

## 11. Phase B3: V11B Review Queue

### 11.1 Tujuan

Mengurutkan train images yang paling mungkin:

- mislabeled;
- ambiguous;
- corrupted;
- duplicate conflict;
- berada pada R/O boundary yang tidak stabil.

Model hanya memberi prioritas. Model tidak menentukan label final.

### 11.2 Audit signals

#### Signal S1: Mixed-label duplicate

Nilai tinggi jika:

- satu duplicate group memiliki lebih dari satu official label.

#### Signal S2: Cross-model alternate consensus

Nilai tinggi jika:

- V7, V10, dan V11A.2 memprediksi alternate class yang sama;
- prediction salah terhadap official label;
- confidence tinggi;
- prediction stabil lintas seed.

#### Signal S3: Assigned-label self-confidence

```text
self_confidence = P(official_label)
```

Nilai rendah lebih mencurigakan.

#### Signal S4: Alternate margin

```text
alternate_margin = max(P(other_class)) - P(official_label)
```

Nilai tinggi lebih mencurigakan.

#### Signal S5: Confident Learning

Gunakan OOF probabilities dan official labels untuk:

- confident joint;
- label quality score;
- issue ranking.

Hasil hanya ranking signal.

#### Signal S6: Seed agreement

```text
seed_agreement = fraction of seeds with same alternate prediction
```

#### Signal S7: Model-family agreement

ConvNeXt boleh dipakai sebagai diagnostic family.

Nilai tinggi jika DINO and ConvNeXt setuju pada alternate label.

#### Signal S8: Nearest-neighbor label purity

Gunakan train embeddings.

Untuk setiap query:

- ambil `k` nearest neighbors;
- exclude exact self;
- ringkas neighbor labels;
- hitung dominant alternate purity;
- simpan similarity minimum and mean.

#### Signal S9: Persistent R/O confusion

Prioritaskan official class 0 atau 2 yang konsisten diprediksi menjadi pasangan lawannya.

#### Signal S10: Image integrity

Flag:

- decode failure;
- truncated image;
- extreme corruption;
- blank or near-blank image;
- alpha-channel anomaly.

### 11.3 Tier definitions

#### P0: Must review

Masuk P0 jika salah satu:

- mixed-label exact or near-duplicate;
- seluruh DINO source and seeds setuju pada alternate class dengan high margin;
- image integrity failure;
- same-content records memiliki conflicting labels.

#### P1: Strong label issue

Masuk P1 jika:

- Confident Learning flagged;
- minimal dua model sources setuju alternate class;
- error stabil lintas seed;
- self-confidence rendah;
- alternate margin tinggi.

#### P2: Champion error analysis

Masuk P2 jika:

- V10 atau V11A.2 salah;
- terutama R/O;
- tidak memenuhi P0 atau P1;
- diurutkan dari assigned-label probability terendah.

#### P3: Neighbor conflict

Masuk P3 jika:

- nearest neighbors sangat konsisten pada alternate label;
- query official label berbeda;
- model confidence belum cukup tinggi untuk P1.

#### P4: Instability

Masuk P4 jika:

- prediction berubah antar-seed;
- entropy tinggi;
- margin rendah;
- kemungkinan besar benar-benar ambiguous.

P4 berguna untuk exclusion review, bukan relabel priority.

### 11.4 Queue size

Full plan:

- 300 sampai 500 unique images.

Deadline plan:

- seluruh P0;
- seluruh P1 sampai cutoff;
- top P2 R/O;
- selected P4 untuk memahami ambiguity.

### 11.5 Dedupe queue

Satu image dapat memenuhi banyak signals. Queue harus memiliki satu row per `row_id`.

Simpan:

- seluruh reason flags;
- primary tier;
- number of supporting signals;
- model predictions;
- probability summary;
- neighbor summary;
- duplicate group.

### 11.6 Queue output schema

`v11b_review_queue.csv`

| Column | Description |
|---|---|
| `review_order` | fixed review order |
| `tier` | P0 to P4 |
| `row_id` | unique record |
| `relative_path` | image location |
| `original_label` | hidden during blind stage |
| `duplicate_group_id` | duplicate group |
| `signals` | pipe-separated signal IDs |
| `signal_count` | number of independent signals |
| `v7_pred` | V7 argmax |
| `v10_pred` | V10 argmax |
| `v11a2_consensus_pred` | V11A.2 consensus |
| `seed_agreement` | seed agreement |
| `self_confidence` | official-label probability |
| `alternate_label` | strongest alternate |
| `alternate_margin` | alternate minus assigned |
| `cl_quality_score` | Confident Learning score |
| `nn_dominant_label` | nearest-neighbor dominant label |
| `nn_purity` | neighbor label purity |
| `review_status` | initially pending |

### 11.7 Queue QA

- [ ] unique `row_id`
- [ ] P0 appears first
- [ ] mixed-label duplicate coverage 100%
- [ ] no test path
- [ ] no test probabilities
- [ ] image path resolves
- [ ] review order fixed before manual review
- [ ] no label overwritten

---

## 12. Phase B4: Blind Manual Review Protocol

### 12.1 Tujuan

Membedakan:

- label resmi yang benar;
- label resmi yang salah;
- gambar ambigu;
- gambar rusak atau tidak layak.

### 12.2 Review stages

#### Stage 1: Blind visual decision

Reviewer hanya melihat:

- image;
- zoomed image jika perlu;
- optional neighboring duplicate images tanpa label.

Reviewer tidak melihat:

- official label;
- model prediction;
- confidence;
- queue signal;
- folder name yang mengandung class.

Pilihan awal:

- `Recyclable`
- `Electronic`
- `Organic`
- `Ambiguous`
- `Corrupted or unusable`

#### Stage 2: Reveal

Setelah keputusan awal dikunci, tampilkan:

- official label;
- model consensus;
- duplicate group context;
- nearest neighbors.

Reviewer memilih keputusan final:

- `confirmed_keep`
- `corrected_label`
- `ambiguous_keep`
- `ambiguous_exclude`
- `corrupted_exclude`
- `needs_second_review`

#### Stage 3: Second review

Wajib untuk:

- setiap correction;
- setiap mixed-label duplicate;
- setiap case yang model dan reviewer sangat bertentangan;
- setiap ambiguous exclusion.

Jika hanya ada satu reviewer:

- lakukan second pass setelah tier selesai;
- acak urutan;
- jangan tampilkan keputusan pass pertama;
- simpan agreement.

### 12.3 Class interpretation guide

Gunakan label berdasarkan objek atau material visual utama pada gambar. Jangan mengandalkan:

- filename;
- folder;
- inferred source;
- image dimensions;
- model confidence.

Jika satu gambar mengandung campuran material dan tidak ada dominant object yang jelas:

- pilih `Ambiguous`;
- jangan memaksa label alternatif.

### 12.4 Review evidence

Setiap correction harus memiliki:

- original label;
- proposed label;
- one-sentence visual reason;
- reviewer;
- timestamp;
- second-review result;
- optional crop or duplicate context reference.

### 12.5 Review decision schema

`v11b_review_decisions.csv`

| Column | Description |
|---|---|
| `row_id` | reviewed record |
| `review_order` | queue position |
| `tier` | queue tier |
| `blind_choice_pass1` | initial blind label |
| `blind_confidence_pass1` | low, medium, high |
| `decision_pass1` | preliminary action |
| `blind_choice_pass2` | second pass |
| `blind_confidence_pass2` | confidence |
| `final_status` | keep, correct, ambiguous, exclude |
| `review_label` | final reviewed label if applicable |
| `review_reason` | short visual explanation |
| `reviewer` | reviewer identifier |
| `review_timestamp` | time |
| `agreement` | pass agreement |
| `source_tier` | P0 to P4 |

### 12.6 Policy for ambiguous images

Gunakan dua evaluation views:

1. **Official-label view**
   - seluruh original rows;
   - label resmi;
   - untuk continuity dengan historical score.

2. **Reviewed-label view**
   - confirmed corrections menggunakan reviewed label;
   - ambiguous-exclude tidak masuk headline reviewed metric;
   - kandidat dibandingkan pada sample set yang sama.

Jangan melaporkan reviewed-label score tanpa official-label score.

### 12.7 Training policy

| Review status | Training treatment | Evaluation treatment |
|---|---|---|
| `confirmed_keep` | use original label | include |
| `corrected_label` | use reviewed label | include with reviewed label |
| `ambiguous_keep` | use original label, optional lower weight only in later ablation | include in official view, exclude from clean headline if predeclared |
| `ambiguous_exclude` | exclude from training | exclude from reviewed view |
| `corrupted_exclude` | exclude | exclude |
| `unreviewed` | use original label | include |

Untuk exact V10 clean control pertama, jangan memakai sample weighting. Perubahan hanya:

- corrected labels;
- explicit exclusions;
- duplicate-grouped folds.

### 12.8 Review gate

Review valid jika:

- seluruh corrections memiliki evidence;
- seluruh mixed-label groups direview;
- tidak ada auto-filled review label;
- second review dilakukan untuk corrections;
- queue tier tercatat;
- keputusan dibuat tanpa test.

---

## 13. Phase B5: Cleaned Manifest and Split Lock

### 13.1 Cleaned manifest

`train_manifest_v11b_clean.csv`

| Column | Description |
|---|---|
| `row_id` | stable record |
| `relative_path` | image path |
| `original_label` | official label |
| `review_status` | review outcome |
| `review_label` | reviewed label |
| `training_label` | actual label used in training |
| `evaluation_label` | label used in reviewed evaluation |
| `include_train` | training inclusion |
| `include_reviewed_eval` | reviewed metric inclusion |
| `duplicate_group_id` | grouping key |
| `source_tier` | review source |
| `manifest_version` | version |

### 13.2 Manifest audit

- row count before exclusion;
- row count after exclusion;
- class counts before and after;
- correction matrix;
- exclusion reasons;
- duplicate group count;
- mixed-label group resolution;
- checksum.

### 13.3 Fold construction

Gunakan:

```python
StratifiedGroupKFold(
    n_splits=5,
    shuffle=True,
    random_state=42,
)
```

Inputs:

- `y = training_label`
- `groups = duplicate_group_id`

### 13.4 Fold selection policy

Fold assignment dibuat satu kali setelah manifest lock.

Jangan:

- mencoba banyak seed lalu memilih Macro F1 terbaik;
- memindahkan group karena model error;
- mengoptimalkan folds terhadap V10 predictions.

Fold quality dinilai hanya dari:

- class balance;
- sample balance;
- group balance;
- zero overlap.

### 13.5 Fold audit

`v11b_grouped_fold_audit.json`

Wajib mencatat:

- train and valid samples per fold;
- class counts per fold;
- group counts per fold;
- max group size;
- duplicate overlap;
- reviewed correction counts per fold;
- excluded sample counts;
- manifest checksum;
- fold checksum.

### 13.6 Split gate

- zero duplicate group overlap;
- each row appears in exactly one validation fold;
- no missing fold;
- class proportion reasonable;
- all folds contain all classes;
- fold checksum locked.

---

## 14. Phase B6: Exact V10 Grouped Controls

### 14.1 Tujuan

Mengukur secara terpisah:

1. dampak duplicate-grouped evaluation;
2. dampak verified label repair;
3. dampak exclusion;
4. dampak model change.

### 14.2 Experiment matrix

| Run ID | Training labels | Split | Evaluation labels | Tujuan |
|---|---|---|---|---|
| B6-A | raw official | grouped locked | official | honest raw baseline |
| B6-B | raw official | grouped locked | reviewed | evaluate baseline against reviewed truth |
| B6-C | cleaned | grouped locked | reviewed | causal cleaning effect |
| B6-D | cleaned | grouped locked | official | continuity diagnostic |

B6-A dan B6-B berasal dari predictions model yang sama.  
B6-C dan B6-D berasal dari predictions model yang sama.

### 14.3 Control invariants

Untuk B6-A and B6-C, semua hal berikut harus sama:

- feature cache;
- head architecture;
- optimizer;
- learning rate;
- batch size;
- class weighting policy;
- epochs;
- early stopping;
- seeds;
- folds;
- preprocessing;
- checkpoint selection.

Perubahan yang diizinkan:

- training label;
- explicit inclusion or exclusion status.

### 14.4 Paired comparison

Bandingkan pada exact same reviewed evaluation rows:

- baseline correct, cleaned wrong;
- baseline wrong, cleaned correct;
- both correct;
- both wrong;
- R/O transitions;
- Electronic transitions.

Gunakan bootstrap by duplicate group untuk confidence interval.

### 14.5 Metrics table

`v11b_control_comparison.csv`

| Metric | B6-A | B6-B | B6-C | B6-D |
|---|---:|---:|---:|---:|
| Macro F1 | | | | |
| Recyclable F1 | | | | |
| Electronic F1 | | | | |
| Organic F1 | | | | |
| Total error | | | | |
| R/O error | | | | |
| Log loss | | | | |
| Fold mean | | | | |
| Fold std | | | | |

### 14.6 Data repair adoption gate

Adopt cleaned manifest untuk model berikutnya jika:

- corrections telah diverifikasi;
- grouped split zero overlap;
- B6-C mengalahkan B6-B pada reviewed evaluation;
- R/O error turun pada minimal 4 dari 5 folds;
- Electronic F1 tidak turun lebih dari 0.0005;
- gain tidak berasal dari satu fold atau satu duplicate cluster.

Jika Macro F1 gain kecil tetapi log loss dan R/O stability membaik, cleaned manifest tetap dapat dipakai sebagai training foundation untuk LoRA.

### 14.7 Interpretation cases

#### Case 1: Grouped score turun

Interpretasi:

- OOF lama terinflasi duplicate leakage.

Keputusan:

- gunakan grouped score sebagai baseline baru;
- jangan kembali ke leaking split untuk mengejar angka.

#### Case 2: Cleaning tidak menaikkan Macro F1

Interpretasi:

- jumlah correction kecil;
- model frozen tidak cukup responsif;
- correction mungkin lebih berguna saat adaptation.

Keputusan:

- simpan cleaned manifest;
- jangan menambah manual relabel tanpa signal baru;
- lanjut V12A atau LoRA dengan protocol yang sama.

#### Case 3: Cleaning merusak Electronic

Interpretasi:

- correction or exclusion policy terlalu agresif;
- class balance berubah;
- review error.

Keputusan:

- audit Electronic corrections;
- jangan tuning threshold;
- revert hanya correction yang gagal second review.

#### Case 4: Cleaning memberi gain stabil

Keputusan:

- adopt cleaned manifest;
- freeze version;
- lanjut V12A.

### 14.8 V11B completion criteria

V11B dianggap selesai jika tersedia:

- artifact registry;
- canonical raw manifest;
- aligned OOF table;
- duplicate groups;
- review queue;
- review decisions;
- cleaned manifest;
- grouped folds;
- raw grouped control;
- cleaned grouped control;
- comparison report;
- signed decision file.

---

## 15. Phase C: V12A Spatial Gram and Prototype Head

### 15.1 Tujuan

Mengambil material texture signal dari spatial cache tanpa mengekstrak ulang DINOv3.

### 15.2 Hipotesis

Mean pooling hanya menyimpan first-order statistics. R/O classification memerlukan:

- texture;
- local material relation;
- patch distribution;
- repeated patterns;
- surface cues.

Projected Gram atau covariance descriptor dapat menangkap hubungan antar-patch.

### 15.3 Input

- locked V11 spatial cache `[N, 64, 512]`;
- locked global feature;
- cleaned or raw manifest selected by V11B;
- grouped folds;
- V10 protocol-matched control;
- selected seeds.

### 15.4 Candidate descriptors

#### C0: Control

- exact V11A.1 or V10-compatible descriptor.

#### C1: Mean plus standard deviation

Untuk patch tokens:

- channel mean;
- channel standard deviation;
- concatenate with global feature.

#### C2: Projected Gram

1. project token dimension 512 to 32 or 64;
2. normalize tokens;
3. compute compact Gram matrix;
4. keep upper triangular entries;
5. apply signed square root if configured;
6. L2 normalize;
7. concatenate with compact global projection.

Jangan menyimpan full 512 x 512 Gram per sample.

#### C3: Prototype distances

Build class prototypes hanya dari training fold.

Features:

- cosine distance to Recyclable prototype;
- cosine distance to Electronic prototype;
- cosine distance to Organic prototype;
- R/O prototype margin;
- optional local top-k similarity summary.

Validation samples tidak boleh masuk prototype construction.

#### C4: Gram plus prototype

Hanya dijalankan jika C2 atau C3 menang atas control.

### 15.5 Candidate screen

#### Stage C1: Fold 0, seed 42

Run:

- C0;
- C1;
- C2 with projection 32;
- C2 with projection 64;
- C3.

Maksimal lima candidates.

#### Stage C2: Stability

Top two candidates:

- fold 0;
- seeds 314 and 2026.

#### Stage C3: Confirmation

Top one candidate:

- folds 1 to 4;
- seed 42;
- optional full seeds jika waktu cukup.

### 15.6 Leakage checks

- projection fitted on train fold only jika data-dependent;
- normalization statistics fitted on train fold only;
- prototypes built on train fold only;
- validation feature transform tidak menggunakan validation labels;
- duplicate groups tetap terkunci.

### 15.7 Gate

Adopt V12A jika:

- full OOF gain minimal `+0.0003`;
- menang minimal 3 dari 4 confirmation folds;
- R/O error turun;
- seed std tidak lebih buruk dari V11A.2;
- Electronic F1 terjaga;
- feature and runtime feasible untuk final single model.

### 15.8 Stop condition

Jika semua spatial candidates gagal:

- tandai cache-only spatial head path exhausted;
- jangan menambah pooling zoo;
- lanjut geometry atau LoRA hanya jika waktu cukup.

---

## 16. Phase D: V12B Aspect-Preserving Rectangular Geometry

### 16.1 Posisi dalam deadline

V12B bersifat conditional. Jangan menjalankannya jika:

- V11B control belum selesai;
- final-training buffer terancam;
- V11A.2 or V12A sudah memberi kandidat yang cukup kuat;
- extraction ViT-7B diperkirakan melewati cutoff.

### 16.2 Hipotesis

Direct-square resize ke 256 x 256 dapat:

- merusak aspect ratio;
- mengubah bentuk object;
- menghilangkan small material cues;
- memperlemah texture.

DINOv3 menerima rectangular inputs selama dimensi sesuai patch grid.

### 16.3 Causal screen

Control:

- direct-square 256;
- frozen backbone;
- exact selected head.

Candidate:

- aspect-preserving;
- long side 320 atau 384;
- dimensions rounded to multiples of 16;
- same backbone;
- same head policy.

Jangan mengubah geometry dan LoRA dalam run yang sama.

### 16.4 Preprocessing

1. EXIF transpose.
2. Convert RGB.
3. Resize preserving aspect ratio.
4. Bound short side to prevent extreme token count.
5. Round height and width to multiple of 16.
6. Pad only if batching requires it.
7. Build attention or valid-token mask if model path needs it.
8. Record original and processed dimensions.

### 16.5 Smoke test

Gunakan representative images:

- square;
- portrait;
- landscape;
- extreme aspect;
- low resolution;
- high resolution.

Check:

- token grid;
- padding behavior;
- finite outputs;
- batch collation;
- peak VRAM;
- samples per second.

### 16.6 Gate

Promote dari fold-0 screen jika:

- Macro F1 naik minimal `+0.0010`;
- gain muncul pada dua seeds;
- R/O error turun minimal 10%;
- extreme-aspect subset tidak memburuk;
- extraction dapat selesai sebelum final-training cutoff.

### 16.7 Stop condition

Jika throughput tidak feasible atau gain di bawah gate:

- jangan extract full dataset;
- jangan langsung naik ke 512;
- simpan smoke and fold-0 results;
- kembali ke cache-only champion.

---

## 17. Phase E: V13 DINOv3 ViT-L LoRA

### 17.1 Posisi

LoRA memiliki theoretical upside terbesar, tetapi deadline risk juga terbesar. Dalam deadline path, LoRA hanya boleh dimulai jika:

- V11B grouped protocol sudah locked;
- satu GPU configuration sudah smoke-tested;
- minimal 10 sampai 12 jam reserve masih tersedia sebelum final inference;
- final fallback checkpoint sudah aman.

### 17.2 Causal experiment matrix

| Candidate | Geometry | Adaptation | Purpose |
|---|---|---|---|
| E0 | square 256 | frozen | protocol control |
| E1 | square 256 | Q/V LoRA rank 8 | causal adaptation |
| E2 | rectangular 384 | Q/V LoRA rank 8 | only after E1 passes |

### 17.3 Initial LoRA config

- backbone: DINOv3 ViT-L;
- rank: 8;
- alpha: 16;
- dropout: 0.05;
- target modules: query and value projections;
- optimizer: AdamW;
- base learning rate: 1e-4;
- weight decay: 0.1;
- schedule: cosine;
- warmup: 10%;
- gradient clip: 1.0;
- precision: mixed precision;
- gradient checkpointing: enabled;
- head dropout: 0.2;
- loss: weighted cross-entropy control.

### 17.4 Loss ablation order

Hanya setelah E1 lolos:

1. weighted cross-entropy;
2. cross-entropy plus R/O supervised contrastive auxiliary;
3. ELR if memorization evidence exists.

Focal loss bukan prioritas sebelum data audit karena dapat memberi bobot lebih besar pada noisy hard samples.

### 17.5 Training diagnostics

Log:

- train loss;
- valid loss;
- Macro F1;
- per-class F1;
- R/O errors;
- gradient norm;
- learning rate;
- trainable parameter count;
- peak VRAM;
- epoch time;
- best epoch;
- early-learning behavior;
- high-confidence training errors.

### 17.6 Screen gate

Promote LoRA ke full confirmation jika:

- fold-0 gain minimal `+0.0010`;
- gain muncul pada two seeds;
- total error and R/O error turun;
- Electronic F1 tidak turun lebih dari 0.0005;
- log loss tidak memburuk drastis;
- no instability.

### 17.7 Full adoption gate

Adopt LoRA jika:

- full grouped OOF gain minimal `+0.0008`;
- menang minimal 4 dari 5 folds;
- R/O error turun konsisten;
- result tidak bergantung pada threshold post-hoc;
- satu final model dapat dilatih and diinfer sebelum deadline.

### 17.8 Stop condition

Stop jika:

- OOM berulang setelah one safe batch-size reduction;
- non-finite loss;
- no gain pada two seeds;
- training time mengancam submission buffer;
- final fallback belum tersedia.

---

## 18. Champion Selection

### 18.1 Candidate table

Semua kandidat final harus masuk tabel:

| Candidate | Data | Split | Representation | Adaptation | OOF F1 | R/O errors | E F1 | Fold wins | Seed std | Runtime | Eligible |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| V10 grouped raw | raw | grouped | frozen global | none | | | | | | | |
| V10 grouped clean | clean | grouped | frozen global | none | | | | | | | |
| V11A.2 | selected | grouped | material branch | none | | | | | | | |
| V12A | selected | grouped | Gram/prototype | none | | | | | | | |
| V12B | selected | grouped | rectangular | none | | | | | | | |
| V13 | selected | grouped | selected | LoRA | | | | | | | |

### 18.2 Eligibility gate

`Eligible = true` hanya jika:

- integrity checks pass;
- no test-derived decision;
- grouped split pass;
- full or sufficient confirmation available;
- final inference single model;
- runtime feasible;
- reproducible config available.

### 18.3 Selection order

1. Remove ineligible candidates.
2. Pick highest full grouped OOF Macro F1.
3. If difference below 0.0002, prefer:
   - lower R/O error;
   - better fold consistency;
   - lower seed variance;
   - safer final training;
   - lower runtime.
4. Do not choose based on leaderboard expectation.

### 18.4 Tie-break policy

If candidates are statistically indistinguishable:

- prefer simpler model;
- prefer fewer trainable components;
- prefer lower inference risk;
- prefer artifact path already validated;
- prefer candidate with better Electronic preservation.

---

## 19. Final Single-Model Training

### 19.1 Single-model interpretation

Final prediction must come from:

- one backbone configuration;
- one head;
- one checkpoint;
- one deterministic inference recipe.

Tidak boleh average:

- five fold checkpoints;
- multiple seeds;
- V10 and ConvNeXt;
- global and crop models with separately trained weights;
- multiple submissions.

Internal branches dalam satu jointly trained architecture diperbolehkan hanya jika menghasilkan satu checkpoint and satu forward graph.

### 19.2 Epoch selection

Cross-validation menentukan training duration.

Gunakan:

```text
final_epochs = rounded median best epoch across accepted folds and seeds
```

Lock sebelum final training.

Jangan memakai test untuk early stopping.

### 19.3 Final train set

Gunakan selected manifest:

- raw or cleaned sesuai champion decision;
- include/exclude flags locked;
- all eligible train rows;
- no validation holdout jika fixed epoch full-data training digunakan.

### 19.4 Final seed

Pilih satu seed yang dikunci sebelum full-data training.

Recommended default:

- seed 42, kecuali stability study menunjukkan seed-specific failure.

Jangan train banyak final seeds lalu memilih berdasarkan test.

### 19.5 Final artifact

Wajib:

- `final_model.pt` or equivalent;
- `final_config.yaml`;
- `final_train_manifest.csv`;
- `final_training_history.csv`;
- `final_model_signature.json`;
- `final_inference_notebook.ipynb`;
- `final_environment.txt`;
- `final_decision.md`.

### 19.6 Checkpoint QA

- load checkpoint from clean process;
- run inference on fixed train smoke subset;
- compare predictions with saved smoke predictions;
- check finite logits;
- check class order;
- record checksum;
- ensure no fold ensemble logic remains.

---

## 20. Test Inference and Submission QA

### 20.1 Test isolation

Test baru dimuat setelah:

- champion locked;
- final config locked;
- final checkpoint locked;
- preprocessing locked;
- no further hyperparameter changes.

### 20.2 Inference procedure

1. load official test directory;
2. parse IDs using official template;
3. preserve template order;
4. decode image;
5. apply locked preprocessing;
6. run one model;
7. compute logits;
8. take argmax;
9. map to class integer;
10. write CSV.

### 20.3 Submission schema

File:

```text
submission_NamaTim.csv
```

Columns:

```text
id,predicted
```

### 20.4 Automated checks

- [ ] exactly 1.458 rows
- [ ] columns exactly `id`, `predicted`
- [ ] no index column
- [ ] comma separator
- [ ] IDs exactly match template
- [ ] ID order exactly match template
- [ ] no missing prediction
- [ ] predictions subset of `{0, 1, 2}`
- [ ] no duplicate ID
- [ ] file opens cleanly
- [ ] class counts reported
- [ ] SHA256 stored
- [ ] source checkpoint hash stored
- [ ] config hash stored

### 20.5 Distribution audit

Prediction distribution boleh dipakai sebagai sanity check, bukan tuning target.

Flag untuk manual pipeline audit jika:

- satu class missing;
- Electronic prediction count near zero;
- distribution berubah ekstrem akibat class-order bug;
- all predictions identical.

Jangan mengubah threshold agar distribution menyerupai train atau submission lama.

### 20.6 Submission usage

Jika dua submission masih tersedia:

1. submit kandidat high-confidence pertama hanya setelah QA;
2. submission terakhir hanya dipakai jika kandidat kedua memiliki pre-submission validation evidence yang lebih kuat.

Jangan submit dua config yang hanya berbeda seed tanpa evidence.

---

## 21. Notebook Blueprint

### 21.1 Notebook V11B

Suggested title:

```text
v11b_train_only_label_audit_grouped_validation.ipynb
```

Cell structure:

1. Markdown: purpose and hard constraints.
2. Imports and environment.
3. Config.
4. Path resolution.
5. Artifact registry.
6. Raw manifest load.
7. Image integrity scan.
8. OOF source load.
9. OOF alignment.
10. Alignment assertions.
11. Exact duplicate detection.
12. Near-duplicate candidate generation.
13. Duplicate group construction.
14. Mixed-label group report.
15. Confident Learning scores.
16. Cross-model consensus features.
17. Seed stability features.
18. Nearest-neighbor purity.
19. Tier assignment.
20. Review queue export.
21. Optional review gallery export.
22. Review decisions import.
23. Review decision validation.
24. Cleaned manifest build.
25. StratifiedGroupKFold build.
26. Fold audit.
27. Control config load.
28. Raw grouped control.
29. Clean grouped control.
30. Paired comparison.
31. Decision gate.
32. Artifact export.
33. Final summary.

### 21.2 Notebook V12A

Suggested title:

```text
v12a_spatial_gram_prototype_head.ipynb
```

Cell structure:

1. Purpose and hypothesis.
2. Imports.
3. Locked config.
4. Load manifest and folds.
5. Load spatial cache.
6. Alignment assertions.
7. Descriptor implementations.
8. Leakage-safe prototype construction.
9. Smoke test.
10. Fold-0 candidate screen.
11. Seed stability.
12. Confirmation folds.
13. Full OOF assembly.
14. Metrics and error analysis.
15. Gate decision.
16. Artifact export.

### 21.3 Notebook final

Suggested title:

```text
satdat_final_single_model_submission.ipynb
```

Cell structure:

1. Competition and integrity statement.
2. Imports and versions.
3. Locked constants.
4. Resolve train and test paths.
5. Validate official counts.
6. Load selected manifest.
7. Define preprocessing.
8. Define one model.
9. Train final fixed epochs or load verified checkpoint.
10. Checkpoint QA.
11. Load official template.
12. Test inference.
13. Submission QA.
14. Save submission.
15. Save documentation artifacts.

### 21.4 Notebook quality rules

- All config values in one cell.
- No hidden state dependency.
- Restart and run all must work.
- Assertions precede expensive compute.
- No test scan in research notebooks.
- No hardcoded Kaggle input index.
- Output directories versioned.
- No overwrite of champion artifacts.
- Exceptions fail closed.
- Runtime summary printed.

---

## 22. Directory Structure

```text
satdat_part2/
├── data/
│   ├── manifests/
│   │   ├── train_manifest_raw.csv
│   │   ├── train_manifest_v11b_clean.csv
│   │   └── grouped_fold_assignments.csv
│   └── review/
│       ├── v11b_review_queue.csv
│       ├── v11b_review_decisions.csv
│       └── review_gallery/
├── artifacts/
│   ├── registry/
│   │   └── artifact_registry.csv
│   ├── duplicates/
│   │   ├── duplicate_groups.csv
│   │   └── duplicate_audit.json
│   ├── v11a2/
│   ├── v11b/
│   ├── v12a/
│   ├── v12b/
│   ├── v13/
│   └── final/
├── notebooks/
│   ├── v11a2_frozen_material_stabilization.ipynb
│   ├── v11b_train_only_label_audit_grouped_validation.ipynb
│   ├── v12a_spatial_gram_prototype_head.ipynb
│   └── satdat_final_single_model_submission.ipynb
├── configs/
│   ├── v11a2.yaml
│   ├── v11b.yaml
│   ├── v12a.yaml
│   └── final.yaml
├── logs/
│   ├── experiment_ledger.csv
│   └── decisions/
└── submissions/
    ├── candidate/
    └── uploaded/
```

---

## 23. Experiment Ledger

### 23.1 Ledger schema

`experiment_ledger.csv`

| Column | Description |
|---|---|
| `experiment_id` | unique ID |
| `parent_id` | control or prior experiment |
| `timestamp_start` | start |
| `timestamp_end` | end |
| `hypothesis` | one testable statement |
| `major_change` | one main change |
| `data_version` | manifest version |
| `fold_signature` | split signature |
| `model_config_hash` | model config |
| `seed` | seed |
| `status` | planned, running, complete, failed |
| `macro_f1` | score |
| `ro_error` | R/O error |
| `electronic_f1` | class metric |
| `runtime_minutes` | runtime |
| `peak_vram_mb` | memory |
| `decision` | adopt, reject, investigate |
| `decision_reason` | concise reason |
| `artifact_path` | output |

### 23.2 Hypothesis format

Good:

> Projected Gram statistics reduce R/O errors because they preserve second-order patch relations missing from mean pooling.

Bad:

> Try Gram head.

### 23.3 Decision format

Every complete run must end with one:

- `ADOPT`
- `REJECT`
- `INCONCLUSIVE`
- `BLOCKED`

No experiment remains in `complete but undecided`.

---

## 24. Failure Recovery

### 24.1 Cache mismatch

Symptoms:

- row count correct but sample alignment wrong;
- implausible score;
- duplicate IDs;
- label mismatch.

Action:

1. stop;
2. inspect cache index;
3. rebuild join using SHA;
4. invalidate current output;
5. rerun metrics.

### 24.2 Non-finite feature or loss

Action:

- backbone compute FP32 if required;
- storage FP16 only after finite check;
- reduce batch size once;
- enable gradient clipping;
- log offending samples;
- do not filter samples silently.

### 24.3 Kaggle session interruption

Checkpoint:

- completed fold;
- completed seed;
- config;
- fold predictions;
- training history;
- model state;
- RNG state if practical.

Resume only if config and data signatures match.

### 24.4 OOM

Safe order:

1. reduce batch size;
2. gradient accumulation;
3. mixed precision;
4. gradient checkpointing;
5. reduce resolution only as a new documented experiment.

Do not silently change resolution mid-run.

### 24.5 Manual review incomplete

- lock completed decisions;
- mark remaining rows unreviewed;
- do not infer decisions;
- generate manifest version with explicit coverage;
- continue grouped validation.

### 24.6 Final training failure

Fallback order:

1. last verified champion trained under grouped protocol;
2. V11A.2 if adopted and final path works;
3. V10 historical champion if exact inference artifacts exist;
4. V7 only if newer final checkpoints cannot be recovered.

Fallback must still satisfy single-model rule.

---

## 25. Risk Register

| Risk | Probability | Impact | Early signal | Mitigation |
|---|---|---|---|---|
| V10 artifacts unavailable | medium | high | missing OOF/config | use V7 for audit, do not claim exact V10 rerun |
| V11A.2 unstable | medium | medium | seed variance | stop stabilization path |
| Manual review bias | high | high | corrections match model almost perfectly | blind first pass, second review |
| Duplicate false merge | medium | high | visually different images one group | visual pair audit, lock threshold |
| Grouped score drops | high | medium | lower OOF than historical | accept honest baseline |
| Cleaning gives no direct gain | medium | medium | B6-C equals B6-B | retain clean data for adaptation |
| V12A overfits fold 0 | medium | high | no confirmation-fold wins | require confirmation |
| Geometry extraction misses cutoff | high | high | low throughput | smoke and cutoff |
| LoRA OOM | medium | high | first batch failure | batch reduction, checkpointing |
| LoRA memorizes noise | medium | high | train improves, valid degrades | clean manifest, early learning logs |
| Electronic class degrades | medium | high | E F1 drop | class-specific gate |
| Test order mismatch | low | critical | ID audit fail | template-driven merge |
| Ensemble accidentally used | low | critical | multiple checkpoints averaged | final graph and code audit |
| Submission buffer too small | medium | critical | final model late | H+27 training cutoff |

---

## 26. Go or No-Go Decision Tree

### 26.1 After V11A.2

```text
Does V11A.2 pass full adoption gate?
├── Yes
│   ├── Keep as current champion
│   └── Use its OOF in V11B
└── No
    ├── Keep V10 as champion
    ├── Use valid V11A.2 OOF as audit signal
    └── Close material stabilization path
```

### 26.2 After V11B controls

```text
Does cleaned grouped control beat raw grouped control?
├── Yes
│   ├── Adopt cleaned manifest
│   └── Continue V12A on cleaned grouped protocol
└── No
    ├── Are corrections verified and representation-limited?
    │   ├── Yes: retain clean manifest for LoRA ablation
    │   └── No: retain raw training labels
    └── Keep grouped folds in all cases
```

### 26.3 After V12A

```text
Does V12A pass gain, fold, seed, and R/O gates?
├── Yes
│   ├── Adopt as champion
│   └── Train final if deadline buffer is tight
└── No
    ├── Enough time for geometry or LoRA?
    │   ├── Yes: run one causal screen
    │   └── No: finalize current champion
```

### 26.4 Before LoRA

```text
Are grouped protocol, fallback checkpoint, and time reserve ready?
├── Yes: run ViT-L LoRA-256 screen
└── No: do not start LoRA
```

---

## 27. Detailed Completion Checklist

### 27.1 Project grounding

- [ ] raw counts verified
- [ ] official label mapping verified
- [ ] deadline and submission count verified
- [ ] manual test labels quarantined
- [ ] single-model rule documented

### 27.2 Artifact recovery

- [ ] V10 config recovered
- [ ] V10 OOF recovered
- [ ] V10 fold map recovered
- [ ] V11 spatial cache recovered
- [ ] cache index recovered
- [ ] V11A.2 output recovered or rerun
- [ ] artifact registry created
- [ ] checksums stored

### 27.3 V11A.2

- [ ] smoke test passed
- [ ] four candidate screen complete
- [ ] seed stability complete
- [ ] confirmation folds complete or deadline exception documented
- [ ] full OOF assembled
- [ ] adoption decision written

### 27.4 V11B queue

- [ ] canonical manifest built
- [ ] OOF aligned by stable ID
- [ ] exact duplicates grouped
- [ ] near-duplicates grouped
- [ ] mixed-label duplicates flagged
- [ ] Confident Learning score generated
- [ ] seed consensus generated
- [ ] nearest-neighbor purity generated
- [ ] tiered queue exported
- [ ] no test information present

### 27.5 Manual review

- [ ] blind stage used
- [ ] all P0 reviewed
- [ ] mixed-label duplicate coverage 100%
- [ ] correction reasons saved
- [ ] second review complete for corrections
- [ ] incomplete rows marked unreviewed

### 27.6 Manifest and folds

- [ ] cleaned manifest created
- [ ] correction matrix audited
- [ ] exclusions audited
- [ ] duplicate group per row exists
- [ ] grouped folds built once
- [ ] duplicate overlap equals zero
- [ ] fold checksum locked

### 27.7 Controls

- [ ] raw grouped control complete
- [ ] cleaned grouped control complete
- [ ] official and reviewed views reported
- [ ] paired comparison complete
- [ ] R/O analysis complete
- [ ] data policy decision written

### 27.8 V12 or V13

- [ ] hypothesis written
- [ ] one major change
- [ ] control matched
- [ ] fold-0 screen complete
- [ ] seed stability complete
- [ ] confirmation gate respected
- [ ] decision written

### 27.9 Final training

- [ ] champion table complete
- [ ] eligible candidate selected
- [ ] final epochs locked
- [ ] final seed locked
- [ ] one model trained
- [ ] checkpoint reload test passed
- [ ] checksum stored

### 27.10 Submission

- [ ] test loaded only after lock
- [ ] 1.458 rows
- [ ] exact columns
- [ ] exact ID order
- [ ] class values valid
- [ ] no missing values
- [ ] no ensemble
- [ ] output hash stored
- [ ] upload completed before 16.00 WIB

---

## 28. Final Priority List

### P0: Wajib selesai

1. Artifact recovery.
2. V11A.2 decision.
3. V11B mixed-label duplicate and consensus audit.
4. Duplicate-grouped fold lock.
5. Protocol-matched V10 control.
6. Final single-model checkpoint.
7. Submission QA.

### P1: Kerjakan jika P0 aman

1. Complete 300 to 500 image review.
2. V12A Gram/prototype screen.
3. V12A confirmation.

### P2: Conditional

1. V12B rectangular extraction.
2. ViT-L LoRA-256.

### P3: Jangan dikerjakan sebelum deadline

- head zoo tambahan;
- broad hyperparameter sweep;
- ViT-7B LoRA;
- full ViT-7B fine-tuning;
- unverified auto-relabel;
- test pseudo-labeling;
- model blend for final;
- post-hoc class threshold tuning;
- repeated leaderboard probing.

---

## 29. Recommended Immediate Next Actions

Urutan tindakan paling konkret:

1. Salin V10, V11A.1, dan V11A.2 artifacts terbaru ke satu working directory.
2. Buat `artifact_registry.csv`.
3. Verifikasi cache row map dan canonical train signature.
4. Selesaikan selected V11A.2 candidate sampai memiliki OOF probabilities.
5. Bangun `v11b_review_queue.csv` dari:
   - mixed-label duplicates;
   - V7;
   - V10;
   - V11A.2 seeds;
   - Confident Learning;
   - nearest-neighbor purity.
6. Review P0 and P1 secara blind.
7. Lock `train_manifest_v11b_clean.csv`.
8. Lock `grouped_fold_assignments.csv`.
9. Jalankan raw and cleaned protocol-matched V10 controls.
10. Jika masih ada minimal enam jam sebelum final-training cutoff, jalankan V12A.
11. Pilih champion menggunakan full candidate table.
12. Train one final model pada seluruh eligible train.
13. Jalankan test inference sekali dengan config locked.
14. Validasi and upload submission.

---

## 30. Bottom Line

V11B tetap perlu karena ia memperbaiki dua hal yang paling berbahaya bagi riset lanjutan:

1. label train yang salah atau ambigu;
2. near-duplicate leakage antar-fold.

Namun V11B bukan tujuan akhir. Jalur utama tetap:

```text
V11A.2 stabilization
→ V11B verified train audit
→ duplicate-grouped validation
→ exact V10 control
→ V12A material-aware spatial representation
→ conditional geometry or LoRA
→ one final model
→ locked test inference
```

Dengan deadline yang dekat, keputusan terbaik bukan menjalankan semua ide. Keputusan terbaik adalah menyelesaikan rangkaian eksperimen termurah yang memberi informasi paling kuat, mempertahankan fallback yang valid, dan menghentikan eksperimen mahal sebelum mengorbankan waktu final training serta submission.

---

## 31. Reference Basis

1. BDC Satria Data 2026 Problem 1 technical guide.
2. Project V1 to V8 notebooks and V7 analysis bundle.
3. Project handoff dated 26 July 2026.
4. V10, V11A.1, and V11A.2 state reconstructed from latest project conversation.
5. `SATDAT_0.997_RESEARCH_ROADMAP.md`.
6. [mxslr/mlcraft](https://github.com/mxslr/mlcraft).
7. [DINOv3](https://arxiv.org/abs/2508.10104).
8. [DINOv3 model card](https://github.com/facebookresearch/dinov3/blob/main/MODEL_CARD.md).
9. [Efficient Fine-Tuning of DINOv3](https://arxiv.org/html/2508.21041v3).
10. [DINOv3 LoRA for image forensics](https://arxiv.org/html/2604.16083v1).
11. [Confident Learning](https://arxiv.org/abs/1911.00068).
12. [Area Under the Margin](https://proceedings.neurips.cc/paper/2020/file/c6102b3727b2a7d8b1bb6981147081ef-Paper.pdf).
13. [Early-Learning Regularization](https://proceedings.neurips.cc/paper/2020/hash/ea89621bee7c88b2c5be6681c8ef4906-Abstract.html).
14. [FSSDINO](https://arxiv.org/html/2602.07550v1).
15. [Bilinear CNN Models for Fine-Grained Visual Recognition](https://openaccess.thecvf.com/content_iccv_2015/papers/Lin_Bilinear_CNN_Models_ICCV_2015_paper.pdf).
