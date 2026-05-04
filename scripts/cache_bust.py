#!/usr/bin/env python3
"""
cache_bust.py — derive cache-bust query suffixes from file content hashes.

Scans every production HTML file for `<link rel="stylesheet" href=".../theme.css?v=N">`
or `<script src=".../mermaid-init.js?v=N">` style references and rewrites the `?v=`
suffix to a short content hash of the referenced asset on disk.

Usage:
    python3 scripts/cache_bust.py            # rewrite in place
    python3 scripts/cache_bust.py --check    # exit 1 if anything would change

Conventions:
- Only rewrites refs whose path resolves to a real file under the repo root.
- Hash is the first 8 chars of sha256 of the file bytes.
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

# Match href="/path/to/asset.ext?v=ANYTHING"  or src="..."
PATTERN = re.compile(
    r'((?:href|src)=")(/[^"?#]+\.(?:css|js))\?v=([^"&#]+)(")'
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


def rewrite_one(html: str) -> tuple[str, int]:
    changes = 0

    def repl(m: re.Match) -> str:
        nonlocal changes
        prefix, asset_path, old_ver, suffix = m.groups()
        candidate = ROOT / asset_path.lstrip("/")
        new_ver = file_hash(candidate)
        if new_ver is None or new_ver == old_ver:
            return m.group(0)
        changes += 1
        return f"{prefix}{asset_path}?v={new_ver}{suffix}"

    out = PATTERN.sub(repl, html)
    return out, changes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="Do not write; exit 1 if any file would change.")
    args = ap.parse_args()

    total_files = 0
    changed_files = 0
    total_subs = 0

    for html_path in iter_html_files(ROOT):
        total_files += 1
        original = html_path.read_text(encoding="utf-8")
        new, n = rewrite_one(original)
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
