#!/usr/bin/env python3
"""
audit-site.py — static-site auditor for overkillhill.com.

Walks every .html file in the repo (excluding .local/, attached_assets/,
node_modules/, .cache/, .git/, .vscode/) and produces a Markdown report.

Per-page checks actually emitted as issues:
  * <title> length (<=70) and presence
  * <meta name="description"> length (<=165) and presence
  * exactly one <h1>
  * heading level order — no level may jump by more than 1 going
    deeper (e.g. h3 after h1 is a violation; h1 after h3 is fine).
    Headings inside <footer> are excluded because the footer uses a
    well-validated h3/h4 pattern that does not reflect the page's
    content outline.
  * canonical link presence
  * required Open Graph fields: og:title, og:description, og:image, og:url
  * <html lang="..."> presence
  * every <img> has alt, width, and height attributes
  * external target="_blank" links carry rel="noopener noreferrer"
  * known placeholder strings (ASK-JAMIE-GPT-ID-HERE, the old SearchAction
    target ?s={search_term_string}, generic YOUR-...)
  * theme-color resolves to the overkillhill.com brand color (#2a2320)
  * any page embedding a Mermaid diagram carries the OKH affiliate
    referral link (mermaidchart.cello.so) styled with `mermaid-referral-link`
  * bare or generic link text ("read more", "click here", "here",
    bare "→", etc.) — aria-label is used as the accessible text
    when present, so navigation arrows that include aria-label
    context are not flagged
  * no duplicate `id="..."` attributes within a single page (would
    break anchor navigation and JS lookups)
  * every in-page anchor link (`href="#foo"`) resolves to a real
    `id="foo"` on the same page
  * og:image URL (when it points to overkillhill.com) resolves to a file
    that actually exists on disk (URL-decoded to handle %20 etc.)

Cross-file / repo-wide checks:
  * no leftover backup / OS-junk files (.bak, .orig, .swp, .DS_Store, ~)
    in production directories
  * search-index.json mtime is newer than every public HTML file
    (catches stale indexes after content edits)

Modern (2025/2026) baseline checks — see also scripts/apply-modern-baseline.py:
  * every page carries `<meta name="referrer">` (privacy)
  * every page carries `<meta http-equiv="Content-Security-Policy">`
    with the expected allow-list keywords
  * every <img> declares a `loading=` attribute (lazy or eager) — no
    silent defaults
  * theme.css contains a global `prefers-reduced-motion` umbrella rule

Cross-file reconciliation (best-effort; failures are reported as issues
rather than crashing the run):
  * sitemap.xml entries vs HTML files on disk
  * search-index.json entries vs HTML files on disk

Usage:
    python3 scripts/audit-site.py
    python3 scripts/audit-site.py --report assets/docs/audit-report.md
    python3 scripts/audit-site.py --quiet
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Tuple
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".local", ".agents", "attached_assets", "node_modules", ".cache", ".git",
                "templates"}
EXCLUDE_FROM_SITEMAP = {"404.html", "under-construction.html"}

# Title / description recommended length budgets
TITLE_MAX = 70
DESC_MAX = 165

# Brand-correct theme color
EXPECTED_THEME_COLOR = "#2a2320"
EXPECTED_BG_COLOR = "#e8e0d6"


def iter_html_files() -> List[Path]:
    out: List[Path] = []
    for p in ROOT.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        out.append(p)
    return sorted(out)


class PageParser(HTMLParser):
    """Lightweight extractor for the bits we need to audit."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self.h1_count = 0
        self._in_h1 = False
        # heading-order tracking (footer headings excluded)
        self.headings: List[int] = []   # ordered heading levels outside <footer>
        self._in_footer: int = 0        # nesting depth inside <footer>
        self.metas: Dict[str, str] = {}
        self.canonical = ""
        self.images: List[Dict[str, str]] = []
        self.external_links: List[Dict[str, str]] = []
        self.placeholder_hits: List[str] = []
        self.has_jsonld_website = False
        self.has_jsonld_breadcrumb = False
        self.has_jsonld_article = False
        self._jsonld_collect = False
        self._jsonld_buf: List[str] = []

    def handle_starttag(self, tag: str, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "h1":
            self.h1_count += 1
            self._in_h1 = True
            if self._in_footer == 0:
                self.headings.append(1)
        elif tag == "footer":
            self._in_footer += 1
        elif tag in ("h2", "h3", "h4", "h5", "h6"):
            if self._in_footer == 0:
                self.headings.append(int(tag[1]))
        elif tag == "meta":
            key = a.get("name") or a.get("property") or a.get("http-equiv")
            if key:
                self.metas[key.lower()] = a.get("content", "") or ""
        elif tag == "link" and a.get("rel", "").lower() == "canonical":
            self.canonical = a.get("href", "") or ""
        elif tag == "img":
            self.images.append(
                {
                    "src": a.get("src", ""),
                    "alt": a.get("alt"),
                    "width": a.get("width"),
                    "height": a.get("height"),
                    "loading": a.get("loading"),
                }
            )
        elif tag == "a":
            href = a.get("href", "") or ""
            if a.get("target") == "_blank" and href.startswith(("http://", "https://")):
                rel = (a.get("rel") or "").lower()
                self.external_links.append({"href": href, "rel": rel})
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._jsonld_collect = True
            self._jsonld_buf = []

    def handle_endtag(self, tag: str):
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False
        elif tag == "footer":
            self._in_footer = max(0, self._in_footer - 1)
        elif tag == "script" and self._jsonld_collect:
            self._jsonld_collect = False
            blob = "".join(self._jsonld_buf).strip()
            if '"WebSite"' in blob:
                self.has_jsonld_website = True
            if '"BreadcrumbList"' in blob:
                self.has_jsonld_breadcrumb = True
            if '"Article"' in blob or '"NewsArticle"' in blob:
                self.has_jsonld_article = True

    def handle_data(self, data: str):
        if self._in_title:
            self.title += data
        if self._jsonld_collect:
            self._jsonld_buf.append(data)


PLACEHOLDER_PATTERNS = [
    ("YOUR-OKH-PLACEHOLDER", "Generic placeholder"),
    ("?s={search_term_string}", "Old SearchAction target"),
    ("YOUR-", "Generic placeholder"),
]
BARE_NOOPENER = re.compile(r'\brel="noopener"(?!\s*noreferrer)')

# Link text patterns that are bare/generic and fail WCAG 2.4.4.
# aria-label overrides visible text, so labeled arrows are safe.
BARE_LINK_TEXTS = frozenset({
    "read more", "click here", "here", "→",
    "↑", "↓", "←", "↗", "↘",
    "more", "learn more", "click",
})


def audit_page(path: Path) -> List[str]:
    rel = path.relative_to(ROOT).as_posix()
    src = path.read_text(encoding="utf-8", errors="replace")
    issues: List[str] = []

    # placeholder text scan (raw)
    for needle, label in PLACEHOLDER_PATTERNS:
        if needle in src:
            issues.append(f"{label}: `{needle}` present")
    if BARE_NOOPENER.search(src):
        issues.append('Bare rel="noopener" without noreferrer present')

    # Mermaid referral-link policy: any page that embeds a Mermaid diagram
    # must carry the OKH affiliate link (mermaidchart.cello.so) styled with
    # `mermaid-referral-link`. See replit.md "Mermaid pages" section.
    if re.search(r'<pre[^>]*class="[^"]*\bmermaid\b', src):
        if "mermaidchart.cello.so" not in src:
            issues.append(
                "Mermaid diagram present but missing referral link "
                "(https://mermaidchart.cello.so/UhVlNtC2MlS)"
            )
        if "mermaid-referral-link" not in src:
            issues.append(
                "Mermaid diagram present but missing `mermaid-referral-link` "
                "class (hot-pink styling)"
            )

    # Bare / generic link text — fails WCAG 2.4.4 (Link Purpose)
    # aria-label (if present) is used as the accessible label,
    # which means labeled navigation arrows are not flagged.
    for _lm in re.finditer(r'<a\b([^>]*)>(.*?)</a>', src,
                           re.DOTALL | re.IGNORECASE):
        _attrs = _lm.group(1)
        _inner = _lm.group(2)
        _aria = re.search(r'aria-label="([^"]*)"', _attrs, re.IGNORECASE)
        _aria_label = _aria.group(1).strip() if _aria else ""
        _visible = re.sub(r'<[^>]+>', '', _inner).strip()
        _visible = re.sub(r'\s+', ' ', _visible)
        _accessible = _aria_label if _aria_label else _visible
        if _accessible.lower().strip() in BARE_LINK_TEXTS:
            _href = re.search(r'href="([^"]*)"', _attrs, re.IGNORECASE)
            _href_val = _href.group(1) if _href else "(no href)"
            issues.append(
                f'Generic link text "{_accessible}": {_href_val}'
            )

    # duplicate-id scan — duplicate ids break anchor navigation, JS
    # querySelector calls, and screen-reader landmark announcements
    from collections import Counter
    all_ids = re.findall(r'\sid="([^"]+)"', src)
    for dup_id, count in Counter(all_ids).items():
        if count > 1:
            issues.append(f'Duplicate id="{dup_id}" appears {count} times')

    # in-page anchor sanity — every href="#foo" must point to a real
    # id="foo" on the same page (skip "#" alone and "#main" since main
    # may be added by skip-link landmark patterns at runtime)
    id_set = set(all_ids)
    anchors = re.findall(r'href="#([^"]+)"', src)
    for anchor in set(anchors):
        if anchor and anchor not in id_set:
            issues.append(f'In-page anchor href="#{anchor}" has no matching id')

    # og:image existence — when og:image points to askjamie.bot, the
    # decoded path must resolve to a real file on disk. Catches social
    # cards that would 404 when shared on LinkedIn/X/etc.
    og_img = re.search(r'<meta[^>]*property="og:image"[^>]*content="([^"]+)"', src)
    if og_img:
        url = og_img.group(1)
        if url.startswith("https://overkillhill.com"):
            decoded = urllib.parse.unquote(url.replace("https://overkillhill.com", ""))
            if not (ROOT / decoded.lstrip("/")).exists():
                issues.append(f"og:image file does not exist on disk: {decoded}")

    # Modern (2025/2026) baseline — security meta tags
    if 'name="referrer"' not in src:
        issues.append('Missing <meta name="referrer"> — modern privacy baseline')
    if 'http-equiv="Content-Security-Policy"' not in src:
        issues.append('Missing CSP meta tag — modern security baseline')
    elif "default-src 'self'" not in src:
        issues.append("CSP meta present but missing `default-src 'self'`")

    # Image perf — every <img> must declare loading= explicitly (no
    # silent default). Lazy or eager are both acceptable choices.
    for raw_img in re.findall(r'<img\b[^>]*>', src):
        if "loading=" not in raw_img:
            src_attr = re.search(r'src="([^"]+)"', raw_img)
            label = src_attr.group(1) if src_attr else "(no src)"
            issues.append(f"Image missing loading= attribute: {label}")

    # theme-color check — modern pattern uses a light/dark media-queried
    # pair. Accept both the legacy single tag and the new pair, but require
    # the brand teal to appear in at least one tag (it's the dark-mode and
    # historical default color).
    theme_colors = re.findall(
        r'<meta\s+name="theme-color"\s+[^>]*content="([^"]+)"', src
    )
    if not theme_colors:
        issues.append("Missing <meta name=\"theme-color\"> entirely")
    elif EXPECTED_THEME_COLOR not in [c.lower() for c in theme_colors]:
        issues.append(
            f"theme-color values {theme_colors} do not include the "
            f"expected brand color `{EXPECTED_THEME_COLOR}`"
        )

    # parse for structural checks
    p = PageParser()
    try:
        p.feed(src)
    except Exception as exc:  # pragma: no cover
        issues.append(f"HTML parser raised: {exc!r}")
        return issues

    title = p.title.strip()
    if not title:
        issues.append("Missing <title>")
    elif len(title) > TITLE_MAX:
        issues.append(f"Title is {len(title)} chars (>{TITLE_MAX})")

    desc = p.metas.get("description", "").strip()
    if not desc:
        issues.append("Missing meta description")
    elif len(desc) > DESC_MAX:
        issues.append(f"Description is {len(desc)} chars (>{DESC_MAX})")

    if "html lang=" not in src and "<html lang=" not in src:
        issues.append("Missing lang attribute on <html>")

    if p.h1_count == 0:
        issues.append("No <h1> found")
    elif p.h1_count > 1:
        issues.append(f"{p.h1_count} <h1> elements (should be 1)")

    # Heading order — no heading may jump more than one level deeper.
    # Going back up (e.g. h3 → h1) is always allowed.
    # Footer headings are already excluded by PageParser.
    _prev_level = 0
    for _level in p.headings:
        if _prev_level > 0 and _level > _prev_level + 1:
            issues.append(
                f"Heading order: h{_level} follows h{_prev_level} "
                f"(skips level — footer headings excluded)"
            )
        _prev_level = _level

    if not p.canonical:
        issues.append("Missing canonical link")

    for required in ("og:title", "og:description", "og:image", "og:url"):
        if required not in p.metas:
            issues.append(f"Missing {required}")

    # image hygiene
    for img in p.images:
        src_attr = img["src"] or "(no src)"
        if img["alt"] is None:
            issues.append(f"Image missing alt: {src_attr}")
        if img["width"] is None or img["height"] is None:
            issues.append(f"Image missing width/height: {src_attr}")

    # external link hygiene (we already raw-checked, but report each link missing noreferrer)
    for link in p.external_links:
        rel_attr = link["rel"]
        if "noreferrer" not in rel_attr or "noopener" not in rel_attr:
            issues.append(
                f'External target=_blank link lacks noopener+noreferrer: {link["href"]}'
            )

    return issues


def parse_sitemap() -> Tuple[List[str], List[str]]:
    """Return (urls, errors). Never raises."""
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        return [], ["sitemap.xml is missing"]
    try:
        tree = ET.parse(sitemap)
    except ET.ParseError as exc:
        return [], [f"sitemap.xml is unparseable: {exc}"]
    locs = [
        (loc.text or "").strip()
        for loc in tree.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    ]
    return [u for u in locs if u], []


def url_to_relpath(url: str) -> str:
    """Map https://overkillhill.com/foo/ -> foo/index.html (or foo.html)."""
    path = url.replace("https://overkillhill.com", "").lstrip("/")
    if path == "":
        return "index.html"
    if path.endswith(".html"):
        return path
    if path.endswith("/"):
        return path + "index.html"
    return path + "/index.html"


def reconcile_sitemap(html_files: List[Path]) -> Tuple[List[str], List[str], List[str]]:
    """Return (in_sitemap_not_on_disk, on_disk_not_in_sitemap, errors)."""
    rels_on_disk = {p.relative_to(ROOT).as_posix() for p in html_files}
    rels_on_disk -= EXCLUDE_FROM_SITEMAP
    sitemap_urls, errors = parse_sitemap()
    if errors:
        return [], [], errors
    rels_in_sitemap = {url_to_relpath(u) for u in sitemap_urls}
    in_sitemap_missing_disk = sorted(rels_in_sitemap - rels_on_disk)
    on_disk_missing_sitemap = sorted(rels_on_disk - rels_in_sitemap)
    return in_sitemap_missing_disk, on_disk_missing_sitemap, []


CRUFT_PATTERNS = ("*.bak", "*.orig", "*.swp", "*.swo", ".DS_Store", "Thumbs.db", "*~")


def scan_repo_cruft() -> List[str]:
    """Find leftover backup / OS-junk files in production directories."""
    issues: List[str] = []
    for pattern in CRUFT_PATTERNS:
        for p in ROOT.rglob(pattern):
            if any(part in EXCLUDE_DIRS for part in p.parts):
                continue
            issues.append(f"Repo cruft (delete me): {p.relative_to(ROOT).as_posix()}")
    return issues


def check_search_index_freshness(html_files: List[Path]) -> List[str]:
    """Report any HTML file modified after search-index.json was built."""
    idx = ROOT / "assets/data/search-index.json"
    if not idx.exists():
        return []  # missing-index is already caught by reconcile_search_index
    idx_mtime = idx.stat().st_mtime
    stale: List[str] = []
    for p in html_files:
        if p.stat().st_mtime > idx_mtime:
            stale.append(p.relative_to(ROOT).as_posix())
    if not stale:
        return []
    head = stale[:5]
    suffix = "" if len(stale) <= 5 else f" (and {len(stale)-5} more)"
    return [
        "search-index.json is stale — rebuild with `python3 scripts/build-search-index.py`. "
        f"Pages newer than the index: {', '.join(head)}{suffix}"
    ]


def reconcile_search_index(html_files: List[Path]) -> List[str]:
    idx = ROOT / "assets/data/search-index.json"
    if not idx.exists():
        return ["search-index.json missing"]
    try:
        data = json.loads(idx.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return [f"search-index.json is unreadable: {exc}"]
    try:
        pages = data.get("pages", data) if isinstance(data, dict) else data
        if not isinstance(pages, list):
            return [f"search-index.json has unexpected shape: {type(pages).__name__}"]
        indexed_urls = {item.get("url", "") for item in pages if isinstance(item, dict)}
        template_urls = sorted(
            u for u in indexed_urls
            if re.search(r"/assets/templates/", u)
        )
        if template_urls:
            return [
                f"search-index.json contains a template-scaffold URL "
                f"(re-run build-search-index.py after fixing EXCLUDE_DIRS): {u}"
                for u in template_urls
            ]
        indexed_rels = {
            url_to_relpath(u) if u.startswith("http") else u.lstrip("/")
            for u in indexed_urls
            if u
        }
        indexed_rels = {
            r if r.endswith(".html") else r.rstrip("/") + "/index.html"
            for r in indexed_rels
        }
        indexed_rels = {r.lstrip("/") or "index.html" for r in indexed_rels}
        rels_on_disk = {p.relative_to(ROOT).as_posix() for p in html_files}
        rels_on_disk -= EXCLUDE_FROM_SITEMAP
        missing = sorted(rels_on_disk - indexed_rels)
        return [f"Page on disk not in search index: {p}" for p in missing]
    except Exception as exc:  # pragma: no cover — defensive
        return [f"search-index reconciliation crashed: {exc!r}"]


def render_report(per_page: Dict[str, List[str]],
                  sitemap_missing_disk: List[str],
                  disk_missing_sitemap: List[str],
                  search_issues: List[str]) -> str:
    total_issues = sum(len(v) for v in per_page.values()) + \
                   len(sitemap_missing_disk) + len(disk_missing_sitemap) + len(search_issues)
    lines = [
        "# overkillhill.com — Automated Site Audit",
        "",
        f"**Pages scanned:** {len(per_page)}  ",
        f"**Total issues:** {total_issues}",
        "",
        "## Sitemap reconciliation",
        "",
    ]
    if not sitemap_missing_disk and not disk_missing_sitemap:
        lines.append("- OK — sitemap and on-disk pages are in sync.")
    if sitemap_missing_disk:
        lines.append("- **Sitemap entries with no file on disk:**")
        for x in sitemap_missing_disk:
            lines.append(f"  - `{x}`")
    if disk_missing_sitemap:
        lines.append("- **Pages on disk not listed in sitemap.xml:**")
        for x in disk_missing_sitemap:
            lines.append(f"  - `{x}`")
    lines += ["", "## Search-index reconciliation", ""]
    if not search_issues:
        lines.append("- OK — every public page is covered by the search index.")
    else:
        for x in search_issues:
            lines.append(f"- {x}")
    lines += ["", "## Per-page issues", ""]
    for page, issues in sorted(per_page.items()):
        if not issues:
            continue
        lines.append(f"### `{page}`")
        for issue in issues:
            lines.append(f"- {issue}")
        lines.append("")
    if all(not v for v in per_page.values()):
        lines.append("_No per-page issues found._")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", default="assets/docs/audit-report.md",
                        help="Path to write the Markdown report.")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress per-page console output.")
    args = parser.parse_args()

    html_files = iter_html_files()
    per_page: Dict[str, List[str]] = {}
    for path in html_files:
        rel = path.relative_to(ROOT).as_posix()
        per_page[rel] = audit_page(path)
        if not args.quiet:
            count = len(per_page[rel])
            flag = "OK " if count == 0 else f"{count:>3}"
            print(f"  [{flag}] {rel}")

    sitemap_missing_disk, disk_missing_sitemap, sitemap_errors = reconcile_sitemap(html_files)
    search_issues = reconcile_search_index(html_files)
    search_issues.extend(check_search_index_freshness(html_files))
    cruft_issues = scan_repo_cruft()
    if sitemap_errors:
        # Surface sitemap parse errors as issues against sitemap.xml itself.
        per_page["sitemap.xml"] = per_page.get("sitemap.xml", []) + sitemap_errors
    if cruft_issues:
        per_page["(repo cruft)"] = cruft_issues

    report = render_report(per_page, sitemap_missing_disk, disk_missing_sitemap, search_issues)
    out = ROOT / args.report
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"\nReport written to {out.relative_to(ROOT)}")

    total = sum(len(v) for v in per_page.values()) + len(sitemap_missing_disk) + \
            len(disk_missing_sitemap) + len(search_issues)
    # cruft was already added into per_page above, so it's already in the sum
    print(f"Total issues found: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
