#!/usr/bin/env python3
"""Generate deterministic live-edge reports used by Actions-summary tests."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIRECTORY = ROOT / "tests" / "fixtures" / "actions-summary"
VERIFY_PATH = ROOT / "scripts" / "verify-live-edge.py"

VERIFY_SPEC = importlib.util.spec_from_file_location("verify_live_edge", VERIFY_PATH)
if VERIFY_SPEC is None or VERIFY_SPEC.loader is None:
    raise RuntimeError("could not load scripts/verify-live-edge.py")
VERIFY = importlib.util.module_from_spec(VERIFY_SPEC)
VERIFY_SPEC.loader.exec_module(VERIFY)


RUN_AT = "2026-09-08T00:00:00+00:00"
BASE = "https://fixture.example"
FIXTURE_TIMEOUT = 10.0


SCENARIOS: dict[str, dict[str, Any]] = {
    "live-edge-pass.json": {
        "hosting": "strict",
        "expected_commit": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "checks": [
            {
                "check": "release manifest",
                "status": "PASS",
                "evidence": "validated commit aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            },
            {
                "check": "route /",
                "status": "PASS",
                "evidence": "HTTP 200; text/html; charset=utf-8",
            },
            {
                "check": "route / security header x-frame-options",
                "status": "PASS",
                "evidence": "SAMEORIGIN",
            },
        ],
    },
    "live-edge-pages-blocked.json": {
        "hosting": "github-pages",
        "expected_commit": None,
        "checks": [
            {
                "check": "route /",
                "status": "PASS",
                "evidence": "HTTP 200; text/html; charset=utf-8",
            },
            {
                "check": "route / cache policy",
                "status": "BLOCKED",
                "evidence": "GitHub Pages serves this response but does not apply repository _headers; configure the custom edge proxy before treating this policy as enforced",
            },
            {
                "check": "route / security header x-frame-options",
                "status": "BLOCKED",
                "evidence": "GitHub Pages serves this response but does not apply repository _headers; configure the custom edge proxy before treating this policy as enforced",
            },
        ],
    },
    "live-edge-failure.json": {
        "hosting": "strict",
        "expected_commit": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "checks": [
            {
                "check": "release manifest",
                "status": "FAIL",
                "evidence": "expected validated commit bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb, received 'cccccccccccccccccccccccccccccccccccccccc'",
            },
            {
                "check": "route / security header x-frame-options",
                "status": "FAIL",
                "evidence": "expected 'SAMEORIGIN', received 'ALLOWALL'",
            },
            {
                "check": "route / cache policy",
                "status": "BLOCKED",
                "evidence": "GitHub Pages serves this response but does not apply repository _headers; configure the custom edge proxy before treating this policy as enforced",
            },
        ],
    },
}


def report_for(scenario: dict[str, Any]) -> dict[str, Any]:
    checks = scenario["checks"]
    failures = sum(item["status"] == "FAIL" for item in checks)
    blocked = sum(item["status"] == "BLOCKED" for item in checks)
    warnings = sum(item["status"] == "WARN" for item in checks)
    status = "FAILED" if failures else ("PARTIAL" if blocked or warnings else "PASS")
    report = {
        "verifier": "verify-live-edge.py",
        "run_at": RUN_AT,
        "base": BASE,
        "timeout_seconds": FIXTURE_TIMEOUT,
        "hosting": scenario["hosting"],
        "expected_commit": scenario["expected_commit"],
        "status": status,
        "summary": {
            "checks": len(checks),
            "failures": failures,
            "blocked": blocked,
            "warnings": warnings,
        },
        "checks": checks,
    }
    VERIFY.validate_report_shape(report)
    return report


def rendered_fixtures() -> dict[str, str]:
    return {
        name: json.dumps(report_for(scenario), indent=2) + "\n"
        for name, scenario in SCENARIOS.items()
    }


def sync_fixtures(output_directory: Path, *, write: bool) -> list[str]:
    expected = rendered_fixtures()
    problems: list[str] = []
    if write:
        output_directory.mkdir(parents=True, exist_ok=True)

    for name, content in expected.items():
        path = output_directory / name
        if write:
            path.write_text(content, encoding="utf-8")
        elif not path.is_file():
            problems.append(f"missing generated fixture: {path}")
        elif path.read_text(encoding="utf-8") != content:
            problems.append(f"generated fixture is stale: {path}")

    if not write:
        expected_names = set(expected)
        for path in sorted(output_directory.glob("live-edge-*.json")):
            if path.name not in expected_names:
                problems.append(f"unexpected generated fixture: {path}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="fail when committed fixtures differ")
    mode.add_argument("--write", action="store_true", help="write the deterministic fixtures")
    parser.add_argument(
        "--output-directory",
        type=Path,
        default=DEFAULT_OUTPUT_DIRECTORY,
        help="fixture directory (default: tests/fixtures/actions-summary)",
    )
    args = parser.parse_args()
    problems = sync_fixtures(args.output_directory, write=args.write)
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}")
        return 1
    print(
        f"{'wrote' if args.write else 'checked'} "
        f"{len(SCENARIOS)} deterministic Actions-summary fixtures in "
        f"{args.output_directory}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())