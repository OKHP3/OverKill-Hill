#!/usr/bin/env python3
"""Keep every localized homepage on the current responsive MurderBird hero."""
from __future__ import annotations

import importlib.util
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build-locale-drafts.py"
SPEC = importlib.util.spec_from_file_location("build_locale_drafts", BUILDER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load locale builder: {BUILDER}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

HERO_RE = re.compile(r'<div class="hero-visual">\s*(.*?)\s*</div>', re.S)
LOCALES = ("fr", "de", "es", "en-gb", "es-mx")



class HeroParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.sources: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs_list) -> None:
        attrs = {key: value or "" for key, value in attrs_list}
        if tag == "source":
            self.sources.append(attrs)
        elif tag == "img":
            self.images.append(attrs)


def hero_fragment(page: str) -> str:
    match = HERO_RE.search(page)
    if match is None:
        raise AssertionError("homepage hero visual is missing")
    return match.group(1)


class HomepageHeroParityTests(unittest.TestCase):
    def assert_current_hero(self, page: str, locale: str) -> None:
        fragment = hero_fragment(page)
        self.assertNotIn("sentinel", fragment.lower())
        parser = HeroParser()
        parser.feed(fragment)
        self.assertEqual(1, len(parser.sources))
        self.assertEqual(1, len(parser.images))
        source = parser.sources[0]
        image = parser.images[0]
        canonical = HeroParser()
        canonical.feed(hero_fragment((ROOT / "index.html").read_text(encoding="utf-8")))
        expected_source = canonical.sources[0]
        expected_image = canonical.images[0]
        self.assertEqual("image/webp", source.get("type"))
        self.assertEqual(expected_source.get("srcset"), source.get("srcset"))
        self.assertEqual(expected_source.get("sizes"), source.get("sizes"))
        self.assertIn("MurderBird", image.get("alt", ""))
        self.assertNotRegex(image.get("alt", ""), r"sentinel|chouette|búho", msg="alt text names the former identity")
        self.assertEqual(expected_image.get("src"), image.get("src"))
        self.assertEqual(expected_image.get("width"), image.get("width"))
        self.assertEqual(expected_image.get("height"), image.get("height"))
        self.assertEqual("eager", image.get("loading"))
        self.assertEqual("high", image.get("fetchpriority"))
        self.assertEqual(expected_image.get("sizes"), image.get("sizes"))

    def test_localized_homepages_match_the_current_hero_asset_contract(self):
        for locale in LOCALES:
            with self.subTest(locale=locale):
                page = (ROOT / locale / "index.html").read_text(encoding="utf-8")
                self.assert_current_hero(page, locale)

    def test_es_mx_regeneration_keeps_the_current_hero(self):
        dictionary, _profile = MODULE.load_pair_contract("es-mx")
        reviewed = (ROOT / "i18n/pilot/es-mx/reviewed/index.html").read_text(encoding="utf-8")
        canonical = (ROOT / "index.html").read_text(encoding="utf-8")
        rendered = MODULE.build_es_mx(reviewed, canonical, "/", dictionary)
        self.assert_current_hero(rendered, "es-mx")

    def test_regeneration_tracks_a_changed_canonical_hero_and_escapes_alt(self):
        canonical = (ROOT / "index.html").read_text(encoding="utf-8")
        changed = canonical.replace("murderbird-unified-master-03-2026-09-06", "future-canonical-hero")
        previous = MODULE.HOMEPAGE_HERO_ALTS['es-mx']
        try:
            MODULE.HOMEPAGE_HERO_ALTS['es-mx'] = 'MurderBird "fuerte" & claro'
            result = MODULE.replace_homepage_hero(canonical, 'es-mx', changed)
            parser = HeroParser()
            parser.feed(hero_fragment(result))
            self.assertIn('future-canonical-hero', parser.images[0]['src'])
            self.assertEqual('MurderBird "fuerte" & claro', parser.images[0]['alt'])
            self.assertIn('&quot;fuerte&quot; &amp;', result)
        finally:
            MODULE.HOMEPAGE_HERO_ALTS['es-mx'] = previous
        with self.assertRaisesRegex(SystemExit, 'No reviewed homepage hero alt'):
            MODULE.replace_homepage_hero(canonical, 'unknown', canonical)

    def test_regeneration_preserves_new_alt_and_english_story_invitation(self):
        canonical = (ROOT / "index.html").read_text(encoding="utf-8")
        for locale in ("en-gb", "es-mx"):
            dictionary, _ = MODULE.load_pair_contract(locale)
            if locale == "en-gb":
                rendered = MODULE.build_en_gb(canonical, "/", dictionary)
            else:
                reviewed = (ROOT / "i18n/pilot/es-mx/reviewed/index.html").read_text(encoding="utf-8")
                rendered = MODULE.build_es_mx(reviewed, canonical, "/", dictionary)
            fragment = hero_fragment(rendered)
            parser = HeroParser()
            parser.feed(fragment)
            self.assertEqual(MODULE.HOMEPAGE_HERO_ALTS[locale], parser.images[0]["alt"])
            self.assertIn(MODULE.HOMEPAGE_STORY_CTAS[locale], fragment)
            self.assertIn('href="/writings/murderbird/" hreflang="en"', fragment)

    def test_former_lazy_sentinel_hero_fails_the_contract(self):
        page = (ROOT / "es-mx/index.html").read_text(encoding="utf-8")
        former = hero_fragment(page).replace(
            "/assets/img/webp/murderbird-unified-master-03-2026-09-06-960.webp",
            "/assets/img/over-kill-hill-p3-sentinel-waiting-square-1024.png",
        ).replace('loading="eager"', 'loading="lazy"')
        with self.assertRaises(AssertionError):
            self.assert_current_hero(page.replace(hero_fragment(page), former), "es-mx")


if __name__ == "__main__":
    unittest.main()
