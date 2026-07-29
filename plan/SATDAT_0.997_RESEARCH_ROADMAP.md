# Research Roadmap BDC Satria Data 2026

## Jalur yang paling masuk akal untuk mendekati skor 0.997

Tanggal analisis: 29 Juli 2026  
Target: klasifikasi citra 3 kelas dengan Macro F1  
Constraint: train-only research, single final model, tanpa label test, tanpa external labeled data, tanpa auto-relabel

## Kesimpulan utama

Target 0.997 tidak akan tercapai hanya dengan menambah head baru di atas cache DINOv3 ViT-7B yang sama. Evidence project menunjukkan head-only improvement sudah masuk fase diminishing returns:

- V7 frozen ViT-7B full OOF berada di sekitar 0.9901.
- V10 historical champion berada di 0.990166.
- V11A.1 `material_frozen_global` naik menjadi 0.990275, hanya +0.000109 atas V10.
- V11A.1 masih membuat 285 error, dengan 242 error Recyclable dan Organic.
- Oracle diagnostik DINO dan ConvNeXt hanya sekitar 0.993813. Bahkan kombinasi dua pola representasi lama belum cukup untuk menyentuh 0.997.

Jalur yang layak dikejar terdiri dari tiga intervensi:

1. memperbaiki label train yang benar-benar salah melalui audit visual manual berbasis train-only OOF;
2. memperbaiki representasi material melalui geometry, resolution, dan spatial token statistics;
3. mengadaptasi backbone dengan LoRA, bukan terus memperbesar head frozen.

Target 0.997 tetap ambisius dan tidak bisa dijamin. Skor leaderboard 0.997 juga berbeda dari OOF 0.997. Pada 1.458 citra test, Macro F1 0.997 berada pada level single-digit mistakes, tergantung distribusi serta arah error antar-kelas. OOF dan leaderboard tidak memiliki hubungan linear pada project ini.

## 1. Grounding kondisi project

### Dataset dan evaluasi

| Komponen | Kondisi terkunci |
|---|---:|
| Train | 26.527 gambar |
| Recyclable | 9.999 |
| Electronic | 3.961 |
| Organic | 12.567 |
| Test | 1.458 gambar tanpa label |
| Headline metric | Macro F1 |
| Development policy | Train-only cross-validation |
| Final inference | Satu model |

Aturan resmi melarang penggunaan test untuk training, validation, model selection, atau hyperparameter tuning. Prediksi test juga harus dibuat otomatis. Manual test labels tetap dikarantina dan tidak digunakan dalam analisis ini.

### Riwayat performa yang relevan

| Versi | Perubahan utama | Hasil | Keputusan |
|---|---|---:|---|
| V5 | DINOv3 ViT-L frozen | full OOF 0.986149 | baseline lama |
| V6 | DINOv3 ViT-H+ frozen | fold 0 0.985188 | scale tanpa adaptation tidak membantu |
| V7 | DINOv3 ViT-7B frozen | fold 0 0.989918, folds 1-4 0.990191 | backbone frozen utama |
| V10 | frozen ViT-7B upgrade | historical full OOF 0.990166 | current primary |
| V11A.1 | spatial material branch | 0.990275, 285 errors, 242 R/O | signal ada, gain belum stabil |
| V11A.2 | material stabilization | belum ada hasil final | eksperimen aktif berikutnya |

V11A.2 sudah memiliki empat kandidat:

- `lr4e4_plain`
- `lr2e4_plain`
- `lr4e4_roaux`
- `lr4e4_roaux_reg`

Adoption gate yang sudah dikunci:

- full OOF gain minimal 0.0003;
- total error dan R/O error turun;
- menang minimal pada 3 dari 4 confirmation folds;
- stabil pada seed 42, 314, dan 2026.

## 2. Diagnosis bottleneck berdasarkan artifact project

### 2.1 Error terkonsentrasi pada batas Recyclable dan Organic

Rekonstruksi V7 full OOF menghasilkan:

| Error type | Jumlah |
|---|---:|
| Total error | 287 |
| R/O error | 241 |
| Error lain | 46 |

Sekitar 84% error berasal dari pasangan Recyclable dan Organic. Electronic sudah cukup kuat, sehingga eksperimen yang mengubah seluruh decision surface memiliki risiko merusak kelas yang sudah selesai.

### 2.2 Ada label issue nyata, tetapi cleaning saja belum cukup

