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


def main() -> int:
    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    staging = Path(tempfile.mkdtemp(prefix="replit-release-", dir=ROOT))
    staged_output = staging / "site-release"
    backup = ROOT / ".replit-release-backup"
    try:
        subprocess.run(
            [sys.executable, str(BUILDER), "--output", str(staged_output), "--commit", commit],
            cwd=ROOT,
            check=True,
        )
        if backup.exists():
            shutil.rmtree(backup)
        if OUTPUT.exists():
            OUTPUT.replace(backup)
        staged_output.replace(OUTPUT)
        if backup.exists():
            shutil.rmtree(backup)
        return 0
    except Exception:
        if not OUTPUT.exists() and backup.exists():
            backup.replace(OUTPUT)
        raise
    finally:
        shutil.rmtree(staging, ignore_errors=True)
        if backup.exists() and OUTPUT.exists():
            shutil.rmtree(backup, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
