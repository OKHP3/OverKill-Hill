#!/usr/bin/env python3
"""
convert-gpt-icons-webp.py — Generate WebP variants for GPT icon PNGs
=====================================================================
Converts every Glee-fullyTools-GPTIcon-*-Background-RetroStripe-Square-1024.png
in assets/img/ to WebP at two widths (512, 1024) using Pillow, saving into
assets/img/webp/.

Naming convention:
  source : Glee-fullyTools-GPTIcon-01a-Resume-Builder-...-Square-1024.png
  outputs: Glee-fullyTools-GPTIcon-01a-Resume-Builder-...-Square-512.webp
           Glee-fullyTools-GPTIcon-01a-Resume-Builder-...-Square-1024.webp

Idempotent: existing WebP files are skipped unless --force is passed.

Usage:
    python3 scripts/convert-gpt-icons-webp.py
    python3 scripts/convert-gpt-icons-webp.py --force
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
IMG_DIR = REPO / "assets" / "img"
WEBP_DIR = REPO / "assets" / "img" / "webp"
TARGET_WIDTHS = [150, 300, 512, 600, 1024]
WEBP_QUALITY = 85


def discover_icons() -> list[Path]:
    """Return all RetroStripe GPT icon PNGs in assets/img/."""
    return sorted(IMG_DIR.glob("Glee-fullyTools-GPTIcon-*-Background-RetroStripe-Square-1024.png"))


def webp_name(png_path: Path, width: int) -> str:
    """Derive WebP filename from PNG path + target width."""
    stem = png_path.stem  # e.g. Glee-fullyTools-GPTIcon-01a-...-Square-1024
    # Replace the trailing -1024 with -<width>; normalize spaces to hyphens
    new_stem = stem.rsplit("-1024", 1)[0] + f"-{width}"
    return new_stem.replace(" ", "-") + ".webp"


def convert(force: bool = False) -> int:
    try:
        from PIL import Image
    except ImportError:
        print("ERROR: Pillow not installed. Run: pip install Pillow", file=sys.stderr)
        return 1

    WEBP_DIR.mkdir(parents=True, exist_ok=True)
    icons = discover_icons()

    if not icons:
        print("ERROR: No GPT icon PNGs found in assets/img/", file=sys.stderr)
        return 1

    converted = 0
    skipped = 0
    errors = 0

    for src in icons:
        try:
            img = Image.open(src).convert("RGBA")
        except Exception as e:
            print(f"  ! cannot open {src.name}: {e}")
            errors += 1
            continue

        orig_w, orig_h = img.size
        print(f"  source: {src.name}  ({orig_w}×{orig_h})")

        for width in TARGET_WIDTHS:
            out_name = webp_name(src, width)
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

    print(f"\nDone. Converted {converted} WebP file(s); skipped {skipped}; errors {errors}.")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    force = "--force" in sys.argv
    sys.exit(convert(force=force))
