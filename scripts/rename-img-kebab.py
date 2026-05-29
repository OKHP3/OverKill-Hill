#!/usr/bin/env python3
"""
scripts/rename-img-kebab.py
Renames every file in assets/img/ (including webp/) to strict kebab-case and
updates every reference in HTML, JSON, and Python files.

Conversion rules (per AGENTS.md §1):
  - Spaces -> hyphens
  - PascalCase segments split at case boundaries (GPTIcon -> gpt-icon)
  - Everything lowercased
  - Multiple hyphens collapsed to one

Idempotent: running on already-renamed files produces no changes.
"""

import os
import re
import sys
import json
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent.parent
IMG_DIR = ROOT / "assets" / "img"
SKIP_DIRS = {".git", "node_modules", ".pythonlibs", ".cache", ".local"}

# File extensions to update references in
TEXT_EXTS = {".html", ".json", ".py", ".md", ".sh"}


# ---------------------------------------------------------------------------
# Kebab conversion
# ---------------------------------------------------------------------------

def segment_to_kebab(seg: str) -> str:
    """Convert a single PascalCase / camelCase segment to kebab-case."""
    if not seg:
        return seg
    # Step 1: split before uppercase sequences followed by uppercase+lowercase
    #   GPTIcon -> GPT-Icon
    seg = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1-\2", seg)
    # Step 2: split at lowercase/digit -> uppercase boundary
    #   fullyTools -> fully-Tools, bLinkIn -> b-Link-In
    seg = re.sub(r"([a-z\d])([A-Z])", r"\1-\2", seg)
    return seg.lower()


def to_kebab_name(filename: str) -> str:
    """Return the kebab-case equivalent of a filename, preserving extension."""
    p = Path(filename)
    stem = p.stem
    ext = p.suffix.lower()

    # Normalise any run of whitespace or hyphens to a single hyphen first
    stem = re.sub(r"[\s\-]+", "-", stem)

    # Split on hyphens, convert each segment, rejoin
    segments = stem.split("-")
    converted = [segment_to_kebab(s) for s in segments if s]
    result = "-".join(converted)

    # Final safety: collapse any double hyphens produced by the process
    result = re.sub(r"-{2,}", "-", result)
    result = result.strip("-")

    return result + ext


# ---------------------------------------------------------------------------
# Build rename map
# ---------------------------------------------------------------------------

def build_rename_map() -> dict[str, str]:
    """
    Walk assets/img/ and return {old_relative_path: new_relative_path}
    for every file whose name differs from its kebab equivalent.
    Paths are relative to ROOT (e.g. 'assets/img/Foo Bar.png').
    """
    rename_map: dict[str, str] = {}
    for dirpath, dirnames, filenames in os.walk(IMG_DIR):
        # Skip hidden / detritus dirs
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            new_fname = to_kebab_name(fname)
            if new_fname == fname:
                continue  # already compliant
            old_abs = Path(dirpath) / fname
            new_abs = Path(dirpath) / new_fname
            old_rel = str(old_abs.relative_to(ROOT))
            new_rel = str(new_abs.relative_to(ROOT))
            rename_map[old_rel] = new_rel
    return rename_map


# ---------------------------------------------------------------------------
# Reference replacement helpers
# ---------------------------------------------------------------------------

def make_substitutions(content: str, rename_map: dict[str, str]) -> str:
    """
    Replace every occurrence of each old path (both raw and %20-encoded)
    with the corresponding new path.
    """
    for old_rel, new_rel in rename_map.items():
        old_fname = Path(old_rel).name
        new_fname = Path(new_rel).name

        # Replace URL-encoded form (spaces as %20, etc.)
        old_encoded = urllib.parse.quote(old_fname, safe="-._~/")
        new_fname_safe = new_fname  # new name has no chars needing encoding

        if old_encoded != old_fname:
            content = content.replace(old_encoded, new_fname_safe)

        # Replace raw form
        content = content.replace(old_fname, new_fname)

    return content


def update_text_files(rename_map: dict[str, str]) -> list[str]:
    """Walk the repo and update references in text files. Returns list of changed files."""
    changed: list[str] = []

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [
            d for d in dirnames
            if d not in SKIP_DIRS and not d.startswith(".")
               or d in {".github", ".well-known", ".agents"}
        ]
        # Skip the assets/img subtree itself (we handle renames separately)
        dirnames[:] = [d for d in dirnames if Path(dirpath, d) != IMG_DIR]

        for fname in filenames:
            fpath = Path(dirpath) / fname
            if fpath.suffix.lower() not in TEXT_EXTS:
                continue
            try:
                original = fpath.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            updated = make_substitutions(original, rename_map)
            if updated != original:
                fpath.write_text(updated, encoding="utf-8")
                changed.append(str(fpath.relative_to(ROOT)))

    return changed


# ---------------------------------------------------------------------------
# File renames
# ---------------------------------------------------------------------------

def rename_files(rename_map: dict[str, str]) -> list[tuple[str, str]]:
    """Perform the filesystem renames. Returns list of (old, new) tuples done."""
    done: list[tuple[str, str]] = []
    for old_rel, new_rel in rename_map.items():
        old_abs = ROOT / old_rel
        new_abs = ROOT / new_rel
        if not old_abs.exists():
            print(f"  SKIP (missing): {old_rel}", file=sys.stderr)
            continue
        if new_abs.exists() and new_abs != old_abs:
            print(f"  SKIP (target exists): {new_rel}", file=sys.stderr)
            continue
        new_abs.parent.mkdir(parents=True, exist_ok=True)
        old_abs.rename(new_abs)
        done.append((old_rel, new_rel))
    return done


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    dry_run = "--dry-run" in sys.argv

    print("Building rename map...")
    rename_map = build_rename_map()

    if not rename_map:
        print("All files in assets/img/ are already kebab-case. Nothing to do.")
        return

    print(f"Found {len(rename_map)} files to rename.")
    for old, new in sorted(rename_map.items()):
        print(f"  {Path(old).name}")
        print(f"    -> {Path(new).name}")

    if dry_run:
        print("\n[dry-run] No changes made.")
        return

    print("\nUpdating references in text files (before renaming)...")
    changed_files = update_text_files(rename_map)
    print(f"  Updated {len(changed_files)} file(s):")
    for f in sorted(changed_files):
        print(f"    {f}")

    print("\nRenaming image files...")
    done = rename_files(rename_map)
    print(f"  Renamed {len(done)} file(s).")

    print("\nDone. Run the following to verify:")
    print("  python3 scripts/validate-site.py")
    print("  python3 scripts/check-links.py")


if __name__ == "__main__":
    main()
