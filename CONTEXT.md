# CONTEXT — BDC Satria Data 2026 (Klasifikasi Citra Sampah)

**Dokumen grounding tunggal.** Menggabungkan juknis resmi, seluruh handoff di `sum/`, kedua roadmap di `plan/`, artifact di `results/`, dan notebook di `scripts/`.

**Tanggal grounding:** 29 Juli 2026
**Deadline submission:** 30 Juli 2026, 16.00 WIB
**Champion saat ini:** V10 `timm_control` — five-fold OOF Macro F1 **0.9901662323927614**
**Status:** V13 (resampling model-native) siap jalan. V12 (ViT-L LoRA) siap tetapi **tidak layak dijalankan di sisa waktu** — lihat §14.
**Submission tersisa: 1 dari 3.**

> **Aturan baca:** kalau `sum/` atau `plan/` bertentangan dengan `results/`, **`results/` yang menang.** Lihat §13.

---

## 1. Status Ringkas

| Item | Nilai |
|---|---|
| Champion | V10 `timm_control` (frozen DINOv3 ViT-7B + MLP head) |
| Five-fold OOF Macro F1 | 0.9901662323927614 |
| Total error OOF | 287 dari 26.527 |
| Error Recyclable↔Organic | 242 (84,3% dari seluruh error) |
| Checkpoint final | `results/v10_dinov3_vit7b_timm_rich_spatial/final_head.pt` |
| Distribusi prediksi test | 520 / 201 / 737 |
| Submission terpakai | **2** (ConvNeXt relabel ~98,0473 + satu percobaan lain) |
| Submission tersisa | **1** |
| Eksperimen terakhir gagal | V11 material-query attention |
| Eksperimen siap jalan | **V13 resampling model-native (bicubic)** |
| Eksperimen siap tapi ditunda | V12 ViT-L + LoRA @ 320px — tidak muat di sisa waktu, lihat §14 |

---

## 2. Kompetisi

Klasifikasi citra sampah tiga kelas untuk mendukung pemilahan otomatis.

| Kode | Kelas | Definisi resmi |
|---:|---|---|
| 0 | Recyclable | Sampah non-elektronik yang berpotensi didaur ulang: botol plastik, kaleng, kertas, kardus, kaca |
| 1 | Electronic | Perangkat/limbah elektronik, berfungsi maupun rusak: HP, laptop, keyboard, mouse, charger, kabel |
| 2 | Organic | Bahan hayati yang mudah terurai: daun, buah, sayuran, sisa makanan, ranting, bagian tumbuhan |

**Dataset**

| Split | Jumlah | Keterangan |
|---|---:|---|
| Train total | 26.527 | berlabel, terpisah per subfolder kelas |
| — `0_Recyclable` | 9.999 | |
| — `1_Electronic` | 3.961 | kelas minoritas |
| — `2_Organic` | 12.567 | kelas mayoritas |
| Test | 1.458 | tanpa label, dinamai `1.jpg`–`1458.jpg` |

**Metrik:** Macro-averaged F1-Score = `mean(F1_Recyclable, F1_Electronic, F1_Organic)`.

**Submission**

- Nama file: `submission_NamaTim.csv`
- Kolom persis: `id,predicted` — CSV pemisah koma, tanpa kolom index
- `predicted` diisi kode numerik `0` / `1` / `2`
- Urutan baris **wajib** identik dengan `submission.csv` panitia (tersedia di `data/submission.csv`, 1458 baris + header)
- Maksimal **3 submission**; nilai tertinggi yang dipakai
- Tidak ada perpanjangan waktu

**Seleksi:** 20 tim teratas lolos semifinal, maksimal 3 tim per perguruan tinggi. Nilai sama → yang upload lebih dulu menang. **Tim terpilih wajib membuktikan lewat video bahwa prediksi tidak dibuat manual** — karena itu pipeline harus reproducible dan auditable.

**Konteks leaderboard** (snapshot yang pernah dibagikan): Rank 1–3 = 100,0000 · Rank 4–5 = 99,9462 · Rank 20 = 99,6179. Benchmark eksternal peserta lain: 99,7311. Target user: ≥ 99,8925.

---

## 3. Aturan Panitia (Hard Constraints)

### 3.1 Dari juknis §5 — Batasan

- Model **wajib** dibangun dari Data Latih panitia.
- Hanya **informasi visual** yang boleh dipakai. Metadata, label tambahan, atau informasi lain di luar konten citra **dilarang** sebagai fitur prediksi.
- Preprocessing dan augmentasi Data Latih **diperbolehkan**, sepanjang tidak memanfaatkan informasi dari Data Uji.
- Data Uji **hanya** untuk menghasilkan prediksi akhir. Dilarang dipakai untuk training, validasi, model selection, maupun hyperparameter tuning.
- Software/library/framework open source **diperbolehkan**.
- **Model pre-trained publik diperbolehkan** untuk transfer learning (EfficientNet, ResNet, ConvNeXt, ViT, …) selama tidak pernah dilatih pada data kompetisi ini. Backbone **wajib didokumentasikan** di laporan akhir.
- **Dilarang** menambah citra berlabel dari sumber lain.
- Format submission tidak boleh diubah (nama kolom, format file, urutan data).
- Seluruh pengembangan mandiri, tanpa label Data Uji.
- Panitia berhak memverifikasi metode; pelanggaran → diskualifikasi.

