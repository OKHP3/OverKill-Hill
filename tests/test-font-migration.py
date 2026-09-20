"""Font migration must preserve recovery bytes and remain generator-compatible."""
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
SCRIPT = runpy.run_path(str(ROOT / 'scripts/strip-google-fonts-links.py'))
LINK = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans"/>'


class FontMigrationTests(unittest.TestCase):
    def test_inventory_excludes_recovery_fixtures_evidence_and_untracked_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            allowed = ['index.html', 'fr/index.html', 'assets/partials/head.html', 'site-src/pages/index.main.html']
            excluded = ['.local/recovery/index.html', 'tests/fixture.html', 'i18n/reviewed/index.html', 'node_modules/page.html']
            for name in allowed + excluded + ['untracked.html']:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(LINK.encode())
            tracked = subprocess.CompletedProcess([], 0, stdout='\0'.join(allowed + excluded) + '\0')
            with patch('subprocess.run', return_value=tracked):
                paths = list(SCRIPT['find_html_files'](root))
            self.assertEqual({p.relative_to(root).as_posix() for p in paths}, set(allowed))
            for path in paths:
                SCRIPT['process_file'](path, True)
            for name in excluded + ['untracked.html']:
                self.assertEqual((root / name).read_bytes(), LINK.encode())

    def test_links_are_removed_without_rewriting_csp_or_unrelated_text(self):
        source = '<meta content="style-src https://fonts.googleapis.com">\r\n' + LINK + '\r\n<link href="https://fonts.googleapis.com.evil.invalid/x" rel="stylesheet">\r\n'
        updated = SCRIPT['strip_links'](source)
        self.assertIn('<meta content="style-src https://fonts.googleapis.com">', updated)
        self.assertIn('fonts.googleapis.com.evil.invalid', updated)
        self.assertEqual(updated.count(SCRIPT['MARKER']), 1)
        self.assertEqual(SCRIPT['strip_links'](updated), updated)
        self.assertEqual(updated.count('\r\n'), source.count('\r\n'))

    def test_dry_run_preserves_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'index.html'
            original = (LINK + '\r\n').encode()
            path.write_bytes(original)
            self.assertTrue(SCRIPT['process_file'](path, False))
            self.assertEqual(path.read_bytes(), original)

    def test_regional_regeneration_uses_local_fonts_without_changing_reviewed_input(self):
        builder = runpy.run_path(str(ROOT / 'scripts/build-locale-drafts.py'))
        reviewed = (ROOT / 'i18n/pilot/es-mx/reviewed/index.html').read_text(encoding='utf-8')
        canonical = (ROOT / 'index.html').read_text(encoding='utf-8')
        dictionary, _ = builder['load_pair_contract']('es-mx')
        generated = builder['build_es_mx'](reviewed, canonical, '/', dictionary)
        self.assertIn('/assets/css/theme.css', generated)
        self.assertNotIn('href="https://fonts.googleapis.com', generated)
        self.assertNotIn('href="https://fonts.gstatic.com', generated)
        self.assertEqual(reviewed, (ROOT / 'i18n/pilot/es-mx/reviewed/index.html').read_text(encoding='utf-8'))

    def test_original_font_bytes_and_family_licenses_are_present(self):
        manifest = json.loads((ROOT / 'assets/fonts/provenance.json').read_text())
        self.assertEqual(len(manifest['files']), 11)
        for item in manifest['files']:
            font = ROOT / 'assets/fonts' / item['file']
            self.assertEqual(hashlib.sha256(font.read_bytes()).hexdigest(), item['sha256'])
            self.assertTrue(item['source'].startswith('https://fonts.gstatic.com/'))
        for family in manifest['licenses']:
            self.assertIn('SIL OPEN FONT LICENSE', (ROOT / 'assets/fonts' / (family + '-license.txt')).read_text())


if __name__ == '__main__':
    unittest.main()
