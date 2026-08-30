#!/usr/bin/env python3
"""sync-portfolio-stats.py — Idempotent portfolio-stat patcher for about/index.html.

Reads assets/data/search-index.json and live tool-ette HTML to compute:
  PAGES       — real indexable pages (excludes /assets/ templates, 404, under-construction)
  TOOL_ETTES  — /toolbox/NX-branch/NXx-tool/ URLs
  BRANCHES    — /toolbox/NX-branch/ URLs
  GPTS        — tool-ette pages that contain a chatgpt.com link

Patches about/index.html in two ways:
  1. AUTOGEN block  <!-- AUTOGEN:PORTFOLIO-STATS --> … <!-- /AUTOGEN:PORTFOLIO-STATS -->
     Regenerates the section-header summary paragraph with live counts.
  2. Inline STAT markers  <!-- STAT:X -->N<!-- /STAT:X -->
     Patches secondary occurrences in pillar paragraphs.

Run order: after build-search-index.py (so the index is fresh).
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent
ABOUT    = REPO / "about" / "index.html"
SHOWCASE = REPO / "showcase" / "index.html"
INDEX    = REPO / "assets" / "data" / "search-index.json"
THEME_CSS = REPO / "assets" / "css" / "theme.css"

AUTOGEN_START = "<!-- AUTOGEN:PORTFOLIO-STATS -->"
AUTOGEN_END   = "<!-- /AUTOGEN:PORTFOLIO-STATS -->"


def compute_stats() -> dict:
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    pages_list = idx.get("pages", [])

    real = [
        p for p in pages_list
        if "/assets/" not in p["url"]
        and p["url"] not in ("/404/", "/under-construction/")
    ]

    tool_ette_pat = re.compile(r"^.*/toolbox/\d+-[^/]+/\d+[a-z]-[^/]+/$")
    branch_pat    = re.compile(r"^.*/toolbox/\d+-[^/]+/$")

    tool_ettes = [p for p in real if tool_ette_pat.match(p["url"])]
    branches   = [p for p in real if branch_pat.match(p["url"])]

    gpt_count = 0
    for f in sorted(REPO.glob("toolbox/*/*/index.html")):
        html = f.read_text(encoding="utf-8")
        if re.search(r"chatgpt\.com|chat\.openai\.com", html):
            gpt_count += 1

    css_lines = sum(1 for _ in THEME_CSS.open(encoding="utf-8"))

    return {
        "pages":      len(real),
        "tool_ettes": len(tool_ettes),
        "branches":   len(branches),
        "gpts":       gpt_count,
        "css_lines":  css_lines,
    }


def build_autogen_block(stats: dict) -> str:
    p = stats["pages"]
    t = stats["tool_ettes"]
    b = stats["branches"]
    g = stats["gpts"]
    lines = [
        AUTOGEN_START,
        f"          <p>",
        f"            Glee&#8209;fully isn't just a collection of tools — it's a fully",
        f"            designed system. {p} pages, {t} Tool&#8209;ettes across {b} branches,",
        f"            {g} Custom GPTs, a shared design language, and a governance model",
        f"            that keeps it all coherent as it grows. Here's the craft underneath",
        f"            the warmth.",
        f"          </p>",
        AUTOGEN_END,
    ]
    return "\n".join(lines)


def patch_autogen(html: str, block: str) -> str:
    rgx = re.compile(
        r"[ \t]*" + re.escape(AUTOGEN_START) + r".*?" + re.escape(AUTOGEN_END),
        re.DOTALL,
    )
    if rgx.search(html):
        return rgx.sub(block, html)
    old_p = (
        "          <p>\n"
        "            Glee&#8209;fully isn't just a collection of tools"
    )
    if old_p in html:
        close = html.index("          </p>", html.index(old_p))
        end = close + len("          </p>")
        return html[:html.index(old_p)] + block + html[end:]
    print("  WARNING: could not locate section-header <p> to patch", file=sys.stderr)
    return html


def patch_stat_markers(html: str, stats: dict) -> str:
    css_lines = stats["css_lines"]
    css_lines_fmt = f"{css_lines:,}"

    mapping = {
        "PAGES":      str(stats["pages"]),
        "TOOL-ETTES": str(stats["tool_ettes"]),
        "BRANCHES":   str(stats["branches"]),
        "GPTS":       str(stats["gpts"]),
        "CSS-LINES":  css_lines_fmt,
    }
    for key, val in mapping.items():
        pattern = re.compile(
            r"<!-- STAT:" + re.escape(key) + r" -->[^<]*<!-- /STAT:" + re.escape(key) + r" -->"
        )
        replacement = f"<!-- STAT:{key} -->{val}<!-- /STAT:{key} -->"
        html = pattern.sub(replacement, html)
    return html


def main() -> int:
    stats = compute_stats()
    print(f"  pages={stats['pages']}  tool-ettes={stats['tool_ettes']}  "
          f"branches={stats['branches']}  gpts={stats['gpts']}  "
          f"css-lines={stats['css_lines']}")

    # --- about/index.html (AUTOGEN block + STAT markers) ---
    src = ABOUT.read_text(encoding="utf-8")
    block = build_autogen_block(stats)
    patched = patch_autogen(src, block)
    patched = patch_stat_markers(patched, stats)
    if patched == src:
        print(f"  {ABOUT.relative_to(REPO)} — already up to date")
    else:
        ABOUT.write_text(patched, encoding="utf-8")
        print(f"  + {ABOUT.relative_to(REPO)} — updated")

    # --- showcase/index.html (STAT markers only) ---
    src2 = SHOWCASE.read_text(encoding="utf-8")
    patched2 = patch_stat_markers(src2, stats)
    if patched2 == src2:
        print(f"  {SHOWCASE.relative_to(REPO)} — already up to date")
    else:
        SHOWCASE.write_text(patched2, encoding="utf-8")
        print(f"  + {SHOWCASE.relative_to(REPO)} — updated")

    return 0


if __name__ == "__main__":
    sys.exit(main())
