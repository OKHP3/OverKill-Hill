"""Clean-checkout dependencies and narrative placement for the accepted still release."""
import runpy
import tempfile
import unittest
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
MODULE = runpy.run_path(str(ROOT / 'scripts/build-murderbird-release-register.py'))
RELEASE = runpy.run_path(str(ROOT / 'scripts/build-release.py'))


class MurderBirdStillTests(unittest.TestCase):
    def test_dependency_closure_and_exact_source_identity(self):
        payload = MODULE['record']()
        self.assertEqual(6, len(payload['masters']))
        self.assertEqual(18, sum(len(m['derivatives']) for m in payload['masters']))
        source = ROOT / payload['masters'][0]['path']
        with self.assertRaisesRegex(ValueError, 'identity changed'):
            MODULE['describe'](source, '0' * 64)

    def test_story_semantics_and_no_video_placeholders(self):
        page = BeautifulSoup((ROOT / 'writings/murderbird/index.html').read_text(encoding='utf-8'), 'html.parser')
        for scene in ('maker', 'water', 'mechanic', 'heart', 'sentinel'):
            figure = page.select_one('#media-' + scene)
            self.assertIsNotNone(figure)
            self.assertEqual('the-builder' if scene == 'heart' else 'the-' + scene, figure.parent['id'])
            self.assertEqual('lazy', figure.img['loading'])
            self.assertTrue(figure.img['alt'])
            self.assertTrue(figure.figcaption.get_text(strip=True))
        self.assertEqual('p', page.select_one('#media-maker').find_next_sibling().name)
        self.assertIn('morning of the demonstration', page.select_one('#media-maker').find_next_sibling().get_text())
        self.assertFalse(page.select('video, audio'))

    def test_exploratory_package_not_required(self):
        self.assertTrue((ROOT / 'assets/murderbird/v2').is_dir())
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'site-release'
            RELEASE['build'](ROOT, output, 'a' * 40)
            self.assertFalse((output / 'assets/murderbird/v2').exists())
            for name in MODULE['HELD_NAMES']:
                self.assertTrue((ROOT / 'assets/img/library' / name).is_file())
                self.assertFalse((output / 'assets/img/library' / name).exists())


if __name__ == '__main__':
    unittest.main()