### 3.2 Dari juknis §7 — Sanksi

Diskualifikasi untuk: pelanggaran ketentuan, plagiarisme/manipulasi hasil, penggunaan label Data Uji, rekayasa prediksi, kolusi antarpeserta, dan ketidakmampuan menunjukkan proses pengembangan model saat diminta.

### 3.3 Klarifikasi panitia via grup peserta

> Sumber: `sum/satdat_chat_handoff_full2/00_MASTER_HANDOFF.md` §2. Bukan teks juknis — perlakukan sebagai interpretasi yang sudah disepakati dalam proyek ini.

1. Pretrained publik diperbolehkan, termasuk DINOv2/DINOv3.
2. **Frozen backbone + hanya melatih classifier head tetap dianggap transfer learning yang legal.**
3. Peserta boleh melakukan preprocessing apa pun pada train selama tidak menambah data luar.
4. **Menghapus data train yang salah label diperbolehkan.**
5. **Relabeling juga dipahami legal.**
6. Augmentasi dari data panitia diperbolehkan.
7. Test tidak boleh dipakai untuk training, fine-tuning, pseudo-labeling, atau pembaruan parameter.
8. Submission memakai angka kelas, bukan nama folder.
9. Tim top 20 diminta menjelaskan cara memperoleh prediksi → pipeline harus reproducible.

---

## 4. Constraint yang Dipaksakan Tim Sendiri

> **Ini bukan aturan panitia.** Ini keputusan internal. Mencampurnya dengan §3 adalah kesalahan paling mahal untuk sesi berikutnya.

**Single-model contract** — final submission harus dari **satu** model:

- Tanpa fold ensembling, seed ensembling, model soup, probability blending.
- Tanpa multiple backbone families, specialist heads, multi-crop, TTA/hflip.
- Ensemble hanya boleh untuk **diagnosis** dan **ranking manual review queue**.
- Branch internal dalam satu arsitektur yang di-train bersama boleh, asal menghasilkan satu checkpoint dan satu forward graph.

*(Sumber: `results/v10_.../locked_contract.json` → `single_model_contract`; `plan/...EXECUTION_PLAN...` §19.1.)*

**Data policy**

- Raw official labels = canonical development dataset. Cleaned dataset hanya cadangan/ablation.
- Validation **selalu** memakai label official original — treatment cleaning hanya di training partition.
- Tidak ada auto-relabel. Semua relabel wajib setelah inspeksi visual manusia.
- Gambar ambigu dibiarkan raw, tidak dipaksa mengikuti prediksi model.
- `manual-labeling.csv` / manual test labels **dikarantina**, tidak boleh dibuka.
- Test probabilities tidak boleh memengaruhi cleaning.

**Proses**

- Satu perubahan besar per eksperimen.
- Kandidat mahal wajib lolos screen fold-0 sebelum full 5-fold.
- Leaderboard **tidak** dipakai sebagai debugger (hanya 3 upload; final memakai test baru).
- Semua hasil negatif tetap dicatat; tidak ada eksperimen berstatus "selesai tapi belum diputuskan".
- Tidak ada eksekusi lokal — laptop tanpa GPU. Semua di Kaggle **T4 × 2**.
- Tidak meminta/memakai notebook, kode, checkpoint, atau config privat peserta lain.

---

## 5. Ledger Eksperimen V1–V12

| Versi | Perubahan utama | Fold 0 | Full OOF | Error | R/O | Keputusan |
|---|---|---:|---:|---:|---:|---|
| V1–V4 | ConvNeXt / MaxViT baseline | — | ~0.982327 (ConvNeXt) | 519 | — | ditinggalkan; DINOv3 lebih kuat & lebih cepat |
| V5 | DINOv3 ViT-L/16 frozen, `mlp_concat_weighted_ce` | 0.985022 | **0.986149** | ~402 | 336 | baseline lama |
| V6 | DINOv3 ViT-H+ frozen | 0.985188 | — | — | — | ditolak: scale tanpa adaptasi tidak membantu |
| V7 | DINOv3 ViT-7B frozen, `regularized_mlp_final` | 0.989918 | **0.9901360067264733** | 287 | 241 | **diadopsi** — backbone dikunci |
| V8 | Hierarchical specialist biner R vs O | 0.989322 / 0.989472 | — | 65 / 64 | 58 / 57 | **ditolak**: net -4 / -3 sampel, boundary R/O memburuk |
| V9 | Audited cleaning: drop vs relabel | C1 0.989471 · C2 0.989303 · C3 0.989301 | — | 64 / 66 / 66 | 57 / 60 / 60 | **ditolak**: ketiganya di bawah kontrol 0.989918 |
| V9A | Head zoo + pairwise blend di cache V7 | — | 0.9904393 vs kontrol 0.9903008 | 225 | 192 | **ditolak**: +0,000139, hanya 2 fold win, blend dilarang kontrak |
| V10 `timm_control` | Pindah backend ke timm, readout V7 | 0.9897706675032462 | **0.9901662323927614** | 287 | 242 | **CHAMPION** |
| V10 `rich_spatial_fusion` | 17 branch spatial/distribusional | 0.9882367633437932 | — | 72 | 65 | **ditolak**: -0,00153 vs kontrol pada fold 0 |
| V11 | Material-query cross-attention, 3 view | ~0.983106 | — | — | — | **ditolak keras**: -0,0067 vs kontrol; `timm_control` diadopsi lagi |
| V12 | DINOv3 **ViT-L** + LoRA r8 @ 320px | — | — | — | — | **belum dijalankan**; ditunda (§14) — notebook melanggar single-model contract dan tidak muat di sisa waktu |
| V13 | **Resampling model-native**: bilinear → bicubic, geometri & readout & head tidak berubah | — | — | — | — | **belum dijalankan** (notebook READY, `scripts/v13-dinov3-vit7b-model-native-resampling.ipynb`) |

