#!/usr/bin/env python3
"""Regional generator regressions. Run: python3 tests/test-locale-drafts.py."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('locale_builder', ROOT / 'scripts/build-locale-drafts.py')
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
DICTIONARY = {'entries': [
    {'source': 'Color', 'target': 'Colour', 'handling': 'adapt'},
    {'source': 'colors', 'target': 'colours', 'handling': 'adapt'},
    {'source': 'Color Studio', 'target': 'Color Studio', 'handling': 'preserve'},
    {'source': 'MurderBird', 'target': 'Changed', 'handling': 'adapt'},
]}


class ProtectedTextTests(unittest.TestCase):
    def test_all_eight_outputs_preserve_retained_content(self):
        # CSP/fingerprints belong to release generation. The only editorial
        # cleanup permitted here is the formerly translated metadata comment.
        def comparable(page):
            return BUILDER.normalized_translation_source(page.encode()).replace(
                b'METADATA: Colour Scheme & Theme', b'METADATA: Color Scheme & Theme')

        for locale in BUILDER.PAIR_CONTRACTS:
            dictionary, _ = BUILDER.load_pair_contract(locale)
            for route, rel in BUILDER.ROUTES.items():
                with self.subTest(locale=locale, route=route):
                    canonical = (ROOT / rel).read_text(encoding='utf-8')
                    if locale == 'en-gb':
                        rendered = BUILDER.build_en_gb(canonical, route, dictionary)
                    else:
                        reviewed = (ROOT / 'i18n/pilot/es-mx/reviewed' / BUILDER.REVIEWED_ES_MX[rel]).read_text(encoding='utf-8')
                        rendered = BUILDER.build_es_mx(reviewed, canonical, route, dictionary)
                    retained = (ROOT / locale / rel).read_text(encoding='utf-8')
                    self.assertEqual(comparable(retained), comparable(rendered))

    def test_url_query_entities_do_not_split_protection(self):
        source = '<p>https://example.com/?a=1&amp;Color=colors Color &#67; &Color;</p>'
        expected = '<p>https://example.com/?a=1&amp;Color=colors Colour &#67; &Color;</p>'
        self.assertEqual(expected, BUILDER.adapt_visible_text(source, DICTIONARY))

    def test_multiline_unicode_source_preserves_offsets(self):
        source = '<p>é\r\nColor &amp; colors</p>\n<p>Color</p>'
        expected = '<p>é\r\nColour &amp; colours</p>\n<p>Colour</p>'
        self.assertEqual(expected, BUILDER.adapt_visible_text(source, DICTIONARY))

    def test_es_mx_rejects_another_locale_as_input(self):
        with self.assertRaisesRegex(SystemExit, 'Expected reviewed es-MX input'):
            BUILDER.build_es_mx('<html lang="es">', '', '/', DICTIONARY)

    def test_visible_words_only_and_no_substring_replacement(self):
        self.assertEqual('<p>Colour colours watercolors Colorful</p>',
                         BUILDER.adapt_visible_text('<p>Color colors watercolors Colorful</p>', DICTIONARY))

    def test_attributes_with_angle_brackets_and_entities_are_byte_preserved(self):
        source = '<p title="x > Color colors" data-colors="Color">Color &amp; colors</p>'
        self.assertEqual('<p title="x > Color colors" data-colors="Color">Colour &amp; colours</p>',
                         BUILDER.adapt_visible_text(source, DICTIONARY))

    def test_comments_and_code_containers_are_untouched(self):
        for fragment in ('<!-- x > Color colors -->', '<code>Color colors</code>',
                         '<pre><b>Color colors</b></pre>', '<template><p>Color colors</p></template>',
                         '<script>if (a < b) { x = "<code>Color colors"; }</script>',
                         '<style>.colors { content: "Color"; }</style>'):
            with self.subTest(fragment=fragment):
                self.assertEqual(fragment + '<p>Colour</p>',
                                 BUILDER.adapt_visible_text(fragment + '<p>Color</p>', DICTIONARY))

    def test_urls_paths_placeholders_and_brand_tokens_are_untouched(self):
        tokens = 'https://example.com/Color/colors /Color/colors {{Color}} Color Studio MurderBird'
        self.assertEqual('<p>' + tokens + ' Colour</p>',
                         BUILDER.adapt_visible_text('<p>' + tokens + ' Color</p>', DICTIONARY))

    def test_explicit_locked_subtrees_are_untouched(self):
        for fragment in ('<span translate="no">Color <b>colors</b></span>',
                         '<span class="brand notranslate">Color colors</span>'):
            with self.subTest(fragment=fragment):
                self.assertEqual(fragment + '<p>Colour</p>',
                                 BUILDER.adapt_visible_text(fragment + '<p>Color</p>', DICTIONARY))

    def test_void_elements_do_not_extend_protection(self):
        source = '<img translate="no" alt="Color"><p>Color</p>'
        self.assertEqual('<img translate="no" alt="Color"><p>Colour</p>',
                         BUILDER.adapt_visible_text(source, DICTIONARY))

    def test_en_gb_builder_does_not_bypass_text_protection(self):
        canonical = (ROOT / 'about/index.html').read_text(encoding='utf-8')
        fragment = '<p title="Color Scheme colors">colors</p><code>colors</code><!-- Color Scheme -->'
        result = BUILDER.build_en_gb(canonical.replace('</main>', fragment + '</main>'), '/about/', DICTIONARY)
        self.assertIn('<p title="Color Scheme colors">colours</p><code>colors</code><!-- Color Scheme -->', result)

    def test_es_mx_reviewed_prose_is_not_retranslated(self):
        canonical = (ROOT / 'about/index.html').read_text(encoding='utf-8')
        reviewed = (ROOT / 'i18n/pilot/es-mx/reviewed/about-index.html').read_text(encoding='utf-8')
        fragment = '<p title="ordenador móvil">ordenador móvil https://example.com/es/ordenador</p><code>móvil</code>'
        result = BUILDER.build_es_mx(reviewed.replace('</main>', fragment + '</main>'), canonical, '/about/', DICTIONARY)
        self.assertIn(fragment, result)


if __name__ == '__main__':
    unittest.main()
