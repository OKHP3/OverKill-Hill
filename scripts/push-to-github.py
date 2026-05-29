#!/usr/bin/env python3
"""
push-to-github.py
-----------------
Pushes the unified governance files to all three OKHP3 repos via the GitHub API.

Usage:
    GITHUB_TOKEN=<pat> python3 scripts/push-to-github.py

The PAT needs: repo (read + write contents) scope on all three repos.
"""

import base64
import json
import os
import sys
import urllib.request
import urllib.error

GITHUB_API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
COMMITTER = {
    "name": "OKHP3 Sync Bot",
    "email": "contact@overkillhill.com",
}

# Map of repo -> list of (file_path_in_repo, local_content_path)
REPOS = {
    "OKHP3/OverKill-Hill": [
        ("AGENTS.md", "/tmp/okhp3-sync/okh/AGENTS.md"),
    ],
    "OKHP3/AskJamie": [
        ("AGENTS.md", "/tmp/okhp3-sync/askjamie/AGENTS.md"),
        ("humans.txt", "/tmp/okhp3-sync/askjamie/humans.txt"),
    ],
    "OKHP3/Glee-fullyTools": [
        ("AGENTS.md", "/tmp/okhp3-sync/glee/AGENTS.md"),
        ("CHANGELOG.md", "/tmp/okhp3-sync/glee/CHANGELOG.md"),
        ("CONTRIBUTING.md", "/tmp/okhp3-sync/glee/CONTRIBUTING.md"),
        ("CODE_OF_CONDUCT.md", "/tmp/okhp3-sync/glee/CODE_OF_CONDUCT.md"),
        ("SECURITY.md", "/tmp/okhp3-sync/glee/SECURITY.md"),
        ("llms.txt", "/tmp/okhp3-sync/glee/llms.txt"),
    ],
}


def gh_request(method, path, body=None):
    url = f"{GITHUB_API}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
            "User-Agent": "OKHP3-Sync",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read()), resp.status
    except urllib.error.HTTPError as e:
        body_text = e.read().decode()
        return json.loads(body_text) if body_text else {}, e.code


def get_file_sha(repo, path):
    data, status = gh_request("GET", f"/repos/{repo}/contents/{path}")
    if status == 200:
        return data.get("sha")
    return None


def push_file(repo, repo_path, local_path, commit_message):
    with open(local_path, "r", encoding="utf-8") as f:
        content = f.read()
    encoded = base64.b64encode(content.encode()).decode()

    sha = get_file_sha(repo, repo_path)
    body = {
        "message": commit_message,
        "content": encoded,
        "committer": COMMITTER,
    }
    if sha:
        body["sha"] = sha

    method = "PUT"
    data, status = gh_request(method, f"/repos/{repo}/contents/{repo_path}", body)
    return status, data


def main():
    if not TOKEN:
        print("ERROR: GITHUB_TOKEN environment variable is not set.")
        sys.exit(1)

    print(f"Pushing governance files to {len(REPOS)} repos...\n")
    errors = []

    for repo, files in REPOS.items():
        print(f"--- {repo} ---")
        for repo_path, local_path in files:
            commit_msg = f"chore: sync {repo_path} to unified OKHP3 standard (v2.0)"
            status, result = push_file(repo, repo_path, local_path, commit_msg)
            if status in (200, 201):
                action = "updated" if status == 200 else "created"
                sha_short = (result.get("content", {}) or {}).get("sha", "")[:7]
                print(f"  [{action}] {repo_path}  ({sha_short})")
            else:
                msg = result.get("message", "unknown error")
                print(f"  [FAILED]  {repo_path}  HTTP {status}: {msg}")
                errors.append((repo, repo_path, status, msg))
        print()

    if errors:
        print(f"FAILED: {len(errors)} file(s) could not be pushed:")
        for repo, path, status, msg in errors:
            print(f"  {repo}/{path}  HTTP {status}: {msg}")
        sys.exit(1)
    else:
        print("All files pushed successfully.")


if __name__ == "__main__":
    main()
