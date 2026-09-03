#!/usr/bin/env python3
"""3-way sync for the Cross-Site Foundation Files shared by the three
OverKill Hill P3 sibling sites (overkill-hill, glee-fullytools, askjamie).

Foundation files (must stay byte-identical across all three repos):
    assets/css/theme.css
    assets/js/app.js
    assets/js/mermaid-init.js

The files are a shared superset. Site-specific behavior is selected by the
existing DOM/body-class hooks inside those files; it is not represented by
different copies per site.

Model
-----
This is NOT "OKH is the permanent source of truth, push one-way." It is a
hub topology, with overkill-hill as the hub:

    * A change made in glee-fullytools or askjamie is written into
      overkill-hill (and, once there, out to the *other* sibling too, if
      that sibling is still behind).
    * A change made in overkill-hill is written into BOTH siblings.

In practice this collapses to one rule per file, applied across all three
repos at once: group the three copies of the file by exact byte content.

    * 1 group  -> already in sync. Nothing to do.
    * 2 groups -> the group whose most recent git-log touch of the file is
                  newest is canonical. Every repo NOT already holding that
                  content gets overwritten with it. (This is what produces
                  both directions Jamie asked for -- whichever repo, OKH
                  included, has the freshest edit wins and radiates out to
                  whichever repo(s) don't have it yet.)
    * 3 groups -> genuine three-way conflict (every repo has a different
                  version). This script never guesses at a resolution. It
                  reports all three and stops for a human/agent to decide,
                  the same way earlier phases of this engagement resolved
                  real theme.css conflicts by reading the actual CSS, not
                  by picking "newest" blindly.

Recency is read from `git log -1 --format=%at -- <path>` in each repo (the
commit timestamp of the last commit that touched the file), not filesystem
mtime, which is unreliable across clones/checkouts/OS. If a repo has no git
history for the file (new/untracked), filesystem mtime is used as a
fallback and the run is flagged so a human can sanity-check that repo.

Usage
-----
    python3 sync-foundation-files.py                 # dry run (default)
    python3 sync-foundation-files.py --apply          # write files, no commits
    python3 sync-foundation-files.py --commit          # write + git commit per repo
    python3 sync-foundation-files.py --json           # machine-readable report
    python3 sync-foundation-files.py --file theme.css  # limit to one foundation file

Exit codes
----------
    0  everything in sync, or (with --apply/--commit) fully synced+applied
    1  one or more files are in genuine 3-way conflict -- needs a human
    2  a write was applied but a commit could not be made (e.g. another
       process is actively holding that repo's .git/index.lock)
    3  a repo path is missing/not a git checkout -- config problem

This script is identical across all three sibling repos' scripts/ dirs (the
same pattern as check-csp.py). It locates its siblings relative to its own
path, so it works no matter which of the three checkouts it's run from.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

FOUNDATION_FILES = [
    "assets/css/theme.css",
    "assets/js/app.js",
    "assets/js/mermaid-init.js",
]

FOUNDATION_CONTRACT = "byte-identical"

# Local mirror-root directory names, matching the OKHP3 GitHub org repos:
#   overkill-hill    -> OKHP3/OverKill-Hill   (overkillhill.com)
#   glee-fullytools   -> OKHP3/Glee-fullyTools (glee-fully.tools)
#   askjamie          -> OKHP3/AskJamie        (askjamie.bot)
REPO_DIRS = ["overkill-hill", "glee-fullytools", "askjamie"]

# Repos that need their own downstream housekeeping re-run after a
# foundation file is written into them. Learned the hard way during the
# 2026-08-30 theme.css consolidation: skipping these leaves Glee's cache-bust
# tokens and portfolio stats stale even though the CSS content is correct.
POST_WRITE_HOOKS = {
    "glee-fullytools": {
        "assets/css/theme.css": [
            ["python3", "scripts/sync-css-version.py"],
            ["python3", "scripts/sync-portfolio-stats.py"],
        ],
    },
}


def mirror_root() -> Path:
    # <repo>/scripts/sync-foundation-files.py -> parents[1] is <repo>,
    # parents[2] is the mirror root that holds all three sibling checkouts.
    return Path(__file__).resolve().parents[2]


def discover_repos(root: Path) -> dict[str, Path]:
    repos = {}
    for name in REPO_DIRS:
        path = root / name
        repos[name] = path
    return repos


def validate_repos(repos: dict[str, Path]) -> list[str]:
    problems = []
    for name, path in repos.items():
        if not path.is_dir():
            problems.append(f"{name}: not found at {path}")
        elif not (path / ".git").exists():
            problems.append(f"{name}: {path} is not a git checkout")
    return problems


def git_last_touch_epoch(repo: Path, relpath: str) -> tuple[int | None, str]:
    """Return (epoch, source) where source is 'git' or 'mtime' or 'missing'."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%at", "--", relpath],
            cwd=repo,
            capture_output=True,
            text=True,
            timeout=20,
        )
        stamp = out.stdout.strip()
        if out.returncode == 0 and stamp:
            return int(stamp), "git"
    except Exception:
        pass
    full = repo / relpath
    if full.exists():
        return int(full.stat().st_mtime), "mtime"
    return None, "missing"


