#!/usr/bin/env python3
"""Regression tests for project-status surface binding."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECKER_PATH = ROOT / "scripts" / "check-project-status.py"
FIXTURE = ROOT / "tests" / "fixtures" / "project-status" / "swapped-labels.html"

spec = importlib.util.spec_from_file_location("check_project_status", CHECKER_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("could not load scripts/check-project-status.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class ProjectStatusTests(unittest.TestCase):
    def test_swapped_surface_labels_fail_the_scoped_checker(self) -> None:
        registry = {
            "schema": 1,
            "reviewed": "2026-09-05",
            "projects": [
                {
                    "id": "abrahamic-reference-engine",
                    "title": "Abrahamic Reference Engine",
                    "purpose": "Reference engine.",
                    "status": "Active",
                    "surface_status": "Live: Active Build",
                    "version": "v1.1",
                    "reviewed": "2026-09-05",
                    "route": "/projects/abrahamic-reference-engine/",
                },
                {
                    "id": "skillz",
                    "title": "Skillz Forge",
                    "purpose": "Skill catalog.",
                    "status": "Active",
                    "surface_status": "Active / v1.1",
                    "reviewed": "2026-09-05",
                    "route": "/projects/skillz/",
                },
            ],
        }
        with tempfile.TemporaryDirectory(prefix="project-status-") as temp:
            registry_path = Path(temp) / "project-status.json"
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            original_registry = checker.REGISTRY
            original_surfaces = checker.SURFACES
            checker.REGISTRY = registry_path
            checker.SURFACES = (FIXTURE,)
            try:
                with contextlib.redirect_stderr(io.StringIO()):
                    status = checker.main()
            finally:
                checker.REGISTRY = original_registry
                checker.SURFACES = original_surfaces

        self.assertEqual(status, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
