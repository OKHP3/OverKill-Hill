#!/usr/bin/env python3
"""
inject-nav-logo-webp.py — Wrap the site-wide nav logo <img> in a <picture>
           element with WebP srcset variants.
=============================================================================
Idempotent: if the target <img> is already inside a <picture> block bearing
the AUTOGEN:NAV-LOGO-WEBP marker, the page is skipped on subsequent runs.

Usage:
    python3 scripts/inject-nav-logo-webp.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".pythonlibs", ".cache", ".local", "node_modules", ".git",
             "attached_assets", "assets"}

MARKER = "AUTOGEN:NAV-LOGO-WEBP"

OLD_IMG = (
    '<img src="/assets/img/glee-fully-tools-butterfly-waiting-square-1024.png"'
    ' alt="Glee\u2011fully logo" width="40" height="40" />'
)

NEW_PICTURE = (
    "<!-- " + MARKER + " -->"
    "<picture>"
    '<source type="image/webp"'
    ' srcset="'
    "/assets/img/webp/glee-fully-tools-butterfly-waiting-square-40.webp 40w,"
    " /assets/img/webp/glee-fully-tools-butterfly-waiting-square-80.webp 80w,"
    " /assets/img/webp/glee-fully-tools-butterfly-waiting-square-160.webp 160w"
    '"'
    ' sizes="40px" />'
    '<img src="/assets/img/glee-fully-tools-butterfly-waiting-square-1024.png"'
    ' alt="Glee\u2011fully logo" width="40" height="40" />'
    "</picture>"
    "<!-- /" + MARKER + " -->"
)


def process(path: Path) -> bool:
    html = path.read_text(encoding="utf-8", errors="replace")
    if MARKER in html:
        return False  # already patched
    if OLD_IMG not in html:
        return False  # nav logo not present (shouldn't happen, but safe)
    new_html = html.replace(OLD_IMG, NEW_PICTURE, 1)
    path.write_text(new_html, encoding="utf-8")
    return True


def main() -> int:
    edited = skipped = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if any(s in rel.parts for s in SKIP_DIRS):
            continue
        if process(path):
            print(f"  + {rel}")
            edited += 1
        else:
            skipped += 1
    print(f"\nDone. Patched {edited} page(s); {skipped} already up-to-date or skipped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
