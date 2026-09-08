#!/usr/bin/env python3
"""Run required translation and detector suites; reject missing or reduced coverage.

Usage: python3 scripts/test-translation-skills.py [--root REPOSITORY]
Uses only the standard library. Tests write disposable fixtures, not site pages.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import unittest


# Baseline floors preserve the current coverage while allowing additions.
SUITES = tuple(
    (f"okhp3-translation-en-us-{pair}", f"test-en-us-to-{pair}.py", 10)
    for pair in ("de-de", "en-uk", "es-es", "es-mx", "fr-fr")
) + (("okhp3-i18n-page-sync", "test_i18n_page_sync.py", 9),)


def load_suite(test_file: Path) -> unittest.TestSuite:
    module_name = test_file.stem.replace("-", "_")
    spec = importlib.util.spec_from_file_location(module_name, test_file)
    if spec is None or spec.loader is None:
        raise ValueError(f"Unable to import test file: {test_file}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(module)
    if loader.errors:
        raise ValueError("\n".join(loader.errors))
    return suite


def collect(root: Path) -> unittest.TestSuite:
    combined = unittest.TestSuite()
    for package, filename, minimum in SUITES:
        test_file = root / ".agents" / "skills" / package / "tests" / filename
        if not test_file.is_file():
            raise ValueError(f"Missing required suite: {test_file}")
        suite = load_suite(test_file)
        count = suite.countTestCases()
        if count < minimum:
            raise ValueError(f"{package}: discovered {count} tests; required minimum {minimum}")
        print(f"{package}: discovered {count} tests (minimum {minimum})", flush=True)
        combined.addTests(suite)
    return combined


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        suite = collect(args.root.resolve())
    except (ValueError, ImportError) as error:
        parser.exit(1, f"Translation suite discovery failed: {error}\n")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
