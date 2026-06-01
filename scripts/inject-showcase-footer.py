#!/usr/bin/env python3
"""
inject-showcase-footer.py — Add /showcase/ footer nav link to all site pages
=============================================================================
Idempotent: skips any page that already contains href="/showcase/".

Inserts <li><a href="/showcase/">Showcase</a></li> immediately after
the <li><a href="/about/">About Us</a></li> entry in each page's footer
Navigation list.

Usage:
    python3 scripts/inject-showcase-footer.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"node_modules", ".local", ".git", "attached_assets", "assets",
             ".pythonlibs", ".cache"}
SKIP_FILES = {"404.html", "under-construction.html"}

SHOWCASE_LINK = '<li><a href="/showcase/">Showcase</a></li>'

AFTER_PATTERN = re.compile(
    r'(<li><a href="(?:/|)about/">About Us</a></li>)',
)


def process(path: Path) -> bool:
    html = path.read_text(encoding="utf-8", errors="replace")

    if 'href="/showcase/"' in html:
        return False

    if not AFTER_PATTERN.search(html):
        return False

    new_html = AFTER_PATTERN.sub(
        r'\1\n            ' + SHOWCASE_LINK,
        html,
        count=1,
    )
    if new_html == html:
        return False

    path.write_text(new_html, encoding="utf-8")
    return True


def main() -> int:
    edited = 0
    skipped = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if any(s in rel.parts for s in SKIP_DIRS):
            continue
        if path.name in SKIP_FILES:
            continue
        if process(path):
            print(f"  + {rel}")
            edited += 1
        else:
            skipped += 1
    print(f"\nDone. Updated {edited} page(s); {skipped} already had /showcase/ or no anchor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
