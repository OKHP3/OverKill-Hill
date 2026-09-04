#!/usr/bin/env python3
"""
check-banner.py — verify the site-wide "Hot off the Forge" banner text is
consistent across all HTML pages and follows the featured article release.

The canonical banner text is defined once here (CANONICAL_BANNER). Any future
wording change only needs to happen in this file; running the script with
--update will propagate it to every HTML file on the site. The release prefix
is checked against the current featured article in both the source partial and
generated pages, so changing an article release cannot leave the banner behind.

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
FEATURED_ARTICLE_ROUTE = "/writings/first-diagram-is-a-liar/"
FEATURED_ARTICLE_SOURCE = "site-src/pages/writings/first-diagram-is-a-liar/index.main.html"
FEATURED_ARTICLE_GENERATED = "writings/first-diagram-is-a-liar/index.html"
SOURCE_BANNER = "assets/partials/header.html"

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
_HREF_RE = re.compile(r'\bhref="([^"]+)"', re.IGNORECASE)
_ARTICLE_RELEASE_RE = re.compile(
    r"<span\b[^>]*>\s*Article\s+(v\d+(?:\.\d+)+)\s*:",
    re.IGNORECASE,
)
_BANNER_RELEASE_RE = re.compile(
    r"^v(\d+(?:\.\d+)+)\s+is\s+live\s*:",
    re.IGNORECASE,
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


def _featured_article_release(root: str, relative_path: str):
    """Return the sole current article release, or a readable validation error."""
    path = os.path.join(root, relative_path)
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except OSError as exc:
        return None, (
            f"current featured article release is unavailable for "
            f"{FEATURED_ARTICLE_ROUTE}: {relative_path}: {exc}"
        )

    releases = [match.lower() for match in _ARTICLE_RELEASE_RE.findall(content)]
    if len(releases) != 1:
        return None, (
            f"current featured article release is missing or ambiguous for "
            f"{FEATURED_ARTICLE_ROUTE}: expected exactly one "
            f'"Article vN.N" label in {relative_path}'
        )
    return releases[0], None


def _banner_release_issue(raw_text: str, opening_tag: str, expected_release: str):
    """Return a route-aware release mismatch, if this banner targets the article."""
    href_match = _HREF_RE.search(opening_tag)
    if not href_match:
        return f"banner release is missing a link for {FEATURED_ARTICLE_ROUTE}: expected {expected_release}"

    href = href_match.group(1)
    if not href.startswith(FEATURED_ARTICLE_ROUTE):
        return None

    normalised = _normalise(raw_text)
    release_match = _BANNER_RELEASE_RE.match(normalised)
    found = f"v{release_match.group(1).lower()}" if release_match else None
    if found != expected_release:
        found_label = found if found is not None else "missing"
        return (
            f"banner release mismatch for {FEATURED_ARTICLE_ROUTE}: "
            f"expected {expected_release} from the article, found {found_label}"
        )
    return None


def check_file(
    path: str,
    update: bool = False,
    dry_run: bool = False,
    expected_release: str | None = None,
):
    """Return (status, message) where status is 'ok' | 'fixed' | 'mismatch' | 'skip'."""
    with open(path, encoding="utf-8") as f:
        content = f.read()

    matches = list(_LINK_RE.finditer(content))
    if not matches:
        return "skip", None

    issues = []
    release_issues = []
    new_content = content

    for m in matches:
        raw_text = m.group(2)
        normalised = _normalise(raw_text)
        href_match = _HREF_RE.search(m.group(1))
        is_featured_banner = bool(
            href_match and href_match.group(1).startswith(FEATURED_ARTICLE_ROUTE)
        )

        if expected_release is not None:
            release_issue = _banner_release_issue(raw_text, m.group(1), expected_release)
            if release_issue:
                release_issues.append(release_issue)

        # Already canonical?
        if normalised == _normalise(CANONICAL_BANNER):
            continue

        # Intentionally different banner (template token or other article)?
        if any(_normalise(p) == normalised for p in ALLOWED_OTHER_PATTERNS):
            continue
        # Also allow any banner that doesn't look like a stale council-scoring
        # copy — i.e. it doesn't start with the same "v0.5 is live:" prefix at all.
        # Those are intentionally different banners for other articles.
        if not is_featured_banner and not normalised.startswith("v0.5 is live:"):
            continue

        # Known old version?
        known_old = any(_normalise(old) == normalised for old in OLD_BANNERS)
        if known_old:
            issues.append(("old", m, raw_text))
        else:
            issues.append(("unknown", m, raw_text))

    if not issues and not release_issues:
        return "ok", None

    # --update can safely repair known wording drift, but it cannot invent the
    # new article copy when the article has moved to a new release.
    if release_issues:
        messages = [f"  [RELEASE] {issue}" for issue in release_issues]
        if issues:
            messages.extend(
                f"  [{('old' if kind == 'old' else 'UNKNOWN')}] {_normalise(raw_text)!r}"
                for kind, _, raw_text in issues
            )
        return "mismatch", "\n".join(messages)

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

    source_release, source_error = _featured_article_release(root, FEATURED_ARTICLE_SOURCE)
    generated_release, generated_error = _featured_article_release(root, FEATURED_ARTICLE_GENERATED)
    if source_error or generated_error:
        if source_error:
            print(f"  MISMATCH: {source_error}")
        if generated_error:
            print(f"  MISMATCH: {generated_error}")
        sys.exit(1)

    for path in find_html_files(root):
        rel = os.path.relpath(path, root)
        expected_release = source_release if rel == SOURCE_BANNER else generated_release
        status, msg = check_file(
            path,
            update=update,
            dry_run=dry_run,
            expected_release=expected_release,
        )
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
