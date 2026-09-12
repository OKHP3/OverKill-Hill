"""Exercise the CI entry point against disposable package trees."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

RUNNER = Path(__file__).resolve().parents[1] / "scripts/test-translation-skills.py"
SPEC = importlib.util.spec_from_file_location("translation_runner", RUNNER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load translation runner: {RUNNER}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class DiscoveryGuardTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.files = []
        for package, filename, minimum in MODULE.SUITES:
            path = self.root / ".agents" / "skills" / package / "tests" / filename
            path.parent.mkdir(parents=True)
            path.write_text(
                "import unittest\n"
                "class Checks(unittest.TestCase):\n"
                + "".join(f"    def test_{i}(self): self.assertTrue(True)\n" for i in range(minimum))
            )
            self.files.append(path)

    def run_guard(self, success, message):
        result = subprocess.run([sys.executable, str(RUNNER), "--root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0 if success else 1, result.stdout + result.stderr)
        self.assertIn(message, result.stdout + result.stderr)

    def test_complete_inventory_runs_all_tests(self):
        expected = sum(minimum for _package, _filename, minimum in MODULE.SUITES)
        self.run_guard(True, f"Ran {expected} tests")

    def test_missing_translation_suite_fails(self):
        self.files[0].unlink()
        self.run_guard(False, "Missing required suite")

    def test_missing_detector_directory_fails(self):
        self.files[-1].unlink()
        self.files[-1].parent.rmdir()
        self.run_guard(False, "Missing required suite")

    def test_empty_suite_fails(self):
        self.files[0].write_text("import unittest\n")
        self.run_guard(False, "discovered 0 tests")

    def test_reduced_suite_fails(self):
        self.files[0].write_text("import unittest\nclass Checks(unittest.TestCase):\n    def test_one(self): pass\n")
        self.run_guard(False, "required minimum 10")

    def test_other_tests_cannot_mask_an_empty_required_suite(self):
        extra = self.files[0].with_name("test_extra.py")
        extra.write_text(self.files[0].read_text())
        self.files[0].write_text("import unittest\n")
        self.run_guard(False, "discovered 0 tests")

    def test_import_error_fails(self):
        self.files[0].write_text("raise RuntimeError('broken import')\n")
        self.run_guard(False, "broken import")

    def test_test_failure_propagates(self):
        self.files[0].write_text(self.files[0].read_text().replace("assertTrue(True)", "assertTrue(False)", 1))
        self.run_guard(False, "FAILED (failures=1)")


if __name__ == "__main__":
    unittest.main()
