"""Prevent retired branding from returning through pages, locales, or metadata."""
import importlib.util
from pathlib import Path
import re
import unittest
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('release',ROOT/'scripts/build-release.py')
release=importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)

class LineageTests(unittest.TestCase):
    def test_public_references_retire_old_branding(self):
        retired=re.compile(r'over-kill-hill-p3-(?:sentinel-|bird-patrol-|title-horiz-|title-left-comp-right)')
        for relative in release.load_public_pages(ROOT):
            with self.subTest(page=str(relative)):
                text=(ROOT/relative).read_text(encoding='utf-8')
                self.assertIsNone(retired.search(text))
                self.assertNotIn('/assets/murderbird/production/',text)
                self.assertNotIn('frontal-alternate',text)

    def test_historical_sigil_remains_labeled(self):
        for path in ('manifesto/index.html','writings/murderbird/index.html'):
            self.assertIn('over-kill-hill-p3-title-low-right-bird-perch-comp-square-1024.webp',(ROOT/path).read_text(encoding='utf-8'))
        self.assertIn('The original sigil.',(ROOT/'writings/murderbird/index.html').read_text(encoding='utf-8'))

    def test_cutout_alpha_and_delivery_aspect(self):
        for role in ('legal-guardian','contact-warning','under-construction','404-reassembly'):
            with Image.open(ROOT/f'assets/img/murderbird-v2-{role}-960.png') as image:
                self.assertEqual(image.width,960)
                self.assertEqual(image.height,960 if role in ('legal-guardian','contact-warning') else 640)
                if role in ('legal-guardian','contact-warning'):
                    self.assertEqual(image.mode,'RGBA')
                    self.assertEqual(image.getextrema()[3],(0,255))

if __name__=='__main__':unittest.main()
