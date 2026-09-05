#!/usr/bin/env python3
"""Build the four regional locale drafts without changing public release files.

The canonical English HTML is the source for both regional pairs. Existing
target files are preserved as draft working artifacts during regeneration, so
an editorial pass can update changed units without treating another locale as
translation authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTES = {"/": "index.html", "/about/": "about/index.html", "/projects/": "projects/index.html", "/contact/": "contact/index.html"}
REVIEWED_ES_MX = {"index.html": "index.html", "about/index.html": "about-index.html", "projects/index.html": "projects-index.html", "contact/index.html": "contact-index.html"}
BASE = "https://overkillhill.com"
SOURCE_HASHES = ROOT / 'i18n' / 'pilot' / 'source-hashes-release-0ee.json'
PAIR_CONTRACTS = {
    'en-gb': ('dictionary.en-us-en-uk.json', 'voice-profile.en-us.json'),
    'es-mx': ('dictionary.en-us-es-mx.json', 'voice-profile.en-us.json'),
}

ST_GEORGE = (
    '<svg aria-hidden="true" class="lang-flag" height="14" viewBox="0 0 30 20" width="21">'
    '<rect fill="#FFFFFF" height="20" width="30"/><path d="M15 0V20M0 10H30" stroke="#CE1124" stroke-width="4"/>'
    '</svg>'
)
MEXICO = (
    '<svg aria-hidden="true" class="lang-flag" height="14" viewBox="0 0 30 20" width="21">'
    '<rect fill="#006847" height="20" width="10"/><rect fill="#FFFFFF" height="20" width="10" x="10"/><rect fill="#CE1126" height="20" width="10" x="20"/>'
    '<g aria-label="Mexico coat of arms" transform="translate(15 10)"><path d="M-1.7-2.8C.6-3.8 2.8-2 2.1.1C1.5 1.9-.5 3-2.1 2.1C-3.3 1.4-3.1-.7-1.7-2.8Z" fill="#6B4F2F"/><path d="M-2.4 2.6c.7-2.1 1.2-3 2.2-3.8M-3.1 1.1l1.2.5M-2.8-.4l1.1.5" fill="none" stroke="#006847" stroke-linecap="round" stroke-width=".65"/><path d="M1.1-1.7l1.5-.8" stroke="#CE1126" stroke-linecap="round" stroke-width=".65"/></g>'
    '</svg>'
)

USA = (
    '<svg aria-hidden="true" class="lang-flag" height="14" viewBox="0 0 30 20" width="21">'
    '<rect fill="#B22234" height="20" width="30"/><rect fill="#FFFFFF" height="1.54" width="30" y="1.54"/>'
    '<rect fill="#FFFFFF" height="1.54" width="30" y="4.62"/><rect fill="#FFFFFF" height="1.54" width="30" y="7.69"/>'
    '<rect fill="#FFFFFF" height="1.54" width="30" y="10.77"/><rect fill="#FFFFFF" height="1.54" width="30" y="13.85"/>'
    '<rect fill="#FFFFFF" height="1.54" width="30" y="16.92"/><rect fill="#3C3B6E" height="10.77" width="12"/>'
    '</svg>'
)
FRANCE = '<svg aria-hidden="true" class="lang-flag" height="14" viewBox="0 0 30 20" width="21"><rect fill="#0055A4" height="20" width="10"/><rect fill="#FFFFFF" height="20" width="10" x="10"/><rect fill="#EF4135" height="20" width="10" x="20"/></svg>'
GERMANY = '<svg aria-hidden="true" class="lang-flag" height="14" viewBox="0 0 30 20" width="21"><rect fill="#000000" height="6.67" width="30"/><rect fill="#DD0000" height="6.67" width="30" y="6.67"/><rect fill="#FFCE00" height="6.66" width="30" y="13.34"/></svg>'
SPAIN = '<svg aria-hidden="true" class="lang-flag" height="14" viewBox="0 0 30 20" width="21"><rect fill="#AA151B" height="5" width="30"/><rect fill="#F1BF00" height="10" width="30" y="5"/><rect fill="#AA151B" height="5" width="30" y="15"/></svg>'
LOCALE_MENU = (
    ('en', 'en', 'English (US)', USA),
    ('en-gb', 'en-GB', 'English (UK) · Draft', ST_GEORGE),
    ('fr', 'fr', 'Français', FRANCE),
    ('de', 'de', 'Deutsch', GERMANY),
    ('es', 'es', 'Español', SPAIN),
    ('es-mx', 'es-MX', 'Español (México) · Borrador', MEXICO),
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


def locale_href(locale: str, route: str) -> str:
    return route if locale == 'en' else f'/{locale}{route}'


def render_locale_switch(active_locale: str, route: str) -> str:
    """Render the complete draft selector without changing published locale pages."""
    active = next(item for item in LOCALE_MENU if item[0] == active_locale)
    options = []
    for locale, tag, label, flag in LOCALE_MENU:
        current = ' aria-current="true" class="lang-switch-option is-current"' if locale == active_locale else ' class="lang-switch-option"'
        options.append(
            f'<li><a{current} aria-label="{label}" href="{locale_href(locale, route)}" hreflang="{tag}" lang="{tag}">{flag}'
            f'<span class="lang-switch-option-label">{label}</span></a></li>'
        )
    return (
        '<div class="lang-switch"><button aria-expanded="false" aria-haspopup="true" '
        f'aria-label="Language: {active[2]}" class="lang-switch-toggle" type="button">'
        f'<span class="lang-flag-current">{active[3]}</span></button>'
        f'<ul class="lang-switch-menu" hidden>{"".join(options)}</ul></div>'
    )


def replace_locale_switch(page: str, active_locale: str, route: str) -> str:
    updated, count = re.subn(
        r'<div class="lang-switch">.*?</ul></div>',
        render_locale_switch(active_locale, route),
        page,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise SystemExit(f'Missing language switcher for {active_locale} {route}')
    return updated


def load_pair_contract(locale: str) -> tuple[dict, dict]:
    pair_dir = ROOT / 'i18n' / 'pilot' / locale
    dictionary_name, profile_name = PAIR_CONTRACTS[locale]
    dictionary = json.loads((pair_dir / dictionary_name).read_text(encoding='utf-8'))
    profile = json.loads((pair_dir / profile_name).read_text(encoding='utf-8'))
    pair = dictionary.get('language_pair', {})
    profile_pair = profile.get('language_pair', profile)
    if pair.get('source_locale') != 'en-US' or profile_pair.get('source_locale') != 'en-US':
        raise SystemExit(f'Invalid source locale in {locale} pair contract')
    target_locale = 'en-GB' if locale == 'en-gb' else 'es-MX'
    if pair.get('target_locale') != target_locale:
        raise SystemExit(f'Invalid dictionary target locale for {locale}')
    return dictionary, profile


def verify_sources() -> dict:
    expected = json.loads(SOURCE_HASHES.read_text(encoding='utf-8'))
    actual = {}
    for route, rel in ROUTES.items():
        source_path = ROOT / rel
        actual[route] = hashlib.sha256(source_path.read_bytes()).hexdigest()
        if actual[route] != expected['routes'].get(route):
            raise SystemExit(f'Source changed for {route}; refresh the reviewed pair from the recorded source revision')
    return expected


def build_en_gb(source: str, route: str, dictionary: dict) -> str:
    page = source
    page = page.replace('<html lang="en">', '<html lang="en-GB">', 1)
    page = page.replace('https://overkillhill.com' + route, BASE + "/en-gb" + route, 1)
    page = page.replace('content="index, follow', 'content="noindex, follow')
    page = noindex(page)
    page = page.replace('English (US)', 'English (UK) · Draft')
    page = page.replace('Language: English (US)', 'Language: English (UK) · Draft')
    page = page.replace('hreflang="en"', 'hreflang="en-GB"').replace('lang="en"', 'lang="en-GB"')
    page = page.replace('https://overkillhill.com' + route, BASE + '/en-gb' + route)
    for entry in dictionary.get('entries', []):
        if entry.get('handling') == 'adapt':
            page = re.sub(rf'\b{re.escape(entry["source"])}\b', entry['target'], page)
    page = page.replace('colors', 'colours').replace('Color Scheme', 'Colour Scheme')
    page = re.sub(r'<link[^>]+rel="alternate"[^>]*>', '', page, flags=re.I)
    page = page.replace(f'href="{route}" hreflang="en-GB"', f'href="/en-gb{route}" hreflang="en-GB"')
    page = page.replace('class="lang-flag"', 'class="lang-flag"', 1)
    page = re.sub(r'<svg aria-hidden="true" class="lang-flag".*?</svg>', ST_GEORGE, page, count=1, flags=re.S)
    return replace_locale_switch(page, 'en-gb', route)


def build_es_mx(source: str, canonical: str, route: str, dictionary: dict) -> str:
    # The reviewed artifact is the translation authority. Loading the pair
    # dictionary here keeps the generator contract explicit without applying
    # generic Spanish substitutions over reviewed prose.
    if not dictionary.get('entries'):
        raise SystemExit('es-MX dictionary has no reviewed vocabulary entries')
    page = route_links(source, "es", "es-mx")
    page = page.replace('<html lang="es">', '<html lang="es-MX">', 1)
    page = page.replace('https://overkillhill.com/es' + route, BASE + '/es-mx' + route)
    page = noindex(page)
    page = page.replace('hreflang="es"', 'hreflang="es-MX"').replace('lang="es"', 'lang="es-MX"')
    page = re.sub(r'(<meta[^>]+property=["\']og:locale["\'][^>]+content=["\'])es_ES', r'\1es_MX', page, flags=re.I)
    # The shared mobile menu is right-anchored to the flag button. Keep the
    # visible current-locale label compact enough to remain wholly on-screen;
    # the expanded accessible name retains the full regional wording.
    page = page.replace('Español</span>', 'ES-MX · Borrador</span>')
    page = page.replace('aria-label="Language: Español"', 'aria-label="Language: Español (México) · Borrador"')
    page = page.replace('aria-label="Español"', 'aria-label="Español (México) · Borrador"')
    page = re.sub(r'<link[^>]+rel="alternate"[^>]*>', '', page, flags=re.I)
    page = re.sub(r'<svg aria-hidden="true" class="lang-flag".*?</svg>', MEXICO, page, count=1, flags=re.S)
    # Project-level Mexican usage overrides. Preserve intentional technology
    # terms such as workflow and promptcraft rather than forcing calques.
    page = page.replace('ordenador', 'computadora').replace('móvil', 'celular')
    # Draft artifacts retain their reviewed prose, but inherit the canonical
    # font resources and current forge notice so the locale shell renders with
    # the same brand typography and site-wide status context as English.
    if 'href="https://fonts.googleapis.com' not in page:
        font_links = '\n'.join(re.findall(r'<link[^>]+https://fonts\.(?:googleapis|gstatic)\.com[^>]*>', canonical, re.I))
        if not font_links:
            raise SystemExit('Canonical source is missing required font resources')
        page = page.replace('</head>', font_links + '\n</head>')
    if 'class="site-specials site-specials--okh"' not in page:
        notice = (
            '<section aria-label="Actualización de la fragua" class="site-specials site-specials--okh">'
            '<span class="site-specials-label">🔥Recién salido de la FRAGUA⚒️</span>'
            '<a class="site-specials-link" data-banner-localized="true" data-banner-release="v0.5" href="/writings/first-diagram-is-a-liar/#council-scoring">'
            'La versión 0.5 ya está en línea: el Consejo de IAs calificó los diagramas de los demás; cada modelo fue más duro consigo mismo que quien diseñó la evaluación. Léelo →'
            '</a></section>'
        )
        page = page.replace('</header>', notice + '</header>', 1)
    return replace_locale_switch(page, 'es-mx', route)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--locale', choices=('en-gb', 'es-mx'), required=True)
    args = parser.parse_args()
    dictionary, _profile = load_pair_contract(args.locale)
    verify_sources()
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
        rendered = build_en_gb(page, route, dictionary) if args.locale == 'en-gb' else build_es_mx(target_input, page, route, dictionary)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding='utf-8')
        print(output.relative_to(ROOT))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
