#!/usr/bin/env python3
"""Focused regressions for the live-edge verifier and merge hook behavior."""

from __future__ import annotations

import importlib.util
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
    def test_github_pages_headers_are_recorded_as_observed_limitations(self) -> None:
        report: list[dict[str, object]] = []
        response = {
            "ok": True,
            "headers": {
                "x-content-type-options": "nosniff",
                "x-frame-options": "SAMEORIGIN",
                "referrer-policy": "strict-origin-when-cross-origin",
                "permissions-policy": "accelerometer=()",
                "strict-transport-security": "max-age=63072000; includeSubDomains; preload",
                "cross-origin-opener-policy": "same-origin",
                "cross-origin-resource-policy": "same-origin",
                "origin-agent-cluster": "?1",
            },
        }

        verify_live_edge.check_headers(report, "route /", response, "github-pages")

        observed = {item["check"]: item for item in report}
        self.assertIn("route / observed header x-content-type-options", observed)
        self.assertIn(
            "route / accepted Pages limitation content-security-policy",
            observed,
        )
        self.assertNotIn("route / security header x-content-type-options", observed)

    def test_strict_hosting_still_treats_missing_headers_as_failures(self) -> None:
        report: list[dict[str, object]] = []

        verify_live_edge.check_headers(report, "route /", {"ok": True, "headers": {}}, "strict")

        failures = [item for item in report if item["status"] == "FAIL"]
        self.assertGreaterEqual(len(failures), len(verify_live_edge.SECURITY_HEADERS))


if __name__ == "__main__":
    unittest.main(verbosity=2)
