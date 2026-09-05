"""Disposable-repository safety tests for scripts/sync-foundation-files.py."""
from __future__ import annotations

import importlib.util
import io
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sync-foundation-files.py"
FILES = ["assets/css/theme.css", "assets/js/app.js", "assets/js/mermaid-init.js"]


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def load_module():
    spec = importlib.util.spec_from_file_location("sync_foundation_files", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def remove_readonly(func, path, _exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


class SyncFoundationSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repos = {}
        for name in ("overkill-hill", "glee-fullytools", "askjamie"):
            repo = self.root / name
            repo.mkdir()
            git(repo, "init")
            git(repo, "config", "user.email", "safety@example.test")
            git(repo, "config", "user.name", "Safety Test")
            for relpath in FILES:
                path = repo / relpath
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("base\n", encoding="utf-8")
            git(repo, "add", ".")
            git(repo, "commit", "-m", "base")
            self.repos[name] = repo
        # The tested script derives this layout from its own path.
        destination = self.repos["overkill-hill"] / "scripts"
        destination.mkdir()
        shutil.copy2(SCRIPT, destination / SCRIPT.name)
        git(self.repos["overkill-hill"], "add", "scripts/sync-foundation-files.py")
        git(self.repos["overkill-hill"], "commit", "-m", "add sync utility")

    def tearDown(self):
        self.temp.cleanup()

    def invoke(self, *args: str):
        return subprocess.run([sys.executable, "scripts/sync-foundation-files.py", *args], cwd=self.repos["overkill-hill"], capture_output=True, text=True)

    def source_revision(self) -> str:
        return git(self.repos["overkill-hill"], "rev-parse", "HEAD")

    def test_lock_is_untouched_and_blocks_writes(self):
        target = self.repos["askjamie"] / FILES[0]
        target.write_text("different\n", encoding="utf-8")
        git(self.repos["askjamie"], "add", FILES[0])
        git(self.repos["askjamie"], "commit", "-m", "different")
        lock = self.repos["glee-fullytools"] / ".git" / "index.lock"
        lock.write_text("do not move\n", encoding="utf-8")
        result = self.invoke("--apply", "--file", "theme.css", "--source-repo", "overkill-hill", "--source-revision", self.source_revision())
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertTrue(lock.exists())
        self.assertEqual(lock.read_text(encoding="utf-8"), "do not move\n")
        self.assertEqual(target.read_text(encoding="utf-8"), "different\n")

    def test_common_git_lock_in_linked_worktree_blocks_writes(self):
        linked = self.repos["glee-fullytools"]
        # ``onerror`` is retained for the Python 3.11 CI runtime; ``onexc``
        # was introduced later and has the same callback shape here.
        shutil.rmtree(linked, onerror=remove_readonly)
        git(self.repos["overkill-hill"], "worktree", "add", "--detach", str(linked))
        linked_theme = linked / FILES[0]
        linked_theme.write_text("linked version\n", encoding="utf-8")
        git(linked, "add", FILES[0])
        git(linked, "commit", "-m", "linked variant")
        common = Path(git(linked, "rev-parse", "--path-format=absolute", "--git-common-dir"))
        lock = common / "packed-refs.lock"
        lock.write_text("do not move\n", encoding="utf-8")
        result = self.invoke("--apply", "--file", "theme.css", "--source-repo", "overkill-hill", "--source-revision", self.source_revision())
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertTrue(lock.exists())
        self.assertEqual(lock.read_text(encoding="utf-8"), "do not move\n")
        self.assertEqual(linked_theme.read_text(encoding="utf-8"), "linked version\n")
        self.assertIn("common Git directory", result.stdout)

    def test_dirty_target_bytes_are_untouched(self):
        target = self.repos["askjamie"] / FILES[0]
        target.write_text("user work\n", encoding="utf-8")
        result = self.invoke("--apply", "--file", "theme.css", "--source-repo", "overkill-hill", "--source-revision", self.source_revision())
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual(target.read_text(encoding="utf-8"), "user work\n")

    def test_write_without_approved_source_is_rejected(self):
        result = self.invoke("--apply", "--file", "theme.css")
        self.assertEqual(result.returncode, 4, result.stdout + result.stderr)
        self.assertIn("writes require", result.stdout)

    def test_failing_hook_prevents_commit_and_accounts_for_output(self):
        module = load_module()
        glee = self.repos["glee-fullytools"]
        (glee / FILES[0]).write_text("older\n", encoding="utf-8")
        git(glee, "add", FILES[0])
        git(glee, "commit", "-m", "older")
        fail = glee / "scripts" / "fail.py"
        fail.parent.mkdir(exist_ok=True)
        fail.write_text("from pathlib import Path\nPath('generated.txt').write_text('made')\nraise SystemExit(1)\n", encoding="utf-8")
        git(glee, "add", "scripts/fail.py")
        git(glee, "commit", "-m", "failing generator")
        module.POST_WRITE_HOOKS = {"glee-fullytools": {FILES[0]: [[sys.executable, "scripts/fail.py"]]}}
        before = git(glee, "rev-parse", "HEAD")
        with redirect_stdout(io.StringIO()), patch.object(module, "mirror_root", return_value=self.root), patch.object(
            sys, "argv", [str(SCRIPT), "--commit", "--file", "theme.css", "--source-repo", "overkill-hill", "--source-revision", self.source_revision()]
        ):
            self.assertEqual(module.main(), 5)
        self.assertEqual(git(glee, "rev-parse", "HEAD"), before)
        status = git(glee, "status", "--short")
        self.assertIn("M assets/css/theme.css", status)
        self.assertIn("?? generated.txt", status)


if __name__ == "__main__":
    unittest.main()
