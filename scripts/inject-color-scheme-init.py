#!/usr/bin/env python3
"""
inject-color-scheme-init.py

Injects a tiny blocking inline <script> into every HTML page's <head>
so the browser applies the user's saved color-scheme preference from
localStorage BEFORE CSS is painted — preventing a flash of the wrong theme.

The script sets data-color-scheme="dark" or "light" on <html> using the
"glee-color-scheme" localStorage key written by the Glee toggle in app.js.

Injection point  : immediately after <meta charset="utf-8" ...> on the
                   first matching line in <head>.
Idempotency guard: <!-- AUTOGEN:COLOR-SCHEME-INIT --> marker — pages that
                   already have the marker are skipped.

Run from repo root: python3 scripts/inject-color-scheme-init.py
"""

import re
from pathlib import Path

SKIP = {'assets/', 'attached_assets/', '.local/', '.agents/', '.pythonlibs/', 'node_modules/'}

MARKER = '<!-- AUTOGEN:COLOR-SCHEME-INIT -->'

ANTI_FOSC = (
    "<!-- AUTOGEN:COLOR-SCHEME-INIT -->\n"
    "    <script>"
    "(function(){try{var s=localStorage.getItem('glee-color-scheme');"
    "if(s==='dark'||s==='light')"
    "document.documentElement.setAttribute('data-color-scheme',s);"
    "}catch(e){}})();"
    "</script>"
)

CHARSET_RE = re.compile(
    r'(<meta\s[^>]*charset\s*=\s*["\']?utf-8["\']?[^>]*>)',
    re.IGNORECASE,
)

pages = [
    p for p in Path('.').rglob('*.html')
    if not any(s in str(p) for s in SKIP)
]

injected = 0
skipped  = 0

for page in sorted(pages):
    text = page.read_text(encoding='utf-8', errors='replace')

    if MARKER in text:
        skipped += 1
        continue

    m = CHARSET_RE.search(text)
    if not m:
        print(f"  WARN no <meta charset> found: {page}")
        skipped += 1
        continue

    insert_pos = m.end()
    new_text = text[:insert_pos] + '\n    ' + ANTI_FOSC + text[insert_pos:]
    page.write_text(new_text, encoding='utf-8')
    injected += 1
    print(f"  injected: {page}")

print(f"\nColor-scheme init injected into {injected} pages; {skipped} already up-to-date.")
