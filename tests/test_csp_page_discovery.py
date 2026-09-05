#!/usr/bin/env python3
"""Regression coverage for CSP public-page discovery."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CSP_PATH = ROOT / "scripts" / "csp.py"

spec = importlib.util.spec_from_file_location("csp", CSP_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("could not load scripts/csp.py")
csp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(csp)


class CspPageDiscoveryTests(unittest.TestCase):
    def test_test_fixtures_are_not_public_csp_pages(self) -> None:
        pages = {page.relative_to(ROOT).as_posix() for page in csp.all_pages()}

        self.assertIn("index.html", pages)
        self.assertFalse(any(page.startswith("tests/fixtures/") for page in pages))


if __name__ == "__main__":
    unittest.main(verbosity=2)
