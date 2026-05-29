#!/usr/bin/env python3
"""
inject-breadcrumb.py — Visible <nav aria-label="Breadcrumb"> injector
======================================================================
Reads the JSON-LD BreadcrumbList that inject-jsonld.py already emitted
and renders a matching visible breadcrumb just inside <main id="main">.

Idempotent via <!-- AUTOGEN:BREADCRUMB --> markers.
Skips pages without a JSON-LD BreadcrumbList (homepage, search, 404,
under-construction).

Usage:
    python3 scripts/inject-breadcrumb.py
"""
from __future__ import annotations

import html as html_mod
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"node_modules", ".local", ".git", "attached_assets", "assets"}
# Pages that ship their own hand-written visible breadcrumb. Skip to avoid
# duplicate <nav aria-label="Breadcrumb"> blocks (a11y regression).
SKIP_FILES = {"search/index.html"}

START = "<!-- AUTOGEN:BREADCRUMB -->"
END = "<!-- /AUTOGEN:BREADCRUMB -->"


def extract_breadcrumb(html: str) -> list[tuple[str, str]] | None:
    """Find first JSON-LD BreadcrumbList and return [(name, url), ...]."""
    for m in re.finditer(
            r'<script\s+type="application/ld\+json">\s*(.*?)\s*</script>',
            html, re.DOTALL):
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        graph = data.get("@graph") if isinstance(data, dict) else None
        nodes = graph if isinstance(graph, list) else [data]
        for node in nodes:
            if not isinstance(node, dict):
                continue
            crumb = (node.get("breadcrumb")
                     if node.get("@type") in ("WebPage", "SoftwareApplication",
                                               "CollectionPage", "AboutPage",
                                               "ContactPage")
                     else node)
            if not isinstance(crumb, dict):
                continue
            if crumb.get("@type") != "BreadcrumbList":
                continue
            items = []
            for it in crumb.get("itemListElement", []):
                name = it.get("name")
                url = it.get("item")
                if name and url:
                    items.append((name, url))
            if items:
                return items
    return None


def render(items: list[tuple[str, str]]) -> str:
    lis = []
    last = len(items) - 1
    for i, (name, url) in enumerate(items):
        safe = html_mod.escape(name)
        if i == last:
            lis.append(
                f'        <li class="glee-breadcrumb-item glee-breadcrumb-current"'
                f' aria-current="page">{safe}</li>')
        else:
            lis.append(
                f'        <li class="glee-breadcrumb-item">'
                f'<a href="{url}">{safe}</a></li>')
    inner = "\n".join(lis)
    return (
        f"      {START}\n"
        f'      <nav class="glee-breadcrumb" aria-label="Breadcrumb">\n'
        f'        <ol class="glee-breadcrumb-list">\n'
        f"{inner}\n"
        f"        </ol>\n"
        f"      </nav>\n"
        f"      {END}"
    )


def inject(html: str, block: str) -> str:
    """Replace existing AUTOGEN block (with leading indent) or insert just
    after the opening <main id="main"> tag."""
    rgx = re.compile(r"[ \t]*" + re.escape(START) + r".*?" + re.escape(END),
                     re.DOTALL)
    if rgx.search(html):
        return rgx.sub(block, html)
    main_open = re.search(r'<main\b[^>]*\bid="main"[^>]*>', html)
    if not main_open:
        return html
    insert_at = main_open.end()
    return html[:insert_at] + "\n" + block + html[insert_at:]


def main() -> int:
    edited = 0
    skipped = 0
    pre_existing = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if any(s in rel.parts for s in SKIP_DIRS):
            continue
        if rel.as_posix() in SKIP_FILES:
            skipped += 1
            continue
        html = path.read_text(encoding="utf-8", errors="replace")
        # Defensive: if the page ships a hand-written visible breadcrumb
        # (outside our AUTOGEN markers), do not add a duplicate.
        stripped = re.sub(re.escape(START) + r".*?" + re.escape(END), "",
                          html, flags=re.DOTALL)
        if re.search(r'<nav\b[^>]*aria-label="Breadcrumb"', stripped):
            pre_existing += 1
            skipped += 1
            continue
        items = extract_breadcrumb(html)
        if not items:
            skipped += 1
            continue
        block = render(items)
        new_html = inject(html, block)
        if new_html != html:
            path.write_text(new_html, encoding="utf-8")
            edited += 1
            print(f"  + {rel}")
    print(f"\nDone. Injected {edited} breadcrumb(s); skipped {skipped} "
          f"(no JSON-LD breadcrumb, in SKIP_FILES, or already has a hand-written one — "
          f"{pre_existing} of those were the hand-written kind).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
