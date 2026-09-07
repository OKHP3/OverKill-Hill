"""Keep repaired authoring scaffolds and route metadata from regressing."""
import runpy
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


class ReviewCloseoutTests(unittest.TestCase):
    def test_scaffolds_use_current_navigation_and_platform_icons(self):
        templates = list((ROOT / "assets/templates").glob("*.html"))
        self.assertTrue(templates, "No page scaffolds found")
        for template in templates:
            with self.subTest(template=template.name):
                text = template.read_text(encoding="utf-8")
                self.assertIn('/assets/img/murderbird-v2-icon-nav-96.png', text)
                self.assertNotIn('sentinel-warning-square-256', text)
                for suffix in ('browser-16.png', 'browser-32.png', 'opaque-180.png', '.ico'):
                    self.assertIn('murderbird-v2-icon' + ('' if suffix == '.ico' else '-') + suffix, text)
                self.assertNotIn('/favicons/favicon-16x16.png', text)

    def test_navigation_copy_preserves_the_existing_public_asset(self):
        old = ROOT / 'assets/img/favicons/murderbird-v2-icon-nav-96.png'
        new = ROOT / 'assets/img/murderbird-v2-icon-nav-96.png'
        self.assertEqual(old.read_bytes(), new.read_bytes())

    def test_murderbird_has_its_own_active_route_and_grid_minimum(self):
        builder = runpy.run_path(str(ROOT / 'scripts/build-site.py'))
        self.assertEqual('/writings/murderbird/', builder['active_route']('/writings/murderbird/'))
        source = (ROOT / 'site-src/pages/writings/murderbird/index.main.html').read_text(encoding='utf-8')
        self.assertIn('article-body mac-body-main', source)

    def test_organization_logo_matches_builder_partial_and_validator(self):
        logo = 'https://overkillhill.com/assets/img/favicons/murderbird-v2-icon-1024.png'
        for name in ('scripts/build-site.py', 'assets/partials/head.html', 'scripts/validate-site.py'):
            with self.subTest(name=name):
                self.assertIn(logo, (ROOT / name).read_text(encoding='utf-8'))

    def test_rendered_murderbird_navigation_marks_the_article_current(self):
        page = BeautifulSoup((ROOT / 'writings/murderbird/index.html').read_text(encoding='utf-8'), 'html.parser')
        current = page.select('.site-header nav a[aria-current="page"]')
        self.assertEqual(['/writings/murderbird/'], [link.get('href') for link in current])

    def test_mtb_source_uses_correct_indefinite_article(self):
        text = (ROOT / 'site-src/pages/projects/mermaid-theme-builder/index.main.html').read_text(encoding='utf-8')
        self.assertIn('a 10-skill', text)
        self.assertNotIn('an 10-skill', text)


if __name__ == '__main__':
    unittest.main()
