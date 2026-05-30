#!/usr/bin/env python3
"""
audit-meta-versions.py
Scans all HTML files for stale version strings (v0.1, v0.2, v0.3) in meta
name="description", og:description, and meta name="keywords" fields.

Usage:
    python3 scripts/audit-meta-versions.py
    python3 scripts/audit-meta-versions.py --fail-on-stale

Exit codes:
    0 — clean (no stale version references found)
    1 — stale references found
"""

import argparse
import os
import re
import sys

SKIP_DIRS = {
    "assets/templates",
    "_replit",
    "dist",
    ".local",
    ".git",
    "node_modules",
}

STALE_PATTERN = re.compile(r"v0\.[123]", re.IGNORECASE)

META_PATTERNS = [
    re.compile(r'<meta\s[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', re.IGNORECASE),
    re.compile(r'<meta\s[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']description["\']', re.IGNORECASE),
    re.compile(r'<meta\s[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']*)["\']', re.IGNORECASE),
    re.compile(r'<meta\s[^>]*content=["\']([^"\']*)["\'][^>]*property=["\']og:description["\']', re.IGNORECASE),
    re.compile(r'<meta\s[^>]*name=["\']keywords["\'][^>]*content=["\']([^"\']*)["\']', re.IGNORECASE),
    re.compile(r'<meta\s[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']keywords["\']', re.IGNORECASE),
]


def should_skip(path: str) -> bool:
    parts = path.replace("\\", "/").split("/")
    for skip in SKIP_DIRS:
        skip_parts = skip.split("/")
        for i in range(len(parts) - len(skip_parts) + 1):
            if parts[i : i + len(skip_parts)] == skip_parts:
                return True
    return False


def scan_file(filepath: str) -> list[tuple[str, str]]:
    """Return list of (field_type, matched_content) with stale version refs."""
    hits = []
    try:
        with open(filepath, encoding="utf-8", errors="replace") as fh:
            content = fh.read()
    except OSError:
        return hits

    for pattern in META_PATTERNS:
        for match in pattern.finditer(content):
            value = match.group(1)
            if STALE_PATTERN.search(value):
                hits.append((match.group(0)[:60] + "...", value))
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit meta tags for stale version references.")
    parser.add_argument("--fail-on-stale", action="store_true",
                        help="Exit with code 1 if any stale references are found.")
    parser.add_argument("root", nargs="?", default=".", help="Root directory to scan (default: .)")
    args = parser.parse_args()

    stale_found: list[tuple[str, str, str]] = []

    for dirpath, dirnames, filenames in os.walk(args.root):
        rel_dir = os.path.relpath(dirpath, args.root).replace("\\", "/").lstrip("./")
        if should_skip(rel_dir) or should_skip(dirpath):
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if not should_skip(
            os.path.relpath(os.path.join(dirpath, d), args.root).replace("\\", "/")
        )]

        for fname in filenames:
            if not fname.endswith(".html"):
                continue
            fpath = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(fpath, args.root)
            hits = scan_file(fpath)
            for tag, value in hits:
                stale_found.append((rel_path, tag, value))

    if stale_found:
        print(f"STALE VERSION REFERENCES FOUND ({len(stale_found)} occurrence(s)):\n")
        for rel_path, tag, value in stale_found:
            print(f"  {rel_path}")
            print(f"    Content: {value[:120]}")
            print()
        if args.fail_on_stale:
            return 1
    else:
        print("OK — no stale version references found in meta description/og:description/keywords.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
