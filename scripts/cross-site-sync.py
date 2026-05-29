#!/usr/bin/env python3
"""
cross-site-sync.py — OKHP3 Universe cross-site CSS/JS synchronisation tool

Usage:
  python3 scripts/cross-site-sync.py --audit
  python3 scripts/cross-site-sync.py --build-drop
  python3 scripts/cross-site-sync.py --build-drop --dry-run

Modes:
  --audit       Fetch each repo's theme.css and app.js from GitHub, compare
                them against the local OKH source-of-truth files, and print
                a structured drift report with pass/fail checks.

  --build-drop  Package the local OKH foundation files (theme.css, app.js,
                mermaid-init.js) into a dated sync zip at:
                  dist/okh-cross-repo-sync-YYYY-MM-DD.zip
                Ready to commit into sibling repos.

  --dry-run     (with --build-drop) print what would go into the zip without
                creating it.

GitHub repos (public, no auth required):
  OKH   : OKHP3/OverKill-Hill
  Glee  : OKHP3/Glee-fullyTools
  Jamie : OKHP3/AskJamie

Canonical branch: main
Foundation files (all three sites carry identical copies):
  assets/css/theme.css
  assets/js/app.js
  assets/js/mermaid-init.js
"""

import argparse
import datetime
import os
import sys
import urllib.request
import zipfile

# ── Configuration ────────────────────────────────────────────────────────────

REPOS = {
    "okh":   "OKHP3/OverKill-Hill",
    "glee":  "OKHP3/Glee-fullyTools",
    "jamie": "OKHP3/AskJamie",
}

REPO_LABELS = {
    "okh":   "OverKill Hill (OKH — source of truth)",
    "glee":  "Glee-fully Tools",
    "jamie": "AskJamie",
}

FOUNDATION_FILES = [
    "assets/css/theme.css",
    "assets/js/app.js",
    "assets/js/mermaid-init.js",
]

BRANCH = "main"

RAW_BASE = "https://raw.githubusercontent.com/{repo}/{branch}/{path}"

# Relative to repo root (where this script is invoked from)
LOCAL_ROOT = "."

# Sync drop destination directory
DIST_DIR = "dist"

# ── Checks run during --audit ────────────────────────────────────────────────
# Each check is a dict:
#   label   : human-readable description
#   file    : foundation file path (relative)
#   pattern : string that must appear in the file for the check to pass
#   target  : "okh" | "all" | "siblings"  — which repos are checked
#   severity: "error" | "warning"

CHECKS = [
    # ── CSS checks ──────────────────────────────────────────────────────────
    {
        "label": "Sprint 2 tokens present (--color-text-heading)",
        "file": "assets/css/theme.css",
        "pattern": "--color-text-heading",
        "target": "okh",
        "severity": "error",
    },
    {
        "label": "Sprint 2 spacing scale present (--space-xs)",
        "file": "assets/css/theme.css",
        "pattern": "--space-xs",
        "target": "okh",
        "severity": "error",
    },
    {
        "label": "Transition tokens present (--transition-fast)",
        "file": "assets/css/theme.css",
        "pattern": "--transition-fast",
        "target": "okh",
        "severity": "error",
    },
    {
        "label": ".header-controls CSS rule present in OKH",
        "file": "assets/css/theme.css",
        "pattern": ".header-controls",
        "target": "okh",
        "severity": "error",
    },
    {
        "label": ".okh-search-trigger light-mode override present in OKH",
        "file": "assets/css/theme.css",
        "pattern": 'data-theme="light"] body:not(.glee-main):not(.askjamie-main) .okh-search-trigger',
        "target": "okh",
        "severity": "error",
    },
    {
        "label": "GLEE section present in CSS (all sites carry the superset)",
        "file": "assets/css/theme.css",
        "pattern": ".glee-main",
        "target": "okh",
        "severity": "warning",
    },
    {
        "label": "ASKJAMIE section present in CSS (all sites carry the superset)",
        "file": "assets/css/theme.css",
        "pattern": ".askjamie-main",
        "target": "okh",
        "severity": "warning",
    },
    # ── JS checks ───────────────────────────────────────────────────────────
    {
        "label": "3-state theme toggle present in OKH JS",
        "file": "assets/js/app.js",
        "pattern": '"system", "light", "dark"',
        "target": "okh",
        "severity": "error",
    },
    {
        "label": ".header-controls JS injection present in OKH",
        "file": "assets/js/app.js",
        "pattern": "header-controls",
        "target": "okh",
        "severity": "error",
    },
    {
        "label": "OKH search trigger class used in OKH JS",
        "file": "assets/js/app.js",
        "pattern": "okh-search",
        "target": "okh",
        "severity": "warning",
    },
    {
        "label": "injectTrigger targets .header-controls in OKH JS",
        "file": "assets/js/app.js",
        "pattern": "injectTrigger",
        "target": "okh",
        "severity": "warning",
    },
    # ── Architecture decisions (2026-05-28) ─────────────────────────────────
    {
        "label": "Warm-paper baseline in OKH CSS light-mode root tokens",
        "file": "assets/css/theme.css",
        "pattern": "--color-surface: #f6f2ee",   # warm paper, not cool white
        "target": "okh",
        "severity": "error",
    },
    {
        "label": "Glee brand light-mode surface override present in OKH GLEE section",
        "file": "assets/css/theme.css",
        "pattern": 'html[data-theme="light"] .glee-main',
        "target": "okh",
        "severity": "error",
    },
    {
        "label": "AskJamie brand light-mode surface override present in OKH ASKJAMIE section",
        "file": "assets/css/theme.css",
        "pattern": 'html[data-theme="light"] .askjamie-main',
        "target": "okh",
        "severity": "error",
    },
    {
        "label": "GA4 bootstrap must NOT live in app.js (belongs inline in HTML <head>)",
        "file": "assets/js/app.js",
        "pattern": "gtag('config'",   # this string should NOT appear in app.js
        "target": "okh",
        "severity": "error",
        "invert": True,               # PASS when pattern is absent
    },
]

