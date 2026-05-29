#!/usr/bin/env python3
"""
inject-gpt-icon-picture.py — Wrap GPT icon <img> tags in <picture> with WebP sources
======================================================================================
For every HTML page that references a GPT icon PNG (RetroStripe, Square-1024 variant),
replaces bare <img> tags with <picture> elements offering WebP at 512w and 1024w
before falling back to the original PNG.

Idempotent: per-image check — skips any <img> already wrapped in <picture>.
Also sets loading="eager" and fetchpriority="high" on the branch-hero icon
(the first GPT icon on each page); subsequent card icons retain their
existing loading attribute (lazy or none).

WebP naming convention (matches convert-gpt-icons-webp.py):
  PNG  : Glee-fullyTools-GPTIcon-01a-...-Square-1024.png
  WebP : Glee-fullyTools-GPTIcon-01a-...-Square-512.webp
         Glee-fullyTools-GPTIcon-01a-...-Square-1024.webp

Usage:
    python3 scripts/inject-gpt-icon-picture.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

REPO = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"node_modules", ".local", ".git", "attached_assets", ".pythonlibs", ".cache", ".agents"}

WIDTHS = [512, 1024]
WEBP_PREFIX = "/assets/img/webp/"

ICON_IMG_PAT = re.compile(
    r'(<img\b[^>]*?GPTIcon[^"\']*?-Background-RetroStripe-Square-1024\.png[^>]*?>)',
    re.DOTALL,
)

SRC_EXTRACT = re.compile(
    r'src=["\']([^"\']*?GPTIcon[^"\']*?-Background-RetroStripe-Square-1024\.png)["\']'
)


def png_basename_to_webp(png_src: str, width: int) -> str:
    """Derive the WebP filename for a given PNG src path and target width."""
    basename = unquote(png_src.split("/")[-1])  # URL-decode + strip path
    stem = basename.rsplit(".png", 1)[0]         # e.g. ...Square-1024
    new_stem = stem.rsplit("-1024", 1)[0] + f"-{width}"
    return new_stem.replace(" ", "-") + ".webp"


def build_srcset(png_src: str) -> str:
    parts = [
        f"{WEBP_PREFIX}{png_basename_to_webp(png_src, w)} {w}w"
        for w in WIDTHS
    ]
    return ",\n            ".join(parts)


def is_wrapped(html: str, png_src: str) -> bool:
    """Return True if this specific PNG src is already inside a <picture>."""
    escaped = re.escape(png_src)
    return bool(re.search(
        r'<picture[^>]*>.*?' + escaped + r'.*?</picture>',
        html, re.DOTALL
    ))


def build_picture(img_tag: str, png_src: str, is_hero: bool, indent: str) -> str:
    """Wrap an <img> tag in a <picture> element with WebP sources."""
    img_mod = img_tag

    if is_hero:
        # Hero icon: force eager + fetchpriority
        if 'loading="lazy"' in img_mod:
            img_mod = img_mod.replace('loading="lazy"', 'loading="eager"')
        elif 'loading=' not in img_mod:
            img_mod = re.sub(r'\s*/?>\s*$', ' loading="eager">', img_mod)
        if 'fetchpriority=' not in img_mod:
            img_mod = re.sub(r'\s*/?>\s*$', ' fetchpriority="high">', img_mod)

    # Ensure tag closes cleanly
    if not img_mod.rstrip().endswith(">"):
        img_mod = img_mod.rstrip() + ">"

    srcset = build_srcset(png_src)

    return (
        f"<picture>\n"
        f"{indent}  <source\n"
        f"{indent}    type=\"image/webp\"\n"
        f"{indent}    srcset=\"{srcset}\"\n"
        f"{indent}    sizes=\"(max-width: 768px) 512px, 1024px\" />\n"
        f"{indent}  {img_mod}\n"
        f"{indent}</picture>"
    )


def process_page(path: Path) -> bool:
    html = path.read_text(encoding="utf-8", errors="replace")
    modified = html
    changed = False
    first_icon = True

    for m in ICON_IMG_PAT.finditer(html):
        img_tag = m.group(1)
        src_m = SRC_EXTRACT.search(img_tag)
        if not src_m:
            continue
        png_src = src_m.group(1)

        if is_wrapped(modified, re.escape(png_src)) or is_wrapped(modified, png_src):
            first_icon = False
            continue

        line_start = modified.rfind("\n", 0, modified.find(img_tag)) + 1
        indent = " " * (len(modified[line_start:modified.find(img_tag)]) - len(modified[line_start:modified.find(img_tag)].lstrip()))
        if len(indent) > 30:
            indent = "              "

        picture = build_picture(img_tag, png_src, is_hero=first_icon, indent=indent)
        modified = modified.replace(img_tag, picture, 1)
        changed = True
        first_icon = False

    if changed:
        path.write_text(modified, encoding="utf-8")
    return changed


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
