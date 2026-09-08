"""Regression tests for project inventory, proof limits and generated consumers."""
import copy
import contextlib
import io
import json
import runpy
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = runpy.run_path(str(ROOT / 'scripts/project-status.py'))
DATA = json.loads((ROOT / 'site-src/project-status.json').read_text(encoding='utf-8'))


class RegistryTests(unittest.TestCase):
    def reject(self, mutate):
        data = copy.deepcopy(DATA)
        mutate(data)
        with self.assertRaises(ValueError):
            API['validate'](data, ROOT)

    def test_missing_detail(self):
        self.reject(lambda d: d['projects'].pop(0))

    def test_duplicate_route(self):
        self.reject(lambda d: d['projects'][1].update(route=d['projects'][0]['route']))

    def test_undeclared_shelf_exception(self):
        self.reject(lambda d: d['projects'].pop())

    def test_unsubstantiated_delivery(self):
        self.reject(lambda d: d['projects'][0]['evidence'].update(delivery='verified'))

    def test_missing_evidence(self):
        self.reject(lambda d: d['projects'][0]['evidence'].update(source='missing-file.md'))

    def test_renderer_is_idempotent(self):
        records = DATA['projects']
        for route, source in [('/projects/abrahamic-reference-engine/', '<h1>ARE</h1><p>History remains.</p>'), ('/projects/', '<article><h3>ARE</h3><a href="/projects/abrahamic-reference-engine/">Read</a></article>')]:
            first = API['render'](source, route, records)
            self.assertEqual(first, API['render'](first, route, records))
            self.assertEqual(first.count('data-project-status='), 1)

    def test_generated_consumers_and_drift(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            shutil.copytree(ROOT / 'site-src', root / 'site-src')
            for rel in ['index.html', 'projects', 'universe', 'assets/data/search-index.json']:
                source, target = ROOT / rel, root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                if source.is_dir():
                    shutil.copytree(source, target)
                else:
                    shutil.copy2(source, target)
            checker = runpy.run_path(str(ROOT / 'scripts/check-project-status.py'))['main']
            checker.__globals__['ROOT'] = root
            def result():
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    return checker()
            self.assertEqual(result(), 0)
            for rel in ['index.html', 'projects/index.html', 'projects/abrahamic-reference-engine/index.html']:
                path = root / rel
                original = path.read_text(encoding='utf-8')
                path.write_text(original.replace('Availability: Published', 'Availability: Invented', 1), encoding='utf-8')
                self.assertEqual(result(), 1, rel)
                path.write_text(original, encoding='utf-8')
            path = root / 'assets/data/search-index.json'
            index = json.loads(path.read_text(encoding='utf-8'))
            record = next(e for e in index['entries'] if e['url'] == '/projects/abrahamic-reference-engine/')
            record['body'] = 'Stale summary'
            path.write_text(json.dumps(index), encoding='utf-8')
            self.assertEqual(result(), 1)


if __name__ == '__main__':
    unittest.main()
