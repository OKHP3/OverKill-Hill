#!/usr/bin/env python3
"""
Apply modern (2025/2026) HTML hygiene to every production page. Idempotent.

For every page, ensures:
  1. <meta name="color-scheme" content="dark light" />     — UA dark/light hint
  2. Skip-link as first <body> child                       — WCAG 2.2 baseline
  3. <script type="speculationrules">                       — instant nav (Chrome 121+)
  4. (mermaid pages only) preconnect + modulepreload to    — render-time win
     https://cdn.jsdelivr.net for the mermaid ESM module

Each insertion is gated on a presence check so re-runs are no-ops.
Supports --check (exits 1 if any page would change).
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"_replit", ".local", "attached_assets", "node_modules", "dist", ".git"}

COLOR_SCHEME = '    <meta name="color-scheme" content="dark light" />\n'

SKIP_LINK = '    <a class="okh-skip-link" href="#main">Skip to main content</a>\n'

SPECULATION_RULES = '''    <script type="speculationrules">
    {
      "prefetch": [
        { "source": "document", "where": { "and": [
          { "href_matches": "/*" },
          { "not": { "selector_matches": "[rel~=nofollow]" } },
          { "not": { "href_matches": "/*.{png,jpg,jpeg,webp,svg,ico,gif,pdf,zip}" } }
        ]}, "eagerness": "moderate" }
      ]
    }
    </script>
'''

MERMAID_PRECONNECT = '    <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin />\n'
MERMAID_MODULEPRELOAD = '    <link rel="modulepreload" href="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs" crossorigin />\n'


def is_production_page(p: Path) -> bool:
    if set(p.parts) & SKIP: return False
    if "templates" in p.parts: return False
    return p.suffix == ".html"


def has_mermaid(text: str) -> bool:
    return bool(re.search(r'<(?:div|pre|figure)[^>]*class="(?:[^"]*\s)?mermaid(?:\s[^"]*)?"', text))


def apply(text: str, mermaid: bool) -> tuple[str, list[str]]:
    notes: list[str] = []

    # 1. color-scheme meta (insert right after charset meta)
    if 'name="color-scheme"' not in text:
        m = re.search(r'(<meta charset="[^"]+"\s*/?>\s*\n)', text)
        if m:
            text = text[:m.end()] + COLOR_SCHEME + text[m.end():]
            notes.append("color-scheme")

    # 2. speculation rules (insert just before </head>)
    if 'type="speculationrules"' not in text:
        text = text.replace("</head>", SPECULATION_RULES + "  </head>", 1)
        notes.append("speculation-rules")

    # 3. mermaid preconnect + modulepreload (only on diagram pages)
    if mermaid:
        if 'href="https://cdn.jsdelivr.net"' not in text and 'href=\'https://cdn.jsdelivr.net\'' not in text:
            text = text.replace("</head>", MERMAID_PRECONNECT + "  </head>", 1)
            notes.append("jsdelivr-preconnect")
        if 'rel="modulepreload"' not in text or "mermaid.esm.min.mjs" not in text.split('rel="modulepreload"')[0]:
            if "rel=\"modulepreload\" href=\"https://cdn.jsdelivr.net/npm/mermaid" not in text:
                text = text.replace("</head>", MERMAID_MODULEPRELOAD + "  </head>", 1)
                notes.append("mermaid-modulepreload")

    # 4. skip-link as first <body> child.
    # If a legacy `<a class="skip-link">` exists, REPLACE it (avoids dupes).
    legacy_re = re.compile(
        r'[ \t]*<a [^>]*class="skip-link"[^>]*>[^<]*</a>\s*\n'
        r'|[ \t]*<a [^>]*href="#main"[^>]*class="skip-link"[^>]*>[^<]*</a>\s*\n'
    )
    if 'class="okh-skip-link"' not in text:
        if legacy_re.search(text):
            text, n = legacy_re.subn(SKIP_LINK, text, count=1)
            if n: notes.append("skip-link (replaced legacy)")
        else:
            m = re.search(r'(<body[^>]*>\s*\n)', text)
            if m:
                text = text[:m.end()] + SKIP_LINK + text[m.end():]
                notes.append("skip-link")
    else:
        # okh-skip-link already present; remove any leftover legacy duplicate
        if legacy_re.search(text):
            text, n = legacy_re.subn("", text)
            if n: notes.append(f"removed {n} legacy skip-link dupe(s)")

    return text, notes


def main(check: bool = False) -> int:
    changed_pages = 0
    for p in sorted(ROOT.rglob("*.html")):
        if not is_production_page(p): continue
        text = p.read_text(encoding="utf-8")
        new, notes = apply(text, has_mermaid(text))
        if not notes: continue
        changed_pages += 1
        if check:
            print(f"  ~ {p.relative_to(ROOT)}  [{', '.join(notes)}]")
        else:
            p.write_text(new, encoding="utf-8")
            print(f"  ✓ {p.relative_to(ROOT)}  [{', '.join(notes)}]")
    if check:
        print(f"\n--check: {changed_pages} page(s) would change.")
        return 1 if changed_pages else 0
    print(f"\n✓ modernized {changed_pages} page(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main(check="--check" in sys.argv))
