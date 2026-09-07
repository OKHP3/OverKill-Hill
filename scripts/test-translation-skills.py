#!/usr/bin/env python3
"""Run required translation and detector suites; reject missing or reduced coverage.

Usage: python3 scripts/test-translation-skills.py [--root REPOSITORY]
Uses only the standard library. Tests write disposable fixtures, not site pages.
"""

import argparse
from pathlib import Path
import unittest


# Baseline floors preserve the September 7 coverage while allowing additions.
SUITES = tuple(
    (f"okhp3-translation-en-us-{pair}", f"test_en_us_to_{pair.replace('-', '_')}.py", 10)
    for pair in ("de-de", "en-uk", "es-es", "es-mx", "fr-fr")
) + (("okhp3-i18n-page-sync", "test_i18n_page_sync.py", 9),)


def collect(root):
    combined = unittest.TestSuite()
    for package, filename, minimum in SUITES:
        directory = root / ".agents" / "skills" / package / "tests"
        if not (directory / filename).is_file():
            raise ValueError(f"Missing required suite: {directory / filename}")
        loader = unittest.TestLoader()
        required = loader.discover(str(directory), pattern=filename)
        if loader.errors:
            raise ValueError("\n".join(loader.errors))
        count = required.countTestCases()
        if count < minimum:
            raise ValueError(f"{package}: discovered {count} tests; required minimum {minimum}")
        suite = loader.discover(str(directory))
        if loader.errors:
            raise ValueError("\n".join(loader.errors))
        count = suite.countTestCases()
        print(f"{package}: discovered {count} tests (minimum {minimum})", flush=True)
        combined.addTests(suite)
    return combined


def main():
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
