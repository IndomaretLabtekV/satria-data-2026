# SATDAT / BDC Satria Data 2026 — Full Chat Handoff

Dokumen ini merangkum seluruh percakapan dalam room chat ini secara kronologis, tetapi bagian keputusan aktif hanya menampilkan versi terbaru yang sudah disepakati. Tujuannya agar percakapan bisa dilanjutkan di room lain tanpa kehilangan grounding context.

## 1. Konteks proyek

User: Riantama Putra  
Kompetisi: Big Data Challenge Satria Data 2026  
Task: klasifikasi citra sampah  
Kelas:
- 0 = Recyclable
- 1 = Electronic
- 2 = Organic

Data train:
- Total 26.527 gambar
- Recyclable: 9.999
- Electronic: 3.961
- Organic: 12.567

Data test penyisihan:
- 1.458 gambar
- Seluruh 1.458 gambar dipakai oleh leaderboard penyisihan
- Babak final akan memakai test baru yang tidak dibagikan pada tahap penyisihan

Metrik: Macro F1  
Batas submission: maksimal 3 kali selama penyisihan  
Target user: setinggi mungkin dan masuk minimal top 20.

Snapshot leaderboard terbaru yang dibagikan:
- Rank 1–3: 100,0000
- Rank 4–5: 99,9462
- Rank 20: 99,6179
- Panitia terbaru menyebut 20 tim teratas perlu pembuktian/video, bukan 22 tim.

## 2. Klarifikasi aturan yang sudah dianggap final

Berdasarkan isi grup peserta/panitia yang dibagikan:

1. Pretrained model publik diperbolehkan, termasuk DINOv2/DINOv3.
2. Frozen backbone dengan hanya melatih classifier head tetap dianggap transfer learning/fine-tuning yang legal.
3. Peserta boleh melakukan preprocessing apa pun pada data train selama tidak menambah data dari luar dataset panitia.
4. Menghapus data train yang dianggap salah label diperbolehkan.
5. Relabeling juga dianggap legal menurut klarifikasi lanjutan yang dipahami dalam percakapan.
6. Augmentasi dari data panitia diperbolehkan.
7. Test tidak boleh dipakai untuk training, fine-tuning, pseudo-labeling, atau pembaruan parameter.
8. Format submission memakai angka kelas, bukan nama folder.
9. Tim top 20 akan diminta menjelaskan cara memperoleh hasil prediksi; karena itu pipeline harus dapat direproduksi dan diaudit.

Keputusan operasional:
- Raw train original tetap disimpan sebagai sumber canonical.
- Dataset train yang sudah dimodifikasi secara fisik tidak dipakai untuk validasi.
- Cleaning/relabel treatment diterapkan hanya pada training partition melalui manifest/mapping.
- Validation selalu mempertahankan label official original.
- Official test tidak disentuh selama screening eksperimen.

## 3. Arah strategi yang dikunci

Strategi utama proyek:
- Family backbone dikunci pada DINOv3.
- Menggunakan model high-end secara langsung.
- Backbone 100% frozen.
- Yang dioptimalkan selanjutnya adalah classifier head, training strategy, feature use, ensemble, data-centric treatment, calibration, dan inference.
- Tidak ada lagi scaling backbone setelah ViT-7B.
- Tidak menjalankan apa pun secara lokal karena laptop tidak punya GPU.
- Notebook disiapkan untuk Kaggle T4 x2.
- Eksperimen baru diuji fold 0 terlebih dahulu.
- Hanya kandidat yang melewati gate ketat yang boleh lanjut full 5-fold.
- Pada akhirnya seluruh recipe terbaik harus dikonsolidasikan menjadi satu notebook end-to-end seperti `ver34_clean_end_to_end.ipynb`.

## 4. Peran kerja yang disepakati

