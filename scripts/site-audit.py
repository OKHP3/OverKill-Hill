#!/usr/bin/env python3
"""
OverKill Hill P³™ — Static Site Audit Script
Covers the 18-point governance checklist from Sprint 4 Phase 16.

Usage:
    python3 scripts/site-audit.py          # full audit
    python3 scripts/site-audit.py --quiet  # summary counts only
    python3 scripts/site-audit.py --check N [N ...]  # specific check(s)

Exit codes: 0 = all hard checks pass (warnings allowed), 1 = hard failure(s)

Output: summary counts, pass/warn/fail per check, detailed issue list, next actions.

Check definitions (18 points):
  1.  title            — Title present, non-empty (WARN if >70 chars)
  2.  description      — Meta description present (WARN if >160 chars)
  3.  canonical        — Canonical URL present
  4.  h1               — Exactly one <h1> per page
  5.  lang             — html[lang] attribute present
  6.  viewport         — Viewport meta present
  7.  charset          — Charset meta present
  8.  og_title         — og:title present
  9.  og_description   — og:description present
  10. og_image         — og:image present
  11. twitter_card     — twitter:card present
  12. ga4              — GA4 tag (G-VJ1BKXS27H) present
  13. skip_link        — Skip link present
  14. noopener         — All target=_blank links have rel=noopener
  15. alt_text         — No <img> missing alt attribute
  16. footer_tm        — Footer brand name includes ™ (indexed pages only)
  17. noindex_sitemap  — No noindex page listed in sitemap.xml
  18. sitemap_resolve  — All sitemap URLs resolve to real files on disk
"""

import re
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {
    "_replit", ".local", "node_modules", "attached_assets",
    "assets/templates", ".agents", ".git", "dist", "build",
}

GA4_ID = "G-VJ1BKXS27H"
TITLE_SOFT_MAX = 70
DESC_SOFT_MAX = 160

CHECKS = [
    (1,  "title",            "Title present, non-empty (WARN if >70 chars)"),
    (2,  "description",      "Meta description present (WARN if >160 chars)"),
    (3,  "canonical",        "Canonical URL present"),
    (4,  "h1",               "Exactly one <h1> per page"),
    (5,  "lang",             "html[lang] attribute present"),
    (6,  "viewport",         "Viewport meta present"),
    (7,  "charset",          "Charset meta present"),
    (8,  "og_title",         "og:title present"),
    (9,  "og_description",   "og:description present"),
    (10, "og_image",         "og:image present"),
    (11, "twitter_card",     "twitter:card present"),
    (12, "ga4",              f"GA4 tag ({GA4_ID}) present"),
    (13, "skip_link",        "Skip link present"),
    (14, "noopener",         "All target=_blank links have rel=noopener"),
    (15, "alt_text",         "No <img> missing alt attribute"),
    (16, "footer_tm",        "Footer brand name includes ™ (indexed pages)"),
    (17, "noindex_sitemap",  "No noindex page in sitemap.xml"),
    (18, "sitemap_resolve",  "All sitemap URLs resolve to real files"),
]


def find_pages():
    pages = []
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT)
        parts = rel.parts
        if any(skip in parts or str(rel).startswith(skip) for skip in SKIP_DIRS):
            continue
        pages.append(p)
    return pages


def is_noindex(raw):
    m = re.search(r'<meta[^>]+name="robots"[^>]+content="([^"]+)"', raw)
    return bool(m and "noindex" in m.group(1))


