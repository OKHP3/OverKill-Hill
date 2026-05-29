#!/usr/bin/env python3
"""
add-toolbox-to-footer.py
Inserts /toolbox/ as the second footer nav item, after "Why Glee-fully".
Idempotent — skips any page whose <footer> already contains /toolbox/.
Handles both relative (homepage) and absolute URL variants.
Run from repo root.
"""
import re
from pathlib import Path

SKIP = {'assets/', 'attached_assets/', '.local/'}

# Matches the "Why Glee-fully" <li> in both relative (#why) and absolute (/#why) form
WHY_PATTERN = re.compile(
    r'(<li><a href=["\'](?:https?://glee-fully\.tools)?/?#why["\'][^>]*>Why Glee[^<]*</a></li>)',
    re.IGNORECASE
)

pages = [p for p in Path('.').rglob('*.html')
         if not any(s in str(p) for s in SKIP)]

updated = 0
for page in sorted(pages):
    content = page.read_text(encoding='utf-8', errors='replace')

    # Find footer block
    footer_match = re.search(r'<footer\b.*?</footer>', content, re.DOTALL | re.IGNORECASE)
    if not footer_match:
        continue

    footer_html = footer_match.group(0)

    # Skip if already has /toolbox/ in footer
    if '/toolbox/' in footer_html:
        continue

    # Determine URL style: homepage uses relative, inner pages use absolute
    if str(page) == 'index.html':
        toolbox_href = 'toolbox/'
    else:
        toolbox_href = '/toolbox/'

    toolbox_item = f'<li><a href="{toolbox_href}">Opening the Toolbox</a></li>'

    # Find the Why item and inject after it, preserving indentation
    def insert_after_why(m):
        why_item = m.group(1)
        # Detect leading whitespace from the line
        line_start = content.rfind('\n', 0, footer_match.start() + footer_html.find(m.group(0)))
        indent = re.match(r'\n(\s*)', content[line_start:])
        pad = indent.group(1) if indent else '            '
        return why_item + '\n' + pad + toolbox_item

    new_footer = WHY_PATTERN.sub(insert_after_why, footer_html, count=1)

    if new_footer != footer_html:
        content = content[:footer_match.start()] + new_footer + content[footer_match.end():]
        page.write_text(content, encoding='utf-8')
        updated += 1
        print(f"  updated: {page}")

print(f"\nFooter toolbox added to: {updated} of {len(pages)} pages")
