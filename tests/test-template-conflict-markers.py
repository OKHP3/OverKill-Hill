#!/usr/bin/env python3
"""Prevent unresolved Git merge markers from entering template scaffolds."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKER = re.compile(r"^(<<<<<<<|=======|>>>>>>>)")


class TemplateConflictMarkerTests(unittest.TestCase):
    def test_template_html_has_no_unresolved_merge_markers(self) -> None:
        violations: list[str] = []
        for path in sorted((ROOT / "assets/templates").glob("*.html")):
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if MARKER.match(line):
                    violations.append(f"{path.relative_to(ROOT)}:{line_number}")
        self.assertEqual(violations, [], "unresolved merge markers: " + ", ".join(violations))


if __name__ == "__main__":
    unittest.main()
