#!/usr/bin/env python3
"""
picture_upgrade.py — wrap visible <img src="X.png"> tags in <picture> with a
WebP source, when an X.webp sibling exists on disk.

Skips:
- favicons (must stay PNG)
- og:image / twitter:image meta tags (social scrapers do not all support WebP)
- <link rel="icon"> / apple-touch-icon
- already-wrapped <picture> blocks
- non-asset paths (only /assets/img/* are touched)

Usage:
    python3 scripts/picture_upgrade.py            # rewrite in place
    python3 scripts/picture_upgrade.py --check    # exit 1 if anything would change
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"_replit", ".local", "attached_assets", "node_modules", ".git"}

# Match a self-closing or opening <img ... src="/assets/img/...png" ...>
IMG_RE = re.compile(
    r'(<img\b[^>]*\bsrc=")(/assets/img/[^"]+\.png)("[^>]*?/?>)',
    re.IGNORECASE,
)


def webp_sibling_exists(asset_url: str) -> Path | None:
    decoded = unquote(asset_url.lstrip("/"))
    png_path = ROOT / decoded
    webp_path = png_path.with_suffix(".webp")
    if webp_path.is_file():
        return webp_path
    return None


def is_inside_picture(html: str, idx: int) -> bool:
    open_idx = html.rfind("<picture", 0, idx)
    close_idx = html.rfind("</picture>", 0, idx)
    return open_idx != -1 and open_idx > close_idx


def is_favicon(asset_url: str) -> bool:
    return "/favicons/" in asset_url


def upgrade_one(html: str) -> tuple[str, int]:
    out = []
    cursor = 0
    changes = 0
    for m in IMG_RE.finditer(html):
        prefix, asset, suffix = m.groups()
        full_tag = m.group(0)
        start = m.start()

        # skip favicons
        if is_favicon(asset):
            continue
        # skip if already in <picture>
        if is_inside_picture(html, start):
            continue
        # skip if no webp sibling
        if not webp_sibling_exists(asset):
            continue

        # Build the webp src by simple string swap on extension
        webp_url = re.sub(r"\.png(\?.*)?$", r".webp\1", asset)

        # Emit catch-up text + replacement
        out.append(html[cursor:start])
        out.append(
            f'<picture><source type="image/webp" srcset="{webp_url}">'
            f"{full_tag}</picture>"
        )
        cursor = m.end()
        changes += 1

    out.append(html[cursor:])
    return "".join(out), changes


def iter_html_files(root: Path):
    for p in root.rglob("*.html"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        yield p


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="Do not write; exit 1 if any file would change.")
    args = ap.parse_args()

    total_files = changed_files = total_subs = 0
    for path in iter_html_files(ROOT):
        total_files += 1
        original = path.read_text(encoding="utf-8")
        new, n = upgrade_one(original)
        if n > 0:
            changed_files += 1
            total_subs += n
            if args.check:
                print(f"WOULD CHANGE: {path.relative_to(ROOT)} ({n} subs)")
            else:
                path.write_text(new, encoding="utf-8")
                print(f"updated: {path.relative_to(ROOT)} ({n} subs)")

    print(f"\nScanned {total_files} HTML files. "
          f"{'Would change' if args.check else 'Changed'} {changed_files} files "
          f"({total_subs} substitutions).")

    if args.check and changed_files > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
