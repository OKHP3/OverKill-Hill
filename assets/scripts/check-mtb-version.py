#!/usr/bin/env python3
"""
check-mtb-version.py — MTB release version consistency checker + auto-fixer

On every MTB release, update VERSION_CONFIG (the only block you touch),
then run this script to verify every structured version string across the
project page and replit.md is in sync.

Usage:
    python3 assets/scripts/check-mtb-version.py              # check only
    python3 assets/scripts/check-mtb-version.py --dry-run    # preview fixes, no writes
    python3 assets/scripts/check-mtb-version.py --update     # backup + patch + re-verify

Exit codes:
    0 — all checks pass (or dry-run completed)
    1 — one or more strings are stale (check mode)
    2 — patching failed or post-patch re-check still has failures
"""

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

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

# ── REPLACEMENT PATTERNS ───────────────────────────────────────────────────
# Each entry: (file_path, regex, replacement)
#
# Patterns use capture groups for context anchoring so only the exact target
# occurrence is touched.  Backreferences (\1, \2) are used in replacements.
#
# Context anchors used per target:
#   hero tag          → class="tag tag--accent">  …  </span>
#   version meta-val  → status-dot"></span>        …  (lowercase "shipped")
#   active sprint     → <span class="meta-val">    …  </span>  (no status-dot inside)
#   sidebar status    → status-dot"></span>v        …  Alpha Active</span>
#   roadmap shipped   → "Baseline Shipped" is unique literal, no group needed
#   roadmap active    → " — " separator is unique to the roadmap title line
#   replit.md checks  → markdown syntax is unique enough without extra context
#
# "roadmap · active phase marker class" is a structural CSS-class presence
# check — auto-fix is not defined; the script flags it and advises manual fix.

_HTML = "projects/mermaid-theme-builder/index.html"
_MD   = "replit.md"

REPLACEMENTS = {
    # <h2>v0.5.0 — Shipped May 2026</h2>
    "release card h2": (
        _HTML,
        r'(<h2>)v\d+\.\d+\.\d+ — Shipped \w+ \d{4}(</h2>)',
        rf'\g<1>{v} — Shipped {sd}\2',
    ),

    # <span class="meta-val"><span class="status-dot"></span>v0.5.0 — shipped May 2026</span>
    "release card · Version meta-val": (
        _HTML,
        r'(status-dot"></span>)v\d+\.\d+\.\d+ — shipped \w+ \d{4}(</span>)',
        rf'\g<1>{v} — shipped {sd}\2',
    ),

    # <span class="meta-val">v0.5.x SKILL.md Hardening</span>  (both release card + sidebar)
    # Anchor: meta-val span WITHOUT a status-dot child — matches both line 1044 and 1727.
    "release card · Active Sprint meta-val": (
        _HTML,
        r'(<span class="meta-val">)v\d+\.\d+\.x [^<]+(</span>)',
        rf'\g<1>{sp} {spn}\2',
    ),

    # <span class="tag tag--accent">v0.5.x Alpha Active</span>
    "hero tag": (
        _HTML,
        r'(class="tag tag--accent">)v\d+\.\d+\.x Alpha Active(</span>)',
        rf'\g<1>{sp} Alpha Active\2',
    ),

    # v0.5.0 — Baseline Shipped   (plain text inside <li>, no HTML tags around value)
    "roadmap · shipped phase title": (
        _HTML,
        r'v\d+\.\d+\.\d+ — Baseline Shipped',
        f"{v} — Baseline Shipped",
    ),

    # v0.5.x — SKILL.md Hardening   (active phase only — lookahead anchors to phase-pill--active)
    "roadmap · active phase title": (
        _HTML,
        r'v\d+\.\d+\.x — [^\n<]+(?=\n\s+<span class="phase-pill phase-pill--active">)',
        f"{sp} — {spn}",
    ),

    # <span class="meta-val"><span class="status-dot"></span>v0.5.x Alpha Active</span>
    "sidebar · Status meta-val": (
        _HTML,
        r'(status-dot"></span>)v\d+\.\d+\.x Alpha Active(</span>)',
        rf'\g<1>{sp} Alpha Active\2',
    ),

    # sidebar · Build Phase shares same pattern as release card · Active Sprint —
    # both are covered by the "release card · Active Sprint meta-val" replacement above.
    # Listing here as an alias so WARN/SKIP messaging is clear.
    "sidebar · Build Phase meta-val": (
        _HTML,
        r'(<span class="meta-val">)v\d+\.\d+\.x [^<]+(</span>)',
        rf'\g<1>{sp} {spn}\2',
    ),

    # **Current version:** v0.5.0
    "replit.md · current version line": (
        _MD,
        r'(\*\*Current version:\*\* )v\d+\.\d+\.\d+',
        rf'\g<1>{v}',
    ),

    # Active sprint: v0.5.x SKILL.md Hardening
    "replit.md · active sprint": (
        _MD,
        r'(Active sprint: )v\d+\.\d+\.x [^\n]+',
        rf'\g<1>{sp} {spn}',
    ),
}

