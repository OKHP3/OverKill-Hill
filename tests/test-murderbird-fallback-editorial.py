"""Verify the fallback-only update retains reviewed English and French text."""
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BASE = 'd112ca4eb091c0567fc3fd4f3f307168dd38a552'
result = {}
for path in ('index.html', 'fr/index.html'):
    before = subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT).decode('utf-8')
    after = (ROOT / path).read_text(encoding='utf-8')
    old, new = (BeautifulSoup(text, 'html.parser') for text in (before, after))
    assert old.get_text() == new.get_text(), path
    assert [(i.get('alt'), i.get('title')) for i in old.find_all('img')] == [(i.get('alt'), i.get('title')) for i in new.find_all('img')], path
    result[path] = hashlib.sha256(after.encode()).hexdigest()
spec = importlib.util.spec_from_file_location('regional', ROOT / 'scripts/check-regional-drafts.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
result['normalized'] = hashlib.sha256(module.normalized_translation_source((ROOT / 'index.html').read_bytes())).hexdigest()
print(json.dumps(result))
