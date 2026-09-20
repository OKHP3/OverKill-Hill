#!/usr/bin/env python3
"""Remove legacy Google Fonts links from tracked pages and authoring inputs.

Use --dry-run to inspect the inventory. Recovery folders, fixtures, translation
evidence, untracked files, and linked paths are never modified. Canonical CSP
changes belong in csp.py and generate-csp.py. After an authorized migration,
regenerate the site, CSP, indexes, and cache URLs.
"""
from __future__ import annotations
import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse
from public_page_boundary import is_public_page_path

ROOT = Path(__file__).resolve().parents[1]
INPUT_ROOTS = ("assets/partials/", "assets/templates/", "site-src/pages/")
MARKER = "<!-- AUTOGEN:SELF-HOSTED-FONTS -->"


def find_html_files(root: Path):
    root = root.resolve()
    tracked = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.html"], cwd=root,
        check=True, capture_output=True, text=True,
    )
    for name in sorted(filter(None, tracked.stdout.split("\0"))):
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            continue
        path = root / relative
        if not (is_public_page_path(path, root) or name.startswith(INPUT_ROOTS)):
            continue
        # Resolve every ancestor as well as the final file: symlinks and
        # Windows junctions must not redirect an edit, even within this root.
        if path.resolve() != path or path.is_symlink():
            continue
        if path.is_file():
            yield path


class LinkAttributes(HTMLParser):
    def __init__(self):
        super().__init__()
        self.attributes = {}

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "link":
            self.attributes = dict(attrs)


def strip_links(source: str) -> str:
    marked = MARKER in source

    def replace(match):
        nonlocal marked
        parser = LinkAttributes()
        parser.feed(match.group(0))
        attrs = parser.attributes
        host = urlparse(attrs.get("href") or "").hostname
        rel = set((attrs.get("rel") or "").lower().split())
        if host not in {"fonts.googleapis.com", "fonts.gstatic.com"} or not rel.intersection({"stylesheet", "preconnect"}):
            return match.group(0)
        if marked:
            return ""
        marked = True
        return MARKER

    return re.sub(r"(?m)^[ \t]*<link\b[^>]*>[ \t]*(?=\r?$)|<link\b[^>]*>", replace, source, flags=re.I)


def process_file(path: Path, apply: bool) -> bool:
    original = path.read_bytes()
    updated = strip_links(original.decode("utf-8")).encode("utf-8")
    if updated == original:
        return False
    if apply:
        path.write_bytes(updated)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    changed = [p.relative_to(ROOT) for p in find_html_files(ROOT)
               if process_file(p, apply=not args.dry_run)]
    print(f"{'Would update' if args.dry_run else 'Updated'} {len(changed)} tracked HTML files.")
    for path in changed:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