**Detail per fold V10 `timm_control`** (`assessment_per_fold.csv`):

| Fold | Best epoch | Macro F1 | Error | R/O | Electronic err |
|---:|---:|---:|---:|---:|---:|
| 0 (development) | 5 | 0.9897706675 | 62 | 55 | 2 |
| 1 | 8 | 0.9903469895 | 56 | 47 | 1 |
| 2 | 3 | 0.9908291601 | 53 | 44 | 5 |
| 3 | 5 | 0.9890345290 | 64 | 54 | 5 |
| 4 | 6 | 0.9908498967 | 52 | 42 | 3 |
| **Agregat 1–4** | | **0.9902651576** | 225 | 187 | 14 |
| **Full OOF** | | **0.9901662324** | 287 | 242 | 16 |

**Per kelas OOF V10:** Recyclable F1 0.9863779 · Electronic F1 0.9943289 · Organic F1 0.9897918.
**Confusion OOF V10:** R→O 96 · O→R 146 · Electronic error 16 · high-confidence error 33.

---

## 6. Resep Champion (V10 `timm_control`)

**Backbone**

| Item | Nilai |
|---|---|
| Repo timm | `timm/vit_7b_patch16_dinov3.lvd1689m` |
| Ekuivalen Transformers | `facebook/dinov3-vit7b16-pretrain-lvd1689m` |
| Revision (dikunci) | `b40f6c827cb02b13c7a23a76cf598489bb0f94e5` |
| Freeze | 100% frozen, dtype FP16 |
| Checkpoint | LVD-1689M (**bukan** SAT — data kompetisi adalah citra natural) |

**Preprocessing** — PIL, EXIF transpose, konversi RGB, resize `direct_square` **256×256** bilinear + antialias, tanpa center crop, tanpa letterbox, tanpa augmentasi, view `orig` saja. Mean `[0.485, 0.456, 0.406]`, std `[0.229, 0.224, 0.225]`. Large-image guard (>8 MP → downscale sisi maks 1024, LANCZOS) murni untuk keamanan memori decoder, bukan fitur prediktif.

**Token contract** — 261 token = 5 prefix (1 CLS + 4 register) + 256 patch. Hidden size 4096.

- **Register token dikecualikan dari setiap statistik patch.**
- LayerNorm final pretrained resmi diterapkan **tepat sekali per token, sebelum** ekstraksi CLS dan sebelum pooling patch.
- Readout: `final normalized CLS ‖ mean(final normalized true patch tokens)` → **8192-D**, disimpan FP16, pooling dihitung FP32.

**Head** — `LayerNorm(8192) → Linear(512) → GELU → Dropout(0.4) → Linear(3)`, 4.212.739 parameter.

**Training head**

| Param | Nilai |
|---|---|
| Optimizer | AdamW, lr 8e-4, weight decay 1e-4 |
| Scheduler | CosineAnnealingLR |
| Loss | weighted CE, label smoothing 0.05 |
| Class weights | `total / (num_classes × class_count)` dari partisi training aktif |
| Batch | 256 (train) / 512 (predict) |
| Epoch | maks 15, early stopping patience 5 · **full training final = 5 epoch** |
| Grad clip | 1.0 |
| Seed | 42 |
| Model selection | validation Macro F1 (log loss sekunder), tanpa threshold tuning |

**Split** — `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` diurutkan berdasarkan relative official image_id ascending. Fold 0 = development, fold 1–4 = assessment. `fold_assignment_sha256 = 0a06976e5dc3cdb0b3f1f5043ff033bf95a40dd2b0cb82154bbf34d701ee305c`.

**Sharding T4 × 2** — `explicit_contiguous_two_gpu_streamed`: instantiate di `meta`, stream tiap tensor safetensors di CPU, cast FP16, dispatch blok **0–19 → cuda:0**, **20–39 → cuda:1**, final norm di `cuda:1`. Max memory 13 GiB per GPU. **Automatic device map, DataParallel, dan CPU/disk offload dilarang** — audit fail-closed.

**Inference** — 1 pass, argmax atas satu matriks probabilitas. Tanpa hflip, multi-crop, blending, fold/seed ensembling, atau koreksi manual. Reproduction check lulus: `max_abs_probability_difference = 2.98e-08`, prediksi identik, urutan baris identik.

