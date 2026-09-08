#!/usr/bin/env python3
"""Regression coverage for the Replit static publication boundary."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build-release.py"
COMMIT = "0123456789abcdef0123456789abcdef01234567"


class ReplitStaticPublicationTests(unittest.TestCase):
    def test_static_public_dir_is_the_staged_release(self) -> None:
        config = (ROOT / ".replit").read_text(encoding="utf-8")
        self.assertRegex(config, r'(?m)^deploymentTarget\s*=\s*"static"\s*$')
        self.assertRegex(config, r'(?m)^publicDir\s*=\s*"site-release"\s*$')

    def test_allowlisted_release_excludes_private_source_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "site-release"
            result = subprocess.run(
                [sys.executable, str(BUILDER), "--output", str(output), "--commit", COMMIT],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads(
                (output / "assets/audit/release-manifest.json").read_text(encoding="utf-8")
            )
            released = set(manifest["files"])
            for private in (
                "server.py",
                "AGENTS.md",
                "replit.md",
                "site-src/pages.json",
                "scripts/build-release.py",
                "tests/test-preview-server.py",
            ):
                self.assertNotIn(private, released)
                self.assertFalse((output / private).exists(), private)
            self.assertIn("index.html", released)
            self.assertIn("assets/js/app.js", released)


if __name__ == "__main__":
    unittest.main()
