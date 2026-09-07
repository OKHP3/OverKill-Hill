"""Exercise the published Python recipe against a supplied pinned source ZIP.

Run: python tests/test-skillz-install-guide.py --archive /path/to/skillz.zip
The integrity check reads GitHub's public Git tree API. No client is activated.
"""

import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REVISION = "1a8686ce386928cccef04b53ac6bb98e0ab40b61"
PACKAGE = "mermaid/okhp3-universe-map/"
ARCHIVE = None


class InstallGuideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = (ROOT / "site-src/pages/projects/skillz/index.main.html").read_text(encoding="utf-8")
        cls.recipe = html.unescape(re.search(
            r'<pre id="skillz-install-python"[^>]*>(.*?)</pre>', source, re.S
        ).group(1))
        with zipfile.ZipFile(ARCHIVE) as archive:
            prefix = f"skillz-{REVISION}/"
            cls.files = {
                name[len(prefix):]: archive.read(name)
                for name in archive.namelist()
                if name.startswith(prefix + PACKAGE) and not name.endswith("/")
            }
            cls.files["LICENSE"] = archive.read(prefix + "LICENSE")

    def prepare(self, project):
        for name, data in self.files.items():
            target = project / f"skillz-{REVISION}" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)

    def run_recipe(self, project, client=".claude"):
        return subprocess.run(
            [sys.executable, "-c", self.recipe.replace('Path(".claude/', f'Path("{client}/')],
            cwd=project, capture_output=True, text=True,
        )

    def test_public_git_tree_matches_every_archive_byte(self):
        url = f"https://api.github.com/repos/OKHP3/skillz/git/trees/{REVISION}?recursive=1"
        with urllib.request.urlopen(url, timeout=30) as response:
            tree = json.load(response)
        self.assertFalse(tree.get("truncated"))
        expected = {item["path"]: item["sha"] for item in tree["tree"]
                    if item["type"] == "blob" and
                    (item["path"].startswith(PACKAGE) or item["path"] == "LICENSE")}
        self.assertEqual(set(expected), set(self.files))
        self.assertEqual(len(expected), 13)
        for name, data in self.files.items():
            git_blob = f"blob {len(data)}\0".encode() + data
            self.assertEqual(hashlib.sha1(git_blob).hexdigest(), expected[name], name)

    def test_both_client_paths_install_complete_package_and_run_generator_tests(self):
        for client in (".claude", ".github"):
            with self.subTest(client=client), tempfile.TemporaryDirectory() as folder:
                project = Path(folder)
                self.prepare(project)
                result = self.run_recipe(project, client)
                self.assertEqual(result.returncode, 0, result.stderr)
                destination = project / client / "skills/okhp3-universe-map"
                installed = {p.relative_to(destination).as_posix(): p.read_bytes()
                             for p in destination.rglob("*") if p.is_file()}
                expected = {name.removeprefix(PACKAGE): data for name, data in self.files.items()}
                self.assertEqual(installed, expected)
                skill = (destination / "SKILL.md").read_text(encoding="utf-8")
                for resource in re.findall(r'`((?:references|assets|scripts|tests|evals)/[^`]+)`', skill):
                    self.assertTrue((destination / resource).is_file(), resource)
                tests = subprocess.run([sys.executable, str(destination / "tests/test-universe-map.py")],
                                       cwd=project, capture_output=True, text=True)
                self.assertEqual(tests.returncode, 0, tests.stderr)
                self.assertIn("Ran 19 tests", tests.stderr)

    def test_repeat_install_preserves_modified_package(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder)
            self.prepare(project)
            self.assertEqual(self.run_recipe(project).returncode, 0)
            destination = project / ".claude/skills/okhp3-universe-map"
            (destination / "SKILL.md").write_bytes(b"Owner edits must survive.")
            before = {p.relative_to(destination): p.read_bytes() for p in destination.rglob("*") if p.is_file()}
            result = self.run_recipe(project)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("already exists", result.stderr)
            after = {p.relative_to(destination): p.read_bytes() for p in destination.rglob("*") if p.is_file()}
            self.assertEqual(before, after)

    def test_existing_file_is_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder)
            self.prepare(project)
            destination = project / ".claude/skills/okhp3-universe-map"
            destination.parent.mkdir(parents=True)
            destination.write_bytes(b"Existing file")
            self.assertNotEqual(self.run_recipe(project).returncode, 0)
            self.assertEqual(destination.read_bytes(), b"Existing file")

    def test_missing_source_does_not_create_destination(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder)
            result = self.run_recipe(project)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Missing source", result.stderr)
            self.assertFalse((project / ".claude").exists())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    args, remaining = parser.parse_known_args()
    ARCHIVE = args.archive.resolve(strict=True)
    unittest.main(argv=[sys.argv[0], *remaining])
