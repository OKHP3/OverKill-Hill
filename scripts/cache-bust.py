#!/usr/bin/env python3
"""
cache-bust.py — fingerprint shared CSS and JavaScript in every HTML page.

Scans every production HTML file for references to shared assets and normalizes
them to canonical root-relative URLs:
`/assets/<path>?v=<sha256[:8]>`.

Each fingerprint is derived from the referenced file's bytes, so changing a
shared stylesheet or interaction script changes the URL browsers request after
this command runs.

Usage:
    python3 scripts/cache-bust.py            # rewrite in place
    python3 scripts/cache-bust.py --check    # exit 1 if anything would change

Conventions:
- Hash is the first 8 chars of sha256 of each shared asset's canonical text
  bytes (LF line endings, independent of the checkout platform).
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
SHARED_ASSET_PATHS = (
    "/assets/css/theme.css",
    "/assets/js/app.js",
    "/assets/js/mermaid-init.js",
)
# Match an absolute or relative reference to a shared asset, with or without an
# existing query string. The quote backreference preserves the source document's
# attribute style.
SHARED_ASSET_REF = re.compile(
    r"""(?P<prefix>\b(?:href|src)=(?P<quote>['"]))"""
    r"""(?P<path>/?assets/(?:css/theme\.css|js/app\.js|js/mermaid-init\.js))"""
    r"""(?:\?[^'"#]*)?(?P=quote)"""
)


def file_hash(path: Path) -> str | None:
    if not path.is_file():
        return None
    canonical = path.read_bytes().replace(b"\r\n", b"\n")
    h = hashlib.sha256(canonical).hexdigest()
    return h[:8]


def iter_html_files(root: Path):
    for p in root.rglob("*.html"):
        rel = p.relative_to(root)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        yield p


def rewrite_one(html: str, fingerprints: dict[str, str]) -> tuple[str, int]:
    changes = 0

    def repl(m: re.Match) -> str:
        nonlocal changes
        asset_path = f"/{m.group('path').lstrip('/')}"
        canonical_ref = f"{asset_path}?v={fingerprints[asset_path]}"
        if m.group(0) == f"{m.group('prefix')}{canonical_ref}{m.group('quote')}":
            return m.group(0)
        changes += 1
        return f"{m.group('prefix')}{canonical_ref}{m.group('quote')}"

    out = SHARED_ASSET_REF.sub(repl, html)
    return out, changes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="Do not write; exit 1 if any file would change.")
    args = ap.parse_args()

    fingerprints: dict[str, str] = {}
    for asset_path in SHARED_ASSET_PATHS:
        asset = ROOT / asset_path.lstrip("/")
        fingerprint = file_hash(asset)
        if fingerprint is None:
            print(f"ERROR: shared asset not found: {asset.relative_to(ROOT)}")
            return 1
        fingerprints[asset_path] = fingerprint

    total_files = 0
    changed_files = 0
    total_subs = 0

    for html_path in iter_html_files(ROOT):
        total_files += 1
        original = html_path.read_text(encoding="utf-8")
        new, n = rewrite_one(original, fingerprints)
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
