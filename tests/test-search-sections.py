import importlib.util
import unittest

spec = importlib.util.spec_from_file_location('builder', 'scripts/build-search-index.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class SectionTests(unittest.TestCase):
    def test_nested_boundaries_entities_and_heading_once(self):
        html = '<DIV id="demo"><h2>Résumé <em>&amp; tools</em></h2><div><p>' + 'Useful text. ' * 10 + '</p></div><p>Final text.</p></DIV><p>OUTSIDE</p>'
        entry, = builder.extract_div_sections(html, '/demo/', 'Demo', ['demo'])
        self.assertIn('Final text.', entry['body'])
        self.assertNotIn('OUTSIDE', entry['body'])
        self.assertNotIn('</', entry['body'])
        self.assertEqual(entry['body'].count('Résumé'), 1)
        self.assertIn('Résumé & tools', entry['title'])

    def test_scripts_comments_voids_and_truncated_tag(self):
        html = '<div id="demo"><h2>Heading</h2><!-- </div> --><script>"</div>"</script><p>' + 'Useful text. ' * 10 + '</p><br><img src="x"><div'
        entry, = builder.extract_div_sections(html, '/demo/', 'Demo', ['demo'])
        self.assertNotIn('<', entry['body'])
        self.assertNotIn('script', entry['body'])

    def test_article_nested_section_keeps_tail(self):
        html = '<section id="outer"><h2>Outer</h2><section><p>' + 'Useful text. ' * 10 + '</p></section><p>Tail.</p></section><p>OUTSIDE</p>'
        entry, = builder.extract_article_sections(html, '/article/', 'Article')
        self.assertIn('Tail.', entry['body'])
        self.assertNotIn('OUTSIDE', entry['body'])

    def test_nested_label(self):
        html = '<h1 id="label">Useful <em>tools</em></h1><article id="demo" aria-labelledby="label"><p>' + 'Useful text. ' * 10 + '</p></article>'
        entry, = builder.extract_div_sections(html, '/demo/', 'Demo', ['demo'], tag='article')
        self.assertTrue(entry['title'].startswith('Useful tools'))


if __name__ == '__main__':
    unittest.main()
