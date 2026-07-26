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
