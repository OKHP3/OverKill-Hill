"""Canonical editorial project facts and deterministic public summaries."""
from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup, Comment

ROOT = Path(__file__).resolve().parents[1]


def load_registry(root=ROOT):
    data = json.loads((root / 'site-src/project-status.json').read_text(encoding='utf-8'))
    validate(data, root)
    return data['projects']


def validate(data, root=ROOT):
    if data['schema'] != 2:
        raise ValueError('Expected project registry schema 2')
    date.fromisoformat(data['reviewed'])
    ids, routes = set(), set()
    for record in data['projects']:
        for field in ('id', 'title', 'route', 'kind', 'availability', 'maturity'):
            if not isinstance(record[field], str) or not record[field].strip():
                raise ValueError(f'Missing project {field}')
        if record['id'] in ids or record['route'] in routes:
            raise ValueError('Duplicate project ID or route')
        ids.add(record['id'])
        routes.add(record['route'])
        date.fromisoformat(record['reviewed'])
        if record['kind'] not in ('detail', 'shelf-exception'):
            raise ValueError('Unknown project kind')
        if not isinstance(record['shelf'], bool):
            raise ValueError('Shelf membership must be explicit')
        if (not record['shelf'] or record['kind'] == 'shelf-exception') and not record['shelf_exception']:
            raise ValueError('Missing shelf exception reason')
        evidence = record['evidence']
        if not re.fullmatch(r'[0-9a-f]{40}', evidence['revision']):
            raise ValueError('Evidence requires an immutable source revision')
        if not evidence['url'].startswith('https://github.com/OKHP3/') or '/blob/' + evidence['revision'] + '/' not in evidence['url']:
            raise ValueError('Evidence URL must identify its public source revision')
        # This source-review schema deliberately cannot certify runtime delivery.
        if evidence['tier'] != 'source-described' or evidence['delivery'] != 'unknown':
            raise ValueError('Unsupported delivery proof: source review cannot certify operation')
        if not evidence['summary'].strip():
            raise ValueError('Missing evidence scope')
        source = (root / evidence['source']).resolve()
        if not source.is_relative_to(root.resolve()) or not source.is_file():
            raise ValueError('Evidence source must exist inside the repository')
    details = {'/projects/' + p.parent.name + '/' for p in (root / 'site-src/pages/projects').glob('*/index.main.html')}
    if details != {r['route'] for r in data['projects'] if r['kind'] == 'detail'}:
        raise ValueError('Project detail coverage differs from the source inventory')
    shelf = BeautifulSoup((root / 'site-src/pages/projects/index.main.html').read_text(encoding='utf-8'), 'html.parser')
    actual = set()
    for section in shelf.select('[data-project-shelf]'):
        for card in section.find_all('article'):
            actual.add(card.find('a')['href'])
    if actual != {r['route'] for r in data['projects'] if r['shelf']}:
        raise ValueError('Shelf coverage differs from declared records and exceptions')


def summary(record):
    return (f"Availability: {record['availability']}. Maturity: {record['maturity']}. "
            f"Evidence: {record['evidence']['summary']} Delivery: unknown.")


def summary_html(record):
    evidence = record['evidence']
    source = evidence['url']
    return ('<!-- AUTOGEN:PROJECT-STATUS -->'
            f'<p data-project-status="{html.escape(record["id"], quote=True)}">'
            + '<span data-project-status-text="">' + html.escape(summary(record)) + '</span> '
            + f'<a href="{html.escape(source, quote=True)}">Source record</a>'
            + f' (reviewed {record["reviewed"]}).</p><!-- /AUTOGEN:PROJECT-STATUS -->')


def visitor_summary(record):
    """Keep visible limitations derived from the canonical record."""
    if record['evidence']['delivery'] != 'unknown':
        raise ValueError('Disclosure wording requires review for a new delivery state')
    text = record['maturity'].rstrip('.') + '.'
    if record['maturity'] == 'Unknown':
        text = record['availability'] + '. Maturity unknown.'
    if record['id'] == 'mac-studio-local-ai-workbench':
        # The RAG limit is material even when the source disclosure is closed.
        return text + ' ' + record['evidence']['summary']
    software = record['availability'] in ('Published project', 'Published catalog project', 'Noindex concept page')
    label = 'Operation unverified.' if software else 'Delivery unverified.'
    return text + ' ' + label


def disclosure_html(record):
    """Native disclosure preserving complete canonical source facts."""
    return (f'<div data-project-status-disclosure="{html.escape(record["id"], quote=True)}">'
            + '<p data-project-status-brief="">' + html.escape(visitor_summary(record)) + '</p>'
            + '<details><summary>Status and source</summary>'
            + summary_html(record) + '</details></div>')


def render(main, route, records, *, disclosure=False):
    """Render status once per applicable card or detail, preserving source history."""
    if route not in ('/', '/projects/', '/universe/') and not any(r['route'] == route and r['kind'] == 'detail' for r in records):
        return main
    soup = BeautifulSoup(main, 'html.parser')
    disclosure = disclosure or soup.select_one('[data-status-presentation="disclosure"]') is not None
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        if str(comment).strip() in ('AUTOGEN:PROJECT-STATUS', '/AUTOGEN:PROJECT-STATUS'):
            comment.extract()
    for old in soup.select('[data-project-status-disclosure]'):
        old.decompose()
    for old in soup.select('[data-project-status]'):
        old.decompose()
    formatter = disclosure_html if disclosure else summary_html
    by_route = {r['route']: r for r in records}
    record = by_route.get(route)
    if record and record['kind'] == 'detail':
        soup.h1.insert_after(BeautifulSoup(formatter(record), 'html.parser'))
    if route in ('/', '/projects/', '/universe/'):
        for card in soup.find_all('article'):
            matches = {a.get('href') for a in card.find_all('a')} & by_route.keys()
            if len(matches) == 1:
                record = by_route[matches.pop()]
                heading = card.find(['h2', 'h3'])
                if heading:
                    anchor = heading
                    if disclosure:
                        anchor = next((p for p in heading.find_next_siblings('p') if not p.find('a')), heading)
                    anchor.insert_after(BeautifulSoup(formatter(record), 'html.parser'))
    return str(soup)
