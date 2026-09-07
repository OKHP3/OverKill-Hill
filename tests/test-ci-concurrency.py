"""Exercise actual workflow group expressions across trigger/caller contexts.

This is a bounded expression fixture, not a GitHub scheduler simulation.
Live cancellation, deployment ordering, and retry acceptance remain CI checks.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
VALIDATE = (ROOT / '.github/workflows/validate.yml').read_text(encoding='utf-8')
PAGES = (ROOT / '.github/workflows/pages.yml').read_text(encoding='utf-8')


def job(source, name):
    match = re.search(rf'^  {re.escape(name)}:\n(.*?)(?=^  [\w-]+:|\Z)', source, re.M | re.S)
    if not match:
        raise AssertionError(f'missing job {name}')
    return match[1]


def group(source, context):
    template = re.search(r'^      group: (.+)$', source, re.M).group(1)

    def expression(match):
        text = match[1].strip()
        def atom(value):
            value = value.strip()
            if ' == ' in value:
                left, right = value.split(' == ', 1)
                return atom(left) == atom(right)
            if value.startswith('github.'):
                return context[value.removeprefix('github.')]
            if re.fullmatch("'[^']*'", value):
                return value[1:-1]
            raise AssertionError(f'unsupported fixture expression: {value}')
        for disjunction in text.split(' || '):
            result = True
            for conjunction in disjunction.split(' && '):
                result = result and atom(conjunction)
            if result:
                return str(result)
        return str(result)

    return re.sub(r'\$\{\{(.*?)\}\}', expression, template)


def context(workflow='Site Validation', event_name='push', ref='refs/heads/main', run_id='100', run_attempt='1'):
    return locals()


class ConcurrencyTests(unittest.TestCase):
    def test_workflow_cancellation_cannot_reach_deployment(self):
        self.assertNotRegex(VALIDATE, r'(?m)^concurrency:')
        self.assertNotRegex(PAGES, r'(?m)^concurrency:')
        deploy = job(PAGES, 'deploy')
        self.assertIn('needs: validate', deploy)
        self.assertIn('cancel-in-progress: false', deploy)
        self.assertEqual(group(deploy, context()), 'pages')

    def test_standalone_and_reusable_push_do_not_collide(self):
        source = job(VALIDATE, 'validate')
        self.assertNotEqual(group(source, context()), group(source, context(workflow='Publish GitHub Pages')))

    def test_rapid_pushes_and_old_rerun_do_not_cancel_latest(self):
        source = job(VALIDATE, 'validate')
        for workflow in ('Site Validation', 'Publish GitHub Pages'):
            old = group(source, context(workflow=workflow, run_id='100', run_attempt='2'))
            latest = group(source, context(workflow=workflow, run_id='101'))
            self.assertNotEqual(old, latest)

    def test_dispatch_and_push_and_separate_dispatches_are_isolated(self):
        source = job(VALIDATE, 'validate')
        cases = [context(), context(event_name='workflow_dispatch'),
                 context(event_name='workflow_dispatch', run_id='101')]
        self.assertEqual(len({group(source, case) for case in cases}), 3)

    def test_pr_required_name_and_latest_revision_are_preserved(self):
        source = job(VALIDATE, 'validate')
        self.assertIn('name: Validate site HTML, links, and structure', source)
        self.assertIn('cancel-in-progress: true', source)
        first = context(event_name='pull_request', ref='refs/pull/1/merge')
        second = dict(first, run_id='101')
        other = dict(first, ref='refs/pull/2/merge')
        self.assertEqual(group(source, first), group(source, second))
        self.assertNotEqual(group(source, first), group(source, other))
        self.assertRegex(VALIDATE, r'(?m)^  pull_request:')

    def test_monitors_do_not_cancel_manual_validation_or_each_other(self):
        cases = [context(event_name='workflow_dispatch'),
                 context(event_name='workflow_dispatch', run_id='101'),
                 context(event_name='schedule')]
        groups = [group(job(VALIDATE, name), case) for name in
                  ('validate', 'monitor-third-party-runtime', 'monitor-live-edge') for case in cases]
        self.assertEqual(len(set(groups)), len(groups))

    def test_summaries_run_even_after_check_failure(self):
        for source, kind in ((job(PAGES, 'deploy'), 'edge'),
                             (job(VALIDATE, 'monitor-live-edge'), 'edge'),
                             (job(VALIDATE, 'monitor-third-party-runtime'), 'external')):
            self.assertRegex(source, rf'if: always\(\)\n        run: python3 scripts/write-actions-summary.py --kind {kind}')


if __name__ == '__main__':
    unittest.main()
