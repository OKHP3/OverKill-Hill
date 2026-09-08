"""Optional proposal disclosure must preserve canonical facts and visible limits."""
import copy
import json
import runpy
import unittest
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
API = runpy.run_path(str(ROOT / 'scripts/project-status.py'))
RECORDS = json.loads((ROOT / 'site-src/project-status.json').read_text(encoding='utf-8'))['projects']


class DisclosureTests(unittest.TestCase):
    def test_canonical_content_and_sources_preserved(self):
        for record in RECORDS:
            soup = BeautifulSoup(API['disclosure_html'](record), 'html.parser')
            self.assertEqual(str(soup.select_one('[data-project-status]')),
                             str(BeautifulSoup(API['summary_html'](record), 'html.parser').p))
            self.assertFalse(soup.details.has_attr('open'))
            self.assertEqual(soup.summary.get_text(), 'Status and source')
            brief = soup.select_one('[data-project-status-brief]')
            self.assertIsNone(brief.find_parent('details'))
            self.assertIn(record['maturity'].lower(), brief.get_text().lower())
            if record['maturity'] == 'Unknown':
                self.assertIn(record['availability'], brief.get_text())
            self.assertIn('unverified', brief.get_text().lower())

    def test_material_workbench_limit_remains_visible(self):
        record = next(r for r in RECORDS if r['id'] == 'mac-studio-local-ai-workbench')
        self.assertIn(record['evidence']['summary'], API['visitor_summary'](record))

    def test_brief_tracks_record_changes(self):
        record = copy.deepcopy(RECORDS[0])
        record['maturity'] = 'Revised source qualification'
        self.assertIn(record['maturity'], API['visitor_summary'](record))
        record['evidence']['delivery'] = 'verified'
        with self.assertRaises(ValueError):
            API['visitor_summary'](record)

    def test_idempotent_and_opt_in(self):
        route = RECORDS[0]['route']
        source = '<h1>Project</h1><p>Original description.</p>'
        default = API['render'](source, route, RECORDS)
        self.assertNotIn('<details', default)
        proposal = API['render'](source, route, RECORDS, disclosure=True)
        self.assertEqual(proposal, API['render'](proposal, route, RECORDS, disclosure=True))
        self.assertEqual(default, API['render'](proposal, route, RECORDS))
        self.assertIn('Original description.', proposal)

    def test_card_description_and_action_stay_outside_disclosure(self):
        source = '<article><h3>Project</h3><p>Visitor description.</p><p><a href="' + RECORDS[0]['route'] + '">Inspect project</a></p></article>'
        output = API['render'](source, '/projects/', RECORDS, disclosure=True)
        soup = BeautifulSoup(output, 'html.parser')
        self.assertLess(output.index('Visitor description.'), output.index('data-project-status-brief'))
        self.assertIsNone(soup.find('a', string='Inspect project').find_parent('details'))
        self.assertEqual(output, API['render'](output, '/projects/', RECORDS, disclosure=True))


if __name__ == '__main__':
    unittest.main()
