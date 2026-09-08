#!/usr/bin/env python3
"""Build and atomically stage the allowlisted release for Replit Static."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "site-release"
BUILDER = ROOT / "scripts" / "build-release.py"
BACKUP = ROOT / ".replit-release-backup"


def refuse_link(path: Path) -> None:
    if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
        raise RuntimeError(f"refusing linked release path: {path}")


def accepted_commit() -> str:
    value = os.environ.get("REPLIT_RELEASE_SHA", "")
    if len(value) != 40 or any(char not in "0123456789abcdef" for char in value.lower()):
        raise RuntimeError("REPLIT_RELEASE_SHA must be the accepted full 40-character SHA")
    actual = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if actual != value.lower():
        raise RuntimeError("REPLIT_RELEASE_SHA does not match HEAD")
    if subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=all"], cwd=ROOT, text=True).strip():
        raise RuntimeError("checkout must be clean before static publication")
    return value.lower()


def main() -> int:
    commit = accepted_commit()
    refuse_link(OUTPUT)
    refuse_link(BACKUP)
    if BACKUP.exists():
        raise RuntimeError(f"refusing unknown preexisting backup: {BACKUP}")
    staging = Path(tempfile.mkdtemp(prefix="replit-release-", dir=ROOT))
    staged_output = staging / "site-release"
    try:
        subprocess.run(
            [sys.executable, str(BUILDER), "--output", str(staged_output), "--commit", commit],
            cwd=ROOT,
            check=True,
        )
        subprocess.run(
            [sys.executable, str(BUILDER), "--verify", "--source", str(ROOT),
             "--output", str(staged_output), "--commit", commit],
            cwd=ROOT, check=True,
        )
        if OUTPUT.exists():
            OUTPUT.replace(BACKUP)
        staged_output.replace(OUTPUT)
        shutil.rmtree(BACKUP)
        return 0
    except Exception:
        if OUTPUT.exists():
            refuse_link(OUTPUT)
            shutil.rmtree(OUTPUT)
        raise
    finally:
        shutil.rmtree(staging, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
