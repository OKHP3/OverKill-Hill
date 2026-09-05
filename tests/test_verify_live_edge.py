#!/usr/bin/env python3
"""Focused regressions for the live-edge verifier and merge hook behavior."""

from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

spec = importlib.util.spec_from_file_location(
    "verify_live_edge", ROOT / "scripts" / "verify-live-edge.py"
)
if spec is None or spec.loader is None:
    raise RuntimeError("could not load scripts/verify-live-edge.py")
verify_live_edge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify_live_edge)


class VerifyLiveEdgeTests(unittest.TestCase):
    def test_github_pages_missing_headers_are_explicit_warnings(self) -> None:
        report: list[dict[str, object]] = []
        response = {
            "ok": True,
            "headers": {},
        }

        verify_live_edge.check_headers(report, "route /", response, "github-pages")

        observed = {item["check"]: item for item in report}
        self.assertEqual(observed["route / observed header x-content-type-options"]["status"], "WARN")
        self.assertIn("absent", observed["route / observed header x-content-type-options"]["evidence"])
        self.assertEqual(observed["route / enforcing content-security-policy"]["status"], "WARN")

    def test_matching_enforcing_csp_is_observed_without_policy_claim(self) -> None:
        policy = "default-src 'self'"
        report: list[dict[str, object]] = []

        verify_live_edge.check_headers(
            report,
            "route /",
            {"ok": True, "headers": {"content-security-policy": policy}},
            "github-pages",
        )

        csp = next(item for item in report if "enforcing content-security-policy" in item["check"])
        self.assertEqual(csp["status"], "PASS")
        self.assertEqual(csp["value"], policy)
        self.assertIn("not validated", csp["evidence"])

    def test_wrong_security_header_value_remains_a_failure(self) -> None:
        report: list[dict[str, object]] = []

        verify_live_edge.check_headers(
            report,
            "route /",
            {"ok": True, "headers": {"x-frame-options": "ALLOWALL"}},
            "github-pages",
        )

        frame_check = next(item for item in report if "x-frame-options" in item["check"])
        self.assertEqual(frame_check["status"], "FAIL")

    def test_report_only_csp_is_not_enforcing(self) -> None:
        report: list[dict[str, object]] = []

        verify_live_edge.check_headers(
            report,
            "route /",
            {"ok": True, "headers": {"content-security-policy-report-only": "default-src 'self'"}},
            "github-pages",
        )

        enforcing = next(item for item in report if item["check"].endswith("enforcing content-security-policy"))
        report_only = next(item for item in report if "observed report-only" in item["check"])
        self.assertEqual(enforcing["status"], "WARN")
        self.assertEqual(report_only["status"], "WARN")
        self.assertIn("does not enforce", report_only["evidence"])

    def test_strict_hosting_still_treats_missing_headers_as_failures(self) -> None:
        report: list[dict[str, object]] = []

        verify_live_edge.check_headers(report, "route /", {"ok": True, "headers": {}}, "strict")

        failures = [item for item in report if item["status"] == "FAIL"]
        self.assertGreaterEqual(len(failures), len(verify_live_edge.SECURITY_HEADERS))


class PostMergeTests(unittest.TestCase):
    def run_post_merge_with_python_failure(self, failure_target: str) -> subprocess.CompletedProcess[bytes]:
        with tempfile.TemporaryDirectory(prefix="post-merge-") as temp:
            shim = Path(temp) / "python3"
            shim.write_bytes(
                (
                    "#!/bin/bash\n"
                    f"case \"$*\" in *{failure_target}*) exit 1;; *) exit 0;; esac\n"
                ).encode("utf-8")
            )
            shim.chmod(0o755)
            temp_path = Path(temp).resolve()
            drive = temp_path.drive.rstrip(":").lower()
            windows_path = str(temp_path).replace("\\", "/")
            posix_temp = f"/mnt/{drive}{windows_path[2:]}"
            command = f"export PATH={posix_temp}:/usr/bin:/bin; source scripts/post-merge.sh"
            return subprocess.run(
                ["bash", "-c", command],
                cwd=ROOT,
                capture_output=True,
            )

    def test_post_merge_stops_after_early_failed_subprocess(self) -> None:
        result = self.run_post_merge_with_python_failure("check-mtb-version.py")

        self.assertNotEqual(result.returncode, 0)
        output = (result.stderr + result.stdout).decode("utf-8", errors="replace")
        self.assertIn("ERROR: MTB version check failed", output)
        self.assertNotIn("Post-merge: all checks passed.", output)

    def test_post_merge_stops_after_final_validator_failure(self) -> None:
        result = self.run_post_merge_with_python_failure("validate-site.py")

        self.assertNotEqual(result.returncode, 0)
        output = (result.stderr + result.stdout).decode("utf-8", errors="replace")
        self.assertIn("ERROR: full site validation failed.", output)
        self.assertNotIn("Post-merge: all checks passed.", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