Peran assistant:
- Menjadi research/engineering sparring partner.
- Menganalisis hasil eksperimen.
- Menentukan satu next approach yang paling rasional, bukan memberi daftar opsi tanpa keputusan.
- Melakukan static audit notebook sebelum run.
- Membuat prompt Codex/Sol 5.6 Max.
- Memperbaiki notebook bila bug kecil dan spesifik lebih efisien diperbaiki langsung.
- Menjaga leakage guard, reproducibility, artifact contract, dan test isolation.
- Menentukan apakah eksperimen lanjut, dihentikan, atau diadopsi.

Peran user:
- Menjalankan notebook di Kaggle.
- Menyediakan artifact/log/result bundle.
- Mengatur Kaggle input dataset.
- Menyimpan feature cache/checkpoint mahal.
- Melakukan review manusia pada kandidat gambar bila diperlukan.
- Menentukan submission final berdasarkan OOF dan rekomendasi.

## 5. Kronologi eksperimen

### 5.1 Persiapan V7 — DINOv3 ViT-7B frozen

Diputuskan mencoba backbone high-end terakhir:
- Model: `facebook/dinov3-vit7b16-pretrain-lvd1689m`
- LVD natural-image checkpoint, bukan SAT satellite checkpoint
- Official Hugging Face Transformers implementation
- Native input 256×256
- Backbone frozen
- Model sharding lintas T4 x2
- Bukan DataParallel
- Original view saja
- Seed control: 42
- Feature: final CLS + mean true patch tokens
- Register tokens tidak dimasukkan ke patch mean
- Sekali extraction menyimpan pooled representation empat block terakhir
- Cache FP16
- Head training murah dilakukan dari cache

Alasan menolak SAT:
- Dataset kompetisi berupa objek sampah natural, bukan citra satelit/ortho.
- LVD jauh lebih domain-aligned.

### 5.2 Audit V7: bug official final LayerNorm

Notebook V7 awal memiliki bug:
- Hook mengambil output transformer block sebelum official final pretrained LayerNorm.
- Akibatnya baseline bukan representation final resmi DINOv3.

Perbaikan final:
- Intermediate block tokens dilewatkan official final norm per token sebelum pooling.
- Final block menggunakan `model_output.last_hidden_state`.
- Preflight membandingkan `final_norm(raw_last_block)` dengan `last_hidden_state`.
- Cache schema dan revision marker dinaikkan supaya cache lama tidak dapat dipakai ulang.

Keputusan:
- V7 belum boleh run sebelum fix tersebut.
- Setelah fix, notebook lolos static audit.

### 5.3 Masalah sharding ViT-7B

Run pertama gagal karena Accelerate menaruh sebagian parameter ke disk.

Konfigurasi gagal:
- `balanced_low_0`
- max memory asimetris 13 GiB dan 10 GiB

Perbaikan final:
- `SHARDING_STRATEGY = balanced`
- max memory 13 GiB pada masing-masing GPU
- FP16 sudah dipakai saat model loading
- Audit tetap fail-closed bila device map mengandung CPU atau disk

Hasil:
- Model berhasil dimuat hanya di `cuda:0` dan `cuda:1`.
- ViT-7B ternyata feasible pada T4 x2.

### 5.4 Hasil V7

V7 menjadi model terbaik proyek.

Fold 0:
- ViT-7B baseline head Macro F1: 0.987818
- ViT-7B `regularized_mlp_final`: 0.989918
- Total error selected head fold 0: 61
- Recyclable → Organic: 24
- Organic → Recyclable: 30
- R↔O total: 54

Assessment folds 1–4:
- Baseline ViT-7B: 0.989190
- Selected regularized head: 0.990191
- Total error baseline: 253
- Total error selected: 226
- Selected R→O: 81
- Selected O→R: 106

Per fold selected head:
- Fold 1: 0.990363
- Fold 2: 0.990982
- Fold 3: 0.988719
- Fold 4: 0.990698

Combined five-fold OOF:
- Macro F1: 0.9901360067264733
- Accuracy: sekitar 0.989181
- Total error: 287
- R→O: 105
- O→R: 136
- R↔O total: 241

