#!/usr/bin/env python3
"""
Refresh assets/search-index.json against current HTML.

Behaviour:
  - For every entry whose `url` does NOT contain `#`, re-derive
    `title`, `description`, `headings`, `body` from the live HTML.
  - For every top-level page on disk not present in the index,
    append a minimal entry (Category guessed from URL prefix).
  - Anchor entries (`url` contains `#`) are passed through untouched —
    they're hand-curated section deep-links.
  - Write back with stable ordering: anchors stay where they were, new
    pages appended at the end of their natural group.

Idempotent: re-running on a fully-fresh tree changes nothing.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "assets" / "search-index.json"
SKIP_DIRS = {"_replit", ".local", "attached_assets", "node_modules", "dist", ".git"}
SKIP_PAGES = {"404.html", "under-construction.html"}

CATEGORY_BY_PREFIX = [
    ("/writings/first-diagram-is-a-liar/v03/", "Article Variant"),
    ("/writings/", "Writing"),
    ("/projects/", "Project"),
    ("/about/", "Brand"),
    ("/manifesto/", "Brand"),
    ("/contact/", "Brand"),
    ("/legal/", "Brand"),
    ("/found-ry/", "Brand"),
    ("/universe/", "Brand"),
    ("/prompt-forge/", "Tool"),
    ("/search/", "Utility"),
    ("/", "Home"),
]

def url_to_path(url: str) -> Path | None:
    if "#" in url: return None
    rel = url.strip("/")
    p = ROOT / rel / "index.html" if rel else ROOT / "index.html"
    return p if p.exists() else None

def category_for(url: str) -> str:
    for pfx, cat in CATEGORY_BY_PREFIX:
        if url.startswith(pfx): return cat
    return "Page"

def extract(p: Path) -> dict:
    soup = BeautifulSoup(p.read_text(encoding="utf-8"), "lxml")
    title = (soup.title.string.strip() if soup.title and soup.title.string else "").strip()
    desc_tag = soup.find("meta", attrs={"name": "description"})
    desc = (desc_tag.get("content", "") if desc_tag else "").strip()
    headings = [h.get_text(" ", strip=True) for h in soup.find_all(["h1", "h2", "h3"])]
    # body: visible text from <main>, fallback to <body>
    main = soup.find("main") or soup.body
    if main:
        for tag in main.find_all(["script", "style", "nav", "footer"]): tag.decompose()
        body = re.sub(r"\s+", " ", main.get_text(" ", strip=True)).strip()
    else:
        body = ""
    # cap body at ~1200 chars per entry to keep index lean
    if len(body) > 1200: body = body[:1200].rsplit(" ", 1)[0] + "…"
    return {"title": title, "description": desc, "headings": headings, "body": body}

def discover_pages() -> list[str]:
    urls: list[str] = []
    for p in sorted(ROOT.rglob("index.html")):
        rel_parts = p.relative_to(ROOT).parts
        if set(rel_parts) & SKIP_DIRS: continue
        if "templates" in rel_parts: continue
        url = "/" + "/".join(rel_parts[:-1])
        if not url.endswith("/"): url += "/"
        urls.append(url)
    return urls

def main(check: bool = False) -> int:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    entries: list[dict] = data["entries"]
    seen_urls = {e["url"] for e in entries}

    changes = 0
    orphans: list[str] = []
    # 1. refresh top-level entries; flag anchor-less entries with no live page as orphans
    surviving: list[dict] = []
    for e in entries:
        if "#" not in e["url"]:
            p = url_to_path(e["url"])
            if not p:
                orphans.append(e["url"])
                changes += 1
                continue  # drop orphan
            fresh = extract(p)
            for k, v in fresh.items():
                if e.get(k) != v:
                    e[k] = v
                    changes += 1
        surviving.append(e)
    entries[:] = surviving

    # 2. add missing top-level pages
    for url in discover_pages():
        if url in seen_urls: continue
        p = url_to_path(url)
        if not p: continue
        fresh = extract(p)
        entries.append({
            "url": url,
            "title": fresh["title"],
            "category": category_for(url),
            "description": fresh["description"],
            "headings": fresh["headings"],
            "body": fresh["body"],
        })
        changes += 1
        print(f"  + added {url}")

    if data.get("count") != len(entries):
        changes += 1
    data["count"] = len(entries)

    if check:
        if changes:
            print(f"--check: search index is STALE ({changes} change(s)). Re-run without --check.")
            if orphans:
                print(f"  orphaned entries (page no longer exists): {orphans}")
            return 1
        print(f"--check: search index is fresh ({len(entries)} entries).")
        return 0
    if orphans:
        print(f"  − dropped {len(orphans)} orphan entries: {orphans}")

    INDEX.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ wrote {INDEX.relative_to(ROOT)} — {len(entries)} entries, {changes} field/entry change(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main(check="--check" in sys.argv))
