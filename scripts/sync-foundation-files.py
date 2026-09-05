#!/usr/bin/env python3
"""Safely synchronize the three byte-identical cross-site foundation files.

This tool is deliberately an audit by default. It never chooses a winner from
commit dates, file mtimes, or the hub repository. To write, name both a source
checkout and the exact 40-character source commit:

    python3 scripts/sync-foundation-files.py
    python3 scripts/sync-foundation-files.py --apply --source-repo overkill-hill --source-revision <full-commit-sha>
    python3 scripts/sync-foundation-files.py --commit --source-repo overkill-hill --source-revision <full-commit-sha>

Before any write it fails closed when any sibling checkout is dirty, staged,
untracked, or has a Git lock. Locks are reported only; this script never
renames or deletes them. Source bytes come from the named commit, not its
working tree. Post-write hooks run by default; generated paths are recorded.
A failed hook prevents all commits.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

FOUNDATION_FILES = ["assets/css/theme.css", "assets/js/app.js", "assets/js/mermaid-init.js"]
FOUNDATION_CONTRACT = "byte-identical compatible superset (ADR-0001)"
REPO_DIRS = ["overkill-hill", "glee-fullytools", "askjamie"]
POST_WRITE_HOOKS = {"glee-fullytools": {"assets/css/theme.css": [["python3", "scripts/sync-css-version.py"], ["python3", "scripts/sync-portfolio-stats.py"]]}}
SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")


def run(repo: Path, command: list[str], timeout: int = 30):
    return subprocess.run(command, cwd=repo, capture_output=True, text=True, timeout=timeout)


def mirror_root() -> Path:
    return Path(__file__).resolve().parents[2]


def discover_repos(root: Path) -> dict[str, Path]:
    return {name: root / name for name in REPO_DIRS}


def git_dir(repo: Path) -> Path | None:
    result = run(repo, ["git", "rev-parse", "--absolute-git-dir"])
    return Path(result.stdout.strip()) if result.returncode == 0 else None


def git_metadata_dirs(repo: Path) -> list[tuple[str, Path]]:
    """Return the worktree and common Git dirs, without assuming .git is a directory."""
    worktree_dir = git_dir(repo)
    common = run(repo, ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"])
    if worktree_dir is None or common.returncode:
        return []
    common_dir = Path(common.stdout.strip())
    directories = [("worktree Git directory", worktree_dir.resolve())]
    if common_dir.resolve() != worktree_dir.resolve():
        directories.append(("common Git directory", common_dir.resolve()))
    return directories


def git_locks(repo: Path) -> list[tuple[str, Path]]:
    """Find every lock in resolved Git metadata, including linked-worktree common state."""
    locks: dict[Path, str] = {}
    for label, directory in git_metadata_dirs(repo):
        for lock in directory.rglob("*.lock"):
            locks.setdefault(lock.resolve(), label)
    return [(label, lock) for lock, label in sorted(locks.items(), key=lambda item: str(item[0]))]


def validate_repos(repos: dict[str, Path]) -> list[str]:
    return [f"{name}: not a usable git checkout at {repo}" for name, repo in repos.items() if not repo.is_dir() or git_dir(repo) is None]


def safety_problems(repos: dict[str, Path]) -> list[str]:
    """Inspect every mutable-state hazard without changing any checkout."""
    problems = []
    for name, repo in repos.items():
        metadata_dirs = git_metadata_dirs(repo)
        if not metadata_dirs:
            continue
        locks = [f"{label}: {lock}" for label, lock in git_locks(repo)]
        if locks:
            problems.append(f"{name}: Git lock present ({', '.join(locks)})")
        status = run(repo, ["git", "status", "--porcelain=v1", "--untracked-files=all"])
        if status.returncode:
            problems.append(f"{name}: cannot inspect git status: {status.stderr.strip()}")
        elif status.stdout.strip():
            problems.append(f"{name}: working tree is not clean ({status.stdout.strip().splitlines()[0]})")
    return problems


def read_worktree(repo: Path, relpath: str) -> bytes | None:
    path = repo / relpath
    return path.read_bytes() if path.is_file() else None


def source_bytes(repo: Path, revision: str, relpath: str) -> tuple[bytes | None, str | None]:
    result = subprocess.run(["git", "show", f"{revision}:{relpath}"], cwd=repo, capture_output=True, timeout=30)
    return (result.stdout, None) if result.returncode == 0 else (None, result.stderr.decode(errors="replace").strip() or f"{relpath} absent from source revision")


def resolve_revision(repo: Path, revision: str) -> tuple[str | None, str | None]:
    if not SHA_RE.fullmatch(revision):
        return None, "--source-revision must be an explicit full 40-character commit SHA"
    result = run(repo, ["git", "rev-parse", "--verify", f"{revision}^{{commit}}"])
    if result.returncode:
        return None, result.stderr.strip() or "source revision is not a commit in the selected source repository"
    resolved = result.stdout.strip()
    return (resolved, None) if resolved.lower() == revision.lower() else (None, "source revision did not resolve exactly")


def status_paths(repo: Path) -> list[str]:
    result = run(repo, ["git", "status", "--porcelain=v1", "--untracked-files=all"])
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git status failed")
    return [line[3:] for line in result.stdout.splitlines() if len(line) >= 4]


def inspect(files: list[str], repos: dict[str, Path]) -> list[dict]:
    report = []
    for relpath in files:
        groups: dict[str, list[str]] = {}
        for name, repo in repos.items():
            content = read_worktree(repo, relpath)
            fingerprint = "missing" if content is None else hashlib.sha256(content).hexdigest()
            groups.setdefault(fingerprint, []).append(name)
        report.append({"file": relpath, "status": "in-sync" if len(groups) == 1 and "missing" not in groups else "diverged", "groups": groups})
    return report


def apply(files: list[str], repos: dict[str, Path], source_name: str, revision: str, hooks: bool) -> tuple[dict, list[str]]:
    selected, errors = {}, []
    for relpath in files:
        content, error = source_bytes(repos[source_name], revision, relpath)
        if error:
            errors.append(f"{relpath}: {error}")
        else:
            selected[relpath] = content
    if errors:
        return {}, errors
    account = {name: {"foundation_writes": [], "generated_changes": [], "hook_results": []} for name in repos}
    for name, repo in repos.items():
        for relpath, content in selected.items():
            if read_worktree(repo, relpath) != content:
                (repo / relpath).write_bytes(content)
                account[name]["foundation_writes"].append(relpath)
        if hooks:
            for relpath in account[name]["foundation_writes"]:
                for command in POST_WRITE_HOOKS.get(name, {}).get(relpath, []):
                    result = run(repo, command, timeout=90)
                    account[name]["hook_results"].append({"command": command, "returncode": result.returncode, "stderr": result.stderr.strip()})
                    if result.returncode:
                        errors.append(f"{name}: hook {' '.join(command)} failed ({result.returncode})")
        changed = status_paths(repo)
        account[name]["all_changes"] = changed
        account[name]["generated_changes"] = sorted(set(changed) - set(account[name]["foundation_writes"]))
    return account, errors


def commit(repo: Path, paths: list[str], message: str) -> tuple[bool, str]:
    if not paths:
        return True, "no changes"
    locks = git_locks(repo)
    if locks:
        return False, "Git lock present; refusing to stage or commit"
    added = run(repo, ["git", "add", "--", *paths])
    if added.returncode:
        return False, added.stderr.strip() or "git add failed"
    if set(status_paths(repo)) != set(paths):
        return False, "refusing commit: accounted paths differ from status"
    result = run(repo, ["git", "commit", "-m", message])
    return result.returncode == 0, (result.stdout or result.stderr).strip()


def emit(report: dict) -> None:
    print(json.dumps(report, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="write from an explicitly selected immutable source commit")
    parser.add_argument("--commit", action="store_true", help="write and commit every accounted change (implies --apply)")
    parser.add_argument("--source-repo", choices=REPO_DIRS, help="checkout containing the approved source commit")
    parser.add_argument("--source-revision", help="approved full 40-character source commit SHA")
    parser.add_argument("--no-hooks", action="store_true", help="explicitly skip configured post-write generators")
    parser.add_argument("--file", action="append", dest="requested_files", help="foundation basename or path; repeatable")
    parser.add_argument("--json", action="store_true", help="emit machine-readable report")
    args = parser.parse_args()
    writing = args.apply or args.commit
    root = mirror_root()
    repos = discover_repos(root)
    problems = validate_repos(repos)
    if problems:
        emit({"error": "invalid repository configuration", "problems": problems})
        return 3
    files = FOUNDATION_FILES
    if args.requested_files:
        wanted = set(args.requested_files)
        files = [path for path in FOUNDATION_FILES if path in wanted or Path(path).name in wanted]
        if not files:
            parser.error("--file did not match a foundation file")
    report = {"mirror_root": str(root), "mode": "commit" if args.commit else "apply" if args.apply else "dry-run", "foundation_contract": FOUNDATION_CONTRACT, "inspection": inspect(files, repos)}
    if not writing:
        report["next_step"] = "Audit only. Supply --apply/--commit with --source-repo and an approved full --source-revision SHA to write."
        emit(report)
        return 0
    if not args.source_repo or not args.source_revision:
        report["error"] = "writes require --source-repo and --source-revision"
        emit(report)
        return 4
    revision, error = resolve_revision(repos[args.source_repo], args.source_revision)
    if error:
        report["error"] = error
        emit(report)
        return 4
    hazards = safety_problems(repos)
    if hazards:
        report.update({"error": "refusing to write because sibling repositories are not safe", "safety_problems": hazards})
        emit(report)
        return 2
    account, errors = apply(files, repos, args.source_repo, revision, not args.no_hooks)
    report.update({"source": {"repo": args.source_repo, "revision": revision}, "change_account": account})
    if errors:
        report.update({"error": "post-write validation/generation failed; no commits were attempted", "problems": errors})
        emit(report)
        return 5
    if args.commit:
        commits = {}
        for name, repo in repos.items():
            ok, detail = commit(repo, account[name]["all_changes"], f"Sync foundation files from {args.source_repo}@{revision[:12]}")
            commits[name] = {"ok": ok, "detail": detail}
        report["commits"] = commits
        if not all(item["ok"] for item in commits.values()):
            report["error"] = "one or more commits failed; see change_account for recoverable written paths"
            emit(report)
            return 5
    emit(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
