#!/usr/bin/env python3
"""Contract tests for the shared production-page discovery boundary."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load_script(name: str):
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PublicPageBoundaryTests(unittest.TestCase):
    def test_all_four_scanners_exclude_non_public_fixture_directories(self) -> None:
        validator = load_script("validate-site")
        auditor = load_script("audit-site")
        search = load_script("build-search-index")
        links = load_script("check-links")

        with tempfile.TemporaryDirectory(prefix="public-page-boundary-") as directory:
            root = Path(directory)
            public_page = root / "index.html"
            public_page.write_text(
                "<html><head><title>Public</title></head>"
                "<body><main><h1>Public</h1></main></body></html>",
                encoding="utf-8",
            )
            excluded_directories = (
                "tests/fixtures",
                "i18n/pilot",
                "site-src/pages",
                ".local/browser-fixtures",
                "assets/templates",
                "assets/partials",
            )
            for relative_directory in excluded_directories:
                fixture = root / relative_directory / "fixture.html"
                fixture.parent.mkdir(parents=True, exist_ok=True)
                fixture.write_text("<html><body>fixture</body></html>", encoding="utf-8")

            validator_root = validator.ROOT
            auditor_root = auditor.ROOT
            search_root = search.ROOT
            links_root = links.ROOT
            validator.ROOT = auditor.ROOT = search.ROOT = links.ROOT = root
            try:
                inventories = {
                    "validate-site": {
                        path.relative_to(root).as_posix()
                        for path in validator.find_html_files()
                    },
                    "audit-site": {
                        path.relative_to(root).as_posix()
                        for path in auditor.iter_html_files()
                    },
                    "build-search-index": {
                        path.relative_to(root).as_posix()
                        for path in search.iter_html_files()
                    },
                    "check-links": {
                        path.relative_to(root).as_posix()
                        for path in links.iter_html_files()
                    },
                }
            finally:
                validator.ROOT = validator_root
                auditor.ROOT = auditor_root
                search.ROOT = search_root
                links.ROOT = links_root

            for scanner, inventory in inventories.items():
                with self.subTest(scanner=scanner):
                    self.assertEqual(inventory, {"index.html"})

            self.assertEqual(
                len({frozenset(inventory) for inventory in inventories.values()}),
                1,
                "production scanners must share one public-page boundary",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)