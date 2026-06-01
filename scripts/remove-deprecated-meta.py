#!/usr/bin/env python3
"""
remove-deprecated-meta.py
Removes meta tags ignored by all major search engines:
  - meta name="keywords"
  - meta name="revisit-after"
Idempotent. Run from repo root.
"""
import re
from pathlib import Path

SKIP = {'assets/', 'attached_assets/', '.local/'}

PATTERNS = [
    re.compile(r'[ \t]*<meta\s+name=["\']keywords["\']\s+content=["\'][^"\']*["\']\s*/?>\n?', re.IGNORECASE),
    re.compile(r'[ \t]*<meta\s+name=["\']revisit-after["\']\s+content=["\'][^"\']*["\']\s*/?>\n?', re.IGNORECASE),
    re.compile(r'[ \t]*<meta\s+content=["\'][^"\']*["\']\s+name=["\']keywords["\']\s*/?>\n?', re.IGNORECASE),
    re.compile(r'[ \t]*<meta\s+content=["\'][^"\']*["\']\s+name=["\']revisit-after["\']\s*/?>\n?', re.IGNORECASE),
]

pages = [p for p in Path('.').rglob('*.html')
         if not any(s in str(p) for s in SKIP)]

cleaned = 0
for page in sorted(pages):
    content = page.read_text(encoding='utf-8', errors='replace')
    original = content
    for pat in PATTERNS:
        content = pat.sub('', content)
    content = re.sub(r'\n{3,}', '\n\n', content)
    if content != original:
        page.write_text(content, encoding='utf-8')
        cleaned += 1
        print(f"  cleaned: {page}")

print(f"\nTotal pages cleaned: {cleaned} of {len(pages)}")