# ── Size-drift thresholds (sibling vs OKH) ───────────────────────────────────
# Percentage by which a sibling file may be SMALLER than OKH before flagging.
# (Siblings accumulate their own additions, so being LARGER is fine.)
SIZE_WARN_THRESHOLD = {
    "assets/css/theme.css": 0.30,   # warn if sibling is >30% smaller
    "assets/js/app.js":     0.50,   # warn if sibling is >50% smaller
    "assets/js/mermaid-init.js": 0.20,
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def fetch_remote(repo_key, file_path):
    """Fetch a file from GitHub and return its text content. Returns None on error."""
    url = RAW_BASE.format(
        repo=REPOS[repo_key],
        branch=BRANCH,
        path=file_path,
    )
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as exc:
        return None, str(exc)


def fetch_local(file_path):
    """Read a local file relative to repo root. Returns text or None."""
    full = os.path.join(LOCAL_ROOT, file_path)
    if not os.path.exists(full):
        return None
    with open(full, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def lines(text):
    return text.count("\n") if text else 0


def bytes_of(text):
    return len(text.encode("utf-8")) if text else 0


def pct_diff(a, b):
    """Return (b - a) / a as a signed float, or None if a == 0."""
    if not a:
        return None
    return (b - a) / a


# ── Colour helpers (ANSI — suppressed if not a TTY) ─────────────────────────

USE_COLOR = sys.stdout.isatty()

def _c(code, text):
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text

def green(t):  return _c("32", t)
def red(t):    return _c("31", t)
def yellow(t): return _c("33", t)
def bold(t):   return _c("1",  t)
def dim(t):    return _c("2",  t)


# ── Audit mode ────────────────────────────────────────────────────────────────

def run_audit():
    print(bold("\n══ OKHP3 Cross-Site Sync Audit ══"))
    print(dim(f"  Fetching files from GitHub ({BRANCH} branch) …\n"))

    # 1. Fetch everything
    files = {}  # files[repo_key][file_path] = text | None

    for repo_key in REPOS:
        files[repo_key] = {}
        for fp in FOUNDATION_FILES:
            result = fetch_remote(repo_key, fp)
            if isinstance(result, tuple):
                # error tuple
                files[repo_key][fp] = None
                print(f"  {red('FETCH ERROR')} {repo_key}/{fp}: {result[1]}")
            else:
                files[repo_key][fp] = result

    # Also read OKH local (might differ from what's on GitHub if there are
    # uncommitted local changes — this is intentional: local is the working copy)
    local = {}
    for fp in FOUNDATION_FILES:
        local[fp] = fetch_local(fp)

    # 2. Size comparison table
    print(bold("── File size comparison ──────────────────────────────────────────────"))
    for fp in FOUNDATION_FILES:
        okh_bytes  = bytes_of(files["okh"][fp])
        glee_bytes = bytes_of(files["glee"][fp])
        jamie_bytes= bytes_of(files["jamie"][fp])
        local_bytes= bytes_of(local[fp])
        okh_lines  = lines(files["okh"][fp])
        glee_lines = lines(files["glee"][fp])
        jamie_lines= lines(files["jamie"][fp])
        local_lines= lines(local[fp])

        threshold = SIZE_WARN_THRESHOLD.get(fp, 0.30)

        print(f"\n  {bold(fp)}")
        row_fmt = "    {:<12}  {:>7} lines  {:>9} bytes  {}"

        def size_flag(sibling_bytes, okh_bytes, threshold):
            if sibling_bytes is None or okh_bytes is None or okh_bytes == 0:
                return red("UNKNOWN")
            delta = pct_diff(okh_bytes, sibling_bytes)
            if delta is not None and delta < -threshold:
                return yellow(f"↓ {abs(delta)*100:.0f}% smaller than OKH — check for missing sections")
            return green("OK")

        print(row_fmt.format("OKH (GitHub)", okh_lines, okh_bytes, ""))
        print(row_fmt.format("OKH (local)", local_lines, local_bytes,
            yellow("⚠ local differs from GitHub") if local_bytes != okh_bytes else ""))
        print(row_fmt.format("Glee", glee_lines, glee_bytes,
            size_flag(glee_bytes, okh_bytes, threshold)))
        print(row_fmt.format("Jamie", jamie_lines, jamie_bytes,
            size_flag(jamie_bytes, okh_bytes, threshold)))

    # 3. Pattern checks
    print(f"\n{bold('── Pattern checks (OKH local source-of-truth) ────────────────────────')}")
    errors = 0
    warnings = 0

    for check in CHECKS:
        fp = check["file"]
        pattern = check["pattern"]
        target = check["target"]
        severity = check["severity"]

        if target == "okh":
            sources = {"OKH (local)": local[fp]}
        elif target == "all":
            sources = {
                "OKH (local)": local[fp],
                "Glee":  files["glee"][fp],
                "Jamie": files["jamie"][fp],
            }
        elif target == "siblings":
            sources = {
                "Glee":  files["glee"][fp],
                "Jamie": files["jamie"][fp],
            }
        else:
            sources = {}

        invert = check.get("invert", False)
        for site_label, text in sources.items():
            present = text is not None and pattern in text
            found = (not present) if invert else present
            if found:
                status = green("PASS")
            else:
                status = red("FAIL") if severity == "error" else yellow("WARN")
                if severity == "error":
                    errors += 1
                else:
                    warnings += 1
            print(f"  [{status}] {check['label']}")
            if not found and text is None:
                print(f"        {dim(f'({site_label}: file not fetched)')}")
            break  # one result line per check for OKH-target checks

    print()
    if errors == 0 and warnings == 0:
        print(green("  ✓ All checks passed — OKH is in good shape for a sync drop."))
    else:
        if errors:
            print(red(f"  ✗ {errors} error(s) — resolve before building a sync drop."))
        if warnings:
            print(yellow(f"  ⚠ {warnings} warning(s) — review before the next sync cycle."))

    # 4. Architecture decisions (resolved) + remaining open items
    print(f"\n{bold('── Architecture decisions (2026-05-28) ───────────────────────────────')}")

    resolved = [
        ("✓", "Light-mode surface warmth",
         "RESOLVED: OKH warm paper is the shared :root baseline.\n"
         "        Each sibling overrides via html[data-theme=light] .glee-main / .askjamie-main."),
        ("✓", "Search class namespace",
         "RESOLVED: Site-specific namespaces are intentional (okh-search-* / glee-search-* /\n"
         "        site-search-*). Cross-site integration is via peer-results feature, not\n"
         "        a shared namespace. See docs/cross-site-search-prompt.md."),
        ("✓", "GA4 analytics placement",
         "RESOLVED: GA4 inline in each page's <head> only (no app.js, no analytics.js).\n"
         "        OKH tracking ID: G-VJ1BKXS27H  |  Jamie: G-MT9Y10YY0G\n"
         "        Jamie action: remove gtag bootstrap from app.js, add to all HTML pages."),
    ]

    for mark, title, detail in resolved:
        print(f"\n  [{green(mark)}] {bold(title)}")
        print(f"        {detail}")

    print(f"\n{bold('── Remaining open items (Category B — sibling additions to absorb) ─────')}")

    open_items = [
        ("B", "Glee-only CSS blocks not yet in OKH GLEE section",
         "Tool-ette hub cards (.card--tool-ette), refined Mermaid skin,\n"
         "        cross-site sync utilities block — merge into OKH theme.css GLEE section."),
        ("B", "Jamie-only CSS blocks not yet in OKH ASKJAMIE section",
         "BFS hero (~111 lines), system pages (~231 lines), mid-century teal\n"
         "        Mermaid skin (~84 lines) — merge into OKH theme.css ASKJAMIE section."),
        ("B", "_gtag_event() GA4 event helper in Jamie JS",
         "Guard-wrapped helper fires search_open/search_submit events.\n"
         "        OKH can absorb this — it's a no-op when gtag is not loaded on a page."),
    ]

    cat_color = {"A": green, "B": yellow, "C": red}

    for cat, title, detail in open_items:
        color = cat_color.get(cat, dim)
        print(f"\n  [{color(f'Cat {cat}')}] {bold(title)}")
        print(f"        {detail}")

    print(f"\n{dim('  See docs/cross-site-sync-plan.md for the full plan and resolution guide.')}\n")

    return errors


# ── Build-drop mode ───────────────────────────────────────────────────────────

def run_build_drop(dry_run=False):
    today = datetime.date.today().isoformat()
    zip_name = f"okh-cross-repo-sync-{today}.zip"
    zip_path = os.path.join(DIST_DIR, zip_name)

    print(bold("\n══ OKHP3 Cross-Site Sync — Build Drop ══"))
    if dry_run:
        print(yellow("  DRY RUN — no files will be written.\n"))

    # Verify local source files exist
    missing = []
    for fp in FOUNDATION_FILES:
        full = os.path.join(LOCAL_ROOT, fp)
        if not os.path.exists(full):
            missing.append(fp)
    if missing:
        for m in missing:
            print(red(f"  MISSING local file: {m}"))
        print(red("\n  Aborting — cannot build sync drop with missing files."))
        sys.exit(1)

    # Build the per-repo sync structure:
    # sync/glee/assets/css/theme.css etc.
    # sync/jamie/assets/css/theme.css etc.
    sibling_keys = [k for k in REPOS if k != "okh"]

    entries = []  # list of (zip_arc_path, local_src_path)
    for sibling in sibling_keys:
        for fp in FOUNDATION_FILES:
            arc_path = f"sync/{sibling}/{fp}"
            local_src = os.path.join(LOCAL_ROOT, fp)
            entries.append((arc_path, local_src))

    print(f"  Sync drop: {zip_path}")
    print(f"  Files per sibling repo: {len(FOUNDATION_FILES)}")
    print(f"  Sibling repos: {', '.join(sibling_keys)}\n")

    for arc_path, local_src in entries:
        size = os.path.getsize(local_src)
        status = dim("  (dry-run)") if dry_run else ""
        print(f"  {arc_path}  ({size:,} bytes){status}")

    if dry_run:
        print(yellow(f"\n  Would create: {zip_path}"))
        print(yellow("  (dry-run) No files written."))
        return

    os.makedirs(DIST_DIR, exist_ok=True)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for arc_path, local_src in entries:
            zf.write(local_src, arc_path)

    final_size = os.path.getsize(zip_path)
    print(f"\n  {green('✓')} Created {zip_path} ({final_size:,} bytes)")
    print(f"\n  Next steps:")
    print(f"  1. Unzip sync/glee/ into the Glee-fully repo and commit:")
    print(f"       chore(sync): align foundation files with overkillhill.com canonical ({today})")
    print(f"  2. Unzip sync/jamie/ into the AskJamie repo and commit:")
    print(f"       chore(sync): align foundation files with overkillhill.com canonical ({today})")
    print(f"  3. Run --audit after sibling repos are updated to confirm drift is zero.\n")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="OKHP3 Universe cross-site CSS/JS sync tool.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--audit",
        action="store_true",
        help="Fetch all three repos and report divergences vs OKH local source.",
    )
    group.add_argument(
        "--build-drop",
        action="store_true",
        help="Package OKH foundation files into a dated sync zip.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="(with --build-drop) preview what would be written without writing it.",
    )

    args = parser.parse_args()

    if args.audit:
        errors = run_audit()
        sys.exit(1 if errors else 0)
    elif args.build_drop:
        run_build_drop(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
