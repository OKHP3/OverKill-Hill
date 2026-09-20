"""Keep the Python compatibility trial aligned with active validation suites."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def python_test_paths(workflow):
    """Read explicit Python test commands, including unittest module invocation."""
    commands = re.finditer(
        r"^\s*(?:run:\s*)?python3\s+(?:-m\s+unittest\s+)?([^\s]+\.py)",
        workflow, re.MULTILINE,
    )
    return {match[1] for match in commands if Path(match[1]).name.startswith("test")}


def missing_suites(validation, compatibility):
    return python_test_paths(validation) - python_test_paths(compatibility)


class RuntimeCoverageTests(unittest.TestCase):
    def test_all_active_validation_suites_run_in_the_matrix(self):
        validation = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
        compatibility = (ROOT / ".github/workflows/runtime-compatibility.yml").read_text(encoding="utf-8")
        self.assertTrue(python_test_paths(validation), "Validation test inventory must not be empty")
        self.assertEqual(missing_suites(validation, compatibility), set())

    def test_new_active_suite_is_reported_until_added(self):
        validation = "run: python3 -m unittest tests/test-new-boundary.py\n"
        self.assertEqual(missing_suites(validation, ""), {"tests/test-new-boundary.py"})
        self.assertEqual(missing_suites(validation, "run: python3 tests/test-new-boundary.py\n"), set())

    def test_skill_and_script_suites_are_included_but_comments_are_not(self):
        workflow = """
        run: |
          python3 .agents/skills/example/tests/test-example.py
          python3 scripts/test-fixtures.py
          # python3 tests/test-retired.py
          python3 scripts/build-site.py --check
        """
        self.assertEqual(python_test_paths(workflow), {
            ".agents/skills/example/tests/test-example.py", "scripts/test-fixtures.py"})


if __name__ == "__main__":
    unittest.main()
