#!/usr/bin/env python3
"""
strip-google-fonts-links.py

Site-wide sweep: removes the three per-page Google Fonts network requests
(two <link rel="preconnect"> tags + the fonts.googleapis.com/css2 stylesheet
<link>) now that Alfa Slab One, DM Sans, and JetBrains Mono are self-hosted
from assets/fonts/ via the @font-face rules added to assets/css/theme.css
on 2026-09-20 (see that file's "SELF-HOSTED FONTS" section).

Also tightens each page's Content-Security-Policy meta tag by dropping the
now-unused `https://fonts.googleapis.com` allowance from style-src and
`https://fonts.gstatic.com` from font-src, since nothing on the page fetches
those origins anymore.

Idempotent: run it as many times as you like. A page with none of these
strings left is reported as "already clean" and skipped.

Usage:
    python3 scripts/strip-google-fonts-links.py --dry-run   # report only
    python3 scripts/strip-google-fonts-links.py             # apply changes

Then run the existing site checks before committing:
    python3 scripts/validate-site.py
"""
import argparse
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

# Exact substrings as they appear in this repo's baked-in <head> markup
# (confirmed against assets/partials/head.html and index.html, 2026-09-20).
PRECONNECT_GOOGLEAPIS = '<link href="https://fonts.googleapis.com" rel="preconnect"/>'
PRECONNECT_GSTATIC = '<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>'
STYLESHEET_LINK_RE = re.compile(
    r'<link href="https://fonts\.googleapis\.com/css2\?[^"]*" rel="stylesheet"/>'
)

CSP_STYLE_SRC_GOOGLEAPIS = " https://fonts.googleapis.com"
CSP_FONT_SRC_GSTATIC = " https://fonts.gstatic.com"

# Skip build-source fragments and anything under node_modules / .git.
SKIP_DIR_PARTS = {".git", "node_modules"}


def find_html_files(root: pathlib.Path):
    for path in root.rglob("*.html"):
        if any(part in SKIP_DIR_PARTS for part in path.parts):
            continue
        yield path


def process_file(path: pathlib.Path, apply: bool) -> str:
    original = path.read_text(encoding="utf-8")
    text = original

    text = text.replace(PRECONNECT_GOOGLEAPIS + "\n", "")
    text = text.replace(PRECONNECT_GOOGLEAPIS, "")
    text = text.replace(PRECONNECT_GSTATIC + "\n", "")
    text = text.replace(PRECONNECT_GSTATIC, "")
    text = STYLESHEET_LINK_RE.sub("", text)

    text = text.replace(CSP_STYLE_SRC_GOOGLEAPIS, "")
    text = text.replace(CSP_FONT_SRC_GSTATIC, "")

    if text == original:
        return "clean"

    if apply:
        path.write_text(text, encoding="utf-8")
    return "changed"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run", action="store_true", help="Report what would change, write nothing."
    )
    args = parser.parse_args()

    changed, clean = [], []
    for path in sorted(find_html_files(REPO_ROOT)):
        status = process_file(path, apply=not args.dry_run)
        rel = path.relative_to(REPO_ROOT)
        if status == "changed":
            changed.append(rel)
        else:
            clean.append(rel)

    verb = "Would update" if args.dry_run else "Updated"
    print(f"{verb} {len(changed)} file(s):")
    for rel in changed:
        print(f"  - {rel}")
    print(f"Already clean / no match: {len(clean)} file(s).")

    if args.dry_run and changed:
        print("\nRe-run without --dry-run to apply.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
