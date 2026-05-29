#!/usr/bin/env python3
"""
normalize-head.py — Site-wide favicon / theme-color / manifest normalizer
=========================================================================
Ensures every page in the site shares the same canonical <head> chrome:

  • theme-color  →  #d35b2d  (brand rust)
  • SVG favicon  →  /assets/img/favicons/favicon.svg  (modern browsers)
  • PNG favicons (16/32) and apple-touch-icon  →  root-absolute paths
  • favicon.ico  →  root-absolute path
  • manifest     →  /site.webmanifest
  • mobile-web-app-capable + apple-mobile-web-app-capable  →  yes

It rewrites bad theme-colors, replaces relative favicon paths with
root-absolute paths, removes the broken safari-pinned-tab.svg link
(file does not exist), and inserts any missing tags.

Idempotent.

Usage:
    python3 scripts/normalize-head.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"node_modules", ".local", ".git", "attached_assets", "assets"}

THEME = "#d35b2d"

CANONICAL_BLOCK = """    <link rel="icon" href="/assets/img/favicons/favicon.svg" type="image/svg+xml" />
    <link rel="icon" href="/assets/img/favicons/favicon-32x32.png" sizes="32x32" type="image/png" />
    <link rel="icon" href="/assets/img/favicons/favicon-16x16.png" sizes="16x16" type="image/png" />
    <link rel="apple-touch-icon" href="/assets/img/favicons/apple-touch-icon.png" sizes="180x180" type="image/png" />
    <link rel="icon" href="/favicon.ico" sizes="any" />
    <link rel="manifest" href="/site.webmanifest" />"""


def fix_theme_color(html: str) -> tuple[str, bool]:
    pat = re.compile(r'(<meta\s+name="theme-color"\s+content=")[^"]*(")')
    if pat.search(html):
        new = pat.sub(lambda m: m.group(1) + THEME + m.group(2), html)
        return new, new != html
    # Insert before </head>
    insert = f'    <meta name="theme-color" content="{THEME}" />\n'
    new = re.sub(r"(\s*)</head>", f"\n{insert}\\1</head>", html, count=1)
    return new, new != html


def strip_old_favicons(html: str) -> str:
    """Remove every existing favicon/manifest/mask-icon link line."""
    patterns = [
        r'\s*<link\s+rel="icon"[^>]*/?>\s*\n?',
        r'\s*<link\s+rel="apple-touch-icon"[^>]*/?>\s*\n?',
        r'\s*<link\s+rel="manifest"[^>]*/?>\s*\n?',
        r'\s*<link\s+rel="mask-icon"[^>]*/?>\s*\n?',
        r'\s*<link\s+rel="shortcut icon"[^>]*/?>\s*\n?',
    ]
    for p in patterns:
        html = re.sub(p, "\n", html, flags=re.IGNORECASE)
    # Collapse runs of blank lines
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html


def insert_favicon_block(html: str) -> str:
    """Insert the canonical favicon block immediately before </head>."""
    block = "\n" + CANONICAL_BLOCK + "\n"
    return re.sub(r"(\s*)</head>", f"{block}\\1</head>", html, count=1)


def ensure_mobile_meta(html: str) -> str:
    """Ensure mobile-web-app-capable + apple-mobile-web-app-capable exist."""
    needed = [
        ('mobile-web-app-capable', 'yes'),
        ('apple-mobile-web-app-capable', 'yes'),
    ]
    for name, val in needed:
        if re.search(rf'<meta\s+name="{re.escape(name)}"', html, re.IGNORECASE):
            continue
        tag = f'    <meta name="{name}" content="{val}" />\n'
        html = re.sub(r"(\s*)</head>", f"{tag}\\1</head>", html, count=1)
    return html



def ensure_view_transition(html: str) -> str:
    """Insert <meta name="view-transition" content="same-origin"> if absent."""
    if 'name="view-transition"' in html:
        return html
    tag = '    <meta name="view-transition" content="same-origin" />\n'
    return re.sub(r"(\s*)</head>", f"{tag}\\1</head>", html, count=1)


def process(path: Path) -> bool:
    original = path.read_text(encoding="utf-8", errors="replace")
    html = original
    html, _ = fix_theme_color(html)
    # Only touch favicon block if any favicon-ish link is present OR </head> exists
    if "</head>" in html.lower():
        html = strip_old_favicons(html)
        html = insert_favicon_block(html)
        html = ensure_mobile_meta(html)
    html = ensure_view_transition(html)
    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> int:
    edited = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if any(s in rel.parts for s in SKIP_DIRS):
            continue
        if process(path):
            edited += 1
            print(f"  + {rel}")
    print(f"\nDone. Normalized {edited} page(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