Kesimpulan:
- ViT-7B LVD frozen menjadi backbone final.
- `regularized_mlp_final` menjadi head utama.
- Scaling backbone dihentikan.
- Electronic hampir saturasi.
- Mayoritas residual error berasal dari Recyclable ↔ Organic.
- Probability calibration selected head lebih buruk daripada baseline, tetapi Macro F1 lebih baik.
- Untuk argmax/single-model prediction, selected head tetap dipilih.
- Untuk blending, probabilitas perlu diperlakukan hati-hati.

Runtime:
- Throughput sekitar 3.91 image/s.
- Full train feature extraction sekitar 1.88 jam.
- Cache train lengkap dan sangat berharga; jangan dihapus.

### 5.5 Analisis head dan feature V7

Hasil head study:
- Final-layer regularized MLP adalah yang terbaik.
- `last4_layer_weighted_gated` kalah dari final-layer head.
- Dual-branch/cosine/weighted alternatives tidak mengalahkan selected head.
- Hflip pada eksperimen lama hanya memberi sekitar +0.000089.
- Calibration scalar tidak mengubah argmax.
- Simple class bias, confidence switching, dan probability blend tidak memberikan gain kuat yang stabil.
- Multi-layer feature readout tidak diprioritaskan lagi.

### 5.6 V8 — Hierarchical Recyclable/Organic specialist

Hipotesis:
- Main V7 three-class head dipertahankan.
- Tambah binary specialist khusus Recyclable vs Organic.
- Electronic decision dipertahankan.
- V8 cache-only, tanpa menjalankan backbone.

Kandidat:
- `ro_specialist_blend75`
- `ro_specialist_full`

Fold 0:
- V7 control: 0.989918, 61 total error, 54 R↔O error
- Blend 0.75: 0.989322, 65 total error, 58 R↔O error
- Full specialist: 0.989472, 64 total error, 57 R↔O error

Detail:
- Blend memperbaiki 6 sampel, merusak 10, net -4.
- Full memperbaiki 10, merusak 13, net -3.
- Electronic F1 tidak rusak.
- Boundary R/O justru memburuk.

Keputusan final V8:
- V8 ditolak.
- Tidak lanjut folds 1–4.
- V7 tetap pipeline utama.
- Binary specialist terpisah dianggap kurang baik karena kehilangan konteks joint three-class boundary.

### 5.7 Rencana V9 awal dan perubahan karena klarifikasi panitia

Rencana awal V9 sempat berupa targeted R/O manifold Mixup + multi-seed ensemble.

Setelah muncul klarifikasi panitia bahwa peserta bebas melakukan preprocessing data train, termasuk membuang data salah label, prioritas V9 berubah menjadi audited data cleaning.

Versi lama manifold Mixup dianggap superseded.

### 5.8 V9 AUDIT — kandidat cleaning

Mode AUDIT menghasilkan:
- 382 kandidat total
- 2 exact-duplicate conflicts sebagai automatic safe drop
- 23 kandidat Tier B untuk human review
- 357 kandidat ambigu sebagai keep
- 230 consensus-wrong samples dari OOF comparison
- Tidak ada training head pada tahap AUDIT

Dua exact duplicate conflict:
- `0_Recyclable/R_799.jpg`
- `2_Organic/O_8873.jpg`

Keduanya identik tetapi memiliki label berbeda.
Keputusan:
- Drop kedua file.
- Jangan relabel salah satu berdasarkan tebakan.

Sepuluh obvious mislabels yang dipilih untuk treatment:

Recyclable → Electronic:
- `0_Recyclable/R_3825.jpg` — keyboard
- `0_Recyclable/R_8295.jpg` — laptop

Organic → Electronic:
- `2_Organic/O_7701.jpg` — microwave
- `2_Organic/O_7776.jpg` — microwave

Recyclable → Organic:
- `0_Recyclable/R_9775.jpg` — makanan
- `0_Recyclable/R_8580.jpg` — mi/makanan

