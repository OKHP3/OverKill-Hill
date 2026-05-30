#!/usr/bin/env python3
"""
kebab-rename-images.py
----------------------
Converts PascalCase/brand-prefix image filenames to kebab-case in:
  - assets/img/          (brand hero files)
  - assets/img/library/  (brand archive)
  - assets/img/AskJamie/ (cross-site icons)
  - assets/img/AskJamie/BrandGuard/

Usage:
  python3 scripts/kebab-rename-images.py           # dry run (default)
  python3 scripts/kebab-rename-images.py --execute # rename files on disk
  python3 scripts/kebab-rename-images.py --map     # print JSON rename map
"""

import os
import re
import sys
import json

DIRS = [
    "assets/img",
    "assets/img/library",
    "assets/img/AskJamie",
    "assets/img/AskJamie/BrandGuard",
]

SKIP_FILES = {
    ".gitkeep", "README.md",
}

ALREADY_KEBAB_PREFIXES = (
    "etch-",
    "android-",
    "apple-",
    "favicon",
)


def camel_segment_to_kebab(segment: str) -> str:
    s = segment.replace("\u00b3", "3")
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1-\2", s)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", s)
    return s.lower()


def to_kebab_filename(name: str) -> str:
    base, ext = os.path.splitext(name)
    parts = base.split("-")
    converted = []
    for part in parts:
        converted.append(camel_segment_to_kebab(part))
    result = "-".join(converted)
    result = re.sub(r"-{2,}", "-", result)
    result = result.strip("-")
    return result + ext.lower()


def needs_rename(name: str) -> bool:
    if name in SKIP_FILES:
        return False
    if any(name.startswith(p) for p in ALREADY_KEBAB_PREFIXES):
        return False
    kebab = to_kebab_filename(name)
    return kebab != name


def collect_renames(base_dir: str) -> list:
    renames = []
    if not os.path.isdir(base_dir):
        return renames
    for name in sorted(os.listdir(base_dir)):
        if os.path.isdir(os.path.join(base_dir, name)):
            continue
        if not needs_rename(name):
            continue
        new_name = to_kebab_filename(name)
        renames.append((base_dir, name, new_name))
    return renames


def main():
    execute = "--execute" in sys.argv
    output_map = "--map" in sys.argv

    all_renames = []
    for d in DIRS:
        all_renames.extend(collect_renames(d))

    if output_map:
        mapping = {}
        for base_dir, old_name, new_name in all_renames:
            rel_old = os.path.join(base_dir, old_name)
            rel_new = os.path.join(base_dir, new_name)
            mapping[rel_old] = rel_new
        print(json.dumps(mapping, indent=2, ensure_ascii=False))
        return

    print(f"{'DRY RUN' if not execute else 'EXECUTING'} — {len(all_renames)} renames\n")
    print(f"{'OLD NAME':<70}  {'NEW NAME'}")
    print("-" * 140)

    errors = []
    done = 0
    for base_dir, old_name, new_name in all_renames:
        old_path = os.path.join(base_dir, old_name)
        new_path = os.path.join(base_dir, new_name)
        print(f"{os.path.join(base_dir, old_name):<70}  {new_name}")
        if execute:
            if os.path.exists(new_path):
                errors.append(f"SKIP (target exists): {new_path}")
                continue
            try:
                os.rename(old_path, new_path)
                done += 1
            except Exception as e:
                errors.append(f"ERROR renaming {old_path}: {e}")

    print()
    if execute:
        print(f"Renamed: {done}/{len(all_renames)}")
        if errors:
            print("\nErrors:")
            for e in errors:
                print(f"  {e}")
    else:
        print("Re-run with --execute to apply renames.")
        print("Re-run with --map to get JSON mapping for HTML updates.")


if __name__ == "__main__":
    main()
