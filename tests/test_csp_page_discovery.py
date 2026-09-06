#!/usr/bin/env python3
"""Regression coverage for CSP public-page discovery."""

from __future__ import annotations

import importlib.util
import unittest
import json
import tempfile
from types import SimpleNamespace
from unittest.mock import patch
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CSP_PATH = ROOT / "scripts" / "csp.py"

spec = importlib.util.spec_from_file_location("csp", CSP_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("could not load scripts/csp.py")
csp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(csp)


class CspPageDiscoveryTests(unittest.TestCase):
    def test_declared_untracked_route_participates_before_git_add(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "site-src").mkdir()
            (root / "new-story.html").write_text("<main>Story</main>", encoding="utf-8")
            (root / "unrelated.html").write_text("<main>Draft</main>", encoding="utf-8")
            (root / "site-src" / "pages.json").write_text(
                json.dumps({"pages": [{"path": "new-story.html"}]}), encoding="utf-8"
            )
            with patch.object(csp, "ROOT", root), patch.object(
                csp.subprocess, "run", return_value=SimpleNamespace(stdout="index.html\n")
            ):
                pages = {p.relative_to(root).as_posix() for p in csp.all_pages()}
            self.assertEqual(pages, {"index.html", "new-story.html"})

    def test_test_fixtures_are_not_public_csp_pages(self) -> None:
        pages = {page.relative_to(ROOT).as_posix() for page in csp.all_pages()}

        self.assertIn("index.html", pages)
        self.assertFalse(any(page.startswith("tests/fixtures/") for page in pages))


if __name__ == "__main__":
    unittest.main(verbosity=2)
