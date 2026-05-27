#!/usr/bin/env python3
"""
check-mtb-version.py — MTB release version consistency checker

On every MTB release, update VERSION_CONFIG (the only block you touch),
then run this script to verify every structured version string across the
project page and replit.md is in sync.

Usage:
    python3 assets/scripts/check-mtb-version.py

Exit codes:
    0 — all checks pass
    1 — one or more strings are stale
"""

# ── SINGLE SOURCE OF TRUTH ─────────────────────────────────────────────────
# Edit ONLY this block when cutting a new MTB release.

VERSION_CONFIG = {
    # The released version tag, e.g. "v0.6.0"
    "current_version": "v0.5.0",

    # Month + year the version shipped, e.g. "August 2026"
    "shipped_date": "May 2026",

    # The active sprint series label, e.g. "v0.6.x"
    "active_sprint": "v0.5.x",

    # The active sprint short name (no series prefix), e.g. "Ko-fi Artifacts"
    "active_sprint_name": "SKILL.md Hardening",
}

# ── DERIVED STRINGS (do not edit) ──────────────────────────────────────────

v   = VERSION_CONFIG["current_version"]
sd  = VERSION_CONFIG["shipped_date"]
sp  = VERSION_CONFIG["active_sprint"]
spn = VERSION_CONFIG["active_sprint_name"]

EXPECTED = {
    # Key: human label shown in the report
    # Val: (file_path, substring that must appear verbatim in that file)

    # ── projects/mermaid-theme-builder/index.html ──────────────────────────

    "release card h2":
        ("projects/mermaid-theme-builder/index.html",
         f"{v} — Shipped {sd}"),

    "release card · Version meta-val":
        ("projects/mermaid-theme-builder/index.html",
         f"{v} — shipped {sd}"),

    "release card · Active Sprint meta-val":
        ("projects/mermaid-theme-builder/index.html",
         f"{sp} {spn}"),

    "hero tag":
        ("projects/mermaid-theme-builder/index.html",
         f"{sp} Alpha Active"),

    "roadmap · shipped phase title":
        ("projects/mermaid-theme-builder/index.html",
         f"{v} — Baseline Shipped"),

    "roadmap · active phase title":
        ("projects/mermaid-theme-builder/index.html",
         f"{sp} — {spn}"),

    "roadmap · active phase marker class":
        ("projects/mermaid-theme-builder/index.html",
         "progress-marker--active"),

    "sidebar · Status meta-val":
        ("projects/mermaid-theme-builder/index.html",
         f"{sp} Alpha Active"),

    "sidebar · Build Phase meta-val":
        ("projects/mermaid-theme-builder/index.html",
         f"{sp} {spn}"),

    # ── replit.md ──────────────────────────────────────────────────────────

    "replit.md · current version line":
        ("replit.md",
         f"**Current version:** {v}"),

    "replit.md · active sprint":
        ("replit.md",
         f"Active sprint: {sp} {spn}"),
}

# ── CHECKER ────────────────────────────────────────────────────────────────

def run_checks():
    file_cache = {}
    failures = []
    passes = []

    for label, (filepath, expected_sub) in EXPECTED.items():
        if filepath not in file_cache:
            try:
                with open(filepath, encoding="utf-8") as f:
                    file_cache[filepath] = f.read()
            except FileNotFoundError:
                failures.append((label, filepath, expected_sub, "FILE NOT FOUND"))
                continue

        content = file_cache[filepath]
        if expected_sub in content:
            passes.append((label, filepath, expected_sub))
        else:
            failures.append((label, filepath, expected_sub, "NOT FOUND"))

    return passes, failures


def main():
    print()
    print("MTB Version Consistency Check")
    print(f"  current_version : {v}")
    print(f"  shipped_date    : {sd}")
    print(f"  active_sprint   : {sp}")
    print(f"  active_sprint_name: {spn}")
    print()

    passes, failures = run_checks()

    if not failures:
        print(f"  ✓ All {len(passes)} checks passed — no stale version strings detected.\n")
        return 0

    print(f"  ✗ {len(failures)} stale string(s) found (out of {len(passes) + len(failures)} checks):\n")
    for label, filepath, expected, reason in failures:
        print(f"  [{reason}]  {label}")
        print(f"             file     : {filepath}")
        print(f"             expected : {repr(expected)}")
        print()

    print("  Fix each location above, then re-run this script to confirm.\n")
    return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
