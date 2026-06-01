#!/usr/bin/env python3
"""
check-links.py — Internal link validator
=========================================
Walks every HTML file and validates every internal href against the
filesystem.  Cross-references the result with `sitemap.xml`.

Outputs:
  assets/audit/links-report-2026-05-03.json

Usage:
    python3 scripts/check-links.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"node_modules", ".local", ".git", "attached_assets", "assets", ".pythonlibs", ".cache", ".agents"}
SITE = "https://glee-fully.tools"


def is_external(href: str) -> bool:
    return href.startswith((
        "http://", "https://", "mailto:", "tel:",
        "javascript:", "data:", "#"
    ))


def resolves(href: str, source_dir: Path) -> bool:
    """Does this internal href resolve to a real file or dir/index.html?"""
    clean = href.split("#")[0].split("?")[0]
    if not clean:
        return True
    if clean.startswith("/"):
        target = ROOT / clean.lstrip("/")
    else:
        target = (source_dir / clean).resolve()
    if target.is_file():
        return True
    if target.is_dir() and (target / "index.html").is_file():
        return True
    if (Path(str(target).rstrip("/")) / "index.html").is_file():
        return True
    return False


def main() -> int:
    pages = []
    all_internal = 0
    all_external = 0
    broken: list[dict] = []
    style_issues: list[dict] = []

    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if any(s in rel.parts for s in SKIP_DIRS):
            continue
        html = path.read_text(encoding="utf-8", errors="replace")
        n_int = n_ext = 0
        for m in re.finditer(r'href=["\']([^"\']+)["\']', html):
            href = m.group(1)
            if is_external(href):
                n_ext += 1
                continue
            n_int += 1
            if not resolves(href, path.parent):
                broken.append({"page": rel.as_posix(), "href": href})
            # style: directory URLs ought to end in trailing /
            clean = href.split("#")[0].split("?")[0]
            if (clean and not clean.endswith(("/", ".html", ".png", ".jpg",
                                               ".jpeg", ".svg", ".gif",
                                               ".webp", ".ico", ".pdf",
                                               ".xml", ".json", ".webmanifest",
                                               ".css", ".js", ".txt"))
                    and "?" not in href and "#" not in href.split("?")[0]):
                # Could be a directory missing slash; only flag if a dir exists.
                clean_path = (ROOT / clean.lstrip("/")
                              if clean.startswith("/")
                              else (path.parent / clean).resolve())
                if clean_path.is_dir():
                    style_issues.append({
                        "page": rel.as_posix(),
                        "href": href,
                        "issue": "missing trailing slash",
                    })
        pages.append({"path": rel.as_posix(),
                      "internal_links": n_int,
                      "external_links": n_ext})
        all_internal += n_int
        all_external += n_ext

    # Sitemap coverage
    sitemap = ROOT / "sitemap.xml"
    sitemap_urls: set[str] = set()
    if sitemap.exists():
        sitemap_urls = {m.group(1)
                        for m in re.finditer(r"<loc>([^<]+)</loc>",
                                             sitemap.read_text(encoding="utf-8"))}

    file_urls = set()
    for p in ROOT.rglob("index.html"):
        rel = p.relative_to(ROOT)
        if any(s in rel.parts for s in SKIP_DIRS):
            continue
        if rel.parts[0] in {"under-construction.html"}:
            continue
        if rel.as_posix() == "index.html":
            file_urls.add(f"{SITE}/")
        else:
            file_urls.add(f"{SITE}/{'/'.join(rel.parts[:-1])}/")

    missing_from_sitemap = sorted(file_urls - sitemap_urls
                                   - {f"{SITE}/under-construction.html",
                                      f"{SITE}/404.html"})
    extra_in_sitemap = sorted(sitemap_urls - file_urls)

    audit_dir = ROOT / "assets" / "audit"
    audit_dir.mkdir(exist_ok=True)
    out = audit_dir / "links-report-2026-05-03.json"
    out.write_text(json.dumps({
        "generated": "2026-05-03",
        "pages_scanned": len(pages),
        "internal_links": all_internal,
        "external_links": all_external,
        "broken_links": broken,
        "style_issues": style_issues,
        "sitemap": {
            "total_urls": len(sitemap_urls),
            "missing_from_sitemap": missing_from_sitemap,
            "extra_in_sitemap": extra_in_sitemap,
        },
        "by_page": pages,
    }, indent=2), encoding="utf-8")

    print(f"Pages scanned:    {len(pages)}")
    print(f"Internal links:   {all_internal}")
    print(f"External links:   {all_external}")
    print(f"Broken links:     {len(broken)}")
    for b in broken[:20]:
        print(f"  ! {b['page']}: {b['href']}")
    print(f"Style issues:     {len(style_issues)}")
    print(f"Sitemap URLs:     {len(sitemap_urls)}  "
          f"(file pages without sitemap: {len(missing_from_sitemap)}, "
          f"sitemap entries without files: {len(extra_in_sitemap)})")
    if missing_from_sitemap:
        for u in missing_from_sitemap:
            print(f"  + missing in sitemap: {u}")
    if extra_in_sitemap:
        for u in extra_in_sitemap:
            print(f"  - sitemap entry has no file: {u}")
    print(f"Detail: {out.relative_to(ROOT)}")
    return 1 if (broken or extra_in_sitemap) else 0


if __name__ == "__main__":
    sys.exit(main())
