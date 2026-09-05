#!/usr/bin/env python3
"""Build the four regional locale drafts without changing public release files.

The canonical English HTML is the source for both regional pairs. Existing
target files are preserved as draft working artifacts during regeneration, so
an editorial pass can update changed units without treating another locale as
translation authority.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTES = {"/": "index.html", "/about/": "about/index.html", "/projects/": "projects/index.html", "/contact/": "contact/index.html"}
REVIEWED_ES_MX = {"index.html": "index.html", "about/index.html": "about-index.html", "projects/index.html": "projects-index.html", "contact/index.html": "contact-index.html"}
BASE = "https://overkillhill.com"

ST_GEORGE = (
    '<svg aria-hidden="true" class="lang-flag" height="14" viewBox="0 0 30 20" width="21">'
    '<rect fill="#FFFFFF" height="20" width="30"/><path d="M0 0L30 20M30 0L0 20" stroke="#CE1124" stroke-width="3"/>'
    '<path d="M15 0V20M0 10H30" stroke="#FFFFFF" stroke-width="6"/><path d="M15 0V20M0 10H30" stroke="#CE1124" stroke-width="3"/>'
    '</svg>'
)
MEXICO = (
    '<svg aria-hidden="true" class="lang-flag" height="14" viewBox="0 0 30 20" width="21">'
    '<rect fill="#006847" height="20" width="10"/><rect fill="#FFFFFF" height="20" width="10" x="10"/><rect fill="#CE1126" height="20" width="10" x="20"/>'
    '</svg>'
)


def noindex(page: str) -> str:
    page = re.sub(r'(<meta[^>]+name=["\']robots["\'][^>]+content=["\'])[^"\']*', r'\1noindex, follow', page, flags=re.I)
    page = re.sub(r'(<meta[^>]+content=["\'])[^"\']*(?=["\'][^>]+name=["\']robots)', r'\1noindex, follow', page, flags=re.I)
    if "name=\"robots\"" not in page and "name='robots'" not in page:
        page = page.replace("</head>", '<meta name="robots" content="noindex, follow">\n</head>')
    return page


def route_links(page: str, source_locale: str, target_locale: str) -> str:
    page = page.replace(f"/{source_locale}/", f"/{target_locale}/")
    return page


def build_en_gb(source: str, route: str) -> str:
    page = source
    page = page.replace('<html lang="en">', '<html lang="en-GB">', 1)
    page = page.replace('https://overkillhill.com' + route, BASE + "/en-gb" + route, 1)
    page = page.replace('content="index, follow', 'content="noindex, follow')
    page = noindex(page)
    page = page.replace('English (US)', 'English (UK) · Draft')
    page = page.replace('Language: English (US)', 'Language: English (UK) · Draft')
    page = page.replace('hreflang="en"', 'hreflang="en-GB"').replace('lang="en"', 'lang="en-GB"')
    page = page.replace('https://overkillhill.com' + route, BASE + '/en-gb' + route)
    page = re.sub(r'<link[^>]+rel="alternate"[^>]*>', '', page, flags=re.I)
    page = page.replace(f'href="{route}" hreflang="en-GB"', f'href="/en-gb{route}" hreflang="en-GB"')
    page = page.replace('class="lang-flag"', 'class="lang-flag"', 1)
    page = re.sub(r'<svg aria-hidden="true" class="lang-flag".*?</svg>', ST_GEORGE, page, count=1, flags=re.S)
    page = re.sub(r'(<a[^>]*class="lang-switch-option is-current"[^>]*>)<svg.*?</svg>(<span class="lang-switch-option-label">).*?</span>(</a>)', r'\1' + ST_GEORGE + r'\2English (UK) · Draft</span>\3', page, count=1, flags=re.S)
    return page


def build_es_mx(source: str, route: str) -> str:
    page = route_links(source, "es", "es-mx")
    page = page.replace('<html lang="es">', '<html lang="es-MX">', 1)
    page = page.replace('https://overkillhill.com/es' + route, BASE + '/es-mx' + route)
    page = noindex(page)
    page = page.replace('hreflang="es"', 'hreflang="es-MX"').replace('lang="es"', 'lang="es-MX"')
    page = page.replace('Español</span>', 'Español (México) · Borrador</span>')
    page = page.replace('aria-label="Language: Español"', 'aria-label="Language: Español (México) · Borrador"')
    page = page.replace('aria-label="Español"', 'aria-label="Español (México) · Borrador"')
    page = re.sub(r'<link[^>]+rel="alternate"[^>]*>', '', page, flags=re.I)
    page = re.sub(r'<svg aria-hidden="true" class="lang-flag".*?</svg>', MEXICO, page, count=1, flags=re.S)
    page = re.sub(r'(<a[^>]*class="lang-switch-option is-current"[^>]*>)<svg.*?</svg>(<span class="lang-switch-option-label">).*?</span>(</a>)', r'\1' + MEXICO + r'\2Español (México) · Borrador</span>\3', page, count=1, flags=re.S)
    # Project-level Mexican usage overrides. Preserve intentional technology
    # terms such as workflow and promptcraft rather than forcing calques.
    page = page.replace('ordenador', 'computadora').replace('móvil', 'celular')
    return page


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--locale', choices=('en-gb', 'es-mx'), required=True)
    args = parser.parse_args()
    for route, rel in ROUTES.items():
        source_path = ROOT / rel
        if not source_path.exists():
            raise SystemExit(f'Missing source page: {source_path}')
        page = source_path.read_text(encoding='utf-8')
        output = ROOT / args.locale / rel
        # The canonical English page is always opened first. es-MX output is
        # emitted from the reviewed pair artifact, never from another locale
        # or from the generated output directory.
        reviewed = ROOT / 'i18n' / 'pilot' / 'es-mx' / 'reviewed' / REVIEWED_ES_MX[rel]
        target_input = reviewed.read_text(encoding='utf-8') if args.locale == 'es-mx' else page
        rendered = build_en_gb(page, route) if args.locale == 'en-gb' else build_es_mx(target_input, route)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding='utf-8')
        print(output.relative_to(ROOT))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