Organic → Recyclable:
- `2_Organic/O_1949.jpg` — pitcher/teko plastik
- `2_Organic/O_9175.jpg` — notebook/buku catatan
- `2_Organic/O_1807.jpg` — botol plastik
- `2_Organic/O_1978.jpg` — amplop kertas

Semua kandidat lain:
- KEEP atau AMBIGUOUS_KEEP.
- Kasus isi vs kemasan, kain, spons, mangkuk, close-up material, dan objek manufactured yang kelas targetnya tidak pasti tidak diubah.

### 5.9 Keputusan membandingkan drop vs relabel

Karena panitia mengizinkan preprocessing fleksibel dan relabeling dipahami legal, diputuskan tidak menebak secara teori.

Fold 0 membandingkan:
- C0: V7 original control
- C1: drop 2 duplicate conflict + drop 10 obvious mislabels
- C2: drop 2 duplicate conflict + relabel 10 obvious mislabels
- C3: 50% C0 + 50% C2

Leakage guard:
- Treatment hanya diterapkan pada training partition.
- Validation tetap lengkap dengan label original.
- Bila reviewed sample berada di validation fold, sample tersebut tidak dihapus dan labelnya tidak diubah.
- Raw original dataset tetap canonical.
- Folder train cleaned fisik tidak dipakai untuk validation.

Sempat ada bug timestamp campuran pada reviewed manifest.
Perbaikan:
- Timestamp parser memakai format mixed.
- Dataset audit tidak perlu diubah.
- Notebook V9 v2 dijalankan ulang.

### 5.10 Hasil V9 drop-vs-relabel

Fold 0:
- C0 original V7: 0.989918, 61 total error, 54 R↔O error
- C1 drop-only: 0.989471, 64 total error, 57 R↔O error
- C2 relabel: 0.989303, 66 total error, 60 R↔O error
- C3 blend 50/50: 0.989301, 66 total error, 60 R↔O error

Deltas:
- Drop-only turun sekitar 0.000447 dan menambah 3 error.
- Relabel turun sekitar 0.000615 dan menambah 5 error.
- Blend tidak membantu.
- Relabel meningkatkan Electronic F1, tetapi memperburuk Organic → Recyclable.
- Log loss C1/C2 membaik, tetapi argmax Macro F1 memburuk.
- Control V7 berhasil direproduksi persis sehingga eksperimen dianggap valid.

Keputusan final V9:
- Drop-only ditolak.
- Relabel ditolak.
- Blend ditolak.
- Tidak lanjut full five-fold.
- Jangan mengganti raw train original dengan versi cleaned.
- Cleaning audit tetap disimpan sebagai eksperimen negatif yang sah.
- V7 original tetap model utama.

## 6. Current best pipeline

Backbone:
- DINOv3 ViT-7B LVD-1689M
- Exact model revision yang pernah dipakai:
  `b80367753773648a6793235ab9c65cdbb029506f`
- Frozen 100%
- Native 256
- Official final LayerNorm sebelum pooling
- Final CLS + true-patch mean
- Original view
- No TTA
- No pseudo-label
- No cleaning treatment
- No specialist
- No partial unfreezing
- No LoRA

Head:
- `regularized_mlp_final`
- Joint three-class classifier
- V7 original training labels

Validation benchmark:
- Fold 0: 0.989918
- Five-fold OOF: 0.9901360067264733

Status:
- Ini fallback final yang sudah terbukti.
- Ini kandidat Submission 1 paling aman.

## 7. Next experiment yang sedang aktif: V10

V10 adalah eksperimen murah terakhir yang masih dianggap rasional sebelum berhenti research dan membangun notebook end-to-end.

Nama konsep:
- V10 multi-seed ensemble pada V7 original

Desain:
- Backbone tetap ViT-7B frozen.
- Feature tetap final CLS + patch mean dari cache V7.
- Head tetap `regularized_mlp_final`.
- Data tetap original, tanpa cleaning.
- Seeds:
  - 42
  - 2026
  - 3407
