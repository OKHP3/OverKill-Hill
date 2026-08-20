#!/usr/bin/env python3
"""
cache-bust.py — fingerprint the shared stylesheet in every HTML page.

Scans every production HTML file for a reference to `assets/css/theme.css` and
normalizes it to the canonical root-relative URL:
`/assets/css/theme.css?v=<sha256[:8]>`.

The fingerprint is derived from the stylesheet's file bytes, so changing the
stylesheet changes the URL browsers request after this command runs.

Usage:
    python3 scripts/cache-bust.py            # rewrite in place
    python3 scripts/cache-bust.py --check    # exit 1 if anything would change

Conventions:
- Hash is the first 8 chars of sha256 of the stylesheet file bytes.
- Relative and legacy query-string references are rewritten to the canonical URL.
- Skips _replit/, .local/, attached_assets/, node_modules/.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {"_replit", ".local", "attached_assets", "node_modules", ".git"}
THEME_STYLESHEET_PATH = "/assets/css/theme.css"
THEME_STYLESHEET = ROOT / THEME_STYLESHEET_PATH.lstrip("/")
# Match an absolute or relative reference to the shared stylesheet, with or
# without an existing query string. The quote backreference preserves the
# source document's attribute style.
THEME_STYLESHEET_REF = re.compile(
    r"""(?P<prefix>\bhref=(?P<quote>['"]))"""
    r"""(?:/?assets/css/theme\.css)(?:\?[^'"#]*)?(?P=quote)"""
)


def file_hash(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    return h[:8]


def iter_html_files(root: Path):
    for p in root.rglob("*.html"):
        rel = p.relative_to(root)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        yield p


def rewrite_one(html: str, fingerprint: str) -> tuple[str, int]:
    changes = 0

    def repl(m: re.Match) -> str:
        nonlocal changes
        canonical_ref = f"{THEME_STYLESHEET_PATH}?v={fingerprint}"
        if m.group(0) == f"{m.group('prefix')}{canonical_ref}{m.group('quote')}":
            return m.group(0)
        changes += 1
        return f"{m.group('prefix')}{canonical_ref}{m.group('quote')}"

    out = THEME_STYLESHEET_REF.sub(repl, html)
    return out, changes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="Do not write; exit 1 if any file would change.")
    args = ap.parse_args()

    fingerprint = file_hash(THEME_STYLESHEET)
    if fingerprint is None:
        print(f"ERROR: shared stylesheet not found: {THEME_STYLESHEET.relative_to(ROOT)}")
        return 1

    total_files = 0
    changed_files = 0
    total_subs = 0

    for html_path in iter_html_files(ROOT):
        total_files += 1
        original = html_path.read_text(encoding="utf-8")
        new, n = rewrite_one(original, fingerprint)
        if n > 0:
            changed_files += 1
            total_subs += n
            if args.check:
                print(f"WOULD CHANGE: {html_path.relative_to(ROOT)} ({n} subs)")
            else:
                html_path.write_text(new, encoding="utf-8")
                print(f"updated: {html_path.relative_to(ROOT)} ({n} subs)")

    print(f"\nScanned {total_files} HTML files. "
          f"{'Would change' if args.check else 'Changed'} {changed_files} files "
          f"({total_subs} substitutions).")

    if args.check and changed_files > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
