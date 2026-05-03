#!/usr/bin/env python3
"""
png_to_webp.py — generate .webp siblings for every PNG in assets/img/.

- Skips favicons by default (small icons compress poorly to webp gain).
- Skips files where a fresh .webp already exists.
- Quality 82 is a strong default for photographic PNG; pages override per-image
  via the <picture><source type="image/webp"></picture> pattern.

Usage:
    python3 scripts/png_to_webp.py                # convert all eligible PNGs
    python3 scripts/png_to_webp.py --quality 78   # tune quality
    python3 scripts/png_to_webp.py --min-bytes 200000   # only large files
    python3 scripts/png_to_webp.py --report-only        # just print savings
"""

from __future__ import annotations

import argparse
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "assets" / "img"
SKIP_DIRS = {"favicons"}


def iter_pngs(min_bytes: int):
    for p in IMG_DIR.rglob("*.png"):
        rel = p.relative_to(IMG_DIR)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if p.stat().st_size < min_bytes:
            continue
        yield p


def convert(p: Path, quality: int, report_only: bool) -> tuple[int, int]:
    out = p.with_suffix(".webp")
    if out.exists() and out.stat().st_mtime >= p.stat().st_mtime:
        return p.stat().st_size, out.stat().st_size
    if report_only:
        return p.stat().st_size, 0
    img = Image.open(p)
    if img.mode == "P":
        img = img.convert("RGBA")
    img.save(out, "WEBP", quality=quality, method=6)
    return p.stat().st_size, out.stat().st_size


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--quality", type=int, default=82)
    ap.add_argument("--min-bytes", type=int, default=50_000)
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()

    total_in = total_out = count = 0
    for p in sorted(iter_pngs(args.min_bytes)):
        old, new = convert(p, args.quality, args.report_only)
        total_in += old
        total_out += new
        count += 1
        rel = p.relative_to(ROOT)
        if args.report_only or new == 0:
            print(f"  {rel} : {old/1024:.0f} KB")
        else:
            saved_pct = (1 - new / old) * 100 if old else 0
            print(f"  {rel} : {old/1024:.0f} KB -> {new/1024:.0f} KB  (-{saved_pct:.0f}%)")

    if total_in:
        if args.report_only:
            print(f"\n{count} PNGs eligible, total {total_in/1024/1024:.1f} MB.")
        else:
            saved = total_in - total_out
            pct = saved / total_in * 100 if total_in else 0
            print(f"\nProcessed {count} PNGs.")
            print(f"  PNG total : {total_in/1024/1024:.1f} MB")
            print(f"  WebP total: {total_out/1024/1024:.1f} MB")
            print(f"  Saved     : {saved/1024/1024:.1f} MB  ({pct:.0f}%)")
    else:
        print("Nothing to do.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
