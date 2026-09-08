#!/usr/bin/env python3
"""Regression coverage for the Replit static publication boundary."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build-release.py"
COMMIT = "0123456789abcdef0123456789abcdef01234567"


class ReplitStaticPublicationTests(unittest.TestCase):
    def test_static_public_dir_is_the_staged_release(self) -> None:
        config = (ROOT / ".replit").read_text(encoding="utf-8")
        self.assertRegex(config, r'(?m)^deploymentTarget\s*=\s*"static"\s*$')
        self.assertRegex(config, r'(?m)^publicDir\s*=\s*"site-release"\s*$')
        self.assertRegex(config, r'(?m)^build\s*=\s*"python3 scripts/build-replit-release\.py"\s*$')

    def test_replit_builder_replaces_release_only_after_success(self) -> None:
        spec = importlib.util.spec_from_file_location("replit_builder", ROOT / "scripts" / "build-replit-release.py")
        wrapper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(wrapper)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "site-release"
            output.mkdir()
            (output / "old.txt").write_text("old", encoding="utf-8")
            def successful_build(command, cwd, check):
                staged = Path(command[command.index("--output") + 1])
                staged.mkdir(exist_ok=True)
                (staged / "new.txt").write_text("new", encoding="utf-8")

            with patch.object(wrapper, "ROOT", root), patch.object(wrapper, "OUTPUT", output), \
                    patch.object(wrapper, "BUILDER", root / "builder.py"), \
                    patch.object(wrapper, "accepted_commit", return_value="a" * 40), \
                    patch.object(wrapper.subprocess, "run", side_effect=successful_build):
                self.assertEqual(wrapper.main(), 0)
            self.assertEqual((output / "new.txt").read_text(encoding="utf-8"), "new")
            self.assertFalse((output / "old.txt").exists())
            with patch.object(wrapper, "ROOT", root), patch.object(wrapper, "OUTPUT", output), \
                    patch.object(wrapper, "BUILDER", root / "builder.py"), \
                    patch.object(wrapper, "accepted_commit", return_value="c" * 40), \
                    patch.object(wrapper.subprocess, "run", side_effect=successful_build):
                self.assertEqual(wrapper.main(), 0)
            self.assertEqual((output / "new.txt").read_text(encoding="utf-8"), "new")

            def failed_build(*args, **kwargs):
                raise subprocess.CalledProcessError(1, "builder")

            (output / "keep.txt").write_text("keep", encoding="utf-8")
            with patch.object(wrapper, "ROOT", root), patch.object(wrapper, "OUTPUT", output), \
                    patch.object(wrapper, "BUILDER", root / "builder.py"), \
                    patch.object(wrapper, "accepted_commit", return_value="b" * 40), \
                    patch.object(wrapper.subprocess, "run", side_effect=failed_build):
                with self.assertRaises(subprocess.CalledProcessError):
                    wrapper.main()
            self.assertFalse(output.exists())

    def test_accepted_commit_rejects_missing_malformed_and_mismatched_sha(self) -> None:
        spec = importlib.util.spec_from_file_location("replit_builder", ROOT / "scripts/build-replit-release.py")
        wrapper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(wrapper)
        for value in (None, "", "not-a-sha", "a" * 39, "g" * 40):
            with self.subTest(value=value), patch.dict(wrapper.os.environ, {}, clear=True):
                if value is not None:
                    wrapper.os.environ["REPLIT_RELEASE_SHA"] = value
                with self.assertRaises(RuntimeError):
                    wrapper.accepted_commit()

    def test_accepted_commit_rejects_mismatched_sha_and_dirty_checkout(self) -> None:
        spec = importlib.util.spec_from_file_location("replit_builder", ROOT / "scripts/build-replit-release.py")
        wrapper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(wrapper)
        with patch.dict(wrapper.os.environ, {"REPLIT_RELEASE_SHA": "a" * 40}, clear=True), \
                patch.object(wrapper.subprocess, "check_output", side_effect=["b" * 40]):
            with self.assertRaises(RuntimeError):
                wrapper.accepted_commit()
        with patch.dict(wrapper.os.environ, {"REPLIT_RELEASE_SHA": "a" * 40}, clear=True), \
                patch.object(wrapper.subprocess, "check_output", side_effect=["a" * 40, " M index.html"]):
            with self.assertRaises(RuntimeError):
                wrapper.accepted_commit()

    def test_release_path_refuses_symlinks(self) -> None:
        spec = importlib.util.spec_from_file_location("replit_builder", ROOT / "scripts/build-replit-release.py")
        wrapper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(wrapper)
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "target"
            target.mkdir()
            link = Path(temporary) / "link"
            try:
                link.symlink_to(target, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")
            with self.assertRaises(RuntimeError):
                wrapper.refuse_link(link)

    def test_fresh_build_and_verification_failure_leave_public_dir_absent(self) -> None:
        spec = importlib.util.spec_from_file_location("replit_builder", ROOT / "scripts/build-replit-release.py")
        wrapper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(wrapper)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "site-release"

            def fail_verify(command, cwd, check):
                staged = Path(command[command.index("--output") + 1])
                staged.mkdir(exist_ok=True)
                if "--verify" in command:
                    raise subprocess.CalledProcessError(1, command)
                (staged / "new.txt").write_text("new", encoding="utf-8")

            with patch.object(wrapper, "ROOT", root), patch.object(wrapper, "OUTPUT", output), \
                    patch.object(wrapper, "BUILDER", root / "builder.py"), \
                    patch.object(wrapper, "accepted_commit", return_value="a" * 40), \
                    patch.object(wrapper.subprocess, "run", side_effect=fail_verify):
                with self.assertRaises(subprocess.CalledProcessError):
                    wrapper.main()
            self.assertFalse(output.exists())

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
