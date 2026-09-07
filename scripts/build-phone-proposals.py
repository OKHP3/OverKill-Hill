#!/usr/bin/env python3
"""Render isolated A14 layout studies from current pages, never production files."""
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import tarfile
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".local/a14"
A11 = '9bfe170badf3133fab8119643aafeb1f04d2d0c9'
ROUTES = ("index.html", "projects/index.html", "projects/skillz/index.html", "contact/index.html")
CONTACT = '''<h3>What are you trying to untangle?</h3>
<p>A few details can help start the conversation. Share whatever is useful:</p>
<ul><li>The problem you want to solve.</li><li>How the process works today, and where it gets stuck.</li>
<li>What a useful result would look like.</li><li>Constraints that matter, such as tools, timing, or budget.</li></ul>
<p>No finished brief needed. If a page here prompted your inquiry, include its link.</p>
<p>If the email link does not open your mail app, copy contact@overkillhill.com into a new message.</p>'''
CSS = """
/* A14 review only. Production continues to use the unmodified theme.css. */
.proposal-note {padding:.65rem 1rem;background:var(--color-surface);border-bottom:2px solid var(--okh-orange);font: .75rem var(--font-mono);}
.proposal-note a {margin-right:1rem;display:inline-block;min-height:32px;}
.proposal .hero {min-height:0;}
.proposal .hero-inner {padding:2rem 1rem;}
.proposal .hero h1 {font-size:clamp(1.9rem,4vw,3.2rem);overflow-wrap:anywhere;}
.proposal .hero-tagline {max-width:56ch;}
.proposal .hero-visual img {object-fit:contain;max-height:320px;width:100%;}
.proposal .hero-grid {align-items:center;gap:1.5rem;}
.proposal .content-section {padding-top:2rem;padding-bottom:2rem;}
.proposal .reveal-on-scroll {opacity:1;transform:none;}
.proposal-choices {display:flex;flex-wrap:wrap;gap:.5rem 1rem;margin:1rem 0;}
.proposal-choices a {display:inline-flex;align-items:center;min-height:44px;font-weight:700;}
.proposal .project-card h3 {font-size:1.2rem;}
.proposal .project-card {border-top:2px solid var(--okh-orange);}
.proposal [data-project-status] {font-size:.9rem;line-height:1.6;}
.proposal .project-card .btn-primary {white-space:normal;max-width:100%;}
.proposal-a .grid-3:has(>.project-card) {grid-template-columns:1fr;gap:0;}
.proposal-a .project-card {border-radius:0;border-left:0;border-right:0;padding:1.2rem 0;background:transparent;box-shadow:none;}
.proposal-b .hero h1 {max-width:17ch;}
.proposal-b .hero-visual img {max-height:380px;}
.proposal-b .latest-block {border-top:2px solid var(--okh-orange);}
@media(min-width:901px){.proposal .hero-grid {grid-template-columns:1.2fr 1fr;}.proposal-a .project-card {display:grid;grid-template-columns:1fr 2fr;column-gap:2rem;}.proposal-a .project-card h3 {grid-column:1;}.proposal-a .project-card p {grid-column:2;}}
@media(max-width:600px){.proposal .container {width:100%;padding-left:1rem;padding-right:1rem;}.proposal .hero-inner {padding-top:1.25rem;padding-bottom:1.25rem;}.proposal .hero-visual img {max-height:220px;}.proposal .hero-grid {gap:.75rem;}.proposal .hero-eyebrow {margin-bottom:.3rem;}.proposal .hero h1 {font-size:1.9rem;}.proposal-b .hero-visual img {max-height:260px;}.proposal .grid {grid-template-columns:1fr;}}
"""