**Environment tervalidasi** — Python 3.12.13 · torch 2.10.0+cu128 · timm 1.0.26 · transformers 4.57.6 · accelerate 1.13.0 · CUDA 12.8 · 2× Tesla T4 (14,56 GiB).

**Signature** — locked contract `e58ab25748ae375018d00602f1e2c86cd6d174bc7453da28ff5b6d5f9ad7d808` · recipe `1ce68a290a451f213a2a0beaff5ec08f354aa80ac031f3d96d892a44894a42bd`.

---

## 7. Diagnosis Bottleneck

**7.1 Error terkonsentrasi di batas Recyclable ↔ Organic**

242 dari 287 error OOF (**84,3%**) adalah R↔O. Electronic sudah hampir saturasi (F1 0.99433, hanya 16 error). Konsekuensi: eksperimen yang mengubah seluruh decision surface berisiko merusak kelas yang sudah selesai — itulah persis yang terjadi pada V8, V10-rich, dan V11.

**7.2 Ada label issue nyata, tapi cleaning saja tidak cukup**

Audit OOF V7: 26 prediksi salah dengan confidence ≥ 0.90 · 79 dengan confidence ≥ 0.80 · 47 dengan margin alternatif ≥ 0.80 · 16 off-diagonal confident-joint · 230 consensus-wrong.

V9 AUDIT menghasilkan 382 kandidat: 2 exact-duplicate conflict (`0_Recyclable/R_799.jpg` dan `2_Organic/O_8873.jpg` — identik tapi beda label, keduanya di-drop), 23 Tier-B untuk review manusia, 357 ambiguous keep. Sepuluh obvious mislabel yang terkonfirmasi visual:

| File | Label folder | Seharusnya | Isi |
|---|---|---|---|
| `0_Recyclable/R_3825.jpg` | 0 | 1 | keyboard |
| `0_Recyclable/R_8295.jpg` | 0 | 1 | laptop |
| `2_Organic/O_7701.jpg` | 2 | 1 | microwave |
| `2_Organic/O_7776.jpg` | 2 | 1 | microwave |
| `0_Recyclable/R_9775.jpg` | 0 | 2 | makanan |
| `0_Recyclable/R_8580.jpg` | 0 | 2 | mi/makanan |
| `2_Organic/O_1949.jpg` | 2 | 0 | teko plastik |
| `2_Organic/O_9175.jpg` | 2 | 0 | buku catatan |
| `2_Organic/O_1807.jpg` | 2 | 0 | botol plastik |
| `2_Organic/O_1978.jpg` | 2 | 0 | amplop kertas |

Namun memperbaiki 16–26 kasus tidak mengubah 285 error menjadi level yang dibutuhkan OOF 0.997. Dan hasil empiris V9: **drop maupun relabel keduanya menurunkan Macro F1** meski log loss membaik.

**7.3 Near-duplicate leakage**

436 grup near-duplicate · 910 file (~3,44% train) · ~742 baris OOF punya near-duplicate yang menyeberang fold · upper-bound inflasi Macro F1 ~0.0007 · 7 grup punya mixed label mencakup 19 file. Grouped validation (`StratifiedGroupKFold`) wajib untuk evaluasi jujur — dan kemungkinan besar **menurunkan** OOF. Itu koreksi pengukuran, bukan regresi.

**7.4 Direct-square 256 berpotensi membuang geometry**

25.256 dari 26.527 gambar punya area < 65.536 px. **Seluruh 241 R/O error V7 berada di kelompok resolusi rendah tersebut.** Aspect ratio ekstrem (>3) punya error rate lebih tinggi. Ini korelasi, bukan kausalitas — tapi DINOv3 resmi menerima input rectangular selama kedua dimensi kelipatan 16, jadi direct-square 256 bukan constraint backbone.

**7.5 Frozen 7B bukan ceiling**

Evidence eksternal (lihat §12): LoRA pada DINOv3-H+ memenangkan MIDOG 2025; LoRA lebih stabil daripada full fine-tuning pada semua skala backbone terutama saat supervisi terbatas; backbone mid-size teradaptasi @512 mengalahkan frozen 7B untuk temuan fine-grained. Domainnya berbeda, jadi angkanya tidak bisa dipindah — nilainya ada pada polanya: **adaptasi dan resolusi bisa lebih penting daripada scale backbone frozen.**

---

## 8. Jalur Mati — Jangan Diulang

Semua sudah diuji atau ditolak berdasarkan hasil OOF, aturan, atau risiko:

**Terbukti gagal secara empiris**

- DINOv3 SAT checkpoint (domain mismatch).
- Scaling backbone di atas ViT-7B.
- V8 binary R/O specialist.
- V9 drop-only cleaning, relabel obvious-mislabel, dan blend 50/50.
- V9A head zoo + pairwise blend.
- V10 rich fixed spatial pooling (17 branch).
- V11 material-query cross-attention.
- `last4_layer_weighted_gated` dan varian dual-branch/cosine — kalah dari final-layer head.
- Hflip TTA: gain hanya ~+0,000089, di bawah threshold 0,0002.
- Calibration scalar: tidak mengubah argmax.
- Simple class bias, confidence switching, probability blend: tidak ada gain stabil.

