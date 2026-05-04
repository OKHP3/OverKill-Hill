#!/usr/bin/env python3
"""
OverKill Hill P³™ — static site validation harness.

Phase 16 of the AUDIT_OVERKILL_HILL_REPLIT_PASS pipeline.

Checks every production HTML page for:
  - <title> present
  - meta description present
  - canonical link present
  - single <h1>
  - JSON-LD structured data present
  - inclusion in sitemap.xml (for non-noindex pages)
  - broken internal links (relative or /-rooted hrefs that resolve to no file)
  - broken asset references (CSS/JS/images)
  - external target="_blank" links missing rel="noopener" / "noreferrer"
  - placeholder hrefs ("#", "javascript:void(0)", empty href)
  - "P3" without superscript inside <title> or <meta> (brand violation)
  - old tagline "Precision. Power. Presence." anywhere (brand regression)

Exits 0 if no errors. Exits 1 if any errors. Warnings do not fail the build.
Run from repo root:  python3 scripts/validate_site.py
"""

from __future__ import annotations

import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"_replit", ".local", ".git", "node_modules", "attached_assets", "dist", "templates"}
SITEMAP = ROOT / "sitemap.xml"
SITE_ORIGIN = "https://overkillhill.com"


class TagCounter(HTMLParser):
    """Collect everything we need for one HTML page in a single pass."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title: str | None = None
        self._in_title = False
        self._title_buf: list[str] = []
        self.h1_count = 0
        self.has_meta_description = False
        self.has_canonical = False
        self.has_jsonld = False
        self.is_noindex = False
        self.anchors: list[dict[str, str]] = []
        self.asset_refs: list[str] = []  # src/href for css/js/img/link

    def handle_starttag(self, tag: str, attrs_list):
        attrs = {k: (v or "") for k, v in attrs_list}
        if tag == "title":
            self._in_title = True
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "meta":
            name = attrs.get("name", "").lower()
            content = attrs.get("content", "")
            if name == "description" and content.strip():
                self.has_meta_description = True
            if name == "robots" and "noindex" in content.lower():
                self.is_noindex = True
        elif tag == "link":
            rel = attrs.get("rel", "").lower()
            href = attrs.get("href", "")
            if rel == "canonical" and href:
                self.has_canonical = True
            if rel in ("stylesheet", "icon", "apple-touch-icon", "manifest") and href:
                self.asset_refs.append(href)
        elif tag == "script":
            t = attrs.get("type", "").lower()
            src = attrs.get("src", "")
            if t == "application/ld+json":
                self.has_jsonld = True
            if src:
                self.asset_refs.append(src)
        elif tag == "img":
            src = attrs.get("src", "")
            if src:
                self.asset_refs.append(src)
        elif tag == "a":
            href = attrs.get("href", "")
            if href is not None:
                self.anchors.append(
                    {
                        "href": href,
                        "target": attrs.get("target", ""),
                        "rel": attrs.get("rel", ""),
                    }
                )

    def handle_endtag(self, tag: str):
        if tag == "title":
            self._in_title = False
            self.title = "".join(self._title_buf).strip()
            self._title_buf = []

    def handle_data(self, data: str):
        if self._in_title:
            self._title_buf.append(data)


def find_html_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT)
        parts = set(rel.parts)
        if parts & SKIP_DIRS:
            continue
        # /assets/templates/ holds stripped template scaffolds with [PLACEHOLDER]
        # tokens — not live pages. They're parsed separately by extract_templates.py.
        rel_posix = rel.as_posix()
        if rel_posix.startswith("assets/templates/"):
            continue
        files.append(path)
    return sorted(files)


def load_sitemap_urls() -> set[str]:
    if not SITEMAP.exists():
        return set()
    text = SITEMAP.read_text(encoding="utf-8")
    return set(re.findall(r"<loc>([^<]+)</loc>", text))


def html_to_route(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def resolve_internal(href: str, source: Path) -> Path | None:
    """Map a /-rooted or relative href back to a filesystem path. Returns None if not local."""
    parsed = urlparse(href)
    if parsed.scheme in ("http", "https", "mailto", "tel", "javascript"):
        return None
    if not parsed.path:
        return None  # pure fragment like "#protocols"
    p = unquote(parsed.path)
    if p.startswith("/"):
        target = ROOT / p.lstrip("/")
    else:
        target = source.parent / p
    return target


def target_exists(target: Path) -> bool:
    if target.exists():
        if target.is_dir():
            return (target / "index.html").exists()
        return True
    # tolerate trailing-slash directory references
    if str(target).endswith("/") and (target / "index.html").exists():
        return True
    return False


# Single class for all findings; severity drives behavior.
class Finding:
    __slots__ = ("severity", "page", "msg")

    def __init__(self, severity: str, page: str, msg: str):
        self.severity = severity
        self.page = page
        self.msg = msg


def validate_page(path: Path, sitemap_urls: set[str]) -> list[Finding]:
    findings: list[Finding] = []
    rel = path.relative_to(ROOT).as_posix()
    raw = path.read_text(encoding="utf-8", errors="replace")

    # --- raw-string brand checks (don't need parsed DOM) ---
    if "Precision. Power. Presence" in raw or "Precision · Power · Presence" in raw:
        findings.append(Finding("ERROR", rel, "old tagline 'Power. Presence.' found — must be 'Precision · Protocol · Promptcraft'"))

    # P3 (no superscript) inside <title> or <meta ...>
    for m in re.finditer(r"<(title|meta)[^>]*>", raw):
        chunk = m.group(0)
        if re.search(r"\bP3\b", chunk) and "P³" not in chunk:
            # ignore github.com/OKHP3 path occurrences (legitimate org handle)
            if "github.com/OKHP3" not in chunk and "OKHP3" not in chunk:
                findings.append(Finding("ERROR", rel, f"'P3' without superscript in {m.group(1)} tag — brand violation"))

    # placeholder hrefs
    for m in re.finditer(r'href="(#|javascript:[^"]*|)"', raw):
        # bare "#" anchor used as a placeholder (not a real fragment) — flag.
        # but allow href="#main" / href="#protocols" etc (fragments to real ids)
        href = m.group(1)
        if href in ("", "#"):
            findings.append(Finding("WARN", rel, f"placeholder href={href!r}"))
        elif href.startswith("javascript:"):
            findings.append(Finding("ERROR", rel, f"javascript: href found ({href!r})"))

    # --- parsed DOM checks ---
    parser = TagCounter()
    try:
        parser.feed(raw)
    except Exception as exc:  # html.parser is forgiving but be defensive
        findings.append(Finding("WARN", rel, f"HTML parser exception: {exc}"))
        return findings

    if not parser.title:
        findings.append(Finding("ERROR", rel, "missing <title>"))
    if not parser.has_meta_description:
        findings.append(Finding("ERROR", rel, "missing meta description"))
    if not parser.has_canonical:
        findings.append(Finding("WARN", rel, "missing canonical link"))
    if parser.h1_count == 0:
        findings.append(Finding("ERROR", rel, "no <h1> found"))
    elif parser.h1_count > 1:
        findings.append(Finding("WARN", rel, f"{parser.h1_count} <h1> elements (should be 1)"))
    if not parser.has_jsonld:
        findings.append(Finding("WARN", rel, "no JSON-LD structured data"))

    # sitemap inclusion (non-noindex, non-utility pages only)
    if not parser.is_noindex and rel not in ("404.html", "under-construction.html"):
        canonical_url = SITE_ORIGIN + html_to_route(path)
        if canonical_url not in sitemap_urls:
            findings.append(Finding("ERROR", rel, f"missing from sitemap.xml ({canonical_url})"))

    # internal link + asset existence
    for ref in parser.asset_refs:
        target = resolve_internal(ref, path)
        if target is not None and not target_exists(target):
            findings.append(Finding("ERROR", rel, f"broken asset reference: {ref}"))

    for a in parser.anchors:
        href = a["href"]
        target = resolve_internal(href, path)
        if target is not None and not target_exists(target):
            # ignore pure-fragment hrefs (no path)
            if not href.startswith("#"):
                findings.append(Finding("ERROR", rel, f"broken internal link: {href}"))

        # external target=_blank must carry rel=noopener (or noreferrer)
        parsed = urlparse(href)
        if parsed.scheme in ("http", "https") and "overkillhill.com" not in parsed.netloc:
            if a["target"] == "_blank" and "noopener" not in a["rel"]:
                findings.append(Finding("ERROR", rel, f"external target=_blank without rel=noopener: {href}"))

    return findings


def main() -> int:
    sitemap_urls = load_sitemap_urls()
    if not sitemap_urls:
        print("WARN: sitemap.xml not found or empty.")

    pages = find_html_files()
    print(f"Validating {len(pages)} HTML pages…\n")

    all_findings: list[Finding] = []
    for path in pages:
        all_findings.extend(validate_page(path, sitemap_urls))

    errors = [f for f in all_findings if f.severity == "ERROR"]
    warnings = [f for f in all_findings if f.severity == "WARN"]

    if errors:
        print(f"ERRORS ({len(errors)}):")
        for f in errors:
            print(f"  ✖ {f.page}: {f.msg}")
        print()
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for f in warnings:
            print(f"  ! {f.page}: {f.msg}")
        print()

    if not errors and not warnings:
        print("✓ all clean.")
    elif not errors:
        print(f"✓ no errors ({len(warnings)} warnings).")
    else:
        print(f"✖ {len(errors)} error(s), {len(warnings)} warning(s).")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