def homepage(text, variant):
    """Only reorder existing sections; no project truth or date claims authored."""
    main = re.search(r'<main\b[^>]*>(.*?)</main>', text, re.S).group(1)
    hero = re.search(r'<section\b.*?</section>', main, re.S).group(0)
    choices = '''<nav class="proposal-choices" aria-label="Start with the work">
<a href="/projects/skillz/">Use a tool</a><a href="/projects/">Inspect the work</a><a href="/contact/">Discuss a project</a></nav>'''
    # Keep the owner motto, accepted picture and full original material below.
    intro = '<p class="hero-tagline">AI tools, working methods, and the evidence behind them.</p>'
    compact = re.sub(r'<p class="hero-tagline">.*?</p>', intro + choices, hero, count=1, flags=re.S)
    compact = re.sub(r'<div aria-label="OverKill Hill active build notice".*?</div>', '', compact, flags=re.S)
    compact = re.sub(r'<div class="hero-actions">.*?</div>', '', compact, flags=re.S)
    compact = re.sub(r'<aside class="hero-forge-card">.*?</aside>', '', compact, flags=re.S)
    # Full removed prose remains reviewable in an optional native disclosure.
    original_copy = re.search(r'<p class="hero-tagline">.*?</p>', hero, re.S).group(0)
    original_aside = re.search(r'<aside class="hero-forge-card">.*?</aside>', hero, re.S).group(0)
    context = '<section class="container content-section"><details><summary>More from the forge</summary>' + original_copy + original_aside + '<p><a href="/manifesto/">Read the manifesto</a></p></details></section>'
    rest = main.replace(hero, '', 1)
    selected = re.search(r'<section aria-labelledby="selected-work-heading".*?</section>', rest, re.S).group(0)
    rest = rest.replace(selected, '', 1)
    if variant == 'b':
        featured = re.search(r'<section aria-labelledby="latest-okh-heading".*?</section>', rest, re.S)
        if featured:
            rest = featured.group(0) + rest.replace(featured.group(0), '', 1)
    return text.replace(main, compact + selected + rest + context, 1)


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    # Read the verified contract into this checkout's ignored preview area only.
    contract_root = OUT / 'contract-source'
    archive = subprocess.check_output(['git', 'archive', A11, 'site-src', 'scripts/project-status.py'], cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
        for member in bundle.getmembers():
            if member.isdir():
                continue
            destination = (contract_root / member.name).resolve()
            if not member.isfile() or not destination.is_relative_to(contract_root.resolve()):
                raise ValueError('Unexpected contract archive member')
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(bundle.extractfile(member).read())
    spec = importlib.util.spec_from_file_location('a14_project_status', contract_root / 'scripts/project-status.py')
    contract = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(contract)
    records = contract.load_registry(contract_root)
    (OUT / 'contract-summaries.json').write_text(json.dumps({r['id']: {'text': contract.summary(r), 'url': r['evidence']['url']} for r in records}, indent=2), encoding='utf-8')
    (OUT / 'proposal.css').write_text(CSS, encoding='utf-8')
    source_hashes = {}
    for variant in ('a', 'b'):
        for route in ROUTES:
            raw = (ROOT / route).read_bytes()
            source_hashes[route] = hashlib.sha256(raw).hexdigest()
            text = raw.decode('utf-8')
            source_path = contract_root / 'site-src/pages' / route.replace('.html', '.main.html')
            main = source_path.read_text(encoding='utf-8')
            main = contract.render(main, '/' + route.removesuffix('index.html'), records)
            text = re.sub(r'(<main\b[^>]*>).*?(</main>)', lambda m: m[1] + main + m[2], text, count=1, flags=re.S)
            if route == 'index.html':
                text = homepage(text, variant)
                # Verified A12 editorial contract, commit 2074a969825e81e742d728b6816fb0adb364b445.
                text = text.replace('Fresh from the Forge', 'Featured from the Forge')
                text = text.replace('The most recent thing to clear the workbench and go public.', 'A selected essay and experiment archive from the forge.')
                text = text.replace('<p class="latest-pill">Featured from the Forge</p>', '<p class="latest-pill">Featured writing</p>')
            if route == 'contact/index.html':
                # A15 optional copy, commit e9154af71eb8248cad2efcf2d44fa5d06bd0ad06.
                text = re.sub(r'(Operating remotely across U.S. Central Time\s*</p>)', r'\1' + CONTACT, text, count=1)
            soup = BeautifulSoup(text, 'html.parser')
            for card in soup.select('.project-card'):
                for heading_link in card.select('h2 a, h3 a'):
                    heading_link.unwrap()
                actions = [a for a in card.select('a[href]') if not a.find_parent(attrs={'data-project-status': True})]
                if actions:
                    primary = actions[0]
                    primary['class'] = ['btn', 'btn-primary']
                    href = primary['href']
                    primary.string = ('Try catalog' if href == 'https://okhp3.github.io/skillz/' else
                                      'Read journal' if '/mac-studio-local-ai-workbench/' in href else
                                      'Inspect project' if href.startswith('/projects/') else
                                      'View concept' if href in ('/writings/magnus-saga/', '/writings/biases-as-constants/') else
                                      'Read essay' if href.startswith('/writings/') else
                                      'Discuss access' if href.startswith('mailto:') else
                                      'Browse resources' if href == '/prompt-forge/' else 'Visit site')
            text = str(soup)
            text = re.sub(r'<body([^>]*)>', rf'<body\1 data-proposal="{variant}">', text, count=1)
            # Existing brand scope is unchanged; proposal styling is scoped via main.
            text = text.replace('<main id="main">', f'<main id="main" class="proposal proposal-{variant}">')
            text = text.replace('</head>', '<meta name="robots" content="noindex,nofollow"/><link rel="stylesheet" href="/proposals/proposal.css"/></head>')
            for target in ROUTES:
                original = '/' + target.removesuffix('index.html')
                text = text.replace(f'href="{original}"', f'href="/proposals/{variant}{original}"')
            note = f'<aside class="proposal-note" aria-label="Proposal status">A14 {variant.upper()} · Proposal for selection. A11 source descriptions; delivery unknown. Introduction and Contact prompts proposed.<br><a href="/proposals/a/">A: Project-led</a><a href="/proposals/b/">B: Editorial</a><a href="/">Current site</a></aside>'
            text = text.replace('<main ', note + '<main ', 1)
            target = OUT / variant / route
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding='utf-8')
    manifest = {'baseline': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(), 'source_sha256': source_hashes, 'status': 'proposal; owner selection and acceptance pending', 'a11': A11, 'a12': '2074a969825e81e742d728b6816fb0adb364b445', 'a15': 'e9154af71eb8248cad2efcf2d44fa5d06bd0ad06', 'routes': list(ROUTES)}
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(f'Rendered 8 proposal pages in {OUT}. Run scripts/serve-phone-proposals.py for review.')


if __name__ == '__main__':
    build()