def run_checks(pages, selected=None):
    """
    Returns:
        hard_passed  dict[int, bool]  — True if check has no hard failures
        warn_lists   dict[int, list]  — soft-limit warnings (not failures)
        issue_lists  dict[int, list]  — hard failure messages
    """
    hard_passed = {n: True for n, _, _ in CHECKS}
    warn_lists  = {n: [] for n, _, _ in CHECKS}
    issue_lists = {n: [] for n, _, _ in CHECKS}

    sitemap_path = ROOT / "sitemap.xml"
    sitemap_urls = set()
    sitemap_raw = ""
    if sitemap_path.exists():
        sitemap_raw = sitemap_path.read_text(errors="replace")
        sitemap_urls = set(re.findall(r"<loc>(.*?)</loc>", sitemap_raw))

    for p in pages:
        raw = p.read_text(errors="replace")
        rel = str(p.relative_to(ROOT))
        noindex = is_noindex(raw)

        def fail(n, msg):
            issue_lists[n].append(f"  {rel}: {msg}")
            hard_passed[n] = False

        def warn(n, msg):
            warn_lists[n].append(f"  {rel}: {msg}")

        # Check 1 — title
        if selected is None or 1 in selected:
            m = re.search(r"<title>(.*?)</title>", raw, re.DOTALL)
            if not m or not m.group(1).strip():
                fail(1, "title missing or empty")
            else:
                length = len(m.group(1).strip())
                if length > TITLE_SOFT_MAX:
                    warn(1, f"title {length} chars (>{TITLE_SOFT_MAX} soft limit — Google truncates in SERPs)")

        # Check 2 — meta description
        if selected is None or 2 in selected:
            m = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', raw)
            if not m:
                fail(2, "meta description missing")
            else:
                length = len(m.group(1))
                if length > DESC_SOFT_MAX:
                    warn(2, f"description {length} chars (>{DESC_SOFT_MAX} soft limit — Google truncates in SERPs)")

        # Check 3 — canonical
        if selected is None or 3 in selected:
            if not re.search(r'<link[^>]+rel="canonical"', raw):
                fail(3, "canonical link missing")

        # Check 4 — single H1
        if selected is None or 4 in selected:
            h1s = re.findall(r"<h1[^>]*>", raw)
            if len(h1s) == 0:
                fail(4, "no <h1> found")
            elif len(h1s) > 1:
                fail(4, f"{len(h1s)} <h1> elements (expected exactly 1)")

        # Check 5 — html lang
        if selected is None or 5 in selected:
            if not re.search(r"<html[^>]+lang=", raw):
                fail(5, "html[lang] missing")

        # Check 6 — viewport
        if selected is None or 6 in selected:
            if 'name="viewport"' not in raw:
                fail(6, "viewport meta missing")

        # Check 7 — charset
        if selected is None or 7 in selected:
            if not re.search(r"<meta[^>]+charset", raw, re.IGNORECASE):
                fail(7, "charset meta missing")

        # Check 8 — og:title
        if selected is None or 8 in selected:
            if 'property="og:title"' not in raw and "property='og:title'" not in raw:
                fail(8, "og:title missing")

        # Check 9 — og:description
        if selected is None or 9 in selected:
            if 'property="og:description"' not in raw and "property='og:description'" not in raw:
                fail(9, "og:description missing")

        # Check 10 — og:image
        if selected is None or 10 in selected:
            if 'property="og:image"' not in raw and "property='og:image'" not in raw:
                fail(10, "og:image missing")

        # Check 11 — twitter:card
        if selected is None or 11 in selected:
            if 'name="twitter:card"' not in raw and "name='twitter:card'" not in raw:
                fail(11, "twitter:card missing")

        # Check 12 — GA4
        if selected is None or 12 in selected:
            if GA4_ID not in raw:
                fail(12, f"GA4 tag {GA4_ID} not found")

        # Check 13 — skip link
        if selected is None or 13 in selected:
            if "skip-link" not in raw and "okh-skip-link" not in raw:
                fail(13, "skip link missing")

        # Check 14 — noopener on external _blank links
        if selected is None or 14 in selected:
            blanks = re.findall(r"<a[^>]+target=[\"']_blank[\"'][^>]*>", raw, re.DOTALL)
            for a in blanks:
                if "noopener" not in a:
                    href = re.search(r'href=["\']([^"\']+)', a)
                    url = href.group(1)[:60] if href else "(unknown)"
                    fail(14, f"target=_blank without rel=noopener: {url}")

        # Check 15 — alt text on images
        if selected is None or 15 in selected:
            imgs = re.findall(r"<img[^>]+>", raw, re.DOTALL)
            for img in imgs:
                if "alt=" not in img:
                    src = re.search(r'src=["\']([^"\']+)', img)
                    s = src.group(1)[:50] if src else "(unknown)"
                    fail(15, f"img missing alt: {s}")

        # Check 16 — footer ™ (indexed pages only)
        if selected is None or 16 in selected:
            if not noindex:
                footer_h3s = re.findall(r"<h3[^>]*>(.*?)</h3>", raw, re.DOTALL)
                brand_h3s = [h for h in footer_h3s if "OverKill" in h or "P³" in h]
                for h in brand_h3s:
                    if "™" not in h:
                        text = re.sub(r"<[^>]+>", "", h).replace("&nbsp;", " ").strip()
                        fail(16, f"footer brand h3 missing ™: '{text[:60]}'")

    # Check 17 — noindex pages not in sitemap (cross-page check)
    if selected is None or 17 in selected:
        for p in pages:
            raw = p.read_text(errors="replace")
            if is_noindex(raw):
                rel_path = str(p.relative_to(ROOT))
                url_path = "/" + rel_path.replace("index.html", "").replace("\\", "/")
                matches = [u for u in sitemap_urls if url_path.rstrip("/") == u.rstrip("/").replace("https://overkillhill.com", "")]
                if matches:
                    issue_lists[17].append(f"  {rel_path}: noindex page in sitemap → {matches[0]}")
                    hard_passed[17] = False

    # Check 18 — sitemap URLs resolve to real files
    if selected is None or 18 in selected:
        for url in sorted(sitemap_urls):
            url_path = re.sub(r"^https?://[^/]+", "", url)
            local = url_path.lstrip("/")
            candidates = [
                ROOT / local,
                ROOT / local / "index.html",
                ROOT / (local.rstrip("/") + ".html"),
            ]
            if not any(c.exists() for c in candidates):
                issue_lists[18].append(f"  sitemap URL not found on disk: {url}")
                hard_passed[18] = False

    return hard_passed, warn_lists, issue_lists


