#!/usr/bin/env python3
"""
apply-modern-baseline.py — one-shot upgrade pass that applies 2025/2026
web baseline best practices across every public HTML page on the site.

Idempotent: re-running on an already-upgraded page is a no-op. Safe to
run after adding new pages.

What it adds (only when missing):

1. Security meta tags right after <meta name="viewport">:
   * <meta name="referrer" content="strict-origin-when-cross-origin">
   * <meta http-equiv="Content-Security-Policy" content="...">
     CSP allow-list:
       - default-src 'self'
       - script-src adds GTM (GA4) + jsdelivr (Mermaid ESM module) +
         'unsafe-inline' (required by the 26 lazy-CSS onload handlers)
       - style-src 'unsafe-inline' (Mermaid injects inline SVG styles)
         + Google Fonts CSS
       - font-src Google Fonts
       - img-src https: + data: (permissive; brand logos vary)
       - connect-src GA4 endpoints
       - object-src 'none'  (no Flash/Java/etc)
       - base-uri 'self'    (clickjacking guard)
       - form-action 'self' (form hijack guard)

2. Image performance attributes — Core Web Vitals best practice:
   * The first <img> inside <main> is the LCP candidate -> add
     fetchpriority="high" if missing (do NOT add loading=lazy).
   * Every other <img> on the page that lacks loading= -> add
     loading="lazy".
   * decoding="async" already present on every img site-wide (v0.7).

The script is conservative: it never overrides an existing attribute.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".local", "attached_assets", "node_modules", ".cache",
                ".git", ".vscode", "templates"}

CSP = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' "
    "https://www.googletagmanager.com https://cdn.jsdelivr.net; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com; "
    "img-src 'self' data: https:; "
    "connect-src 'self' https://www.google-analytics.com "
    "https://*.google-analytics.com https://www.googletagmanager.com; "
    "object-src 'none'; "
    "base-uri 'self'; "
    "form-action 'self'"
)

REFERRER_META = '<meta name="referrer" content="strict-origin-when-cross-origin" />'
CSP_META = f'<meta http-equiv="Content-Security-Policy" content="{CSP}" />'

VIEWPORT_RE = re.compile(
    r'(\s*<meta\s+name="viewport"\s+content="[^"]+"\s*/?>)',
    re.IGNORECASE
)

# theme-color: split a single legacy tag into a light/dark media-queried
# pair so the browser chrome matches the user's color-scheme preference
# (modern baseline; the site already declares `color-scheme: light dark`).
# Light = cream surface, Dark = muted teal — matches existing brand palette.
THEME_COLOR_LEGACY_RE = re.compile(
    r'<meta\s+name="theme-color"\s+content="#2c5e6f"\s*/?>',
    re.IGNORECASE
)
THEME_COLOR_PAIR = (
    '<meta name="theme-color" content="#f5efe1" media="(prefers-color-scheme: light)" />\n'
    '    <meta name="theme-color" content="#2c5e6f" media="(prefers-color-scheme: dark)" />'
)

# Anti-flash: tiny inline script that reads localStorage before theme.css loads,
# so dark-mode users never see a light flash. Placed just before theme.css <link>.
# Idempotency sentinel: 'okh-theme' present in <head>.
ANTI_FLASH_SCRIPT = (
    '<script>'
    '!function(){'
    'var s=localStorage.getItem("okh-theme");'
    'document.documentElement.setAttribute("data-theme",'
    's==="dark"||(s!=="light"&&window.matchMedia&&'
    'window.matchMedia("(prefers-color-scheme:dark)").matches)'
    '?"dark":"light")'
    '}();'
    '</script>'
)
ANTI_FLASH_RE = re.compile(
    r'([ \t]*<link\b[^>]*\brel="stylesheet"[^>]*\bassets/css/theme\.css[^>]*/?>)',
    re.IGNORECASE
)


def iter_html() -> list[Path]:
    out = []
    for p in ROOT.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        out.append(p)
    return sorted(out)


def add_security_meta(src: str) -> tuple[str, list[str]]:
    """Insert security meta tags right after <meta name=viewport>. Idempotent."""
    actions = []
    if 'name="referrer"' in src and 'http-equiv="Content-Security-Policy"' in src:
        return src, actions
    m = VIEWPORT_RE.search(src)
    if not m:
        return src, ["WARN: no <meta viewport> found — security meta not added"]
    insert = ""
    indent = "    "
    if 'name="referrer"' not in src:
        insert += f"\n{indent}{REFERRER_META}"
        actions.append("added referrer meta")
    if 'http-equiv="Content-Security-Policy"' not in src:
        insert += f"\n{indent}{CSP_META}"
        actions.append("added CSP meta")
    if insert:
        src = src[:m.end()] + insert + src[m.end():]
    return src, actions


def split_theme_color(src: str) -> tuple[str, list[str]]:
    """Split single theme-color tag into a light/dark media pair. Idempotent."""
    if 'media="(prefers-color-scheme:' in src:
        return src, []  # already migrated
    if THEME_COLOR_LEGACY_RE.search(src):
        src = THEME_COLOR_LEGACY_RE.sub(THEME_COLOR_PAIR, src, count=1)
        return src, ["split theme-color into light/dark media pair"]
    return src, []


def upgrade_images(src: str) -> tuple[str, list[str]]:
    """Add fetchpriority to LCP img + loading=lazy to all others. Idempotent."""
    actions = []

    # Find the <main>...</main> region (first one wins; site uses one main)
    main_match = re.search(r'<main\b[^>]*>(.*?)</main>', src, re.DOTALL | re.IGNORECASE)
    lcp_img_position: int | None = None
    if main_match:
        # Position of first <img> inside main, in the FULL src offsets
        first_inside = re.search(r'<img\b[^>]*>', main_match.group(1))
        if first_inside:
            lcp_img_position = main_match.start(1) + first_inside.start()

    # Walk every <img> tag; rewrite as needed
    out_parts = []
    last = 0
    lazy_added = 0
    fp_added = 0
    for m in re.finditer(r'<img\b[^>]*>', src):
        out_parts.append(src[last:m.start()])
        tag = m.group(0)
        is_lcp = (m.start() == lcp_img_position)

        if is_lcp:
            # LCP img: add fetchpriority="high" + loading="eager" (explicit
            # opt-out of lazy is 2025 best practice — never rely on the
            # silent default).
            if 'fetchpriority=' not in tag:
                tag = re.sub(r'(\s*/?>)$', r' fetchpriority="high"\1', tag, count=1)
                fp_added += 1
            if 'loading=' not in tag:
                tag = re.sub(r'(\s*/?>)$', r' loading="eager"\1', tag, count=1)
        else:
            # Non-LCP: add loading="lazy" if no loading= present
            if 'loading=' not in tag:
                tag = re.sub(r'(\s*/?>)$', r' loading="lazy"\1', tag, count=1)
                lazy_added += 1

        out_parts.append(tag)
        last = m.end()
    out_parts.append(src[last:])
    new_src = "".join(out_parts)

    if lazy_added:
        actions.append(f'added loading="lazy" to {lazy_added} img(s)')
    if fp_added:
        actions.append(f'added fetchpriority="high" to {fp_added} LCP img')
    return new_src, actions



def add_anti_flash(src: str) -> tuple[str, list[str]]:
    """Inject the anti-flash theme script before theme.css <link>. Idempotent."""
    head = re.search(r'<head\b[^>]*>(.*?)</head>', src, re.DOTALL | re.IGNORECASE)
    if head and 'okh-theme' in head.group(1):
        return src, []
    m = ANTI_FLASH_RE.search(src)
    if not m:
        return src, ['WARN: no theme.css <link> found — anti-flash script not added']
    indent = re.match(r'[ \t]*', m.group(1)).group(0)
    src = src[:m.start()] + indent + ANTI_FLASH_SCRIPT + '\n' + src[m.start():]
    return src, ['injected anti-flash theme script']


def main() -> int:
    files = iter_html()
    print(f"Scanning {len(files)} HTML files...\n")
    touched = 0
    for path in files:
        src = path.read_text(encoding="utf-8", errors="replace")
        original = src
        all_actions: list[str] = []

        src, acts = add_security_meta(src)
        all_actions.extend(acts)

        src, acts = add_anti_flash(src)
        all_actions.extend(acts)

        src, acts = split_theme_color(src)
        all_actions.extend(acts)

        src, acts = upgrade_images(src)
        all_actions.extend(acts)

        if src != original:
            path.write_text(src, encoding="utf-8")
            rel = path.relative_to(ROOT).as_posix()
            print(f"  [MOD] {rel}")
            for a in all_actions:
                print(f"        - {a}")
            touched += 1
        else:
            rel = path.relative_to(ROOT).as_posix()
            print(f"  [ok ] {rel}")

    print(f"\nDone. Files modified: {touched} of {len(files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
