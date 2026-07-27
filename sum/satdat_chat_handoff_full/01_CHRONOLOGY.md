# Kronologi Ringkas

1. Diputuskan memakai DINOv3 high-end, backbone frozen, Kaggle T4 x2, raw official train, tanpa local execution.
2. ViT-7B LVD dipilih sebagai final backbone screen; SAT ditolak.
3. V7 awal diaudit dan ditemukan bug final pretrained LayerNorm sebelum pooling.
4. V7 diperbaiki: official norm per token, final block memakai last_hidden_state, cache schema diubah.
5. Loading pertama offload ke disk; sharding diperbaiki menjadi balanced 13 GiB + 13 GiB.
6. V7 berhasil: regularized MLP fold 0 = 0.989918; five-fold OOF = 0.990136.
7. ViT-7B + regularized MLP ditetapkan sebagai main pipeline.
8. Residual error didominasi Recyclable ↔ Organic; Electronic hampir saturasi.
9. V8 hierarchical R/O specialist dibuat sebagai cache-only.
10. V8 gagal fold 0; V7 tetap dipertahankan.
11. Rencana V9 mixup diganti setelah panitia mengizinkan bebas preprocessing train.
12. V9 AUDIT menghasilkan kandidat mislabel, duplicate conflict, dan ambiguous keep.
13. Dua duplicate conflict dikunci untuk drop; sepuluh obvious mislabels dipilih untuk dibandingkan drop vs relabel.
14. V9 SCREEN menjaga validation original dan hanya menerapkan treatment di training partition.
15. Drop-only, relabel, dan blend semuanya menurunkan Macro F1.
16. V9 ditolak; raw original dataset tetap canonical.
17. Current best tetap V7.
18. Next active experiment: V10 multi-seed V7 original-data ensemble.
19. Setelah V10, buat notebook final end-to-end yang menghasilkan minimal dua submission.
