#!/usr/bin/env python3
"""
Fix the site-wide "Hot off the Forge" banner text to be consistent across all pages.

Old (with em dash):
  v0.5 is live: the Council of AIs scored each other — every model was harder on itself than the architect was. Read it →

New (comma, matching homepage):
  v0.5 is live: the Council of AIs scored each other, every model was harder on itself than the architect was. Read it →
"""

import os
import sys

OLD_TEXT = "v0.5 is live: the Council of AIs scored each other \u2014 every model was harder on itself than the architect was. Read it \u2192"
NEW_TEXT = "v0.5 is live: the Council of AIs scored each other, every model was harder on itself than the architect was. Read it \u2192"

SKIP_DIRS = {"_replit", ".git", "node_modules", "dist"}


def find_html_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            if fname.endswith(".html"):
                yield os.path.join(dirpath, fname)


def fix_file(path, dry_run=False):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if OLD_TEXT not in content:
        return False
    new_content = content.replace(OLD_TEXT, NEW_TEXT)
    count = content.count(OLD_TEXT)
    if not dry_run:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
    print(f"  {'[dry-run] would fix' if dry_run else 'Fixed'} {path} ({count} occurrence{'s' if count != 1 else ''})")
    return True


def main():
    dry_run = "--dry-run" in sys.argv
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    changed = 0
    skipped = 0
    for path in sorted(find_html_files(root)):
        if fix_file(path, dry_run=dry_run):
            changed += 1
        else:
            skipped += 1
    print(f"\n{'Would change' if dry_run else 'Changed'}: {changed} file(s). No match: {skipped} file(s).")


if __name__ == "__main__":
    main()
