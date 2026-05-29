#!/usr/bin/env python3
"""inject-showcase-subnav.py — Idempotent nav-submenu Showcase injector.

Ensures every page's primary nav "About" submenu contains:
    <li><a href="/showcase/">Showcase</a></li>
at 16-space indentation, immediately after the About Us entry.

Handles three cases:
  1. Link present at wrong indent (12 sp) — fix to 16 sp (prior footer
     injector inserted it in the nav but at footer-level indentation).
  2. Link entirely missing from submenu — insert after About Us entry.
  3. Link already correct (16 sp) or has aria-current — skip (idempotent).

Usage:
    python3 scripts/inject-showcase-subnav.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"node_modules", ".local", ".git", "attached_assets", "assets",
             ".pythonlibs", ".cache", ".agents"}
SKIP_FILES = {"404.html", "under-construction.html"}

WRONG_INDENT   = '            <li><a href="/showcase/">Showcase</a></li>'
CORRECT_LINK   = '                <li><a href="/showcase/">Showcase</a></li>'

SUBMENU_MARKER = 'class="submenu" aria-label="About menu"'

ABOUT_US_PAT = re.compile(
    r'([ \t]{16}<li><a href="(?:/|)about/"(?:[^>]*)>About Us</a></li>)'
)


def is_correct(html: str) -> bool:
    return (CORRECT_LINK in html
            or '                <li><a href="/showcase/" aria-current=' in html)


def process(path: Path) -> str | None:
    """Return action taken ('fixed-indent'|'inserted'|None)."""
    html = path.read_text(encoding="utf-8", errors="replace")

    if SUBMENU_MARKER not in html:
        return None

    if is_correct(html):
        return None

    if WRONG_INDENT in html:
        new_html = html.replace(WRONG_INDENT, CORRECT_LINK, 1)
        path.write_text(new_html, encoding="utf-8")
        return "fixed-indent"

    m = ABOUT_US_PAT.search(html)
    if m:
        new_html = html[:m.end()] + "\n" + CORRECT_LINK + html[m.end():]
        path.write_text(new_html, encoding="utf-8")
        return "inserted"

    return None


def main() -> int:
    fixed = inserted = skipped = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if any(s in rel.parts for s in SKIP_DIRS):
            continue
        if path.name in SKIP_FILES:
            continue
        action = process(path)
        if action == "fixed-indent":
            print(f"  ~ {rel}  (indent corrected)")
            fixed += 1
        elif action == "inserted":
            print(f"  + {rel}  (link added)")
            inserted += 1
        else:
            skipped += 1

    print(f"\nDone. Fixed indent: {fixed}  Inserted: {inserted}  Skipped: {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
