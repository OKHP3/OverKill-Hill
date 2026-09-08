"""Regression coverage for parsed search section boundaries."""
import importlib.util
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "builder", Path(__file__).resolve().parents[1] / "scripts/build-search-index.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class SearchSections(unittest.TestCase):
    def test_nested_section_and_entities(self):
        html = '''<DIV id="target" data-note="a > b"><h2>Mermaid &amp; tools</h2>
        <div><p>Useful <strong>nested</strong> content with café &amp; résumé.
        Enough text to make this section independently searchable.</p></div>
        <!-- <div>comment decoy</div> --><script>const x = "<div>script decoy";</script>
        <p>Final paragraph.</p></DIV><div>Outside sentinel</div>'''
        entry, = builder.extract_div_sections(html, "/example/", "Example", ["target"])
        self.assertIn("Final paragraph.", entry["body"])
        self.assertIn("café & résumé", entry["body"])
        for unwanted in ("</div", "Outside sentinel", "decoy"):
            self.assertNotIn(unwanted, entry["body"])
        self.assertEqual(entry["body"].count("Mermaid & tools"), 1)

    def test_heading_not_duplicated(self):
        parser = builder.TextExtractor()
        parser.feed("<h2>Unique heading</h2><p>Useful text</p>")
        self.assertEqual(parser.collected_text(), "Unique heading Useful text")

    def test_incomplete_section_is_not_indexed(self):
        html = '<div id="broken"><h2>Title</h2><p>' + 'Text ' * 30 + '</div'
        self.assertEqual(builder.extract_div_sections(html, "/", "Title", ["broken"]), [])

    def test_published_snippets_have_no_closing_tag_fragments(self):
        entries = json.loads(builder.OUT.read_text(encoding="utf-8"))["entries"]
        for entry in entries:
            for field in ("description", "body"):
                self.assertNotRegex(entry[field], r"</(?:div|section|article)\b", entry["url"])


if __name__ == "__main__":
    unittest.main()
