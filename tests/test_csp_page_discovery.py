#!/usr/bin/env python3
"""Regression coverage for CSP public-page discovery."""

from __future__ import annotations

import importlib.util
import unittest
import json
import tempfile
import sys
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

    def test_translation_evidence_is_not_a_live_asset_consumer(self) -> None:
        # Saved reviews retain their original hashes; actual locale routes must
        # still participate in every live-page and asset-fingerprint check.
        modules = []
        original_path = sys.path[:]
        try:
            sys.path.insert(0, str(ROOT / "scripts"))
            for filename in ("validate-site.py", "cache-bust.py"):
                module_spec = importlib.util.spec_from_file_location(filename[:-3], ROOT / "scripts" / filename)
                if module_spec is None or module_spec.loader is None:
                    raise RuntimeError(f"could not load scripts/{filename}")
                module = importlib.util.module_from_spec(module_spec)
                module_spec.loader.exec_module(module)
                modules.append(module)
        finally:
            sys.path[:] = original_path
        validator, cache = modules
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            names = {"index.html", "es-mx/index.html", "fr/about/index.html",
                     "i18n/pilot/es-mx/reviewed/index.html"}
            for name in names:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("<main>Example</main>", encoding="utf-8")
            expected = names - {"i18n/pilot/es-mx/reviewed/index.html"}
            with patch.object(csp, "ROOT", root), patch.object(
                csp.subprocess, "run", return_value=SimpleNamespace(stdout="\n".join(names))
            ), patch.object(validator, "ROOT", root):
                self.assertEqual({p.relative_to(root).as_posix() for p in csp.all_pages()}, expected)
                self.assertEqual({p.relative_to(root).as_posix() for p in validator.find_html_files()}, expected)
                self.assertEqual({p.relative_to(root).as_posix() for p in cache.iter_html_files(root)}, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