def main():
    parser = argparse.ArgumentParser(description="OverKill Hill P³™ — 18-point site audit")
    parser.add_argument("--quiet", action="store_true", help="Summary counts only, no issue detail")
    parser.add_argument("--check", type=int, nargs="+", metavar="N",
                        help="Run specific check number(s) only")
    args = parser.parse_args()

    pages = find_pages()
    if not pages:
        print("ERROR: No HTML pages found. Check ROOT path or SKIP_DIRS.")
        sys.exit(1)

    selected = set(args.check) if args.check else None
    hard_passed, warn_lists, issue_lists = run_checks(pages, selected)

    checks_to_show = [(n, slug, desc) for n, slug, desc in CHECKS if selected is None or n in selected]

    total         = len(checks_to_show)
    num_passed    = sum(1 for n, _, _ in checks_to_show if hard_passed[n] and not warn_lists[n])
    num_warned    = sum(1 for n, _, _ in checks_to_show if hard_passed[n] and warn_lists[n])
    num_failed    = sum(1 for n, _, _ in checks_to_show if not hard_passed[n])
    total_issues  = sum(len(issue_lists[n]) for n, _, _ in checks_to_show)
    total_warns   = sum(len(warn_lists[n]) for n, _, _ in checks_to_show)

    print(f"\n{'='*65}")
    print(f"  OverKill Hill P³™ — Site Audit (18-Point Checklist)")
    print(f"  Pages scanned: {len(pages)}")
    print(f"{'='*65}")

    for n, slug, desc in checks_to_show:
        if not hard_passed[n]:
            cnt = len(issue_lists[n])
            status = f"✖ FAIL ({cnt} issue{'s' if cnt != 1 else ''})"
        elif warn_lists[n]:
            cnt = len(warn_lists[n])
            status = f"⚠ WARN ({cnt} soft-limit item{'s' if cnt != 1 else ''})"
        else:
            status = "✓ PASS"
        print(f"  [{n:>2}] {status:<40} {desc[:40]}")

    print(f"\n{'─'*65}")
    print(f"  Summary: {num_passed} pass / {num_warned} warn / {num_failed} fail  ({total} checks, {len(pages)} pages)")
    print(f"  Hard failures: {total_issues}   Soft warnings: {total_warns}")

    if num_failed == 0 and total_warns == 0:
        print(f"  ✓ All checks passed cleanly. Site is in good governance health.")
        print(f"{'='*65}\n")
        sys.exit(0)

    if num_failed == 0:
        print(f"  ✓ No hard failures. Warnings are informational (soft SEO limits).")

    if not args.quiet:
        if total_issues:
            print(f"\n{'─'*65}")
            print("  Hard failures:")
            for n, slug, desc in checks_to_show:
                if issue_lists[n]:
                    print(f"\n  Check {n}: {desc}")
                    for issue in issue_lists[n]:
                        print(issue)

        if total_warns:
            print(f"\n{'─'*65}")
            print("  Soft-limit warnings (informational, not blocking):")
            for n, slug, desc in checks_to_show:
                if warn_lists[n]:
                    print(f"\n  Check {n}: {desc}")
                    for w in warn_lists[n]:
                        print(w)

    if not args.quiet and (total_issues or total_warns):
        next_actions = {
            1:  "Update <title> tags — aim for ≤70 chars for full SERP display.",
            2:  "Trim meta descriptions to ≤160 chars — Google truncates beyond this.",
            3:  "Add <link rel='canonical' href='...'> to affected pages.",
            4:  "Ensure each page has exactly one <h1>.",
            5:  "Add lang='en' to the <html> element.",
            6:  "Add <meta name='viewport' content='width=device-width,initial-scale=1'>.",
            7:  "Add <meta charset='UTF-8'> to the <head>.",
            8:  "Add <meta property='og:title' content='...'> to affected pages.",
            9:  "Add <meta property='og:description' content='...'> to affected pages.",
            10: "Add <meta property='og:image' content='...'> to affected pages.",
            11: "Add <meta name='twitter:card' content='summary_large_image'>.",
            12: f"Add GA4 snippet ({GA4_ID}) to affected pages.",
            13: "Add a visually-hidden skip link as the first child of <body>.",
            14: "Add rel='noopener noreferrer' to all external target=_blank links.",
            15: "Add descriptive alt='' attributes to all <img> elements.",
            16: "Ensure footer brand <h3> reads 'OverKill&nbsp;Hill&nbsp;P³™'.",
            17: "Remove noindex pages from sitemap.xml — conflicting crawl signal.",
            18: "Fix sitemap.xml — remove/correct URLs that don't resolve on disk.",
        }
        print(f"\n{'─'*65}")
        print("  Suggested next actions:")
        acted = set()
        for n, slug, desc in checks_to_show:
            if (issue_lists[n] or warn_lists[n]) and n not in acted:
                level = "FAIL" if issue_lists[n] else "WARN"
                print(f"  → [{level}] Check {n}: {next_actions.get(n, 'Review manually.')}")
                acted.add(n)

    print(f"{'='*65}\n")
    sys.exit(1 if num_failed > 0 else 0)


if __name__ == "__main__":
    main()