**Dilarang oleh aturan atau kontrak**

- Pseudo-label test, test distribution tuning, koreksi manual prediksi test.
- Mengubah label validation.
- Mengganti raw official dataset dengan folder cleaned.
- ConvNeXt ensemble untuk submission final.
- Post-hoc class threshold tuning.
- Leaderboard probing berulang.

**Tidak layak biaya**

- Partial unfreezing / LoRA ViT-7B pada T4 × 2.
- Full fine-tuning ViT-7B.
- Head zoo tambahan pada cache global yang sama.
- Sweep hyperparameter besar tanpa gate fold 0.
- Focal loss sebelum label audit (memperbesar bobot hard sample, padahal banyak yang justru mislabeled).
- Filename, urutan, dimensi, atau metadata lain sebagai fitur prediktif — **dilarang juknis**.

---

## 9. Realitas Target 0.997

Pada 26.527 baris, OOF 0.9901 ≈ 287 error. OOF 0.997 butuh turun ke kira-kira **60–100 error**, tergantung arah confusion. Artinya sekitar **dua pertiga sampai empat perlima error harus hilang.**

- Head tuning yang menghasilkan +0,0001 sampai +0,0003 **tidak cukup**.
- Oracle diagnostik DINO + ConvNeXt hanya ~0,993813 — bahkan kombinasi sempurna dua representasi lama belum menyentuh 0,997.
- Label repair membantu objective dan evaluasi, tapi sendirian tidak cukup.

**OOF ≠ leaderboard.** Test hanya 1.458 gambar; Macro F1 0.997 di sana berarti kesalahan single-digit. Hubungan OOF–LB tidak linear pada proyek ini. Benchmark eksternal 0,997311 membuktikan keluarga DINO bisa mencapai level itu di test — tapi angka itu **tidak boleh** dipakai sebagai sinyal model selection.

---

## 10. Rencana yang Tersisa

Rute yang direkomendasikan `plan/`:

```
V11B verified train-label repair
→ honest duplicate-grouped validation
→ material-aware spatial representation
→ LoRA adaptation
→ higher-resolution / aspect-preserving inference
→ satu final model
→ locked test inference
```

| Fase | Isi | Status realistis di sisa waktu |
|---|---|---|
| **V11B** label audit | Review queue P0–P3 (mixed-label duplicate, Confident Learning, consensus error, NN purity), blind manual review 300–500 gambar, cleaned manifest, `StratifiedGroupKFold`, protocol-matched V10 control | Versi minimum saja: 19 file mixed-label duplicate + seluruh consensus high-confidence error + P0. Sisanya `unreviewed`, **tanpa auto-relabel**. |
| **V12A** Gram/prototype head | Second-order pooling dari cache spatial `[N, 64, 512]` | Butuh cache V11 yang tersedia; cache-only, murah |
| **V12B** rectangular geometry | Aspect-preserving, sisi panjang 320/384, kelipatan 16 | Mahal (re-extract ViT-7B); gate ketat |
| **V13** LoRA | ViT-L, LoRA r8 α16 dropout 0.05 pada Q/V | **Notebook V12 sudah siap dan sudah mencakup ini** |

**Protokol review manual (blind, wajib):** tampilkan gambar dulu → reviewer memilih `Recyclable`/`Electronic`/`Organic`/`Ambiguous` → **baru** tampilkan label folder dan prediksi model → relabel hanya bila keputusan visual jelas → `Ambiguous` tidak dipaksa jadi kelas alternatif. Manifest menyimpan `original_label`, `review_label`, `review_status`, `review_reason`, `reviewer`, `review_timestamp`, `source_queue_tier`.

**Gate adopsi standar proyek:**

- Gain full OOF Macro F1 minimal **+0,0003** (untuk perubahan besar/PEFT: +0,0010 di fold 0).
- Total error **dan** R/O error sama-sama turun.
- Menang minimal 3 dari 4 confirmation fold.
- Electronic F1 tidak turun lebih dari 0,0005.
- Stabil lintas seed (42, 314, 2026).
- Gain tidak bergantung pada satu sampel atau satu fold.

**Hierarki keputusan:** integrity gate → data alignment → leakage → full OOF Macro F1 → R/O error → stabilitas per kelas → konsistensi per fold → konsistensi per seed → log loss/kalibrasi → runtime. Kandidat dengan Macro F1 lebih tinggi **tetap ditolak** bila ada duplicate leakage, gain hanya di satu fold, Electronic rusak, config tidak reproducible, ada keputusan turunan-test, atau inference butuh ensemble.

**Rencana submission**

- Submission 1 & 2 (sudah dipakai): ConvNeXt relabel ~98,0473, plus satu percobaan lain.
- **Sisa 1.** Satu-satunya kesempatan tersisa harus dipakai untuk model terkuat yang lolos seluruh gate, dipilih berdasarkan OOF + robustness, **bukan** leaderboard probing.
- Karena tinggal satu, submission wajib murni dari pipeline reproducible: satu checkpoint, satu forward pass, satu argmax, tanpa koreksi manual apa pun.
- Jangan submit dua config yang hanya berbeda seed tanpa evidence.

---

