"""Regression coverage for operator summaries, including mixed failures."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/write-actions-summary.py'


class SummaryTests(unittest.TestCase):
    def load_fixture(self, name):
        return json.loads((ROOT / 'tests/fixtures/actions-summary' / name).read_text())

    def run_summary(self, report, kind='edge'):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'report.json'
            output = Path(directory) / 'summary.md'
            source.write_text(json.dumps(report), encoding='utf-8')
            result = subprocess.run([sys.executable, str(SCRIPT), '--kind', kind,
                                     '--report', str(source), '--summary', str(output)],
                                    capture_output=True, text=True)
            return result.returncode, output.read_text(encoding='utf-8') if output.exists() else ''

    def test_historical_partial_is_not_an_outage_or_full_policy_pass(self):
        report = json.loads((ROOT / 'assets/audit/assessment-2026-09-07/delivery/live-edge.json').read_text())
        code, summary = self.run_summary(report)
        self.assertEqual(code, 0)
        self.assertIn('| Content delivery | PASS |', summary)
        self.assertIn('| Edge policy | PARTIAL |', summary)
        self.assertIn('| External availability | NOT RUN |', summary)
        self.assertIn('ca38d5b9fc46746ea8b41e2ba32e39685c53f511', summary)
        self.assertLess(len(summary.splitlines()), 45)

    def test_first_party_failure_remains_distinct(self):
        code, summary = self.run_summary({'checks': [
            {'check': 'route /', 'status': 'FAIL', 'evidence': 'HTTP 404'},
            {'check': 'route / observed header x-frame-options', 'status': 'WARN', 'evidence': 'absent; GitHub Pages may omit repository headers at the edge'}]})
        self.assertEqual(code, 1)
        self.assertIn('| Content delivery | FAILED |', summary)
        self.assertIn('HTTP 404', summary)

    def test_confirmed_live_edge_failures_remain_visible_in_their_area(self):
        code, summary = self.run_summary(self.load_fixture('live-edge-failure.json'))

        self.assertEqual(code, 1)
        self.assertIn('| Content delivery | FAILED |', summary)
        self.assertIn('| Edge policy | FAILED |', summary)
        self.assertIn('release manifest', summary)
        self.assertIn('x-frame-options', summary)
        self.assertIn('confirmed policy failures remain visible', summary)

    def test_pages_only_blocked_fixture_is_partial_and_not_enforcement_proof(self):
        code, summary = self.run_summary(self.load_fixture('live-edge-pages-blocked.json'))

        self.assertEqual(code, 0)
        self.assertIn('| Content delivery | PASS |', summary)
        self.assertIn('| Edge policy | PARTIAL |', summary)
        self.assertIn('do not prove enforcement', summary)
        self.assertNotIn('| Edge policy | FAILED |', summary)

    def test_transport_block_is_unknown_not_external_outage(self):
        code, summary = self.run_summary({'checks': [{'check': 'route /', 'status': 'BLOCKED', 'evidence': 'timeout'}]})
        self.assertEqual(code, 0)
        self.assertIn('| Content delivery | PARTIAL |', summary)
        self.assertIn('NOT RUN', summary)

    def test_mixed_external_and_local_failure(self):
        code, summary = self.run_summary({'summary': {'routes': 3, 'dependencies': 4, 'available': 2,
            'externalOutages': 2, 'localFailures': 1, 'cspDiagnostics': 1}}, 'external')
        self.assertEqual(code, 1)
        self.assertIn('| Content delivery | FAILED |', summary)
        self.assertIn('| External availability | DEGRADED |', summary)
        self.assertIn('| Browser CSP diagnostics | WARN |', summary)

    def test_external_only_is_nonblocking(self):
        code, summary = self.run_summary({'summary': {'routes': 3, 'dependencies': 4, 'available': 2,
            'externalOutages': 2, 'localFailures': 0, 'cspDiagnostics': 0}}, 'external')
        self.assertEqual(code, 0)
        self.assertIn('DEGRADED', summary)

    def test_invalid_reports_fail_closed(self):
        for report in ({}, {'checks': []}, {'checks': [{'status': 'MAYBE'}]}, []):
            with self.subTest(report=report):
                code, summary = self.run_summary(report)
                self.assertEqual(code, 1)
                self.assertIn('UNKNOWN', summary)

    def test_report_text_is_escaped(self):
        code, summary = self.run_summary({'checks': [{'check': '<script>|bad', 'status': 'FAIL', 'evidence': '<img>\n|bad'}]})
        self.assertEqual(code, 1)
        self.assertNotIn('<script>', summary)
        self.assertNotIn('<img>', summary)

    def test_absent_and_invalid_json_leave_unknown_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'report.json'
            for content in (None, '{'):
                if content:
                    source.write_text(content, encoding='utf-8')
                output = Path(directory) / 'summary.md'
                result = subprocess.run([sys.executable, str(SCRIPT), '--kind', 'edge',
                    '--report', str(source), '--summary', str(output)], capture_output=True)
                self.assertEqual(result.returncode, 1)
                self.assertIn('UNKNOWN', output.read_text(encoding='utf-8'))

    def test_empty_external_sample_does_not_pass(self):
        code, summary = self.run_summary({'summary': dict.fromkeys(
            ('routes', 'dependencies', 'available', 'externalOutages', 'localFailures', 'cspDiagnostics'), 0)}, 'external')
        self.assertEqual(code, 1)
        self.assertIn('UNKNOWN', summary)


if __name__ == '__main__':
    unittest.main()
