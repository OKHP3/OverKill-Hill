#!/usr/bin/env python3
"""
release-mtb.py — One-command MTB release helper

Rewrites VERSION_CONFIG in check-mtb-version.py, then delegates to
check-mtb-version.py --update to patch all target files atomically.

Usage:
    python3 scripts/release-mtb.py \\
        --version v0.6.0 \\
        --date "August 2026" \\
        --sprint v0.6.x \\
        --sprint-name "Ko-fi Artifacts"

    # With sprint promotion (old sprint → Shipped, new sprint → Active):
    python3 scripts/release-mtb.py \\
        --version v0.6.0 \\
        --date "August 2026" \\
        --sprint v0.6.x \\
        --sprint-name "Ko-fi Artifacts" \\
        --prev-sprint v0.5.x

    # Preview all changes without writing any files:
    python3 scripts/release-mtb.py ... --dry-run

Exit codes:
    0 — VERSION_CONFIG patched and all 11 checks pass
    1 — argument error or VERSION_CONFIG patch failed
    2 — post-patch check(s) failed (same as check-mtb-version.py exit 2)
"""

import argparse
import re
import subprocess
import sys
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


def patch_version_config(args, dry_run=False):
    """Rewrite the VERSION_CONFIG block in check-mtb-version.py."""
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

    if not dry_run:
        CHECKER.write_text(new_text, encoding="utf-8")


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

    # Step 1: patch VERSION_CONFIG
    action = "Previewing" if args.dry_run else "Patching"
    print(f"[1/2] {action} VERSION_CONFIG in check-mtb-version.py \u2026")
    patch_version_config(args, dry_run=args.dry_run)
    if args.dry_run:
        print("      (dry run \u2014 check-mtb-version.py not written)")
    else:
        print("      Done.")
    print()

    # Step 2: delegate to check-mtb-version.py --update
    cmd = [sys.executable, str(CHECKER), "--update"]
    if args.prev_sprint:
        cmd += ["--prev-sprint", args.prev_sprint]
    if args.dry_run:
        cmd.append("--dry-run")

    print(f"[2/2] Running: {' '.join(str(c) for c in cmd)}")
    print()

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
