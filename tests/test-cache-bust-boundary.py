"""Regression tests for cache-bust production-page boundaries."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "cache-bust.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("cache_bust", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
cache_bust = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cache_bust)


class CacheBustBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for relative in cache_bust.SHARED_ASSET_PATHS:
            asset = self.root / relative.lstrip("/")
            asset.parent.mkdir(parents=True, exist_ok=True)
            asset.write_text(f"/* {relative} */\n", encoding="utf-8")
        stale = '<script src="/assets/js/app.js"></script>\n'
        self.production = self.root / "index.html"
        self.nested = self.root / ".pr-head" / "stale.html"
        self.nested.parent.mkdir()
        self.tests_fixture = self.root / "tests" / "fixtures.html"
        self.tests_fixture.parent.mkdir()
        self.tests_fixture.write_text(stale, encoding="utf-8")
        self.i18n_fixture = self.root / "i18n" / "pilot" / "reviewed.html"
        self.i18n_fixture.parent.mkdir(parents=True)
        self.i18n_fixture.write_text(stale, encoding="utf-8")
        self.generic_template = self.root / "templates" / "source.html"
        self.generic_template.parent.mkdir()
        self.generic_template.write_text(stale, encoding="utf-8")
        self.asset_template = self.root / "assets" / "templates" / "source.html"
        self.asset_template.parent.mkdir(parents=True)
        self.asset_template.write_text(stale, encoding="utf-8")
        self.production.write_text(stale, encoding="utf-8")
        self.nested.write_text(stale, encoding="utf-8")
        self.patch = patch.object(cache_bust, "ROOT", self.root)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.addCleanup(self.temp.cleanup)

    def run_main(self, *args: str) -> tuple[int, str]:
        with patch("sys.argv", [str(SCRIPT), *args]), redirect_stdout(StringIO()) as output:
            result = cache_bust.main()
        return result, output.getvalue()

    def test_pr_head_is_not_scanned_or_mutated(self) -> None:
        result, output = self.run_main("--check")
        self.assertEqual(result, 1)
        self.assertIn("index.html", output)
        self.assertNotIn(".pr-head/stale.html", output)
        self.assertEqual(self.nested.read_text(encoding="utf-8"), '<script src="/assets/js/app.js"></script>\n')

    def test_shared_boundary_excludes_fixtures_and_generic_templates(self) -> None:
        self.run_main()

        stale = '<script src="/assets/js/app.js"></script>\n'
        for path in (self.nested, self.tests_fixture, self.i18n_fixture, self.generic_template):
            self.assertEqual(path.read_text(encoding="utf-8"), stale)

    def test_asset_templates_remain_cache_bust_inputs(self) -> None:
        result, output = self.run_main("--check")
        self.assertEqual(result, 1)
        self.assertIn("assets/templates/source.html", output)

        self.run_main()
        expected = cache_bust.file_hash(self.root / "assets/js/app.js")
        self.assertIn(f"/assets/js/app.js?v={expected}", self.asset_template.read_text(encoding="utf-8"))

    def test_stale_production_page_is_updated_and_fresh_check_passes(self) -> None:
        result, _ = self.run_main()
        self.assertEqual(result, 0)
        expected = cache_bust.file_hash(self.root / "assets/js/app.js")
        self.assertIn(f"/assets/js/app.js?v={expected}", self.production.read_text(encoding="utf-8"))
        self.assertEqual(self.nested.read_text(encoding="utf-8"), '<script src="/assets/js/app.js"></script>\n')
        result, output = self.run_main("--check")
        self.assertEqual(result, 0, output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
