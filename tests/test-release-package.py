#!/usr/bin/env python3
"""Focused regression coverage for the Pages allowlist boundary."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build-release.py"
COMMIT = "a" * 40


class ReleasePackageTests(unittest.TestCase):
    def build(self, output: Path, source: Path = ROOT) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(BUILDER), "--source", str(source), "--output", str(output), "--commit", COMMIT],
            text=True,
            capture_output=True,
            check=False,
        )

    def verify(self, output: Path, source: Path = ROOT) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(BUILDER), "--verify", "--source", str(source), "--output", str(output), "--commit", COMMIT],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_package_includes_public_routes_and_excludes_repository_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "site-release"
            result = self.build(output)
            self.assertEqual(result.returncode, 0, result.stderr)
            pages = json.loads((ROOT / "site-src/pages.json").read_text(encoding="utf-8"))["pages"]
            for page in pages:
                self.assertTrue((output / page["path"]).is_file(), page["path"])
            self.assertTrue((output / "under-construction.html").is_file())
            self.assertTrue((output / "found-ry/index.html").is_file())
            self.assertTrue((output / "de/index.html").is_file())
            self.assertTrue((output / "es/projects/index.html").is_file())
            for locale in ("en-gb", "es-mx"):
                for route in ("index.html", "about/index.html", "projects/index.html", "contact/index.html"):
                    page = output / locale / route
                    self.assertTrue(page.is_file(), page)
                    self.assertIn('name="robots" content="noindex, follow"', page.read_text(encoding="utf-8"))
            sitemap = (output / "sitemap.xml").read_text(encoding="utf-8")
            search_index = (output / "assets/data/search-index.json").read_text(encoding="utf-8")
            self.assertNotIn("/en-gb/", sitemap)
            self.assertNotIn("/es-mx/", sitemap)
            self.assertNotIn("/en-gb/", search_index)
            self.assertNotIn("/es-mx/", search_index)
            self.assertTrue((output / "assets/downloads/okh-prompt-protocol-template.md").is_file())
            for forbidden in (
                "AGENTS.md", "package-lock.json", "scripts/build-site.py",
                "site-src/pages/index.main.html", "tests/csp-qa.test.mjs",
                "assets/templates/template--homepage.html",
            ):
                self.assertFalse((output / forbidden).exists(), forbidden)
            manifest = json.loads((output / "assets/audit/release-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["commit"], COMMIT)
            self.assertIn("/assets/data/search-index.json", manifest["artifacts"])
            verified = self.verify(output)
            self.assertEqual(verified.returncode, 0, verified.stderr)

            manifest["artifacts"]["/sitemap.xml"]["sha256"] = "0" * 64
            (output / "assets/audit/release-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            mismatched = self.verify(output)
            self.assertNotEqual(mismatched.returncode, 0)
            self.assertIn("hash mismatch", mismatched.stderr)

    def test_rejects_unsafe_source_page_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source"
            shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns(".git", "node_modules"))
            manifest_path = source / "site-src/pages.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["pages"][0]["path"] = "../AGENTS.md"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            result = self.build(Path(temporary) / "site-release", source)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsafe published page path", result.stderr)

    def test_pages_workflow_deploys_only_after_reusable_validation(self) -> None:
        pages_workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        validation_workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", pages_workflow)
        self.assertIn("uses: ./.github/workflows/validate.yml", pages_workflow)
        self.assertRegex(pages_workflow, r"deploy:\n[\s\S]*?needs: validate")
        self.assertRegex(pages_workflow, r"deploy:\n[\s\S]*?group: pages\n\s+cancel-in-progress: false")
        self.assertIn("path: site-release", pages_workflow)
        self.assertIn("actions/download-artifact", pages_workflow)
        self.assertNotIn("Build the explicit public release artifact", pages_workflow)
        self.assertIn("workflow_call:", validation_workflow)
        self.assertRegex(validation_workflow, r"if: github\.event_name != 'schedule'")
        self.assertIn("run: python3 tests/test-release-package.py", validation_workflow)
        self.assertIn("--output site-release", validation_workflow)
        self.assertIn("validated-site-${{ github.sha }}", validation_workflow)


if __name__ == "__main__":
    unittest.main()
