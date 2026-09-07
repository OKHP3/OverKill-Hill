"""Verify delivered files against manifest, without modifying artwork."""
from pathlib import Path
import hashlib
import json
from PIL import Image

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
errors = []
checked = []

def visit(value):
    if isinstance(value, dict):
        if all(key in value for key in ('path', 'width', 'height', 'bytes', 'sha256')):
            path = root / value['path']
            if not path.is_file():
                errors.append(f'Missing: {value["path"]}')
                return
            data = path.read_bytes()
            with Image.open(path) as picture:
                picture.load()
                actual = (picture.width, picture.height, len(data), hashlib.sha256(data).hexdigest())
            expected = tuple(value[key] for key in ('width', 'height', 'bytes', 'sha256'))
            if actual != expected:
                errors.append(f'Manifest mismatch: {value["path"]}')
            checked.append(value['path'])
        for child in value.values():
            visit(child)
    elif isinstance(value, list):
        for child in value:
            visit(child)

visit(manifest)
entries = manifest['entries']
if len(entries) != 8:
    errors.append('Expected eight master entries')
for entry in entries:
    if not entry.get('master') or not entry.get('alt') or not entry.get('originPromptPointers'):
        errors.append(f'Incomplete asset: {entry.get("id")}')
    social = root / 'social' / (entry['id'] + '.png')
    if not social.is_file():
        errors.append(f'Missing social raster: {entry["id"]}')
    else:
        with Image.open(social) as picture:
            if picture.size != (1200, 630):
                errors.append(f'Incorrect social dimensions: {entry["id"]}')
result = {'passed': not errors, 'entries': len(entries), 'verifiedRecords': len(checked), 'uniqueFiles': len(set(checked)), 'errors': errors}
(root / 'verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, indent=2))
raise SystemExit(bool(errors))
