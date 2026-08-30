#!/usr/bin/env python3
"""
release-mtb.py — One-command MTB release helper

Rewrites VERSION_CONFIG in check-mtb-version.py, then delegates to
check-mtb-version.py --update to patch all target files. The checker writes
timestamped backups before it changes target files; this is a sequential,
recoverable update rather than an atomic transaction.

Usage:
    python3 scripts/release-mtb.py \\
        --version v0.6.2 \\
        --date "August 2026" \\
        --sprint v0.6.x \\
        --sprint-name "Export & Workflow Polish"

    # With sprint promotion (old sprint → Shipped, new sprint → Active):
    python3 scripts/release-mtb.py \\
        --version v0.7.0 \\
        --date "September 2026" \\
        --sprint v0.7.x \\
        --sprint-name "Session Persistence + Multi-Diagram Canvas" \\
        --prev-sprint v0.6.x

    # Preview all changes without writing any files:
    python3 scripts/release-mtb.py ... --dry-run

Exit codes:
    0 — VERSION_CONFIG patched and all 11 checks pass
    1 — argument error or VERSION_CONFIG patch failed
    2 — post-patch check(s) failed (same as check-mtb-version.py exit 2)
"""

import argparse
import difflib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

CHECKER = Path(__file__).parent / "check-mtb-version.py"


def parse_args():
    p = argparse.ArgumentParser(
        description="One-command MTB release helper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument(
        "--version", required=True, metavar="TAG",
        help='Released version tag, e.g. "v0.6.0"',
    )
    p.add_argument(
        "--date", required=True, metavar="MONTH_YEAR",
        help='Shipped date, e.g. "August 2026"',
    )
    p.add_argument(
        "--sprint", required=True, metavar="SERIES",
        help='Active sprint series label, e.g. "v0.6.x"',
    )
    p.add_argument(
        "--sprint-name", required=True, metavar="NAME", dest="sprint_name",
        help='Sprint short name, e.g. "Ko-fi Artifacts"',
    )
    p.add_argument(
        "--prev-sprint", default="", metavar="SERIES", dest="prev_sprint",
        help='Sprint being closed out, e.g. "v0.5.x" (triggers roadmap pill promotion)',
    )
    p.add_argument(
        "--dry-run", action="store_true",
        help="Preview all changes without writing any files",
    )
    return p.parse_args()


def render_version_config(args):
    """Return the checker with VERSION_CONFIG replaced by release arguments."""
    if not CHECKER.exists():
        print(f"ERROR: {CHECKER} not found", file=sys.stderr)
        sys.exit(1)

    text = CHECKER.read_text(encoding="utf-8")

    new_block = (
        f'VERSION_CONFIG = {{\n'
        f'    # The released version tag, e.g. "v0.6.0"\n'
        f'    "current_version": "{args.version}",\n'
        f'\n'
        f'    # Month + year the version shipped, e.g. "August 2026"\n'
        f'    "shipped_date": "{args.date}",\n'
        f'\n'
        f'    # The active sprint series label, e.g. "v0.6.x"\n'
        f'    "active_sprint": "{args.sprint}",\n'
        f'\n'
        f'    # The active sprint short name (no series prefix), e.g. "Ko-fi Artifacts"\n'
        f'    "active_sprint_name": "{args.sprint_name}",\n'
        f'\n'
        f'    # The sprint being closed out (the one moving from Active \u2192 Shipped).\n'
        f'    # Set this to the old active_sprint label (e.g. "v0.5.x") when cutting a\n'
        f'    # release that promotes a new sprint to active.\n'
        f'    # Leave blank ("") if no sprint promotion is needed this release.\n'
        f'    # Can also be overridden at the CLI with --prev-sprint.\n'
        f'    "prev_sprint": "{args.prev_sprint}",\n'
        f'}}'
    )

    pattern = re.compile(r'VERSION_CONFIG\s*=\s*\{[^}]*\}', re.DOTALL)
    new_text, n = pattern.subn(new_block, text)

    if n == 0:
        print(
            "ERROR: VERSION_CONFIG block not found in check-mtb-version.py\n"
            "       The block must match: VERSION_CONFIG = { ... } (flat dict, no nested braces)",
            file=sys.stderr,
        )
        sys.exit(1)
    if n > 1:
        print(
            f"ERROR: {n} VERSION_CONFIG matches found — expected exactly 1",
            file=sys.stderr,
        )
        sys.exit(1)

    return text, new_text


def print_config_diff(original, proposed):
    """Print the proposed VERSION_CONFIG change for a release dry run."""
    diff = list(difflib.unified_diff(
        original.splitlines(),
        proposed.splitlines(),
        fromfile=str(CHECKER),
        tofile=f"{CHECKER} (proposed)",
        lineterm="",
    ))
    if not diff:
        print("      VERSION_CONFIG already matches the proposed release.")
        return
    for line in diff:
        print(f"      {line}")


def print_summary(args):
    bar = "\u2501" * 54
    mode = "  Mode      : DRY RUN \u2014 no files will be written" if args.dry_run else ""
    lines = [
        "",
        bar,
        "  MTB RELEASE",
        bar,
        f"  Version   : {args.version}",
        f"  Shipped   : {args.date}",
        f"  Sprint    : {args.sprint} \u2014 {args.sprint_name}",
    ]
    if args.prev_sprint:
        lines.append(f"  Closes    : {args.prev_sprint} \u2192 Shipped")
    if mode:
        lines.append(mode)
    lines.append(bar)
    print("\n".join(lines))
    print()


def main():
    args = parse_args()

    print_summary(args)

    # Step 1: render the proposed VERSION_CONFIG. Dry runs pass that proposed
    # checker to the consistency checker so their output describes the requested
    # release rather than the currently committed configuration.
    action = "Previewing" if args.dry_run else "Patching"
    print(f"[1/2] {action} VERSION_CONFIG in check-mtb-version.py \u2026")
    original_checker, proposed_checker = render_version_config(args)
    if args.dry_run:
        print_config_diff(original_checker, proposed_checker)
        print("      (dry run \u2014 check-mtb-version.py not written)")
    else:
        CHECKER.write_text(proposed_checker, encoding="utf-8")
        print("      Done.")
    print()

    # Step 2: delegate to check-mtb-version.py --update. In dry-run mode use a
    # temporary checker copy that carries the proposed configuration.
    checker_path = CHECKER
    temporary_checker = None
    if args.dry_run:
        temporary_checker = tempfile.TemporaryDirectory(prefix="release-mtb-")
        checker_path = Path(temporary_checker.name) / CHECKER.name
        checker_path.write_text(proposed_checker, encoding="utf-8")

    cmd = [sys.executable, str(checker_path), "--update"]
    if args.prev_sprint:
        cmd += ["--prev-sprint", args.prev_sprint]
    if args.dry_run:
        cmd.append("--dry-run")

    print(f"[2/2] Running: {' '.join(str(c) for c in cmd)}")
    print()

    result = subprocess.run(cmd)
    if temporary_checker is not None:
        temporary_checker.cleanup()
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