- Prediksi kandidat: rata-rata probabilitas tiga seed.
- Tidak menjalankan backbone ulang.
- Tidak menyentuh test saat screening.

Fold 0:
- Reproduce seed-42 control.
- Train seed 2026.
- Train seed 3407.
- Nilai single-seed dan three-seed average.
- Analisis corrected vs regressed samples, disagreement, dan complementarity terhadap V7.

Gate sementara:
- Gain Macro F1 minimal sekitar +0.0003 terhadap V7 control.
- Total error tidak bertambah.
- R/O error berkurang.
- Electronic F1 tidak turun material.
- Kandidat tidak bergantung pada satu sampel saja.

Jika fold 0 lolos:
- Jalankan seluruh 5 fold untuk tiga seed.
- Bandingkan V10 standalone dan blend dengan V7.
- Kandidat terbaik menjadi opsi Submission 2.

Jika V10 gagal:
- Hentikan eksperimen head.
- Langsung bangun notebook final end-to-end dengan V7 sebagai submission utama.

## 8. Rencana submission

Saat ini:
- Submission 1: V7 original-data ViT-7B frozen + regularized MLP, five-fold probability average.
- Submission 2: belum dikunci; targetnya V10 multi-seed ensemble bila lolos OOF gate.
- Submission 3: disimpan sebagai cadangan strategis dan tidak boleh dipakai tanpa bukti OOF kuat.

Tidak boleh memilih submission berdasarkan leaderboard probing karena:
- Hanya ada tiga upload.
- Leaderboard memakai seluruh test penyisihan.
- Final memakai test baru.
- OOF dan robustness harus menjadi dasar utama.

## 9. Notebook final end-to-end

Setelah recipe final dikunci, harus dibuat satu notebook utuh seperti `ver34_clean_end_to_end.ipynb`.

Notebook final harus bisa sekali run:
1. Audit environment dan dua T4.
2. Resolve raw train dan official test.
3. Verifikasi count, class map, fold assignment, dan signature.
4. Load exact DINOv3 ViT-7B revision.
5. Freeze backbone.
6. Reuse train cache atau rebuild train feature cache.
7. Train seluruh fold/head/seed yang dikunci.
8. Extract test feature satu kali.
9. Infer seluruh head.
10. Average probability lintas fold/seed.
11. Menghasilkan Submission 1 dan Submission 2.
12. Menyimpan checkpoint, probability, manifest, audit, dan ZIP artifact.
13. Fail closed bila OOF reproduction melenceng dari benchmark.

Dua mode:
- Fast/default: reuse train cache.
- Full reproducibility: rebuild feature cache dari raw train.

Test feature cukup diekstrak satu kali karena V7 dan kandidat V10 memakai representation yang sama.

## 10. Artifact penting dan lokasi

Local project:
- `C:\Users\riant\Downloads\waste-classification-dinov3`

Local results:
- `C:\Users\riant\Downloads\waste-classification-dinov3\results`

Folder penting:
- `results\v7_analysis_bundle`
- `results\v8_analysis_bundle`
- V9 result bundles tersimpan sebagai hasil eksperimen negatif

Kaggle V7:
- `/kaggle/input/datasets/riantamaputra/v7-results`
- `/kaggle/input/datasets/riantamaputra/v7-results/v7_dinov3_vit7b_frozen_raw`

Kaggle V8:
- `/kaggle/input/datasets/riantamaputra/v8-results`
- `/kaggle/input/datasets/riantamaputra/v8-results/v8_dinov3_vit7b_frozen_cache_upgrade`

Kaggle reviewed audit V9:
- `/kaggle/input/datasets/riantamaputra/v9-audit-reviewed-drop-vs-relabel`
- `/kaggle/input/datasets/riantamaputra/v9-audit-reviewed-drop-vs-relabel/v9_dinov3_vit7b_frozen_audited_cleaning`