# Checks with no auto-fix (structural or intentionally excluded)
NO_AUTOFIX = {"roadmap · active phase marker class"}

# ── CHECKER ────────────────────────────────────────────────────────────────

def load_files(labels_map):
    """Return {filepath: content} for every unique file referenced."""
    file_cache = {}
    for _label, (filepath, _sub) in labels_map.items():
        if filepath not in file_cache:
            try:
                file_cache[filepath] = Path(filepath).read_text(encoding="utf-8")
            except FileNotFoundError:
                file_cache[filepath] = None
    return file_cache


def run_checks(file_cache=None):
    if file_cache is None:
        file_cache = load_files(EXPECTED)

    failures = []
    passes = []

    for label, (filepath, expected_sub) in EXPECTED.items():
        content = file_cache.get(filepath)
        if content is None:
            failures.append((label, filepath, expected_sub, "FILE NOT FOUND"))
            continue
        if expected_sub in content:
            passes.append((label, filepath, expected_sub))
        else:
            failures.append((label, filepath, expected_sub, "NOT FOUND"))

    return passes, failures


# ── ROADMAP STRUCTURAL VALIDATOR ────────────────────────────────────────────

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
    marker_pattern = re.compile(r'class="progress-marker\s+(progress-marker--(?:done|active|planned))"')
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


# ── FIXER ──────────────────────────────────────────────────────────────────

def backup_files(filepaths, dry_run=False):
    """Copy each file to /tmp/ with a timestamped suffix."""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backed_up = []
    for fp in filepaths:
        src = Path(fp)
        if not src.exists():
            continue
        dest = Path("/tmp") / f"{src.name}.{stamp}.bak"
        if not dry_run:
            shutil.copy2(src, dest)
        backed_up.append((str(src), str(dest)))
    return backed_up


def apply_fixes(failures, dry_run=False):
    """
    For each failing check that has a REPLACEMENTS entry, substitute the
    stale string with the expected one.  Returns a summary of actions taken.

    Fixes are grouped by file; within a file they are applied sequentially
    on the accumulated content so each pattern sees the result of prior subs.
    """
    fixes_by_file = {}   # filepath -> list of (label, pattern, replacement)
    skipped = []

    for label, filepath, _expected_sub, _reason in failures:
        if label in NO_AUTOFIX:
            skipped.append((label, "no auto-fix defined (structural check — edit manually)"))
            continue
        if label not in REPLACEMENTS:
            skipped.append((label, "no replacement pattern defined"))
            continue
        rep_file, pattern, replacement = REPLACEMENTS[label]
        fixes_by_file.setdefault(rep_file, []).append((label, pattern, replacement))

    results = []   # list of (label, status, detail)

    for filepath, fix_list in fixes_by_file.items():
        try:
            original = Path(filepath).read_text(encoding="utf-8")
        except FileNotFoundError:
            for label, _p, _r in fix_list:
                results.append((label, "ERROR", f"{filepath} not found"))
            continue

        content = original

        for label, pattern, replacement in fix_list:
            new_content, n = re.subn(pattern, replacement, content)
            if n == 0:
                results.append((label, "WARN", f"pattern matched 0 times — verify HTML structure ({pattern!r})"))
            else:
                results.append((label, "FIXED", f"{n} substitution(s) applied"))
                content = new_content

        if content != original:
            if not dry_run:
                Path(filepath).write_text(content, encoding="utf-8")

    for label, reason in skipped:
        results.append((label, "SKIP", reason))

    return results


