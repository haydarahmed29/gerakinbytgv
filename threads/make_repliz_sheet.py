#!/usr/bin/env python3
"""Bikin CSV format Repliz (Threads) dari threads/manifest.csv.

Contoh:
  # 1 album berisi 5 video preview, jadwal 16/11/2026 19:00
  python3 threads/make_repliz_sheet.py --mode album \
      --slugs tgv-pixel,tgv-papercraft,tgv-petakuno,tgv-chalkboard,tgv-infografis \
      --start "16/11/2026 19:00" --caption-file threads/caption.txt -o repliz.csv

  # 5 post Video terpisah (satu video per baris), jarak 30 menit
  python3 threads/make_repliz_sheet.py --mode video --slugs ... --step 30 -o repliz.csv

Header kolom mengikuti template resmi "SHEET REPLIZ EXAMPLE":
Title, Description, Type, URL Image, URL Video, URL's Album, Schedule Date, Topic
Tanggal: dd/mm/yyyy HH:MM. Album: URL dipisah koma tanpa spasi.
"""
import argparse, csv, sys
from datetime import datetime, timedelta
from pathlib import Path

HEADER = ["Title", "Description", "Type", "URL Image", "URL Video",
          "URL's Album", "Schedule Date", "Topic"]
FMT = "%d/%m/%Y %H:%M"


def load_manifest(path):
    with open(path, encoding="utf-8", newline="") as f:
        return {r["slug"]: r for r in csv.DictReader(f)}


def main():
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", default=str(here / "manifest.csv"))
    ap.add_argument("--mode", choices=["album", "video"], default="album")
    ap.add_argument("--slugs", required=True, help="slug dipisah koma, urutan = urutan di album")
    ap.add_argument("--start", required=True, help='waktu tayang pertama, "dd/mm/yyyy HH:MM"')
    ap.add_argument("--step", type=int, default=30, help="jarak menit antar baris (mode video)")
    ap.add_argument("--title", default="Preview gaya animasi Claude gratis")
    ap.add_argument("--caption-file", help="file teks caption (maks 500 karakter untuk Threads)")
    ap.add_argument("--caption", default="")
    ap.add_argument("--topic", default="AI Threads")
    ap.add_argument("--base", help="ganti awalan URL, mis. https://cdn.jsdelivr.net/gh/USER/REPO@main/threads/previews/")
    ap.add_argument("-o", "--out", default="-")
    a = ap.parse_args()

    manifest = load_manifest(a.manifest)
    slugs = [s.strip() for s in a.slugs.split(",") if s.strip()]
    missing = [s for s in slugs if s not in manifest]
    if missing:
        sys.exit(f"slug tidak ada di manifest: {', '.join(missing)}")

    def url(slug):
        if a.base:
            return a.base.rstrip("/") + "/" + slug + ".mp4"
        return manifest[slug]["url"]

    caption = Path(a.caption_file).read_text(encoding="utf-8").strip() if a.caption_file else a.caption
    if len(caption) > 500:
        sys.exit(f"caption {len(caption)} karakter, batas Threads 500")
    t0 = datetime.strptime(a.start, FMT)

    rows = []
    if a.mode == "album":
        rows.append([a.title, caption, "Album", "", "", ",".join(url(s) for s in slugs),
                     t0.strftime(FMT), a.topic])
    else:
        for i, s in enumerate(slugs):
            rows.append([a.title + " - " + manifest[s]["label"], caption, "Video", "", url(s), "",
                         (t0 + timedelta(minutes=a.step * i)).strftime(FMT), a.topic])

    out = sys.stdout if a.out == "-" else open(a.out, "w", encoding="utf-8", newline="")
    w = csv.writer(out)
    w.writerow(HEADER)
    w.writerows(rows)
    if out is not sys.stdout:
        out.close()


if __name__ == "__main__":
    main()
