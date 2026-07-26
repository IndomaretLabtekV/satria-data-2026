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
