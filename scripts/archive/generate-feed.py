#!/usr/bin/env python3
"""
generate-feed.py — Atom feed generator
=======================================
Emits `/feed.xml` listing every tool-ette and branch hub pulled from
`assets/data/search-index.json`.

Usage:
    python3 scripts/generate-feed.py
"""
from __future__ import annotations

import html as html_mod
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://glee-fully.tools"

# Deterministic build date — bump manually when content actually changes so
# reruns of this script produce byte-identical output (idempotent).
BUILD_DATE = "2026-05-03T00:00:00Z"


def main() -> int:
    idx_path = ROOT / "assets" / "data" / "search-index.json"
    if not idx_path.exists():
        print("!! Run scripts/build-search-index.py first", file=sys.stderr)
        return 1
    pages = json.loads(idx_path.read_text(encoding="utf-8"))
    if isinstance(pages, dict):
        pages = pages.get("pages", [])

    # Keep only toolbox entries (branches + tool-ettes); skip top-level utilities.
    pages = [p for p in pages if p.get("url", "").startswith("/toolbox/")
             and p["url"] != "/toolbox/"]

    now_iso = BUILD_DATE
    items = []
    for p in pages:
        url = SITE + p["url"]
        title = html_mod.escape(p.get("title", "").split(" — ")[0])
        desc = html_mod.escape(p.get("description", ""))
        items.append(
            f"  <entry>\n"
            f"    <title>{title}</title>\n"
            f'    <link href="{url}" />\n'
            f"    <id>{url}</id>\n"
            f"    <updated>{now_iso}</updated>\n"
            f"    <summary>{desc}</summary>\n"
            f"  </entry>")

    feed = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom">\n'
        '  <title>Glee-fully Personalizable Tools™ — New &amp; Updated</title>\n'
        f'  <link href="{SITE}/feed.xml" rel="self" />\n'
        f'  <link href="{SITE}/" />\n'
        f"  <id>{SITE}/</id>\n"
        f"  <updated>{now_iso}</updated>\n"
        '  <author><name>Glee-fully Personalizable Tools™</name></author>\n'
        '  <subtitle>The retro-bright toolbox of Custom GPTs for life, work, '
        'and wonder.</subtitle>\n'
        + "\n".join(items)
        + "\n</feed>\n"
    )
    out = ROOT / "feed.xml"
    out.write_text(feed, encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)} — {len(items)} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
