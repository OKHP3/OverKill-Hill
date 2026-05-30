#!/usr/bin/env python3
"""
convert-hero-webp.py — Generate WebP variants for Wide 1536 hero images
=======================================================================
Converts each eligible PNG in assets/img/ to WebP at three widths
(768, 1024, 1536) using Pillow, saving into assets/img/webp/.

Idempotent: existing WebP files are skipped unless --force is passed.

Usage:
    python3 scripts/convert-hero-webp.py
    python3 scripts/convert-hero-webp.py --force
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
IMG_DIR = REPO / "assets" / "img"
WEBP_DIR = REPO / "assets" / "img" / "webp"
TARGET_WIDTHS = [768, 1024, 1536]
WEBP_QUALITY = 85

HERO_IMAGES = [
    "glee-fully-tools-butterfly-loop-left-wide-1536.png",
    "glee-fully-tools-butterfly-loop-right-wide-1536.png",
    "glee-fully-tools-title-mid-butterfly-multiple-error-explosion-wide-1536.png",
    "glee-fully-tools-title-upper-left-butterfly-multiple-under-construction-wide-1536.png",
]


def webp_stem(png_name: str, width: int) -> str:
    """Derive WebP filename: replace spaces→hyphens, update width, swap ext."""
    base = png_name.replace(".png", "").replace(" 1536", f" {width}")
    return base.replace(" ", "-") + ".webp"


def convert(force: bool = False) -> int:
    try:
        from PIL import Image
    except ImportError:
        print("ERROR: Pillow not installed. Run: pip install Pillow", file=sys.stderr)
        return 1

    WEBP_DIR.mkdir(parents=True, exist_ok=True)
    converted = 0
    skipped = 0
    missing = 0

    for png_name in HERO_IMAGES:
        src = IMG_DIR / png_name
        if not src.exists():
            print(f"  ! missing source: {png_name}")
            missing += 1
            continue

        try:
            img = Image.open(src).convert("RGBA")
        except Exception as e:
            print(f"  ! cannot open {png_name}: {e}")
            missing += 1
            continue

        orig_w, orig_h = img.size
        print(f"  source: {png_name}  ({orig_w}×{orig_h})")

        for width in TARGET_WIDTHS:
            out_name = webp_stem(png_name, width)
            out_path = WEBP_DIR / out_name
            if out_path.exists() and not force:
                print(f"    skip  {out_name} (exists)")
                skipped += 1
                continue
            height = round(orig_h * width / orig_w)
            if width == orig_w:
                resized = img
            else:
                resized = img.resize((width, height), Image.LANCZOS)
            resized.save(out_path, "WEBP", quality=WEBP_QUALITY, method=6)
            kb = out_path.stat().st_size / 1024
            print(f"    wrote {out_name}  ({width}×{height})  {kb:.0f} KB")
            converted += 1

    print(f"\nDone. Converted {converted} WebP file(s); skipped {skipped}; missing sources {missing}.")
    return 0 if missing == 0 else 1


if __name__ == "__main__":
    force = "--force" in sys.argv
    sys.exit(convert(force=force))
