"""Behavioral regression for local-only review output, using tiny temporary fixtures."""
import importlib.util
import json
import os
import subprocess
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup
from PIL import Image

REPO = Path(__file__).resolve().parents[1]


class ReviewBoundaryTests(unittest.TestCase):
    def test_full_and_markup_only_generation_stay_local(self):
        # Use the host default, including macOS /var -> /private/var aliases.
        with tempfile.TemporaryDirectory(prefix='murderbird-review-test-') as temporary:
            self.check_review_boundary(Path(temporary))

    def test_canonical_temporary_root(self):
        with tempfile.TemporaryDirectory(prefix='murderbird-canonical-test-') as temporary:
            self.check_review_boundary(Path(temporary).resolve())

    def test_aliased_temporary_root(self):
        with tempfile.TemporaryDirectory(prefix='murderbird-alias-test-') as temporary:
            base = Path(temporary).resolve()
            canonical = base / 'private' / 'var'
            canonical.mkdir(parents=True)
            alias = base / 'var'
            if os.name == 'nt':
                # Directory junctions exercise real path aliases without requiring
                # the Windows privilege needed to create symbolic links.
                subprocess.run(['cmd', '/c', 'mklink', '/J', str(alias), str(canonical)],
                               check=True, capture_output=True)
            else:
                alias.symlink_to(canonical, target_is_directory=True)
            try:
                self.assertNotEqual(alias, alias.resolve())
                self.assertEqual(alias.resolve(), canonical)
                with tempfile.TemporaryDirectory(dir=alias, prefix='review-') as nested:
                    lexical = Path(nested)
                    self.assertNotEqual(lexical, lexical.resolve())
                    self.check_review_boundary(lexical)
            finally:
                if os.name == 'nt':
                    alias.rmdir()
                else:
                    alias.unlink()

    def check_review_boundary(self, temporary):
        spec = importlib.util.spec_from_file_location('review_builder', REPO / 'assets/murderbird/v2/build-library.py')
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        # Match the archived builder's resolved __file__ entry point. Normalize
        # patched fixture roots here without changing byte-preserved source.
        repo = Path(temporary).resolve()
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
                        destination = (page.parent / url).resolve()
                        self.assertTrue(destination.is_relative_to(root) or destination.is_relative_to(review))
                        self.assertEqual(
                            url,
                            Path(os.path.relpath(destination, page.parent.resolve())).as_posix(),
                            (page, url),
                        )
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
