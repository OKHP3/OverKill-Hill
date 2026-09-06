"""Verify the installed generator owns a stable, index-excluded page block."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class UniverseIntegration(unittest.TestCase):
    def test_generated_source_is_current(self):
        adapter = load("universe_adapter", "scripts/sync-universe-map.py")
        source = adapter.SOURCE.read_text(encoding="utf-8")
        self.assertEqual(adapter.PATTERN.search(source).group(), adapter.render())

    def test_generated_navigation_is_not_search_text(self):
        indexer = load("index_builder", "scripts/build-search-index.py")
        extractor = indexer.TextExtractor()
        extractor.feed('<main><p>Owned introduction</p><section class="universe-generated"><h2>Repeated navigation</h2><p>Do not index this</p></section></main>')
        self.assertNotIn("Repeated navigation", " ".join(extractor._text_parts))
        self.assertNotIn("Do not index this", " ".join(extractor._text_parts))
        self.assertIn("Owned introduction", " ".join(extractor._text_parts))


if __name__ == "__main__":
    unittest.main()
