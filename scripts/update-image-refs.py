#!/usr/bin/env python3
"""
update-image-refs.py
--------------------
Finds all references to the old PascalCase image filenames in HTML, CSS, JS,
and JSON files, then replaces them with the new kebab-case names.

Applies the same conversion logic used by kebab-rename-images.py.

Usage:
  python3 scripts/update-image-refs.py           # dry run
  python3 scripts/update-image-refs.py --execute # apply changes
"""

import os
import re
import sys

SCAN_EXTS = {".html", ".css", ".js", ".json", ".md"}

SKIP_DIRS = {
    ".git", "node_modules", "_replit", ".local", ".agents",
    "assets/img",
}

SCAN_ROOTS = ["."]

OLD_NAME_PATTERNS = [
    re.compile(r"OverKillHillP\xb3[-_][\w\-\.]+\.(png|webp|jpg|jpeg|svg)", re.IGNORECASE),
    re.compile(r"OverKillHillP3[-_][\w\-\.]+\.(png|webp|jpg|jpeg|svg)", re.IGNORECASE),
    re.compile(r"OverKillHillP%C2%B3[-_][\w%\-\.]+\.(png|webp|jpg|jpeg|svg)", re.IGNORECASE),
    re.compile(r"AskJamie-GPTIcon-[\w\-]+\.(png|webp|jpg|jpeg|svg)", re.IGNORECASE),
]


def camel_segment_to_kebab(segment: str) -> str:
    s = segment.replace("\u00b3", "3").replace("%C2%B3", "3")
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1-\2", s)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", s)
    return s.lower()


def to_kebab_filename(name: str) -> str:
    base, ext = os.path.splitext(name)
    parts = base.split("-")
    converted = [camel_segment_to_kebab(p) for p in parts]
    result = "-".join(converted)
    result = re.sub(r"-{2,}", "-", result)
    result = result.strip("-")
    return result + ext.lower()


def convert_match(match: re.Match) -> str:
    original = match.group(0)
    return to_kebab_filename(original)


def should_skip(path: str) -> bool:
    parts = path.replace("\\", "/").split("/")
    for skip in SKIP_DIRS:
        skip_parts = skip.split("/")
        for i in range(len(parts) - len(skip_parts) + 1):
            if parts[i:i+len(skip_parts)] == skip_parts:
                return True
    return False


def collect_files() -> list:
    files = []
    for root_dir in SCAN_ROOTS:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            rel = os.path.relpath(dirpath, ".")
            if should_skip(rel):
                dirnames.clear()
                continue
            dirnames[:] = [d for d in dirnames if not d.startswith(".") or d in {".github"}]
            for fname in filenames:
                _, ext = os.path.splitext(fname)
                if ext in SCAN_EXTS:
                    files.append(os.path.join(dirpath, fname))
    return files


def process_file(path: str, execute: bool) -> list:
    """Returns list of (old_ref, new_ref) pairs found in file."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            original = f.read()
    except Exception:
        return []

    updated = original
    hits = []

    for pattern in OLD_NAME_PATTERNS:
        for match in pattern.finditer(original):
            old_val = match.group(0)
            new_val = to_kebab_filename(old_val)
            if old_val != new_val:
                hits.append((old_val, new_val))

    if not hits:
        return []

    for old_val, new_val in hits:
        updated = updated.replace(old_val, new_val)

    if execute and updated != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)

    return hits


def main():
    execute = "--execute" in sys.argv
    files = collect_files()
    total_hits = 0
    files_changed = 0

    print(f"{'DRY RUN' if not execute else 'EXECUTING'} — scanning {len(files)} files\n")

    for path in sorted(files):
        hits = process_file(path, execute)
        if hits:
            files_changed += 1
            total_hits += len(hits)
            rel = os.path.relpath(path, ".")
            print(f"  {rel} ({len(hits)} replacement{'s' if len(hits) > 1 else ''})")
            for old_val, new_val in sorted(set(hits)):
                print(f"    {old_val}")
                print(f"    -> {new_val}")

    print(f"\nFiles with changes: {files_changed}")
    print(f"Total replacements: {total_hits}")
    if not execute:
        print("Re-run with --execute to apply changes.")


if __name__ == "__main__":
    main()
