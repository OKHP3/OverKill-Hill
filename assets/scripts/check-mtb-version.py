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


# ── ROADMAP STRUCTURAL VALIDATOR ────────────────────────────────────────────

import re as _re

def check_roadmap_structure():
    """
    Parse the #roadmap <ul> in the MTB project page and assert that the
    progress-marker class sequence is internally consistent:

      1. Exactly one phase has class "progress-marker--active".
      2. All "--done" phases appear before the "--active" phase.
      3. No "--done" marker appears after the "--active" marker.
      4. All phases after "--active" have class "progress-marker--planned".
         (A "--active" followed immediately by another "--active" is covered
          by rule 1, so this rule catches "--done" regressions post-active.)

    Returns (passes: list[str], failures: list[str]) — human-readable messages.
    """
    filepath = "projects/mermaid-theme-builder/index.html"
    passes = []
    failures = []

    try:
        with open(filepath, encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        failures.append(f"roadmap structural check: {filepath} NOT FOUND")
        return passes, failures

    # ── Isolate the #roadmap block ─────────────────────────────────────────
    # Find the opening tag of the roadmap ul: <ul class="progress-track">
    # that sits inside the id="roadmap" div.
    roadmap_start = html.find('id="roadmap"')
    if roadmap_start == -1:
        failures.append('roadmap structural check: id="roadmap" not found in HTML')
        return passes, failures

    ul_start = html.find('<ul class="progress-track">', roadmap_start)
    if ul_start == -1:
        failures.append('roadmap structural check: <ul class="progress-track"> not found after #roadmap')
        return passes, failures

    # Walk forward to find the matching </ul> using tag-depth counting.
    depth = 0
    i = ul_start
    ul_end = -1
    while i < len(html):
        if html[i:i+3] == "<ul":
            depth += 1
            i += 3
        elif html[i:i+5] == "</ul>":
            depth -= 1
            if depth == 0:
                ul_end = i + 5
                break
            i += 5
        else:
            i += 1

    if ul_end == -1:
        failures.append("roadmap structural check: could not find closing </ul> for progress-track")
        return passes, failures

    roadmap_html = html[ul_start:ul_end]

    # ── Extract marker classes in DOM order ───────────────────────────────
    # Each <li> in the roadmap has exactly one <span class="progress-marker progress-marker--*">
    marker_pattern = _re.compile(r'class="progress-marker\s+(progress-marker--(?:done|active|planned))"')
    markers = marker_pattern.findall(roadmap_html)

    if not markers:
        failures.append("roadmap structural check: no progress-marker--* spans found in #roadmap ul")
        return passes, failures

    # ── Rule 1: exactly one --active ──────────────────────────────────────
    active_count = markers.count("progress-marker--active")
    if active_count == 1:
        passes.append(f"roadmap · exactly one --active marker ({len(markers)} phases total)")
    elif active_count == 0:
        failures.append(
            f"roadmap · no --active marker found — roadmap must have exactly one active phase "
            f"(found markers: {markers})"
        )
    else:
        failures.append(
            f"roadmap · {active_count} --active markers found — expected exactly 1 "
            f"(found markers: {markers})"
        )

    # ── Rules 2 & 3: order — done* → active → planned* ───────────────────
    # Find the index of the (first) active marker.
    try:
        active_idx = markers.index("progress-marker--active")
    except ValueError:
        # Already reported above; skip order checks.
        return passes, failures

    done_before_active = all(
        m == "progress-marker--done" for m in markers[:active_idx]
    )
    planned_after_active = all(
        m == "progress-marker--planned" for m in markers[active_idx + 1:]
    )

    if done_before_active:
        passes.append(
            f"roadmap · all phases before --active are --done "
            f"({active_idx} done phase(s) before position {active_idx})"
        )
    else:
        bad = [
            (i, m) for i, m in enumerate(markers[:active_idx])
            if m != "progress-marker--done"
        ]
        failures.append(
            f"roadmap · non-done phase(s) appear before --active at position {active_idx}: "
            + ", ".join(f"position {i} = {m}" for i, m in bad)
        )

    if planned_after_active:
        after_count = len(markers) - active_idx - 1
        passes.append(
            f"roadmap · all phases after --active are --planned "
            f"({after_count} planned phase(s) after position {active_idx})"
        )
    else:
        bad = [
            (i + active_idx + 1, m)
            for i, m in enumerate(markers[active_idx + 1:])
            if m != "progress-marker--planned"
        ]
        failures.append(
            f"roadmap · non-planned phase(s) appear after --active at position {active_idx}: "
            + ", ".join(f"position {i} = {m}" for i, m in bad)
        )

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
    roadmap_passes, roadmap_failures = check_roadmap_structure()

    all_passes   = passes   + [(lbl, "", "") for lbl in roadmap_passes]
    all_failures_str = failures  # original tuples
    roadmap_fail_count = len(roadmap_failures)
    total_failures = len(failures) + roadmap_fail_count

    # ── String-check results ───────────────────────────────────────────────
    if not failures:
        print(f"  ✓ All {len(passes)} version-string checks passed.\n")
    else:
        print(f"  ✗ {len(failures)} stale string(s) found (out of {len(passes) + len(failures)} checks):\n")
        for label, filepath, expected, reason in failures:
            print(f"  [{reason}]  {label}")
            print(f"             file     : {filepath}")
            print(f"             expected : {repr(expected)}")
            print()
        print("  Fix each location above, then re-run this script to confirm.\n")

    # ── Roadmap structural results ─────────────────────────────────────────
    print("  Roadmap structural checks:")
    for msg in roadmap_passes:
        print(f"    ✓ {msg}")
    for msg in roadmap_failures:
        print(f"    ✗ {msg}")
    print()

    if total_failures == 0:
        print(f"  ✓ All checks passed ({len(passes)} version strings + {len(roadmap_passes)} roadmap structure).\n")
        return 0

    print(f"  ✗ {total_failures} failure(s) total — fix the items above and re-run.\n")
    return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