Feature cache V7:
- `v7_dinov3_vit7b_frozen_raw/feature_cache/shards`
- 104 shards
- Shape total: `(26527, 2, 4096)`
- Dtype: FP16

Checkpoint V7 penting:
- Fold 0 development regularized head
- Fold 1–4 selected regularized heads
- Jangan hapus checkpoint maupun cache.

## 11. Artifact/notebook yang pernah dibuat

V7:
- `v7-dinov3-vit7b-frozen-raw.ipynb`
- Prompt V7 high-end
- Prompt fix official final LayerNorm
- V7 analysis bundle

V8:
- `v8-dinov3-vit7b-frozen-cache-upgrade.ipynb`
- Prompt V8 cache upgrade
- V8 analysis bundle

V9:
- Prompt V9 audited cleaning
- `v9-dinov3-vit7b-frozen-audited-cleaning.ipynb`
- V9 audit bundle
- `v9-dinov3-vit7b-frozen-drop-vs-relabel-v2.ipynb`
- V9 results bundle drop-vs-relabel

Status artifact:
- V7 diadopsi.
- V8 dan V9 disimpan sebagai negative experiment evidence.
- V10 notebook/prompt belum dibuat pada akhir room ini.

## 12. Hal-hal yang tidak perlu diulang di room baru

Jangan kembali mempertimbangkan:
- DINOv3 SAT checkpoint.
- Scaling backbone di atas ViT-7B.
- Binary R/O specialist V8.
- Drop-only cleaning V9.
- Relabel obvious-mislabel V9.
- 50/50 blend V7 + cleaned model.
- Weighted last-four-layer gated head yang sudah kalah.
- Hflip sebagai prioritas.
- Partial unfreezing/LoRA 7B pada T4 x2.
- Pseudo-label test.
- Mengubah validation label.
- Mengganti raw official dataset dengan folder cleaned.
- Sweep besar tanpa gate fold 0.

Semua itu sudah diuji atau ditolak berdasarkan risiko, aturan, atau hasil OOF.

## 13. Instruksi untuk melanjutkan di room baru

Mulai percakapan baru dengan konteks:

“Lanjutkan proyek BDC Satria Data 2026 dari handoff ini. Current best adalah V7 DINOv3 ViT-7B LVD frozen + regularized_mlp_final dengan five-fold OOF 0.990136. V8 specialist dan V9 cleaning/relabel telah gagal. Next active experiment adalah V10 cache-only multi-seed original-data ensemble menggunakan seeds 42, 2026, dan 3407. Buat satu keputusan eksperimen yang ketat, fold 0 dulu, lalu full 5-fold hanya bila lolos gate. Setelah V10, konsolidasikan pipeline final menjadi satu notebook end-to-end yang menghasilkan dua submission.”

Prioritas pertama room baru:
1. Audit kembali V7 result/cache contract.
2. Buat prompt atau notebook V10 multi-seed.
3. Jangan menjalankan backbone.
4. Jangan menyentuh test.
5. Reproduce V7 fold-0 control persis.
6. Uji three-seed average.
7. Lanjut full fold hanya bila ada gain stabil.
8. Setelah itu bangun notebook end-to-end final.

## 14. Ringkasan satu paragraf

Proyek telah mengunci DINOv3 ViT-7B LVD frozen sebagai backbone final. V7 regularized three-class head mencapai 0.989918 pada fold 0 dan 0.990136 five-fold OOF, sehingga menjadi fallback final dan kandidat Submission 1. V8 hierarchical R/O specialist gagal karena menambah error. V9 audited cleaning membandingkan drop dan relabel terhadap obvious mislabels, tetapi keduanya juga menurunkan Macro F1; raw train original tetap canonical. Eksperimen berikutnya yang aktif adalah V10 multi-seed ensemble pada V7 original dengan seeds 42, 2026, dan 3407, cache-only dan fold-0-first. Bila V10 gagal, research dihentikan dan pipeline langsung dikonsolidasikan menjadi satu notebook end-to-end yang mereproduksi V7 dan membuat submission final.
