#!/usr/bin/env python3
"""Regression tests for audit-site portability boundaries."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "scripts" / "audit-site.py"

spec = importlib.util.spec_from_file_location("audit_site", AUDIT_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("could not load scripts/audit-site.py")
audit_site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_site)


class AuditSitePortabilityTests(unittest.TestCase):
    def test_search_index_is_read_as_utf8_under_legacy_locale(self) -> None:
        with tempfile.TemporaryDirectory(prefix="audit-site-utf8-") as temporary:
            root = Path(temporary)
            index = root / "assets" / "data" / "search-index.json"
            index.parent.mkdir(parents=True)
            index.write_text(
                json.dumps(
                    {"entries": [{"url": "/café/", "title": "Closing quote: ”"}]},
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            code = """
import importlib.util
import sys
from pathlib import Path

path = Path(sys.argv[1]) / "scripts" / "audit-site.py"
spec = importlib.util.spec_from_file_location("audit_site", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.ROOT = Path(sys.argv[2])
assert module.reconcile_search_index([]) == []
"""
            environment = os.environ.copy()
            environment.update(
                {
                    "LC_ALL": "C",
                    "PYTHONCOERCECLOCALE": "0",
                    "PYTHONUTF8": "0",
                }
            )
            result = subprocess.run(
                [sys.executable, "-c", code, str(ROOT), str(root)],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_main_accepts_repository_relative_and_external_absolute_reports(self) -> None:
        with tempfile.TemporaryDirectory(prefix="audit-site-root-") as root_dir:
            with tempfile.TemporaryDirectory(prefix="audit-site-report-") as report_dir:
                root = Path(root_dir)
                external_report = Path(report_dir) / "audit-report.md"
                original_root = audit_site.ROOT
                audit_site.ROOT = root
                try:
                    for argument, expected in (
                        ("assets/docs/in-repo-report.md", "assets/docs/in-repo-report.md"),
                        (str(external_report), str(external_report.resolve())),
                    ):
                        with self.subTest(report=argument):
                            output = io.StringIO()
                            with patch.object(audit_site, "iter_html_files", return_value=[]), \
                                    patch.object(audit_site, "reconcile_sitemap", return_value=([], [], [])), \
                                    patch.object(audit_site, "reconcile_search_index", return_value=[]), \
                                    patch.object(audit_site, "scan_repo_cruft", return_value=[]), \
                                    patch.object(sys, "argv", [str(AUDIT_PATH), "--quiet", "--report", argument]), \
                                    contextlib.redirect_stdout(output):
                                status = audit_site.main()
                            self.assertEqual(status, 0)
                            report = Path(argument) if Path(argument).is_absolute() else root / argument
                            self.assertTrue(report.is_file())
                            self.assertIn(f"Report written to {expected}", output.getvalue())
                finally:
                    audit_site.ROOT = original_root

    def test_unicode_report_output_survives_cp1252_stdout(self) -> None:
        with tempfile.TemporaryDirectory(prefix="audit-site-console-") as report_dir:
            report = Path(report_dir) / "检查报告.md"
            environment = os.environ.copy()
            environment.update({"PYTHONIOENCODING": "cp1252", "PYTHONUTF8": "0"})
            result = subprocess.run(
                [sys.executable, str(AUDIT_PATH), "--quiet", "--report", str(report)],
                cwd=ROOT,
                env=environment,
                capture_output=True,
                check=False,
            )
            stdout = result.stdout.decode("utf-8", errors="replace")
            stderr = result.stderr.decode("utf-8", errors="replace")
            self.assertEqual(result.returncode, 0, stderr)
            self.assertTrue(report.is_file())
            self.assertIn(f"Report written to {report.resolve()}", stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