Audit OOF V7 menunjukkan:

| Sinyal audit | Jumlah |
|---|---:|
| Prediksi salah dengan confidence ≥ 0.90 | 26 |
| Prediksi salah dengan confidence ≥ 0.80 | 79 |
| Alternative-minus-given probability margin ≥ 0.80 | 47 |
| Simplified confident-joint off-diagonal | 16 |

Galeri error ber-confidence tinggi memuat beberapa citra yang secara visual tampak bertentangan dengan folder label. Contohnya mencakup makanan yang diberi label Recyclable serta wadah plastik yang diberi label Organic. Ini cukup kuat untuk membuka kembali manual train review.

Namun, memperbaiki 16 sampai 26 kasus tidak akan mengubah 285 error menjadi level yang dibutuhkan oleh OOF 0.997. Cleaning harus dipakai untuk menghapus noise dari objective dan validation, lalu diikuti model yang mampu mempelajari material cues lebih baik.

Confident Learning memang dirancang untuk menemukan label error menggunakan out-of-sample probabilities dan noisy labels, tepat seperti OOF yang sudah tersedia. Metode ini berguna untuk ranking kandidat review, bukan sebagai izin auto-relabel. [Confident Learning paper](https://arxiv.org/abs/1911.00068), [MIT Data-Centric AI explanation](https://dcai.csail.mit.edu/2024/label-errors/)

AUM memberi sinyal tambahan melalui training dynamics. Sampel mislabeled cenderung memiliki assigned-class margin yang rendah secara konsisten sepanjang training. [AUM paper](https://proceedings.neurips.cc/paper/2020/file/c6102b3727b2a7d8b1bb6981147081ef-Paper.pdf)

### 2.3 Duplicate leakage ada, tetapi bukan penjelasan utama

Audit terdahulu menemukan:

- 436 grup near-duplicate;
- 910 file, sekitar 3,44% train;
- sekitar 742 baris OOF memiliki near-duplicate yang menyeberang fold;
- upper-bound inflasi Macro F1 sekitar 0.0007;
- 7 grup near-duplicate memiliki mixed labels, mencakup 19 file.

Jadi duplicate grouping tetap wajib untuk evaluasi jujur, tetapi memperbaikinya kemungkinan menurunkan OOF sebelum model membaik. Itu bukan regression, melainkan koreksi measurement.

### 2.4 Direct-square preprocessing berpotensi membuang material geometry

V7 mengubah setiap gambar langsung menjadi 256 × 256. Sebagian besar data sumber beresolusi rendah dan banyak gambar memiliki aspect ratio non-square.

Analisis dimensi menunjukkan:

- 25.256 dari 26.527 gambar memiliki area di bawah 65.536 pixel;
- seluruh 241 R/O error V7 berada pada kelompok sumber beresolusi rendah tersebut;
- extreme aspect ratio di atas 3 memiliki error rate lebih tinggi, walau jumlah sampelnya kecil.

Ini korelasi, bukan bukti kausal. Namun DINOv3 resmi menerima gambar yang lebih besar dan rectangular selama kedua dimensi merupakan kelipatan patch size 16. Jadi direct-square 256 bukan constraint dari backbone. [DINOv3 model card](https://github.com/facebookresearch/dinov3/blob/main/MODEL_CARD.md)

### 2.5 Frozen 7B bukan ceiling representasi

Evidence eksternal paling relevan:

- DINOv3-H+ dengan LoRA rank 8 pada Q/V attention, sekitar 1,3 juta trainable parameters, memenangkan MIDOG 2025 Task 2. [Efficient Fine-Tuning of DINOv3](https://arxiv.org/html/2508.21041v3)
- Studi DINOv3 image forensics menemukan LoRA lebih stabil dan lebih kuat daripada full fine-tuning pada seluruh backbone scale yang diuji, terutama ketika supervision terbatas. [DINOv3 LoRA for image forensics](https://arxiv.org/html/2604.16083v1)
- Benchmark resolusi DINOv3 menemukan adapted mid-sized backbones pada 512 × 512 lebih kuat daripada frozen 7B features untuk fine-grained findings. Gain terbesar muncul pada cues kecil dan boundary-dependent. [Resolution scaling for DINOv3 transfer](https://arxiv.org/abs/2510.07191)

Paper-paper tersebut menggunakan domain lain, sehingga angkanya tidak boleh dipindahkan langsung ke waste classification. Nilai utamanya adalah pola yang konsisten: adaptation dan resolution dapat lebih penting daripada model scale frozen.

## 3. Mengapa target 0.997 sangat berat

Pada full OOF sekarang, 0.9901 setara dengan sekitar 285 sampai 287 error. Dengan class counts project dan error yang didominasi R/O, OOF 0.997 memerlukan penurunan ke kira-kira 60 sampai 100 total error, tergantung arah confusion.

Artinya kita harus menghilangkan sekitar dua pertiga sampai empat perlima error yang tersisa. Head tuning dengan gain +0.0001 sampai +0.0003 tidak cukup.

Target leaderboard 0.997 lebih mungkin daripada OOF 0.997 karena test hanya 1.458 gambar dan mungkin lebih mudah daripada cross-validation train. Benchmark eksternal 0.997311 menunjukkan keluarga DINO dapat mencapai level itu pada test, tetapi benchmark tersebut tidak boleh dipakai sebagai model-selection signal.

## 4. Roadmap eksperimen yang direkomendasikan

### Phase A. Selesaikan V11A.2 dan pakai hasilnya untuk audit

Jalankan V11A.2 terlebih dahulu karena:

- cache sudah tersedia;
- tidak perlu DINOv3 forward;
- murah;
- tiga seed menghasilkan evidence stabilitas yang berguna untuk label audit.

Jika V11A.2 gagal gate, jangan menambah varian LR, dropout, atau auxiliary-loss lain. Catat material head stabilization sebagai exhausted path.

### Phase B. V11B Train-Only Label Repair

Ini prioritas tertinggi setelah V11A.2.

#### B.1 Buat review queue berbasis intersection, bukan arbitrary weighted score

Tier kandidat:

| Tier | Kriteria |
|---|---|
| P0 | mixed-label exact/near-duplicate, atau seluruh seed dan model menyetujui alternate class dengan margin tinggi |
| P1 | Confident Learning flagged, minimal dua model families menyetujui alternate class, dan error stabil lintas seed |
| P2 | current champion error dengan R/O confusion, lalu diurutkan berdasarkan assigned-label probability terendah |
| P3 | nearest neighbors memiliki label cluster yang konsisten tetapi label query berbeda |

Review dimulai dari seluruh error V10/V11, 19 file mixed-label near-duplicate, lalu kandidat nearest-neighbor conflict. Target awal yang masuk akal adalah 300 sampai 500 gambar train.

#### B.2 Protokol manual review

Reviewer tidak boleh melihat label test. Untuk mengurangi confirmation bias:

1. tampilkan gambar terlebih dahulu;
2. reviewer memilih `Recyclable`, `Electronic`, `Organic`, atau `Ambiguous`;
3. folder label dan model prediction baru ditampilkan setelah keputusan;
4. relabel hanya jika keputusan visual jelas;
5. `Ambiguous` tidak dipaksa menjadi alternate label.

Manifest final perlu menyimpan:

- `original_label`
- `review_label`
- `review_status`
- `review_reason`
- `reviewer`
- `review_timestamp`
- `source_queue_tier`

Tidak ada auto-relabel.

#### B.3 Rebuild evaluation setelah cleaning

OOF lama tidak lagi valid setelah label berubah. Langkah berikutnya:

1. buat duplicate-cluster group id;
2. gunakan StratifiedGroupKFold;
3. lock manifest cleaned;
4. jalankan exact V10 control pada split baru;
5. bandingkan raw vs cleaned pada split dan protocol yang sama.

Gate data repair:

- tidak ada duplicate cluster menyeberang fold;
- minimal 70% kandidat P0/P1 yang direview memang terkonfirmasi mislabeled atau ambiguous;
- cleaned control menurunkan R/O error pada minimal 4 dari 5 folds;
- tidak ada penurunan Electronic F1 lebih dari 0.0005.

### Phase C. V12 Frozen Geometry and Second-Order Readout

Phase ini masih single-backbone dan dapat dijalankan sebelum PEFT mahal.

#### C.1 V12A Spatial Gram and prototype head

Gunakan cache spatial V11 `[N, 64, 512]`.

Representasi candidate:

- global frozen feature lama;
- projected patch mean;
- projected patch covariance atau compact Gram descriptor;
- class prototypes untuk R/O;
- satu classifier final.

Alasannya:

- mean pooling hanya menangkap first-order statistics;
- covariance atau Gram menangkap hubungan antar-patch yang relevan untuk texture dan material;
- DINOv3 sendiri menggunakan Gram anchoring untuk menjaga dense feature structure;
- prototype + Gram memberikan gain konsisten pada frozen DINOv3 few-shot segmentation, walau task-nya berbeda. [FSSDINO paper](https://arxiv.org/html/2602.07550v1)
- second-order pooling telah lama kuat untuk fine-grained recognition. [Bilinear CNN paper](https://openaccess.thecvf.com/content_iccv_2015/papers/Lin_Bilinear_CNN_Models_ICCV_2015_paper.pdf)

Gate V12A:

- full OOF gain minimal 0.0003;
- menang minimal 3 dari 4 confirmation folds;
- R/O error turun;
- seed standard deviation tidak lebih buruk dari V11A.2.

#### C.2 V12B Aspect-preserving rectangular cache

Bandingkan dengan direct-square 256 menggunakan backbone dan head yang sama.

Candidate preprocessing:

- EXIF transpose dan RGB conversion tetap;
- resize aspect-preserving;
- kedua dimensi dibulatkan ke kelipatan 16;
- tanpa metadata sebagai predictive feature;
- pooling tetap bekerja untuk token grid rectangular.

Mulai dengan long side 320 atau 384. Jangan langsung 512 pada ViT-7B sebelum throughput dan memory smoke test.

Gate V12B:

- fold-0 Macro F1 naik minimal 0.0010 pada dua seed;
- R/O error turun minimal 10%;
- extreme-aspect subset tidak memburuk;
- estimasi full extraction masih muat dalam budget Kaggle.

#### C.3 V12C Same-model global plus salient crop

Jika rectangular input membantu tetapi masih mentok, gunakan patch-token saliency dari forward pertama untuk membuat deterministic foreground crop, lalu forward crop dengan backbone yang sama.

Ini tetap satu set backbone weights. Global dan crop embeddings digabung oleh satu classifier. Crop policy wajib dikunci dari train validation dan tidak boleh berubah setelah melihat test.

### Phase D. V13 Parameter-Efficient Backbone Adaptation

Ini kandidat dengan upside terbesar.

#### D.1 Causal PEFT screen

Mulai dari DINOv3 ViT-L:

| Candidate | Geometry | Adaptation |
|---|---|---|
| control | direct-square 256 | frozen |
| LoRA-256 | direct-square 256 | Q/V LoRA |
| LoRA-384 | aspect-preserving 384 | dijalankan hanya jika LoRA-256 lolos |

Konfigurasi awal berbasis paper MIDOG:

- LoRA rank 8;
- alpha 16;
- dropout 0.05;
- target Q dan V projections;
- AdamW;
- base LR 1e-4;
- weight decay 0.1;
- cosine schedule;
- warmup 10%;
- gradient clip 1.0;
- mixed precision;
- gradient checkpointing;
- head dropout 0.2.

Jangan langsung full fine-tune. Pada data terbatas, evidence DINOv3 terbaru menunjukkan full fine-tuning lebih mudah collapse atau overwrite pretrained representations.

#### D.2 Loss setelah label repair

Urutan ablation:

1. weighted CE control;
2. CE + R/O supervised contrastive auxiliary;
3. ELR jika training dynamics masih menunjukkan memorization.

Focal loss belum menjadi prioritas. Focal loss memperbesar kontribusi hard samples, sedangkan sebelum cleaning hard samples project banyak yang justru mislabeled atau ambiguous.

ELR dirancang untuk mencegah model memasuki fase memorization pada noisy labels. [Early-Learning Regularization paper](https://proceedings.neurips.cc/paper/2020/hash/ea89621bee7c88b2c5be6681c8ef4906-Abstract.html)

#### D.3 Major-experiment gate

PEFT layak full 5-fold jika:

- fold-0 gain minimal 0.0010 atas protocol-matched control;
- gain muncul pada dua seed;
- total error dan R/O error sama-sama turun;
- Electronic F1 tidak turun lebih dari 0.0005;
- log loss membaik atau tidak memburuk drastis.

Adopt sebagai champion jika full OOF:

- naik minimal 0.0008;
- menang minimal 4 dari 5 folds;
- duplicate-grouped validation tetap lolos;
- tidak bergantung pada satu confidence threshold yang dituning secara post-hoc.

## 5. Priority matrix

| Priority | Experiment | Expected upside | Cost | Keputusan |
|---:|---|---|---|---|
| 1 | Jalankan V11A.2 | rendah | sangat rendah | selesaikan karena sudah aktif |
| 2 | Manual train-label audit | tinggi | medium | wajib untuk target ekstrem |
| 3 | Grouped clean-control OOF | measurement-critical | medium | wajib sebelum model besar |
| 4 | Spatial Gram/prototype head | rendah sampai medium | rendah | manfaatkan cache V11 |
| 5 | Rectangular aspect-preserving cache | medium | tinggi | perubahan representation geometry |
| 6 | ViT-L LoRA 256 | tinggi | tinggi | causal adaptation test |
| 7 | ViT-L LoRA 384/512 | tinggi | sangat tinggi | hanya setelah LoRA-256 lolos |
| 8 | Same-model salient crop | medium sampai tinggi | sangat tinggi | fallback setelah geometry screen |
| 9 | ViT-7B LoRA | tidak pasti | ekstrem | bukan eksperimen awal |

## 6. Jalur yang sebaiknya dihentikan

- head zoo tambahan pada global cache yang sama;
- calibration-only untuk mengejar argmax Macro F1;
- hflip TTA tanpa gain OOF yang jelas;
- auto-relabel berdasarkan confidence;
- test-derived pseudo-label, test distribution tuning, atau manual test correction;
- ConvNeXt ensemble untuk final submission;
- full fine-tuning ViT-7B sebagai eksperimen pertama;
- focal loss sebelum label audit;
- hyperparameter sweep besar pada fold 0;
- penggunaan filename, urutan, dimensi, atau metadata lain sebagai predictive feature.

## 7. Urutan kerja yang direkomendasikan

1. Run V11A.2 dan simpan seluruh OOF probability per seed.
2. Bangun V11B review queue dari V7, V10, V11A.2, duplicate conflicts, dan nearest-neighbor label purity.
3. Review manual 300 sampai 500 gambar train, tanpa auto-relabel.
4. Lock cleaned manifest dan duplicate group id.
5. Re-run exact V10 control dengan StratifiedGroupKFold.
6. Jalankan V12A Gram/prototype head pada spatial cache.
7. Jalankan V12B rectangular aspect-preserving extraction.
8. Jika geometry gain nyata, jalankan ViT-L LoRA-256 sebagai causal PEFT test.
9. Naik ke LoRA-384 atau 512 hanya setelah LoRA-256 lolos.
10. Submit hanya kandidat yang menang lintas fold dan seed. Leaderboard tidak dipakai sebagai debugger.

## Bottom line

Rute paling masuk akal menuju 0.997 bukan mencari satu head ajaib. Project perlu:

`verified train-label repair → honest grouped validation → material-aware spatial representation → LoRA adaptation → higher-resolution or aspect-preserving inference`

V11A.2 tetap perlu diselesaikan, tetapi posisinya adalah stabilization checkpoint. Lompatan berikutnya harus datang dari data quality dan backbone adaptation.

## Referensi utama

1. [mxslr/mlcraft](https://github.com/mxslr/mlcraft)
2. [DINOv3 paper](https://arxiv.org/abs/2508.10104)
3. [DINOv3 model card](https://github.com/facebookresearch/dinov3/blob/main/MODEL_CARD.md)
4. [Efficient Fine-Tuning of DINOv3, MIDOG 2025 winner](https://arxiv.org/html/2508.21041v3)
5. [DINOv3 LoRA for image forensics](https://arxiv.org/html/2604.16083v1)
6. [Resolution scaling for DINOv3 transfer](https://arxiv.org/abs/2510.07191)
7. [Confident Learning](https://arxiv.org/abs/1911.00068)
8. [Area Under the Margin](https://proceedings.neurips.cc/paper/2020/file/c6102b3727b2a7d8b1bb6981147081ef-Paper.pdf)
9. [Early-Learning Regularization](https://proceedings.neurips.cc/paper/2020/hash/ea89621bee7c88b2c5be6681c8ef4906-Abstract.html)
10. [FSSDINO prototype and Gram refinement](https://arxiv.org/html/2602.07550v1)
11. [Bilinear CNN for fine-grained recognition](https://openaccess.thecvf.com/content_iccv_2015/papers/Lin_Bilinear_CNN_Models_ICCV_2015_paper.pdf)

