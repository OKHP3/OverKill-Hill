#!/usr/bin/env python3
"""Focused regressions for the live-edge verifier and merge hook behavior."""

from __future__ import annotations

import importlib.util
import hashlib
import io
import json
import shlex
import sys
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent

spec = importlib.util.spec_from_file_location(
    "verify_live_edge", ROOT / "scripts" / "verify-live-edge.py"
)
if spec is None or spec.loader is None:
    raise RuntimeError("could not load scripts/verify-live-edge.py")
verify_live_edge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify_live_edge)


class VerifyLiveEdgeTests(unittest.TestCase):
    def run_live_edge_fixture(
        self,
        *,
        expected_commit: str | None = None,
        manifest_commit: str = "a" * 40,
        hosting_headers: dict[str, str] | None = None,
    ) -> tuple[int, dict[str, object]]:
        """Run the full verifier against deterministic synthetic edge responses."""
        sitemap = verify_live_edge.canonical_text_bytes(verify_live_edge.SITEMAP)
        search_index = verify_live_edge.canonical_text_bytes(verify_live_edge.SEARCH_INDEX)
        manifest = json.dumps(
            {
                "commit": manifest_commit,
                "artifacts": {
                    "/sitemap.xml": {"sha256": hashlib.sha256(sitemap).hexdigest()},
                    "/assets/data/search-index.json": {
                        "sha256": hashlib.sha256(search_index).hexdigest()
                    },
                },
            }
        ).encode("utf-8")
        html_headers = {
            "content-type": "text/html; charset=utf-8",
            "cache-control": "max-age=600",
            "server": "GitHub.com",
            "x-github-edge-region": "iad",
            "x-github-request-id": "fixture-request",
            "x-fastly-request-id": "fixture-fastly",
        }
        html_headers.update(hosting_headers or {})
        html = (
            '<!doctype html><meta name="robots" content="{robots}">'
            '<link href="/assets/css/theme.css?v=f0de78d0" rel="stylesheet">'
        )
        responses = {
            verify_live_edge.RELEASE_MANIFEST: {
                "ok": True,
                "status": 200,
                "headers": {},
                "body": manifest,
            },
            "/sitemap.xml": {
                "ok": True,
                "status": 200,
                "headers": {"content-type": "application/xml", "cache-control": "max-age=600"},
                "body": sitemap,
            },
            "/assets/data/search-index.json": {
                "ok": True,
                "status": 200,
                "headers": {
                    "content-type": "application/json",
                    "cache-control": "max-age=300",
                },
                "body": search_index,
            },
            "/": {
                "ok": True,
                "status": 200,
                "headers": html_headers,
                "body": html.format(robots="index, follow").encode("utf-8"),
            },
            "/404.html": {
                "ok": True,
                "status": 200,
                "headers": html_headers,
                "body": html.format(robots="noindex").encode("utf-8"),
            },
            "/found-ry/": {
                "ok": True,
                "status": 200,
                "headers": html_headers,
                "body": html.format(robots="noindex").encode("utf-8"),
            },
            "/assets/css/theme.css?v=f0de78d0": {
                "ok": True,
                "status": 200,
                "headers": {
                    "content-type": "text/css",
                    "cache-control": "max-age=31536000, immutable",
                },
                "body": (ROOT / "assets/css/theme.css").read_bytes(),
            },
        }

        def fixture_fetch(_base: str, path: str, _timeout: float) -> dict[str, object]:
            try:
                return responses[path]
            except KeyError as exc:
                raise AssertionError(f"fixture did not define a response for {path}") from exc

        argv = [
            "verify-live-edge.py",
            "--base",
            "https://fixture.example",
            "--hosting",
            "github-pages",
            "--accept-blocked",
        ]
        if expected_commit:
            argv.extend(["--expected-commit", expected_commit])
        with tempfile.TemporaryDirectory(prefix="live-edge-fixture-") as directory:
            report_path = Path(directory) / "report.json"
            argv.extend(["--report", str(report_path)])
            output = io.StringIO()
            with (
                patch.object(verify_live_edge, "fetch", side_effect=fixture_fetch),
                patch.object(verify_live_edge, "load_routes", return_value=(["/"], None)),
                patch.object(sys, "argv", argv),
                redirect_stdout(output),
            ):
                return_code = verify_live_edge.main()
            return return_code, json.loads(report_path.read_text(encoding="utf-8"))

    def test_direct_github_pages_limitations_are_partial_not_failures(self) -> None:
        return_code, report = self.run_live_edge_fixture()

        self.assertEqual(return_code, 0)
        self.assertEqual(report["status"], "PARTIAL")
        self.assertEqual(report["summary"]["failures"], 0)
        self.assertGreater(report["summary"]["blocked"], 0)
        checks = {item["check"]: item for item in report["checks"]}
        self.assertEqual(checks["hosting path"]["status"], "PASS")
        self.assertEqual(checks["route / cache policy"]["status"], "BLOCKED")

    def test_mismatched_release_manifest_fails_despite_pages_limitations(self) -> None:
        return_code, report = self.run_live_edge_fixture(
            expected_commit="b" * 40,
            manifest_commit="c" * 40,
        )

        self.assertEqual(return_code, 1)
        self.assertEqual(report["status"], "FAILED")
        self.assertGreater(report["summary"]["failures"], 0)
        checks = {item["check"]: item for item in report["checks"]}
        self.assertEqual(checks["release manifest"]["status"], "FAIL")
        self.assertEqual(checks["route / cache policy"]["status"], "BLOCKED")

    def test_changed_hosting_path_fails_despite_pages_limitations(self) -> None:
        return_code, report = self.run_live_edge_fixture(
            hosting_headers={"server": "cloudflare", "cf-ray": "fixture-ray"}
        )

        self.assertEqual(return_code, 1)
        self.assertEqual(report["status"], "FAILED")
        checks = {item["check"]: item for item in report["checks"]}
        self.assertEqual(checks["hosting path"]["status"], "FAIL")
        self.assertEqual(checks["route / cache policy"]["status"], "BLOCKED")

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
            if temp_path.drive:
                drive = temp_path.drive.rstrip(":").lower()
                windows_path = str(temp_path).replace("\\", "/")
                posix_temp = f"/mnt/{drive}{windows_path[2:]}"
            else:
                posix_temp = str(temp_path)
            command = (
                f"export PATH={shlex.quote(posix_temp)}:/usr/bin:/bin; "
                "source scripts/post-merge.sh"
            )
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

    def test_post_merge_stops_after_link_check_failure(self) -> None:
        result = self.run_post_merge_with_python_failure("check-links.py")

        self.assertNotEqual(result.returncode, 0)
        output = (result.stderr + result.stdout).decode("utf-8", errors="replace")
        self.assertIn("ERROR: internal link check failed.", output)
        self.assertNotIn("Post-merge: all checks passed.", output)

    def test_post_merge_stops_after_canonical_audit_failure(self) -> None:
        result = self.run_post_merge_with_python_failure("audit-site.py")

        self.assertNotEqual(result.returncode, 0)
        output = (result.stderr + result.stdout).decode("utf-8", errors="replace")
        self.assertIn("ERROR: canonical site audit failed.", output)
        self.assertNotIn("Post-merge: all checks passed.", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
