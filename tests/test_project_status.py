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
spec = importlib.util.spec_from_file_location("check_project_status", CHECKER_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("could not load scripts/check-project-status.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class ProjectStatusTests(unittest.TestCase):
    def test_swapped_surface_labels_fail_the_scoped_checker(self) -> None:
        records = [
            {
                "id": "abrahamic-reference-engine",
                "route": "/projects/abrahamic-reference-engine/",
                "kind": "detail",
                "reviewed": "2026-09-05",
                "availability": "Published",
                "maturity": "Active build",
                "evidence": {"url": "https://github.com/OKHP3/OverKill-Hill/blob/" + "a" * 40 + "/README.md", "summary": "Reference source."},
            },
            {
                "id": "skillz",
                "route": "/projects/skillz/",
                "kind": "detail",
                "reviewed": "2026-09-05",
                "availability": "Published",
                "maturity": "Active / v1.1",
                "evidence": {"url": "https://github.com/OKHP3/OverKill-Hill/blob/" + "b" * 40 + "/README.md", "summary": "Catalog source."},
            },
        ]
        with tempfile.TemporaryDirectory(prefix="project-status-") as temp:
            root = Path(temp)
            pages = {}
            for route, record in ((r["route"], r) for r in records):
                page = root / route.lstrip("/") / "index.html"
                page.parent.mkdir(parents=True)
                pages[record["id"]] = page
                page.write_text('<html><head><meta name="robots" content="index, follow"></head><body>'
                                '<main><p data-project-status="%s"><span data-project-status-text="">%s</span> '
                                '<a href="%s">Source record</a> (reviewed %s).</p></main></body></html>'
                                % (record["id"], checker.STATUS["summary"](record), record["evidence"]["url"], record["reviewed"]),
                                encoding="utf-8")
            for route in ("/", "/projects/", "/universe/"):
                page = root / route.lstrip("/") / "index.html"
                page.parent.mkdir(parents=True, exist_ok=True)
                page.write_text("<main></main>", encoding="utf-8")
            (root / "assets/data").mkdir(parents=True)
            (root / "assets/data/search-index.json").write_text(
                json.dumps({"entries": [{"url": r["route"], "body": checker.STATUS["summary"](r)} for r in records]}),
                encoding="utf-8",
            )
            original_root = checker.ROOT
            original_loader = checker.STATUS["load_registry"]
            checker.ROOT = root
            checker.STATUS["load_registry"] = lambda _root: records
            try:
                with contextlib.redirect_stderr(io.StringIO()) as stderr:
                    self.assertEqual(checker.main(), 0)
                pages[records[0]["id"]].write_text(
                    pages[records[0]["id"]].read_text(encoding="utf-8").replace(
                        checker.STATUS["summary"](records[0]), checker.STATUS["summary"](records[1]), 1), encoding="utf-8")
                with contextlib.redirect_stderr(io.StringIO()) as stderr:
                    status = checker.main()
            finally:
                checker.ROOT = original_root
                checker.STATUS["load_registry"] = original_loader

        self.assertEqual(status, 1)
        self.assertIn("stale project summary", stderr.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
