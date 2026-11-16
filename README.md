# gerakinbytgv

Aset Gerak.in: video preview skill TGV, testimoni, dan suara.

## threads/ (untuk automation Repliz)

- `threads/previews/` : 14 video preview skill dengan nama bersih (huruf kecil, tanpa spasi), mis. `tgv-pixel.mp4`.
- `threads/manifest.csv` : daftar slug, label gaya, durasi, resolusi, dan URL langsung (raw GitHub) tiap video.
- `threads/make_repliz_sheet.py` : bikin CSV format Repliz dari manifest. Impor CSV-nya ke Google Sheets, lalu pakai di Repliz.
- `threads/caption.txt` : caption contoh (maks 500 karakter).

Contoh:

```
python3 threads/make_repliz_sheet.py --mode album \
  --slugs tgv-pixel,tgv-papercraft,tgv-petakuno,tgv-chalkboard,tgv-infografis \
  --start "16/11/2026 19:00" --caption-file threads/caption.txt -o repliz.csv
```

Video baru: taruh di `threads/previews/<slug>.mp4`, tambah satu baris di `manifest.csv`.

File lama di root (`PREVIEW ...mp4`, `testimoni/`, `video testimoni/`) sengaja tidak diubah karena mungkin masih dipakai landing page.
