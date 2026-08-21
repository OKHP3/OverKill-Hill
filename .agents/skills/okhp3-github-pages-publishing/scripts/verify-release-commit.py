#!/usr/bin/env python3
"""Read-only gate proving the current Git tree is the validated release commit.

Usage: python3 verify-release-commit.py --expected-sha <full-sha>
Exit 0 only when HEAD equals the expected SHA and the worktree is clean.
"""
import argparse, subprocess, sys
def run(*args):
    return subprocess.run(args, text=True, capture_output=True, check=False)
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--expected-sha", required=True)
    args = ap.parse_args()
    head = run("git", "rev-parse", "HEAD")
    if head.returncode or head.stdout.strip() != args.expected_sha:
        print(f"ERROR: HEAD is {head.stdout.strip() or head.stderr.strip()}, expected {args.expected_sha}", file=sys.stderr); return 1
    status = run("git", "status", "--porcelain")
    if status.returncode:
        print(f"ERROR: cannot inspect worktree: {status.stderr.strip()}", file=sys.stderr); return 1
    if status.stdout:
        print("ERROR: worktree is not clean; refusing release", file=sys.stderr)
        print(status.stdout, file=sys.stderr, end="")
        return 1
    print(f"Release commit verified: {args.expected_sha}")
    print("Worktree clean: yes")
    return 0
if __name__ == "__main__":
    sys.exit(main())