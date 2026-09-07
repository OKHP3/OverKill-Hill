"""Accepted illustrations must remain usable without WebP decoding."""
import unittest
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


class FallbackTests(unittest.TestCase):
    def test_accepted_images_have_real_png_fallbacks(self):
        paths = ['index.html', 'site-src/pages/index.main.html',
                 'writings/murderbird/index.html',
                 'site-src/pages/writings/murderbird/index.main.html']
        paths += [f'{locale}/index.html' for locale in ('fr', 'de', 'es', 'es-mx', 'en-gb')]
        for path in paths:
            soup = BeautifulSoup((ROOT / path).read_text(encoding='utf-8'), 'html.parser')
            images = soup.select('img[src*="murderbird-unified-"]')
            self.assertEqual(6 if 'writings/' in path else 1, len(images), path)
            for image in images:
                with self.subTest(path=path, image=image['src']):
                    self.assertTrue(image['src'].endswith('.png'))
                    self.assertNotIn('srcset', image.attrs)
                    picture = image.find_parent('picture')
                    self.assertIsNotNone(picture)
                    self.assertIsNotNone(picture.find('source', type='image/webp'))
                    with Image.open(ROOT / image['src'].lstrip('/')) as png:
                        self.assertEqual('PNG', png.format)
                        self.assertEqual((int(image['width']), int(image['height'])), png.size)


if __name__ == '__main__':
    unittest.main()