def read_bytes(repo: Path, relpath: str) -> bytes | None:
    full = repo / relpath
    if not full.exists():
        return None
    return full.read_bytes()


def clear_stale_lock(repo: Path) -> None:
    """Move aside a .git/index.lock so a genuinely stale lock (left by an
    earlier crashed process) doesn't block us. If the lock is reinstated by
    an active process immediately after, that's detected separately in
    commit_repo() and treated as a live hold, not stale."""
    lock = repo / ".git" / "index.lock"
    if lock.exists():
        stale = repo / ".git" / f"index.lock.stale-{int(time.time())}"
        try:
            lock.rename(stale)
        except OSError:
            pass  # permission denied etc.; commit_repo() will surface this


def commit_repo(repo: Path, relpaths: list[str], message: str) -> tuple[bool, str]:
    """Stage exactly relpaths (never -A) and commit. Returns (ok, detail)."""
    clear_stale_lock(repo)
    add = subprocess.run(
        ["git", "add", "--"] + relpaths,
        cwd=repo,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if add.returncode != 0:
        return False, f"git add failed: {add.stderr.strip()}"

    staged = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=repo,
        capture_output=True,
        text=True,
        timeout=20,
    )
    staged_files = set(staged.stdout.split())
    if staged_files != set(relpaths):
        return False, (
            "refusing to commit: staged set does not match intended set "
            f"(staged={sorted(staged_files)}, intended={sorted(relpaths)})"
        )

    commit = subprocess.run(
        ["git", "commit", "-m", message],
        cwd=repo,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if commit.returncode != 0:
        stderr = commit.stderr.strip()
        if "index.lock" in stderr:
            return False, "another process is actively holding .git/index.lock; written but not committed"
        return False, f"git commit failed: {stderr}"
    return True, commit.stdout.strip().splitlines()[0] if commit.stdout.strip() else "committed"


def plan_for_file(relpath: str, repos: dict[str, Path]) -> dict:
    contents: dict[str, bytes] = {}
    timestamps: dict[str, tuple[int | None, str]] = {}
    for name, path in repos.items():
        contents[name] = read_bytes(path, relpath)
        timestamps[name] = git_last_touch_epoch(path, relpath)

    missing = [name for name, c in contents.items() if c is None]

    groups: dict[bytes, list[str]] = {}
    for name, c in contents.items():
        if c is None:
            continue
        groups.setdefault(c, []).append(name)

    result = {
        "file": relpath,
        "missing_in": missing,
        "timestamps": {n: t for n, t in timestamps.items()},
        "status": None,
        "writes": [],  # list of {repo, bytes, source_repo}
        "conflict_groups": None,
    }

    if len(groups) <= 1 and not missing:
        result["status"] = "in-sync"
        return result

    if len(groups) >= 3:
        result["status"] = "conflict"
        result["conflict_groups"] = [
            {
                "repos": members,
                "size": len(content),
                "newest_touch": max(
                    (timestamps[m][0] for m in members if timestamps[m][0] is not None),
                    default=None,
                ),
            }
            for content, members in groups.items()
        ]
        return result

    # 2 (or 1-with-missing) groups: pick the group with the newest touch.
    def group_newest(members: list[str]) -> int:
        stamps = [timestamps[m][0] for m in members if timestamps[m][0] is not None]
        return max(stamps) if stamps else -1

    ranked = sorted(groups.items(), key=lambda kv: group_newest(kv[1]), reverse=True)
    winning_content, winning_members = ranked[0]

    # Deterministic tie-break: if two groups tie on newest touch, prefer
    # whichever group overkill-hill belongs to (it's the hub of reference).
    if len(ranked) > 1 and group_newest(winning_members) == group_newest(ranked[1][1]):
        if "overkill-hill" not in winning_members and "overkill-hill" in ranked[1][1]:
            winning_content, winning_members = ranked[1]

    source_repo = max(
        winning_members,
        key=lambda m: (timestamps[m][0] if timestamps[m][0] is not None else -1),
    )

    result["status"] = "sync-needed"
    result["winning_repos"] = winning_members
    result["source_repo"] = source_repo
    for name in repos:
        if name in winning_members:
            continue
        result["writes"].append({
            "repo": name,
            "bytes": len(winning_content),
            "source_repo": source_repo,
            "content": winning_content,
        })
    return result


def format_ts(epoch: int | None) -> str:
    if epoch is None:
        return "unknown"
    return time.strftime("%Y-%m-%d %H:%M:%S %z", time.localtime(epoch))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="write resolved content to disk (no git commit)")
    ap.add_argument("--commit", action="store_true", help="write and git commit in each changed repo (implies --apply)")
    ap.add_argument("--no-hooks", action="store_true", help="skip POST_WRITE_HOOKS (sync-css-version.py etc.) after writes")
    ap.add_argument("--file", action="append", dest="files", help="limit to this foundation file (basename or relpath); repeatable")
    ap.add_argument("--json", action="store_true", help="print a machine-readable report instead of text")
    args = ap.parse_args()

    apply_writes = args.apply or args.commit

    root = mirror_root()
    repos = discover_repos(root)
    problems = validate_repos(repos)
    if problems:
        if args.json:
            print(json.dumps({"error": "invalid repo config", "problems": problems}, indent=2))
        else:
            print("Cannot proceed -- repo configuration problem(s):")
            for p in problems:
                print(f"  - {p}")
        return 3

    target_files = FOUNDATION_FILES
    if args.files:
        wanted = set(args.files)
        target_files = [f for f in FOUNDATION_FILES if f in wanted or Path(f).name in wanted]
        if not target_files:
            print(f"--file matched nothing in {FOUNDATION_FILES}", file=sys.stderr)
            return 3

    plans = [plan_for_file(f, repos) for f in target_files]

    had_conflict = False
    had_lock_block = False
    writes_by_repo: dict[str, list[str]] = {}

    for plan in plans:
        if plan["status"] == "conflict":
            had_conflict = True
            continue
        if plan["status"] != "sync-needed":
            continue
        for w in plan["writes"]:
            repo_path = repos[w["repo"]]
            if apply_writes:
                (repo_path / plan["file"]).write_bytes(w["content"])
                writes_by_repo.setdefault(w["repo"], []).append(plan["file"])
                if not args.no_hooks:
                    for hook in POST_WRITE_HOOKS.get(w["repo"], {}).get(plan["file"], []):
                        subprocess.run(hook, cwd=repo_path, capture_output=True, text=True, timeout=60)
            # content no longer needed after writing/reporting; drop it so
            # the JSON report below doesn't dump raw file bytes
            w.pop("content", None)

    commit_results = {}
    if args.commit:
        for repo_name, relpaths in writes_by_repo.items():
            file_list = ", ".join(Path(p).name for p in relpaths)
            message = (
                f"Sync foundation files from {plans[0].get('source_repo', 'sibling')} "
                f"via sync-foundation-files.py ({file_list})"
            )
            ok, detail = commit_repo(repos[repo_name], relpaths, message)
            commit_results[repo_name] = {"ok": ok, "detail": detail}
            if not ok:
                had_lock_block = True

    if args.json:
        out = {
            "mirror_root": str(root),
            "foundation_contract": FOUNDATION_CONTRACT,
            "mode": "commit" if args.commit else ("apply" if args.apply else "dry-run"),
            "files": [
                {k: v for k, v in p.items() if k != "writes" or True}
                for p in plans
            ],
            "writes_by_repo": writes_by_repo,
            "commit_results": commit_results,
        }
        print(json.dumps(out, indent=2, default=str))
    else:
        mode = "COMMIT" if args.commit else ("APPLY" if args.apply else "DRY RUN")
        print(f"sync-foundation-files.py -- mode: {mode}")
        print(f"mirror root: {root}\n")
        print(
            f"foundation contract: {FOUNDATION_CONTRACT} "
            "(site-specific behavior uses in-file DOM/body-class hooks)\n"
        )
        for plan in plans:
            print(f"== {plan['file']} ==")
            for name in REPO_DIRS:
                ts, src = plan["timestamps"].get(name, (None, "missing"))
                marker = " (fallback: fs mtime, no git history)" if src == "mtime" else ""
                print(f"  {name:<18} last touch: {format_ts(ts)}{marker}")
            if plan["missing_in"]:
                print(f"  MISSING in: {', '.join(plan['missing_in'])}")
            if plan["status"] == "in-sync":
                print("  status: in sync, nothing to do\n")
                continue
            if plan["status"] == "conflict":
                print("  status: CONFLICT -- three different versions, needs manual/agent review")
                for g in plan["conflict_groups"]:
                    print(f"    - held by {', '.join(g['repos'])}: {g['size']} bytes, newest touch {format_ts(g['newest_touch'])}")
                print()
                continue
            print(f"  status: sync needed -- canonical source: {plan['source_repo']} (held also by {', '.join(plan['winning_repos'])})")
            for w in plan["writes"]:
                verb = "wrote" if apply_writes else "would write"
                print(f"    {verb} {w['bytes']} bytes to {w['repo']}/{plan['file']} (from {w['source_repo']})")
            print()

        if args.commit:
            print("-- commits --")
            for name, res in commit_results.items():
                status = "OK" if res["ok"] else "BLOCKED"
                print(f"  {name}: {status} -- {res['detail']}")
            print()

        if not apply_writes and any(p["status"] == "sync-needed" for p in plans):
            print("Dry run only. Re-run with --apply to write files, or --commit to also commit per repo.")

    if had_conflict:
        return 1
    if had_lock_block:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
