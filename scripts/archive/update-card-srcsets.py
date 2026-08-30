#!/usr/bin/env python3
"""
update-card-srcsets.py — Update GPT icon <picture> srcsets with responsive card sizes
======================================================================================
Finds every <picture> element wrapping a GPT icon RetroStripe PNG and replaces
the <source srcset> with accurate small-screen variants (150w, 300w, 600w, 1024w)
and correct `sizes` hints based on display context:

  card__tool-icon  (80px CSS):  srcset 150w/300w/600w  sizes "(max-width:1024px) 160px, 300px"
  non-card icons   (≥300px):    srcset 150w/300w/600w/1024w  sizes "(max-width:768px) 50vw, 512px"

Idempotent: skips any <source> that already contains a 150w entry.

Usage:
    python3 scripts/update-card-srcsets.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

REPO = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"node_modules", ".local", ".git", "attached_assets", ".pythonlibs", ".cache", ".agents"}
WEBP_PREFIX = "/assets/img/webp/"

CARD_WIDTHS = [150, 300, 600]
HERO_WIDTHS = [150, 300, 600, 1024]
CARD_SIZES  = "(max-width: 1024px) 160px, 300px"
HERO_SIZES  = "(max-width: 768px) 50vw, 512px"

PICTURE_PAT = re.compile(r'(<picture[^>]*>)(.*?)(</picture>)', re.DOTALL)
SOURCE_PAT  = re.compile(
    r'(<source\b[^>]*?type="image/webp"[^>]*?srcset=")([^"]+)("[^>]*?sizes=")([^"]+)(")',
    re.DOTALL,
)
IMG_SRC_PAT = re.compile(
    r'<img\b[^>]*?src=["\']([^"\']*?GPTIcon[^"\']*?-Background-RetroStripe-Square-1024\.png)["\']',
    re.DOTALL,
)
IMG_CLASS_PAT = re.compile(r'class=["\']([^"\']*card__tool-icon[^"\']*)["\']')


def png_to_webp(png_src: str, width: int) -> str:
    basename = unquote(png_src.split("/")[-1])
    stem = basename.rsplit(".png", 1)[0]
    new_stem = stem.rsplit("-1024", 1)[0] + f"-{width}"
    return new_stem.replace(" ", "-") + ".webp"


def build_srcset(png_src: str, widths: list[int]) -> str:
    parts = [f"{WEBP_PREFIX}{png_to_webp(png_src, w)} {w}w" for w in widths]
    return ",\n            ".join(parts)


def update_picture(pic_inner: str, open_tag: str, close_tag: str) -> tuple[str, bool]:
    """Return (updated_inner, changed)."""
    img_m = IMG_SRC_PAT.search(pic_inner)
    if not img_m:
        return open_tag + pic_inner + close_tag, False

    png_src = img_m.group(1)

    # Idempotency: skip if already has 150w in the srcset
    if "150w" in pic_inner:
        return open_tag + pic_inner + close_tag, False

    is_card = bool(IMG_CLASS_PAT.search(pic_inner))
    widths  = CARD_WIDTHS if is_card else HERO_WIDTHS
    sizes   = CARD_SIZES  if is_card else HERO_SIZES

    new_srcset = build_srcset(png_src, widths)

    def replace_source(m: re.Match) -> str:
        return m.group(1) + new_srcset + m.group(3) + sizes + m.group(5)

    new_inner, n = SOURCE_PAT.subn(replace_source, pic_inner, count=1)
    if n == 0:
        return open_tag + pic_inner + close_tag, False

    return open_tag + new_inner + close_tag, True


def process_page(path: Path) -> bool:
    html = path.read_text(encoding="utf-8", errors="replace")
    modified = html
    changed_any = False

    def replace_pic(m: re.Match) -> str:
        nonlocal changed_any
        inner = m.group(2)
        if "GPTIcon" not in inner:
            return m.group(0)
        full, changed = update_picture(inner, m.group(1), m.group(3))
        if changed:
            changed_any = True
        return full

    modified = PICTURE_PAT.sub(replace_pic, modified)

    if changed_any:
        path.write_text(modified, encoding="utf-8")
    return changed_any


def main() -> int:
    edited = 0
    for path in sorted(REPO.rglob("*.html")):
        rel = path.relative_to(REPO)
        if any(s in rel.parts for s in SKIP_DIRS):
            continue
        if str(rel).startswith("assets/templates"):
            continue
        if process_page(path):
            print(f"  + {rel}")
            edited += 1

    print(f"\nDone. Updated {edited} page(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