# ── MAIN ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="MTB release version consistency checker + auto-fixer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Modes:\n"
            "  (no flag)   — report stale strings, exit 1 if any found\n"
            "  --dry-run   — preview what --update would change, no writes\n"
            "  --update    — backup files, patch stale strings, re-verify\n"
        ),
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="auto-patch all stale strings in-place (writes files)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="preview patches without writing any files (implies --update logic)",
    )
    args = parser.parse_args()

    update_mode = args.update or args.dry_run
    dry_run     = args.dry_run

    print()
    print("MTB Version Consistency Check")
    print(f"  current_version    : {v}")
    print(f"  shipped_date       : {sd}")
    print(f"  active_sprint      : {sp}")
    print(f"  active_sprint_name : {spn}")
    if dry_run:
        print("  mode               : DRY-RUN (no files will be written)")
    elif update_mode:
        print("  mode               : UPDATE (files will be patched)")
    print()

    # ── Initial check ──────────────────────────────────────────────────────
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

    # ── Roadmap structural failures can't be auto-fixed ────────────────────
    if roadmap_fail_count and not failures:
        print(f"  ✗ {roadmap_fail_count} roadmap structural failure(s) — fix manually and re-run.\n")
        return 1

    # ── String failures: offer or apply auto-fix ───────────────────────────
    if not update_mode:
        print("  Tip: run with --dry-run to preview fixes, or --update to apply them.\n")
        return 1

    # ── Backup ─────────────────────────────────────────────────────────────
    affected_files = sorted({fp for _l, fp, _e, _r in failures})
    backed_up = backup_files(affected_files, dry_run=dry_run)

    if backed_up:
        bak_label = "  [DRY-RUN] Would back up:" if dry_run else "  Backed up:"
        print(bak_label)
        for src, dest in backed_up:
            print(f"    {src}  →  {dest}")
        print()

    # ── Apply fixes ────────────────────────────────────────────────────────
    action_label = "Dry-run preview" if dry_run else "Applying fixes"
    print(f"  {action_label}:")
    fix_results = apply_fixes(failures, dry_run=dry_run)
    for fix_label, status, detail in fix_results:
        icon = {"FIXED": "✓", "SKIP": "—", "WARN": "!", "ERROR": "✗"}.get(status, "?")
        print(f"  [{icon}] {status:<5}  {fix_label}")
        print(f"              {detail}")
    print()

    if dry_run:
        print("  Dry-run complete — no files were written.\n")
        return 0

    # ── Re-verify ──────────────────────────────────────────────────────────
    print("  Re-verifying after patch …\n")
    passes2, failures2 = run_checks()
    roadmap_passes2, roadmap_failures2 = check_roadmap_structure()

    total_failures2 = len(failures2) + len(roadmap_failures2)
    if total_failures2 == 0:
        print(f"  ✓ All checks pass after patching ({len(passes2)} version strings + {len(roadmap_passes2)} roadmap structure).\n")
        return 0

    print(f"  ✗ {total_failures2} check(s) still failing after patch:\n")
    for label, filepath, expected, reason in failures2:
        print(f"  [{reason}]  {label}")
        print(f"             file     : {filepath}")
        print(f"             expected : {repr(expected)}")
        print()
    for msg in roadmap_failures2:
        print(f"  [STRUCTURAL]  {msg}")
    print()
    print("  Check WARN entries above — a pattern may need updating in REPLACEMENTS.\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
