"""Regression tests for cache-bust production-page boundaries."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "cache-bust.py"
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
        self.production = self.root / "index.html"
        self.nested = self.root / ".pr-head" / "stale.html"
        self.nested.parent.mkdir()
        stale = '<script src="/assets/js/app.js"></script>\n'
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
