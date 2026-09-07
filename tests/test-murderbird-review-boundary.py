"""Behavioral regression for local-only review output, using tiny temporary fixtures."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup
from PIL import Image

REPO = Path(__file__).resolve().parents[1]


class ReviewBoundaryTests(unittest.TestCase):
    def test_full_and_markup_only_generation_stay_local(self):
        spec = importlib.util.spec_from_file_location('review_builder', REPO / 'assets/murderbird/v2/build-library.py')
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        with tempfile.TemporaryDirectory(prefix='murderbird-review-test-') as temporary:
            repo = Path(temporary)
            root = repo / 'assets/murderbird/v2'
            review = repo / '.local/murderbird-review'
            (root / 'masters').mkdir(parents=True)
            # A test fixture, never a production artwork or substituted candidate.
            Image.new('RGB', (8, 6), 'gray').save(root / 'masters/01-maker.png')
            for name in ('README.md', 'placement-map.md', 'ART-DIRECTION.md', 'independent-visual-review.md', 'production/README.md'):
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('Fixture', encoding='utf-8')
            with patch.multiple(builder, ROOT=root, REPO=repo, REVIEW_ROOT=review), patch.object(builder.subprocess, 'check_output', return_value='fixture-sha'):
                builder.main()
                manifest_before = (root / 'manifest.json').read_bytes()
                image_before = {p: p.read_bytes() for p in root.rglob('*') if p.suffix in ('.png', '.webp', '.jpg')}
                for _ in range(2):
                    builder.rebuild_social_html()
                    builder.build_gallery(json.loads(manifest_before)['entries'])
                self.assertEqual(manifest_before, (root / 'manifest.json').read_bytes())
                self.assertTrue(all(p.read_bytes() == data for p, data in image_before.items()))
                self.assertFalse(list(root.rglob('*.html')))
                self.assertEqual(len(list(review.rglob('*.html'))), 2)
                for page in review.rglob('*.html'):
                    soup = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
                    self.assertIn('noindex', soup.find('meta', attrs={'name': 'robots'})['content'])
                    for node in soup.select('[src], [href], [srcset]'):
                        urls = [node[a] for a in ('src', 'href') if node.has_attr(a)]
                        if node.has_attr('srcset'):
                            urls += [part.strip().split()[0] for part in node['srcset'].split(',')]
                        for url in urls:
                            self.assertTrue((page.parent / url).resolve().is_file(), (page, url))
                with self.assertRaises(ValueError):
                    builder.write(root / 'social/accidental.html', '<html></html>')
                # Run the real search scanner over the fixture repository.
                search_spec = importlib.util.spec_from_file_location('search_builder', REPO / 'scripts/build-search-index.py')
                search = importlib.util.module_from_spec(search_spec)
                search_spec.loader.exec_module(search)
                with patch.object(search, 'ROOT', repo):
                    self.assertEqual(search.build_payload(scan_root=repo)['entries'], [])


if __name__ == '__main__':
    unittest.main()
