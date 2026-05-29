#!/usr/bin/env python3
"""
inject-hero-picture.py — Wrap hero <img> tags in <picture> with WebP sources
=============================================================================
For every HTML page that uses a Wide 1536 hero image, replaces the bare
<img> with a <picture> element that offers WebP variants at 768w, 1024w,
1536w before falling back to the original PNG.

Idempotent via presence of <picture> wrapping — pages already updated are
skipped.

Also:
  * Sets loading="eager" on hero img (overrides lazy if set)
  * Adds fetchpriority="high" if missing

Usage:
    python3 scripts/inject-hero-picture.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"node_modules", ".local", ".git", "attached_assets", ".pythonlibs", ".cache"}

WEBP_QUALITY = 85

IMG_TO_WEBP_STEM = {
    "glee-fully-tools-butterfly-loop-left-wide-1536.png":
        "Glee-fullyTools-ButterflyLoopLeft-Wide-{w}.webp",
    "glee-fully-tools-butterfly-loop-right-wide-1536.png":
        "Glee-fullyTools-ButterflyLoopRight-Wide-{w}.webp",
    "glee-fully-tools-title-mid-butterfly-multiple-error-explosion-wide-1536.png":
        "Glee-fullyTools-TitleMidButterflyMultipleErrorExplosion-Wide-{w}.webp",
    "glee-fully-tools-title-upper-left-butterfly-multiple-under-construction-wide-1536.png":
        "Glee-fullyTools-TitleUpperLeftButterflyMultipleUnderConstruction-Wide-{w}.webp",
}

WIDTHS = [768, 1024, 1536]


def webp_srcset(stem_template: str, prefix: str = "/assets/img/webp/") -> str:
    parts = [f"{prefix}{stem_template.format(w=w)} {w}w" for w in WIDTHS]
    return ",\n            ".join(parts)


def build_picture(img_tag: str, png_url_encoded: str, stem: str,
                  indent: str = "              ") -> str:
    """Wrap an existing <img> tag in a <picture> element with WebP sources."""
    img_modified = img_tag

    # Ensure loading="eager"
    if 'loading="lazy"' in img_modified:
        img_modified = img_modified.replace('loading="lazy"', 'loading="eager"')
    elif 'loading=' not in img_modified:
        img_modified = img_modified.rstrip(">").rstrip(" />").rstrip(" /") + ' loading="eager">'

    # Ensure fetchpriority="high"
    if 'fetchpriority=' not in img_modified:
        img_modified = img_modified.rstrip(">").rstrip(" />").rstrip(" /") + ' fetchpriority="high">'

    # Fix self-closing if needed
    if not img_modified.rstrip().endswith(">"):
        img_modified = img_modified.rstrip() + ">"

    srcset = webp_srcset(stem)

    picture = (
        f"<picture>\n"
        f"{indent}  <source\n"
        f"{indent}    type=\"image/webp\"\n"
        f"{indent}    srcset=\"{srcset}\"\n"
        f"{indent}    sizes=\"100vw\" />\n"
        f"{indent}  {img_modified}\n"
        f"{indent}</picture>"
    )
    return picture


def process_page(path: Path) -> bool:
    html = path.read_text(encoding="utf-8", errors="replace")
    modified = html
    changed = False

    for url_encoded, stem_template in IMG_TO_WEBP_STEM.items():
        if url_encoded not in html:
            continue

        # Skip if already wrapped in <picture>
        picture_check = re.search(
            r'<picture[^>]*>.*?' + re.escape(url_encoded) + r'.*?</picture>',
            html, re.DOTALL
        )
        if picture_check:
            continue

        # Find the <img> tag
        img_pat = re.compile(
            r'(<img\b[^>]*?' + re.escape(url_encoded) + r'[^>]*?>)',
            re.DOTALL
        )
        for m in img_pat.finditer(modified):
            img_tag = m.group(1)
            # Detect indentation from preceding text
            line_start = modified.rfind('\n', 0, m.start()) + 1
            indent = " " * (m.start() - line_start)
            if len(indent) > 30:
                indent = "              "
            picture = build_picture(img_tag, url_encoded, stem_template, indent)
            modified = modified[:m.start()] + picture + modified[m.end():]
            changed = True
            break  # one replacement at a time; re-scan on next iteration if needed

    if changed:
        path.write_text(modified, encoding="utf-8")
    return changed


def main() -> int:
    edited = 0
    for path in sorted(REPO.rglob("*.html")):
        rel = path.relative_to(REPO)
        if any(s in rel.parts for s in SKIP_DIRS):
            continue
        if any(str(rel).startswith(s) for s in {"assets/templates"}):
            continue
        if process_page(path):
            print(f"  + {rel}")
            edited += 1

    print(f"\nDone. Updated {edited} page(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
