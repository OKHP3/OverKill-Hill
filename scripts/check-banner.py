#!/usr/bin/env python3
"""
check-banner.py — verify the site-wide "Hot off the Forge" banner text is
consistent across all HTML pages.

The canonical banner text is defined once here (CANONICAL_BANNER). Any future
wording change only needs to happen in this file; running the script with
--update will propagate it to every HTML file on the site.

Usage:
    python3 scripts/check-banner.py              # check only (exits 1 on mismatch)
    python3 scripts/check-banner.py --update     # update all files to match canonical
    python3 scripts/check-banner.py --dry-run    # preview --update without writing

The script matches the banner link text inside .site-specials-link anchors. It
detects both the current canonical string and any prior version listed in
OLD_BANNERS so the diff is always legible.
"""

import os
import re
import sys

# ── Single source of truth ────────────────────────────────────────────────────
CANONICAL_BANNER = (
    "v0.5 is live: the Council of AIs scored each other, every model was harder"
    " on itself than the architect was. Read it \u2192"
)

# Known prior versions — used for detection only, never written.
OLD_BANNERS = [
    # em-dash version (original)
    (
        "v0.5 is live: the Council of AIs scored each other \u2014 every model was harder"
        " on itself than the architect was. Read it \u2192"
    ),
]

# Banner text patterns that are intentionally NOT the canonical council-scoring
# banner and should not be flagged as mismatches. This includes:
#   - Template placeholder tokens (never rendered by users)
#   - Other articles' banners on pages that announce a different piece of content
ALLOWED_OTHER_PATTERNS = [
    "[[SPECIALS-COPY]]",   # template placeholder token
]
# ─────────────────────────────────────────────────────────────────────────────

SKIP_DIRS = {"_replit", ".git", "node_modules", "dist"}

# Matches whitespace-normalised content of a .site-specials-link anchor.
# The banner text may be indented / wrapped across lines in the source.
_LINK_RE = re.compile(
    r'(<a\s[^>]*class="[^"]*site-specials-link[^"]*"[^>]*>)'  # opening tag
    r"([\s\S]*?)"                                              # content
    r"(</a>)",                                                 # closing tag
    re.MULTILINE,
)


def _normalise(text: str) -> str:
    """Collapse internal whitespace for comparison."""
    return " ".join(text.split())


def find_html_files(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in sorted(filenames):
            if fname.endswith(".html"):
                yield os.path.join(dirpath, fname)


def check_file(path: str, update: bool = False, dry_run: bool = False):
    """Return (status, message) where status is 'ok' | 'fixed' | 'mismatch' | 'skip'."""
    with open(path, encoding="utf-8") as f:
        content = f.read()

    matches = list(_LINK_RE.finditer(content))
    if not matches:
        return "skip", None

    issues = []
    new_content = content

    for m in matches:
        raw_text = m.group(2)
        normalised = _normalise(raw_text)

        # Already canonical?
        if normalised == _normalise(CANONICAL_BANNER):
            continue

        # Intentionally different banner (template token or other article)?
        if any(_normalise(p) == normalised for p in ALLOWED_OTHER_PATTERNS):
            continue
        # Also allow any banner that doesn't look like a stale council-scoring
        # copy — i.e. it doesn't start with the same "v0.5 is live:" prefix at all.
        # Those are intentionally different banners for other articles.
        if not normalised.startswith("v0.5 is live:"):
            continue

        # Known old version?
        known_old = any(_normalise(old) == normalised for old in OLD_BANNERS)
        if known_old:
            issues.append(("old", m, raw_text))
        else:
            issues.append(("unknown", m, raw_text))

    if not issues:
        return "ok", None

    if update or dry_run:
        for kind, m, raw_text in issues:
            if kind == "old":
                # Preserve surrounding whitespace/indentation pattern — just
                # replace the text portion, keeping lead/trail whitespace.
                lead = len(raw_text) - len(raw_text.lstrip())
                trail = len(raw_text) - len(raw_text.rstrip())
                indent = raw_text[:lead]
                suffix = raw_text[len(raw_text.rstrip()):]
                replacement = indent + CANONICAL_BANNER + suffix
                new_content = new_content.replace(m.group(2), replacement, 1)

        if not dry_run:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
        return "fixed", f"{len(issues)} banner(s) updated"

    # Report only
    msgs = []
    for kind, _, raw_text in issues:
        label = "old" if kind == "old" else "UNKNOWN"
        msgs.append(f"  [{label}] {_normalise(raw_text)!r}")
    return "mismatch", "\n".join(msgs)


def main():
    update = "--update" in sys.argv
    dry_run = "--dry-run" in sys.argv

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ok = fixed = mismatch = skip = 0

    for path in find_html_files(root):
        rel = os.path.relpath(path, root)
        status, msg = check_file(path, update=update, dry_run=dry_run)
        if status == "ok":
            ok += 1
        elif status == "fixed":
            fixed += 1
            verb = "[dry-run] would fix" if dry_run else "Fixed"
            print(f"  {verb}: {rel} — {msg}")
        elif status == "mismatch":
            mismatch += 1
            print(f"  MISMATCH: {rel}\n{msg}")
        else:
            skip += 1

    print()
    if dry_run:
        print(f"Dry run: would fix {fixed}, already ok {ok}, no banner {skip}.")
    else:
        print(f"OK: {ok}  Fixed: {fixed}  Mismatch: {mismatch}  No banner: {skip}")

    if mismatch:
        print("\nRun with --update to fix, or --dry-run to preview.")
        sys.exit(1)


if __name__ == "__main__":
    main()