## 11. Peta Artifact

```
waste-classification-dinov3/
├── Petunjuk_Teknis_BDC_Satria_Data_2026.md   juknis resmi
├── CONTEXT.md                                dokumen ini
├── data/                                     (gitignored)
│   ├── train/{0_Recyclable,1_Electronic,2_Organic}/
│   ├── test/                                 1.458 gambar
│   └── submission.csv                        template resmi
├── scripts/                                  notebook V1–V12
├── results/                                  artifact eksperimen
├── plan/                                     roadmap + execution plan
├── sum/                                      handoff chat (BASI — lihat §13)
└── ref/{code,papers}/                        referensi
```

**`scripts/`**

| Notebook | Isi |
|---|---|
| `baseline-v1-convnext.ipynb` | baseline ConvNeXt |
| `experiment-v2-maxvit.ipynb` | MaxViT |
| `v3-convnext.ipynb`, `v4-freeze-convnext.ipynb` | iterasi ConvNeXt |
| `v5-dinov3-frozen-raw.ipynb` | ViT-L frozen |
| `v6-dinov3-vithplus-frozen-raw.ipynb` | ViT-H+ frozen |
| `v7-dinov3-vit7b-frozen-raw.ipynb` | **ViT-7B frozen, fondasi champion** |
| `v8-dinov3-vit7b-frozen-cache-upgrade.ipynb` | R/O specialist (ditolak) |
| `v9-dinov3-vit7b-frozen-audited-cleaning.ipynb` | audit cleaning |
| `v9-dinov3-vit7b-frozen-drop-vs-relabel-v2.ipynb` | drop vs relabel (ditolak) |
| `cari-task-head.ipynb` | head zoo (V9A) |
| `v10-dinov3-vit7b-timm-rich-spatial-end-to-end.ipynb` | **champion end-to-end** |
| `v11-dinov3-vit7b-material-aware-patch-attention.ipynb` | material-query attention (ditolak) |
| `v12-dinov3-vitl-lora-material-adaptation-READY-...ipynb` | **ViT-L LoRA, siap jalan** |

**`results/`**

| Folder | Isi |
|---|---|
| `v7_analysis_bundle/` | OOF, per-fold, classification report, high-confidence errors, galeri R/O, fold assignments, cache manifest, audit model & preprocessing |
| `v8_analysis_bundle/` | bukti hasil negatif specialist + `heads/` |
| `v9_analysis_bundle/` | audit cleaning, ranking kandidat, contact sheet Tier A/B/C |
| `v9_dinov3_vit7b_frozen_drop_vs_relabel/` | perbandingan C0–C3, paired error delta, decision |
| `v9a_v7_cached_head_zoo/` | ~30 varian head, leaderboard, `final_train_only_decision.json`, `models/`, `predictions/` |
| `v10_dinov3_vit7b_timm_rich_spatial/` | **champion**: `final_head.pt`, OOF prob/pred, locked contract, data contract, manifest model/test/repro, error analysis, `figures/` |

**Cache & path Kaggle**

- Feature cache V7: `v7_dinov3_vit7b_frozen_raw/feature_cache/shards` — **104 shard**, total shape `(26527, 2, 4096)`, FP16. **Jangan dihapus.**
- Cache V11: global `[26.527, 8.192]` + spatial `[26.527, 64, 512]`.
- `/kaggle/input/datasets/riantamaputra/v7-results/v7_dinov3_vit7b_frozen_raw`
- `/kaggle/input/datasets/riantamaputra/v8-results/v8_dinov3_vit7b_frozen_cache_upgrade`
- `/kaggle/input/datasets/riantamaputra/v9-audit-reviewed-drop-vs-relabel/v9_dinov3_vit7b_frozen_audited_cleaning`
- `/kaggle/input/datasets/riantamaputra/bdc-2026-waste-classification-dataset/submission.csv`

**Throughput V7:** ~3,91 image/s → ekstraksi fitur train penuh ~1,88 jam.

**`ref/code/`** — `best-public-findit-dinov2-v0.ipynb`, `findit-v17.ipynb`, `ver34_clean_end_to_end.ipynb` (template notebook end-to-end yang jadi acuan struktur), `image_classification_dinov3_template.ipynb`, `deduplicate.py`, `relabel.py`, `preprocess_dataset_v1.py`, `raw_duplicates.py`, materi pelatihan Gemastik.

---

## 12. Referensi

**`ref/papers/`**

| File | Judul |
|---|---|
| `2508.10104v1.md` | DINOv3 (Siméoni, Vo, Seitzer, Baldassarre, Oquab, et al.) |
| `2508.21041v3.md` | Efficient Fine-Tuning of DINOv3 — pemenang MIDOG 2025 Task 2 |
| `2604.16083v1.md` | DINOv3 Beats Specialized Detectors: Foundation Model Baseline for Image Forensics |
| `2601.08078v1.md` | DINOv3-Based Self-Supervised Features for Robust Few-Shot Medical Image Segmentation |
| `2602.07550v1.md` | Revealing the Semantic Selection Gap in DINOv3 (FSSDINO — prototype + Gram) |
| `2603.28297v1.md` | DinoDental: Benchmarking DINOv3 as a Unified Vision Encoder |
| `2605.07221v1.md` | DINO-MVR: Multi-View Readout of Frozen DINOv3 |
| `2604.09697v1.md` | I Can't Believe TTA Is Not Better: When Test-Time Augmentation Hurts |
| `2606.25784v1.md` | S2-FracMix: Label-Preserving Self-Saliency Mixup Augmentation |
| `2505.16513v1.md` | (tanpa judul terbaca di ekstraksi) |
| `A_Review_of_Computer_Vision_for_Industrial-Grade_Waste_Classification.md` | IEEE Access 2025, DOI 10.1109/ACCESS.2025.3603903 |

