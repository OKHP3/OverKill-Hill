#!/usr/bin/env python3
"""Prevent unresolved Git merge markers from entering tracked site sources."""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKER = re.compile("^(?:" + "<" * 7 + r" .+|" + ">" * 7 + r" .+)$")
TEXT_SUFFIXES = {".css", ".html", ".js", ".json", ".md", ".mjs", ".py", ".sh", ".yaml", ".yml"}


class ConflictMarkerTests(unittest.TestCase):
    def tracked_text_paths(self) -> list[Path]:
        output = subprocess.run(
            ["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True
        ).stdout
        paths = [ROOT / item.decode("utf-8") for item in output.split(b"\0") if item]
        return sorted(path for path in paths if path.suffix.lower() in TEXT_SUFFIXES)

    def test_tracked_text_has_no_unresolved_merge_markers(self) -> None:
        violations: list[str] = []
        for path in self.tracked_text_paths():
            for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if MARKER.match(line):
                    violations.append(f"{path.relative_to(ROOT)}:{line_number}")
        self.assertEqual(violations, [], "unresolved merge markers: " + ", ".join(violations))


if __name__ == "__main__":
    unittest.main()
