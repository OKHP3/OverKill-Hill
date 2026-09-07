#!/usr/bin/env python3
"""Render isolated A14 alternatives. No published source or runtime mutation."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.local/a14'
TEMPLATE = ROOT / 'assets/templates/a14/template--preview.html'
PAGES = {'home': 'index', 'projects': 'projects/index',
         'detail': 'projects/mermaid-theme-builder/index', 'contact': 'contact/index'}


def section(text, label):
    pattern = rf'<section aria-labelledby="{label}".*?</section>'
    matches = re.findall(pattern, text, re.S)
    if len(matches) != 1:
        raise ValueError(f'Expected one section: {label}')
    return matches[0]


def selected():
    # Deliberate proposal samples, not a competing project-status registry.
    return '''<section class="selected proposal-wrap" aria-labelledby="selection-title">
<p class="eyebrow">A few ways into the work</p><h2 id="selection-title">Selected work</h2>
<div class="selected-grid">
<article class="selection"><p class="eyebrow">Tool · v0.6.1 described</p><h3>Mermaid Theme Builder</h3><p class="summary">Reusable visual rules for Mermaid diagrams.</p><p class="evidence">The project page documents the release and links its source. External behavior is not verified here.</p><a class="primary-action" href="detail.html">Inspect project →</a></article>
<article class="selection"><p class="eyebrow">Prototype</p><h3>BPMN for Mermaid</h3><p class="summary">A text-first approach to process diagrams.</p><p class="evidence">The project page documents prototype scope, examples and limitations.</p><a class="primary-action" href="/projects/bpmn-for-mermaid/">Inspect prototype →</a></article>
<article class="selection"><p class="eyebrow">Published writing</p><h3>The First Diagram Is Usually a Liar</h3><p class="summary">An experiment and its evidence archive.</p><p class="evidence">The article includes first passes, revisions and the Council’s scores.</p><a class="primary-action" href="/writings/first-diagram-is-a-liar/">Read the evidence →</a></article>
</div></section>'''


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    template = TEMPLATE.read_text()
    inputs = {key: (ROOT / f'site-src/pages/{path}.main.html').read_text()
              for key, path in PAGES.items()}
    art_picture = re.search(r'<picture>.*?</picture>', inputs['home'], re.S).group()
    art = f'''<figure class="accepted-art">{art_picture}<figcaption><a href="/writings/murderbird/">Meet the MurderBird: read the origin story →</a></figcaption></figure>'''
    tasks = '''<nav class="task-choices" aria-label="Start with the work"><a href="https://okhp3.github.io/mermaid-theme-builder/#compose">Try a tool ↗</a><a href="projects.html">Inspect projects</a><a href="contact.html">Discuss a project</a></nav>'''
    for direction, name in [('a', 'Forge front door'), ('b', 'Work first')]:
        target = OUT / direction
        target.mkdir(exist_ok=True)
        for page, source in inputs.items():
            body = source
            if page == 'home':
                old_hero = section(source, 'hero-title')
                body = source.replace(old_hero, '')
                for label in ['start-here-heading', 'selected-work-heading']:
                    body = body.replace(section(body, label), '')
                # Preserve original owner copy below the proposed entry, including motto.
                original_intro = re.search(r'<aside class="hero-forge-card">(.*?)</aside>', old_hero, re.S).group(1)
                lead = f'''<section class="proposal-wrap proposal-hero" id="forge"><div><p class="eyebrow">The digital forge</p><h1>Precision · Protocol · Promptcraft</h1><p class="proposal-lead">AI tools, documented experiments, and methods you can inspect.</p>{tasks}</div>{art if direction == 'a' else ''}</section>'''
                body = lead + selected() + (f'<div class="proposal-wrap">{art}</div>' if direction == 'b' else '') + f'<aside class="proposal-wrap orientation">{original_intro}</aside>' + body
            elif page == 'projects':
                end = body.index('</section>') + len('</section>')
                body = body[:end] + selected() + '<p class="proposal-wrap">The full shelf follows. Existing descriptions below await A11/A12 reconciliation.</p>' + body[end:]
            elif page == 'detail':
                end = body.index('</h1>') + len('</h1>')
                body = body[:end] + '''<nav aria-label="Project evidence"><a href="#release">Jump to release details ↓</a></nav>''' + body[end:]
            else:
                end = body.index('</h1>') + len('</h1>')
                body = body[:end] + '''<p><a class="btn btn-primary" href="mailto:contact@overkillhill.com">Email the Hill</a></p><p><a href="#contact-details">Contact details ↓</a> · <a href="#support">Creator support ↓</a></p>''' + body[end:]
            result = template
            for token, value in {'DIRECTION': direction, 'NAME': name, 'PAGE': page, 'BODY': body}.items():
                result = result.replace(f'[[{token}]]', value)
            (target / f'{page}.html').write_text(result)
    panels = ''
    for d, name, note in [('a', 'Forge front door', 'Task choices, then the accepted artwork, then selected work.'), ('b', 'Work first', 'Task choices, then compact selected work, then the accepted artwork.')]:
        links = ' · '.join(f'<a href="{d}/{p}.html">{p.title()}</a>' for p in PAGES)
        panels += f'<section><h2>{d.upper()}: {name}</h2><p>{note}</p><p>{links}</p><a href="{d}/home.html"><img width="390" height="844" src="evidence/{d}-home-390-entry.png" alt="{name} at 390 pixels wide"></a></section>'
    (OUT / 'index.html').write_text(f'''<!doctype html><html lang="en-US"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>A14 alternatives</title><style>body{{background:#2a2320;color:#f0ebe5;font:18px/1.5 sans-serif;margin:24px auto;padding:0 20px;max-width:1120px}}a{{color:#e6a03c}}main{{display:flex;flex-wrap:wrap;gap:40px}}section{{flex:1;min-width:280px}}img{{max-width:100%;height:auto}}</style><h1>A14 layout alternatives</h1><p>Local proposals. New copy and status examples await owner selection and reviewed A11/A12 content. The full archive and published pages remain unchanged.</p><main>{panels}</main></html>''')
    (OUT / 'inputs.json').write_text(json.dumps({path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in [str(TEMPLATE.relative_to(ROOT)), 'assets/css/theme.css'] + [f'site-src/pages/{p}.main.html' for p in PAGES.values()]}, indent=2) + '\n')
    print(f'Rendered eight local pages at {OUT}')


if __name__ == '__main__':
    main()