**Tautan eksternal kunci**

- [DINOv3 paper](https://arxiv.org/abs/2508.10104) · [DINOv3 model card](https://github.com/facebookresearch/dinov3/blob/main/MODEL_CARD.md)
- [Efficient Fine-Tuning of DINOv3](https://arxiv.org/html/2508.21041v3) · [DINOv3 LoRA for image forensics](https://arxiv.org/html/2604.16083v1)
- [Resolution scaling for DINOv3 transfer](https://arxiv.org/abs/2510.07191)
- [Confident Learning](https://arxiv.org/abs/1911.00068) · [MIT Data-Centric AI: label errors](https://dcai.csail.mit.edu/2024/label-errors/)
- [Area Under the Margin (AUM)](https://proceedings.neurips.cc/paper/2020/file/c6102b3727b2a7d8b1bb6981147081ef-Paper.pdf)
- [Early-Learning Regularization](https://proceedings.neurips.cc/paper/2020/hash/ea89621bee7c88b2c5be6681c8ef4906-Abstract.html)
- [Bilinear CNN for fine-grained recognition](https://openaccess.thecvf.com/content_iccv_2015/papers/Lin_Bilinear_CNN_Models_ICCV_2015_paper.pdf)
- [mxslr/mlcraft](https://github.com/mxslr/mlcraft)

---

## 13. Catatan Rekonsiliasi

Bagian ini mencatat di mana dokumen lama bertentangan dengan artifact.

**13.1 `sum/satdat_chat_handoff_full` == `sum/satdat_chat_handoff_full2`**

Byte-identical (diverifikasi `diff -r`). Bukan dua versi — satu duplikat. Baca salah satu saja.

**13.2 Handoff mendefinisikan V10 sebagai eksperimen yang berbeda**

`sum/satdat_chat_handoff_full2` §7 menyebut *"V10 multi-seed ensemble pada V7 original, seeds 42/2026/3407"* sebagai next experiment. **Itu tidak pernah terjadi.** V10 yang benar-benar dijalankan adalah `v10_dinov3_vit7b_timm_rich_spatial` — pindah backend ke timm plus screen 17-branch rich spatial pooling. Multi-seed ensemble juga akan melanggar single-model contract yang dikunci kemudian. **Abaikan §7 handoff itu.**

**13.3 Penomoran "V11A.1 / V11A.2" di `plan/` tidak cocok dengan `scripts/`**

Kedua dokumen `plan/` menulis V11A.1 `material_frozen_global` = 0.990275 (285 error, 242 R/O) dan V11A.2 dengan empat kandidat `lr4e4_plain` / `lr2e4_plain` / `lr4e4_roaux` / `lr4e4_roaux_reg`. Angka-angka itu **direkonstruksi dari percakapan, bukan dari artifact** (`plan/...EXECUTION_PLAN...` §3.2 dan §3.3 mengakuinya secara eksplisit: "belum tersedia di arsip lokal"). Satu-satunya notebook V11 yang ada di repo adalah material-query patch attention, sudah dijalankan, dan **ditolak di ~0.983106** — jauh di bawah kontrol. Tidak ada folder `results/v11_*`.

**13.4 `sum/SATDAT_CHAT_HANDOFF_2026-07-26` adalah era ViT-L**

Handoff itu masih menempatkan ViT-L frozen (`mlp_concat_weighted_ce`, OOF 0.986149) sebagai baseline dan membahas ConvNeXt. Sudah dua generasi tertinggal. Nilainya hanya sebagai riwayat ConvNeXt, manual-review queue (174/729), dan pencatatan aturan.

**13.5 V7 vs V10 bukan perbandingan protocol-matched**

`error_analysis.json` V10 mencatatnya sendiri: angka V7 berasal dari backend Transformers dan cache CLS + patch-mean; V10 memakai timm. Fold dan label sama, tapi ini konteks proyek, **bukan perbandingan kausal**. Selisih +0,00003 antara keduanya tidak bermakna.

**13.6 Yang wajib dibawa ke sesi berikutnya**

1. Champion = V10 `timm_control`, OOF 0.9901662323927614, checkpoint di `results/v10_dinov3_vit7b_timm_rich_spatial/final_head.pt`.
2. Deadline 30 Juli 2026 16.00 WIB, 2 submission tersisa.
3. Single-model contract adalah keputusan tim, bukan aturan panitia (§4).
4. V8, V9, V9A, V10-rich, V11 semuanya sudah ditolak — jangan diulang (§8).
5. V13 (resampling model-native) siap jalan. V12 (ViT-L LoRA @320) ditunda — lihat §14.
6. 84% error ada di batas R↔O; Electronic sudah selesai.
7. Submission tersisa **1**, bukan 2.

---

## 14. Audit V12 dan alasan V13 didahulukan

Ditulis 29 Juli 2026, sebelum V13 dijalankan. Tidak ada angka baru di sini — semuanya pembacaan notebook dan aritmetika anggaran waktu.

### 14.1 Notebook V12 melanggar single-model contract

`scripts/v12-...-CUDA-FORK-FIXED.ipynb` §17 melakukan inferensi test **lima kali**, satu per fold, lalu:

```python
average = normalize_probabilities(np.mean(fold_probabilities, axis=0))
```

Submission dibuat dari `average` itu. Itu **fold ensembling**, yang dilarang eksplisit oleh §4 dan oleh `results/v10_.../locked_contract.json` → `single_model_contract.fold_ensembling: false`. Notebook juga mencatat sendiri `"fold_probability_average": 5` di blok kontraknya. Jadi V12 tidak bisa dipakai apa adanya untuk submission final tanpa diubah menjadi satu model penuh-data.

### 14.2 V12 tidak bisa lolos gate adopsi di sisa waktu

Anggaran V12: ViT-L @ 320px (405 token), LoRA r8, microbatch 2/GPU × grad-accum 4, maks 8 epoch, 5 fold. Estimasi ± 2–4 jam per fold di T4 × 2 → **10–20 jam untuk lima fold**, di luar unduh model dan ekstraksi test. Batas sesi Kaggle 12 jam, dan sisa waktu < 1,5 hari.

Konsekuensinya bukan sekadar "lambat": gate proyek mensyaratkan **menang ≥ 3 dari 4 confirmation fold**. Screen fold 0 saja tidak pernah cukup untuk adopsi. Jadi walaupun fold 0 menang besar, V12 **tetap tidak bisa diadopsi secara sah** sebelum deadline — menjalankannya tidak dapat mengubah isi submission terakhir. Itu argumen penentu, bukan sekadar soal jam.

V12 tetap disimpan. Kalau ada perpanjangan waktu atau kompetisi berikutnya, perbaiki §17-nya jadi satu model penuh-data lebih dulu.

### 14.3 Mengapa V13 (bicubic) yang dijalankan

Dipilih karena ia satu-satunya kandidat yang **muat penuh** — ekstraksi, lima fold, gate, dan submission — dalam satu sesi ± 4,5 jam:

- **Confound terdokumentasi, belum pernah diuji.** `data_contract.json` V10 menyebutnya sendiri sebagai `documented_future_ablation`. timm me-*resolve* bicubic; V7/V10 memakai bilinear.
- **Mekanismenya cocok dengan bottleneck.** 25.256 / 26.527 citra (95,2%) di-*upsample* ke 256×256. Pada *upsampling*, `antialias` tidak berpengaruh, jadi bilinear vs bicubic murni selisih kernel — dan bilinear membuang frekuensi tinggi. Seluruh 241 error R/O V7 ada di kelompok resolusi rendah itu (§7.4). Batas R↔O adalah keputusan tekstur.
- **Perbandingan benar-benar protocol-matched.** Kontrol bilinear diekstraksi ulang di sesi yang sama, sehingga cacat §13.5 (V7 vs V10 tidak apple-to-apple) hilang; kontrol itu sekaligus jadi uji regresi terhadap angka champion 0.9901662323927614.
- **Satu perubahan.** Geometri, readout, head, fold, seed, dan optimizer identik.

### 14.4 Yang sengaja tidak dijadikan bagian V13

- **Geometri crop-pct timm** (resize sisi pendek lalu center-crop): membuang konten tepi, dan menggabungnya dengan perubahan kernel = dua perubahan.
- **Aspect-preserving / letterbox**: butuh masking patch padding pada `patch_mean`, jadi dua perubahan.
- **Resolusi 320/384**: 95% citra sudah di-*upsample* pada 256, jadi menaikkan resolusi menambah token tanpa menambah informasi. Ini juga melemahkan premis V12B di §10.
- **Augmentasi**: belum pernah dipakai sepanjang V1–V13. Pada frozen-cache probe, gain-nya kecil; nilainya baru muncul kalau backbone diadaptasi (bukti MIDOG 2025: LoRA + augmentasi berat, bukan LoRA saja). Catat sebagai jalur untuk kompetisi berikutnya.

### 14.5 Konteks leaderboard yang perlu diingat saat membaca hasil

Snapshot skor hampir linier terhadap jumlah error pada 1.458 citra: ≈ `100 − 0,0538 × k`. Jadi rank 1–3 = **0 error**, rank 4–5 = 1, rank 6 = 2, rank 15 = 5, rank 20 = **7 error**. Error rate OOF champion 1,082% memproyeksikan ± 16 error di test.

Artinya target top-20 menuntut error rate ± 0,48% — kira-kira **separuh** error saat ini. Tidak ada kandidat tersisa yang realistis mencapai itu dalam < 1,5 hari. Tujuan yang jujur untuk submission terakhir adalah **memaksimalkan kekuatan model tunggal terbaik**, bukan mengejar 0,997.
