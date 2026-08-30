#!/usr/bin/env python3
"""
fix-audit-2026-05-12.py
Idempotent remediation for the 2026-05-12 6-domain site audit.
Fixes: color-scheme, viewport-fit=cover, author meta, og:site_name,
       twitter:description, twitter:image, DOCTYPE case.
Safe to re-run: every transform checks current state before writing.
"""
import re
import sys
from pathlib import Path

SKIP_PARTS = {'assets', '.local', 'attached_assets', 'node_modules', '.git', 'tools'}

AUTHOR_TAG   = '<meta name="author" content="Glee&#8209;fully Personalizable Tools™" />'
SITE_NAME_TAG = '<meta property="og:site_name" content="Glee&#8209;fully Personalizable Tools™" />'
VP_CANONICAL  = 'width=device-width, initial-scale=1, viewport-fit=cover'
CS_CANONICAL  = '<meta name="color-scheme" content="light dark" />'

def skip(path):
    return any(part in SKIP_PARTS for part in path.parts)

def get_pages():
    return [p for p in sorted(Path('.').rglob('*.html')) if not skip(p)]

changes_log = []

def fix_page(path):
    content = original = path.read_text(encoding='utf-8', errors='replace')
    page_changes = []

    # ── 1. DOCTYPE case normalisation ───────────────────────────────────────
    if '<!doctype html>' in content and '<!DOCTYPE html>' not in content:
        content = content.replace('<!doctype html>', '<!DOCTYPE html>', 1)
        page_changes.append('DOCTYPE → uppercase')

    # ── 2. color-scheme ─────────────────────────────────────────────────────
    cs_re = re.compile(
        r'<meta\s+name=["\']color-scheme["\']\s+content=["\']([^"\']*)["\'][^>]*/?>',
        re.IGNORECASE
    )
    cs_match = cs_re.search(content)
    if cs_match:
        val = cs_match.group(1)
        if val != 'light dark':
            content = cs_re.sub(CS_CANONICAL, content, count=1)
            page_changes.append(f'color-scheme: "{val}" → "light dark"')
    else:
        # Insert after the dark-media theme-color tag
        dark_tc_re = re.compile(
            r'(<meta\s+name=["\']theme-color["\']\s+content="[^"]+"\s+media=["\'][^"\']+["\'][^>]*/?>)',
            re.IGNORECASE
        )
        new = dark_tc_re.sub(r'\1\n    ' + CS_CANONICAL, content, count=1)
        if new != content:
            content = new
            page_changes.append('color-scheme: added (was missing)')
        else:
            # Fallback: insert after charset
            cs_tag_re = re.compile(r'(<meta\s+charset=[^>]*/?>)', re.IGNORECASE)
            new = cs_tag_re.sub(r'\1\n    ' + CS_CANONICAL, content, count=1)
            if new != content:
                content = new
                page_changes.append('color-scheme: added after charset (fallback)')

    # ── 3. viewport-fit=cover ────────────────────────────────────────────────
    vp_re = re.compile(r'(<meta\s+name=["\']viewport["\']\s+content=["\'])([^"\']+)(["\'])', re.IGNORECASE)
    vp_match = vp_re.search(content)
    if vp_match:
        cur = vp_match.group(2).strip()
        if 'viewport-fit=cover' not in cur:
            # Normalise scale value and append viewport-fit
            normed = re.sub(r'initial-scale=\d+(\.\d+)?', 'initial-scale=1', cur)
            normed = normed.rstrip(', ') + ', viewport-fit=cover'
            content = vp_re.sub(lambda m: m.group(1) + normed + m.group(3), content, count=1)
            page_changes.append('viewport: added viewport-fit=cover')
    else:
        # No viewport at all — insert after charset
        cs_tag_re = re.compile(r'(<meta\s+charset=[^>]*/?>)', re.IGNORECASE)
        vp_full = f'<meta name="viewport" content="{VP_CANONICAL}" />'
        new = cs_tag_re.sub(r'\1\n    ' + vp_full, content, count=1)
        if new != content:
            content = new
            page_changes.append('viewport: inserted full tag (was missing)')

    # ── 4. author meta ────────────────────────────────────────────────────────
    if not re.search(r'name=["\']author["\']', content, re.IGNORECASE):
        # Insert before <meta name="creator"> if present, else before og:title
        ins_re = re.compile(r'(<meta\s+name=["\']creator["\'][^>]*/?>)', re.IGNORECASE)
        new = ins_re.sub(AUTHOR_TAG + '\n    ' + r'\1', content, count=1)
        if new == content:
            ins_re = re.compile(r'(<meta\s+property=["\']og:title["\'][^>]*/?>)', re.IGNORECASE)
            new = ins_re.sub(AUTHOR_TAG + '\n    ' + r'\1', content, count=1)
        if new == content:
            # Fallback: before </head>
            new = content.replace('</head>', '    ' + AUTHOR_TAG + '\n  </head>', 1)
        if new != content:
            content = new
            page_changes.append('author: meta added')

    # ── 5. og:site_name ───────────────────────────────────────────────────────
    if not re.search(r'og:site_name', content, re.IGNORECASE):
        # Insert after og:image:height (or og:image if height not present)
        for anchor_pat in [
            r'(<meta\s+property=["\']og:image:height["\']\s+content=["\'][^"\']*["\'][^>]*/?>)',
            r'(<meta\s+property=["\']og:image:alt["\']\s+content=["\'][^"\']*["\'][^>]*/?>)',
            r'(<meta\s+property=["\']og:image["\'][^>]*/?>)',
        ]:
            ins_re = re.compile(anchor_pat, re.IGNORECASE)
            new = ins_re.sub(r'\1\n    ' + SITE_NAME_TAG, content, count=1)
            if new != content:
                content = new
                page_changes.append('og:site_name: added')
                break

    # ── 6. twitter:description ────────────────────────────────────────────────
    if not re.search(r'twitter:description', content, re.IGNORECASE):
        # Derive from og:description
        og_desc_m = re.search(r'og:description["\']\s+content=["\']([^"\']{1,300})', content, re.IGNORECASE)
        if og_desc_m:
            tw_desc = og_desc_m.group(1)[:200]
            tw_desc_tag = f'<meta name="twitter:description" content="{tw_desc}" />'
            # Insert after twitter:title
            ins_re = re.compile(r'(<meta\s+name=["\']twitter:title["\'][^>]*/?>)', re.IGNORECASE)
            new = ins_re.sub(r'\1\n    ' + tw_desc_tag, content, count=1)
            if new == content:
                # Insert before twitter:site
                ins_re = re.compile(r'(<meta\s+name=["\']twitter:site["\'][^>]*/?>)', re.IGNORECASE)
                new = ins_re.sub(tw_desc_tag + '\n    ' + r'\1', content, count=1)
            if new != content:
                content = new
                page_changes.append('twitter:description: added')

    # ── 7. twitter:image ─────────────────────────────────────────────────────
    if not re.search(r'twitter:image', content, re.IGNORECASE):
        # Derive from og:image
        og_img_m = re.search(r'og:image["\']\s+content=["\']([^"\']+)["\']', content, re.IGNORECASE)
        if og_img_m:
            tw_img = og_img_m.group(1)
            tw_img_tag = f'<meta name="twitter:image" content="{tw_img}" />'
            # Insert after twitter:description (or twitter:title)
            for anchor_pat in [
                r'(<meta\s+name=["\']twitter:description["\'][^>]*/?>)',
                r'(<meta\s+name=["\']twitter:title["\'][^>]*/?>)',
            ]:
                ins_re = re.compile(anchor_pat, re.IGNORECASE)
                new = ins_re.sub(r'\1\n    ' + tw_img_tag, content, count=1)
                if new != content:
                    content = new
                    page_changes.append('twitter:image: added')
                    break

    # ── Write back if changed ─────────────────────────────────────────────────
    if content != original:
        path.write_text(content, encoding='utf-8')
        changes_log.append((str(path), page_changes))
        return len(page_changes)
    return 0

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    pages = get_pages()
    total_files = 0
    total_fixes = 0
    for page in pages:
        n = fix_page(page)
        if n:
            total_files += 1
            total_fixes += n

    print(f'\n{"="*60}')
    print(f'fix-audit-2026-05-12.py — complete')
    print(f'Files modified : {total_files} of {len(pages)}')
    print(f'Total fixes    : {total_fixes}')
    print(f'{"="*60}\n')
    for path, fxs in changes_log:
        print(f'  {path}')
        for fx in fxs:
            print(f'    ✓ {fx}')
    print()
    if '--dry-run' not in sys.argv and total_files == 0:
        print('Nothing to fix — site is already compliant.')
