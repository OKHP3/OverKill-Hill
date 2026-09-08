#!/usr/bin/env python3
"""Check project inventory and generated status across cards, details and search."""
import json
import runpy
import sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
STATUS = runpy.run_path(str(ROOT / 'scripts/project-status.py'))


def main():
    try:
        records = STATUS['load_registry'](ROOT)
        by_id = {r['id']: r for r in records}
        routes = ['/', '/projects/', '/universe/'] + [r['route'] for r in records if r['kind'] == 'detail']
        index = json.loads((ROOT / 'assets/data/search-index.json').read_text(encoding='utf-8'))
        entries = index['entries']
        for route in routes:
            path = ROOT / route.lstrip('/') / 'index.html'
            soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
            main = soup.find('main')
            for block in main.select('[data-project-status]'):
                record = by_id[block['data-project-status']]
                text = block.select_one('[data-project-status-text]')
                if text is None or text.get_text() != STATUS['summary'](record):
                    raise ValueError(f'{route}: stale project summary')
                link = block.find('a')
                if link is None or link.get('href') != record['evidence']['url'] or record['reviewed'] not in block.get_text():
                    raise ValueError(f'{route}: stale evidence link or review date')
            record = next((r for r in records if r['route'] == route), None)
            if record and record['kind'] == 'detail':
                if len(main.select(f'[data-project-status="{record["id"]}"]')) != 1:
                    raise ValueError(f'{route}: missing or duplicated detail status')
                noindex = 'noindex' in soup.find('meta', attrs={'name': 'robots'})['content']
                if noindex != (record['availability'] == 'Noindex concept page'):
                    raise ValueError(f'{route}: availability disagrees with indexing policy')
                found = [e for e in entries if e['url'].split('#')[0] == route]
                if noindex and found:
                    raise ValueError(f'{route}: concept leaked into search')
                page_entries = [e for e in found if e['url'] == route]
                if not noindex and (len(page_entries) != 1 or not page_entries[0]['body'].startswith(STATUS['summary'](record))):
                    raise ValueError(f'{route}: missing or stale search status')
            for card in main.find_all('article'):
                matches = {a.get('href') for a in card.find_all('a')} & {r['route'] for r in records}
                if route in ('/', '/projects/', '/universe/') and len(matches) == 1:
                    expected = next(r for r in records if r['route'] in matches)
                    if len(card.select(f'[data-project-status="{expected["id"]}"]')) != 1:
                        raise ValueError(f'{route}: missing or duplicated card status')
        print(f'Project status valid: {len(records)} records; details, shelves and search agree')
        return 0
    except (KeyError, TypeError, ValueError, OSError) as exc:
        print(f'Project status invalid: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
