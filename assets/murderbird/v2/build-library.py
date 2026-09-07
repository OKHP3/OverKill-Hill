"""Build a review library. Pillow only resizes/encodes whole images; never crops.
Run: py -3 assets/murderbird/v2/build-library.py
"""
from pathlib import Path
from PIL import Image
import hashlib, html, json, os, subprocess
from bs4 import BeautifulSoup
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
REVIEW_ROOT = REPO / '.local' / 'murderbird-review'
CATALOG = [
 ('01-maker','The Maker','Ancient commission','An ancient bronze MurderBird in the Maker’s workshop.','The body is made; the bones remain evidence, never machinery.',['story: Maker','process essays']),
 ('02-water','What the Water Kept','Submerged centuries','The inert bronze MurderBird beneath water.','Stillness, mineral deposits, and the long preservation of a body.',['story: water','editorial divider']),
 ('03-recovery','The Recovery','1853','The bronze MurderBird during its nineteenth-century recovery.','Excavation and transport precede the later restoration.',['story: recovery','archive feature']),
 ('04-mechanic','The Mechanic','1873','The bronze MurderBird undergoing industrial restoration.','Iron braces and brass bushings remain visibly distinct from ancient bronze.',['story: Mechanic','engineering essays']),
 ('05-heart','The Heart','2025','The MurderBird receives its modern power assembly.','A modern heart gives the old mechanisms energy; a mind is a separate achievement.',['story: Builder','technology feature']),
 ('06-choice','The First Choice','2025','The MurderBird stands in a modern workshop as it begins to act independently.','The first choice is measured, observant, and consequential.',['story: first choice','about/process']),
 ('07-sentinel','The Sentinel','Modern','The bronze MurderBird stands beside a computer in a modern workshop.','The floor bears its weight; the screen holds its questions.',['story: ending','about','manifesto companion']),
 ('08-hero','The MurderBird','Modern brand portrait','The large bronze MurderBird in a workshop setting.','Ancient body. Industrial repairs. Modern heart and mind.',['homepage','localized homepages','brand social']),
]

def write(path, value):
    if path.suffix == '.html' and path.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError('Review HTML must be written under the excluded review directory')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding='utf-8')

def write_review(relative, markup):
    """Retarget local links while leaving all production files in place."""
    source = ROOT / relative
    target = REVIEW_ROOT / relative
    def relocated(url):
        if urlsplit(url).scheme or url.startswith(('#', '/', '//')):
            return url
        resolved = (source.parent / url).resolve()
        if resolved.suffix == '.html' and resolved.is_relative_to(ROOT.resolve()):
            resolved = REVIEW_ROOT / resolved.relative_to(ROOT.resolve())
        return Path(os.path.relpath(resolved, target.parent)).as_posix()
    soup = BeautifulSoup(markup, 'html.parser')
    for node in soup.find_all(True):
        for attribute in ('href', 'src'):
            if node.has_attr(attribute):
                node[attribute] = relocated(node[attribute])
        if node.has_attr('srcset'):
            node['srcset'] = ', '.join(' '.join([relocated(parts[0]), *parts[1:]]) for item in node['srcset'].split(',') if (parts := item.strip().split()))
    write(target, str(soup))


def facts(path):
    with Image.open(path) as im: width,height=im.size
    return dict(path=path.relative_to(ROOT).as_posix(),width=width,height=height,bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest())

def social_layout(title, alt, source_path):
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="robots" content="noindex"><title>{html.escape(title)} — social card candidate</title><style>*{{box-sizing:border-box}}html,body{{margin:0;width:1200px;height:630px;background:#101919;color:#f5ead6;font-family:Georgia,serif}}main{{height:570px;display:flex;justify-content:center}}img{{width:100%;height:100%;object-fit:contain}}footer{{height:60px;display:flex;align-items:center;justify-content:space-between;padding:0 32px;border-top:1px solid #806a43;font-size:24px}}small{{font:14px system-ui;letter-spacing:2px;color:#bfcac5}}</style><main><img src="../{source_path}" alt="{html.escape(alt,quote=True)}"></main><footer><span>{html.escape(title)}</span><small>OVERKILL HILL P³ · WHAT THE WATER KEPT</small></footer></html>'''


def rebuild_social_html():
    """Refresh review markup without changing images or provenance records."""
    manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    count = 0
    for entry in manifest['entries']:
        if 'derivatives' not in entry:
            continue
        derivatives = entry['derivatives']
        source = next((d for d in reversed(derivatives) if d['path'].endswith('.jpg')), derivatives[-1])
        write_review(f"social/{entry['id']}.html", social_layout(entry['title'], entry['alt'], source['path']))
        count += 1
    print(f'Rebuilt {count} noindex social review layouts; rasters and provenance unchanged.')


def main():
    (ROOT/'derivatives').mkdir(parents=True,exist_ok=True)
    (ROOT/'social').mkdir(exist_ok=True)
    try: revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    except Exception: revision=None
    provenance={}
    for record in sorted((ROOT/'masters').glob('*-metadata.json')):
        document=json.loads(record.read_text(encoding='utf-8-sig'))
        for asset in document.get('assets',[]):
            provenance[asset['id']]={**asset,'record':record.relative_to(ROOT).as_posix(),'storySourceCommit':document.get('storySourceCommit')}
    entries=[]
    for slug,title,era,alt,caption,placements in CATALOG:
        origin=provenance.get(slug,{})
        title=origin.get('title',title);era=origin.get('era',era);alt=origin.get('alt',alt);placements=origin.get('placements',placements)
        matches=sorted(p for p in (ROOT/'masters').glob(slug+'*') if p.suffix.lower() in {'.png','.jpg','.jpeg','.webp'})
        entry=dict(id=slug,title=title,storyEra=era,alt=alt,caption=caption,placements=placements,reviewStatus='pending-visual-and-canon-review',generationTool='OpenAI native image generation',originPromptPointers=[p.relative_to(ROOT).as_posix() for p in sorted((ROOT/'prompts').glob(slug+'*'))],status='missing-master')
        if origin:
            entry['originPromptPointers'].append(origin['record']+'#'+slug)
            entry['prompt']=origin.get('prompt');entry['storySourceCommit']=origin.get('storySourceCommit');entry['limitations']=origin.get('limitations',[])
            for key in ('correctivePrompt','correctionPrompt','corrections','review','reviewStatus'):
                if key in origin: entry[key]=origin[key]
        if (ROOT/'independent-visual-review.md').exists():
            entry['reviewStatus']='visual-review-recorded; canon-and-publication-pending'
            entry['visualReviewPointer']='independent-visual-review.md'
        if len(matches)>1:
            entry['status']='ambiguous-masters';entry['candidates']=[str(p.relative_to(ROOT)) for p in matches];entries.append(entry);continue
        if not matches: entries.append(entry);continue
        master=matches[0];entry['master']=facts(master);entry['status']='candidate';entry['derivatives']=[]
        with Image.open(master) as im:
            im.load()
            for target in (480,960,1600):
                width=min(target,im.width);height=round(im.height*width/im.width)
                scaled=im.resize((width,height),Image.Resampling.LANCZOS) if width!=im.width else im.copy()
                for extension in ('webp','jpg'):
                    # Never discard alpha: JPEG is omitted for nonopaque artwork.
                    if extension=='jpg' and 'A' in scaled.getbands() and scaled.getextrema()[-1][0]<255: continue
                    dest=ROOT/'derivatives'/f'{slug}-{width}.{extension}'
                    if extension=='webp': scaled.save(dest,'WEBP',quality=84,method=6)
                    else: scaled.convert('RGB').save(dest,'JPEG',quality=88,optimize=True,progressive=True)
                    if not any(d['path']==dest.relative_to(ROOT).as_posix() for d in entry['derivatives']): entry['derivatives'].append(facts(dest))
        source=next((d for d in reversed(entry['derivatives']) if d['path'].endswith('.jpg')),entry['derivatives'][-1])
        social = social_layout(title, alt, source['path'])
        write_review(f'social/{slug}.html', social)
        entry['socialCard']=dict(layout=Path(os.path.relpath(REVIEW_ROOT / 'social' / f'{slug}.html', ROOT)).as_posix(),width=1200,height=630,status='html-layout-needs-browser-rasterization')
        social_raster=ROOT/'social'/f'{slug}.png'
        if social_raster.exists():
            entry['socialCard'].update(raster=facts(social_raster),status='rasterized-candidate')
            source=entry['socialCard']['raster']
        # These URLs describe intended deployment, not a claim that files are live.
        public='https://overkillhill.com/assets/murderbird/v2/'+source['path']
        entry['imageObjectDraft']={'@context':'https://schema.org','@type':'ImageObject','name':title,'description':alt,'caption':caption,'contentUrl':public,'encodingFormat':'image/png' if source['path'].endswith('.png') else 'image/jpeg' if source['path'].endswith('.jpg') else 'image/webp','width':source['width'],'height':source['height']}
        entry['metadataSnippetDraft']=f'<meta property="og:image" content="{public}">\n<meta property="og:image:width" content="{source["width"]}">\n<meta property="og:image:height" content="{source["height"]}">\n<meta property="og:image:alt" content="{html.escape(alt,quote=True)}">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="{public}">\n<meta name="twitter:image:alt" content="{html.escape(alt,quote=True)}">'
        entries.append(entry)
    manifest=dict(version=1,publicationStatus='local-review-only',sourceRepositoryRevision=revision,storySource='site-src/pages/writings/murderbird/index.main.html',scaleStatus='proposed approximately 1.8 m standing height; pending canon confirmation',processing='Whole-frame proportional resize and encoding only. No crop, retouch, compositing, or generation in Pillow.',entries=entries)
    write(ROOT/'manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    build_gallery(entries)
    print(json.dumps({'candidates':sum(e['status']=='candidate' for e in entries),'pending':[e['id'] for e in entries if e['status']!='candidate'],'manifest':str(ROOT/'manifest.json')}))


def build_gallery(entries):
    cards=[]
    for e in entries:
        if 'master' not in e:
            cards.append(f'<article class="pending"><div class="placeholder">Awaiting master</div><div class="copy"><p class="era">{e["storyEra"]}</p><h2>{e["title"]}</h2><p>{e["caption"]}</p></div></article>');continue
        variants=[d for d in e['derivatives'] if d['path'].endswith('.webp')];chosen=variants[min(1,len(variants)-1)]
        srcset=', '.join(f'{d["path"]} {d["width"]}w' for d in variants)
        cards.append(f'''<article><a class="art" href="{e['master']['path']}" aria-label="Open full master: {e['title']}"><img src="{chosen['path']}" srcset="{srcset}" sizes="(max-width:720px) 94vw, 46vw" width="{chosen['width']}" height="{chosen['height']}" alt="{html.escape(e['alt'],quote=True)}" loading="lazy"></a><div class="copy"><p class="era">{e['storyEra']}</p><h2>{e['title']}</h2><p>{e['caption']}</p><p class="meta">{e['master']['width']} × {e['master']['height']} master · {chosen['bytes']/1024:.0f} KB preview</p><p><a href="{e['master']['path']}">Master</a> · <a href="social/{e['id']}.html">Social layout</a></p></div></article>''')
    page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>MurderBird — A body across centuries</title><style>:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#101918;color:#eae7dd;font:17px/1.65 system-ui,sans-serif}header,main,footer{max-width:1380px;margin:auto;padding:36px}header{padding-top:70px}h1{font:clamp(40px,6vw,76px)/1.1 Georgia,serif;max-width:900px;margin:18px 0}h2{font:32px Georgia,serif;margin:8px 0}a{color:#e7bb74;text-underline-offset:4px}a:focus-visible{outline:3px solid #ffcc72;outline-offset:5px}.eyebrow,.era{text-transform:uppercase;letter-spacing:2px;font-size:12px;color:#c7ac7a}.intro{max-width:790px;color:#c4d1ca}.notice{padding:16px 22px;border-left:3px solid #af874b;background:#1b2824;max-width:900px;font-size:15px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:30px}article{border:1px solid #33413a;background:#16211e;overflow:hidden;border-radius:8px}.art{display:block;background:#090e0c}.art img{display:block;width:100%;height:auto}.copy{padding:22px 26px}.copy p{margin:10px 0}.meta{font-size:13px;color:#aebbb2}.placeholder{padding:90px 20px;text-align:center;color:#b9c4bd;background:#14201b}.pending{opacity:.75}footer{font-size:14px;color:#aebbb2;border-top:1px solid #33413a;margin-top:35px}@media(max-width:720px){header,main,footer{padding:22px}.grid{grid-template-columns:1fr}header{padding-top:38px}}</style></head><body><header><p class="eyebrow">OverKill Hill P³ · Visual library · Review edition</p><h1>A body across centuries.</h1><p class="intro">The MurderBird: ancient bronze, industrial repair, and a modern heart and mind. An eight-image sequence for the story and the wider site.</p><p class="notice">Candidate artwork. Approximately adult-height scale is a proposed design target. Review continuity and visible details before publication. Existing site imagery remains unchanged.</p><p><a href="manifest.json">Asset metadata</a> · <a href="placement-map.md">Placement map</a> · <a href="README.md">Delivery notes</a></p></header><main class="grid">'''+''.join(cards)+'''</main><footer>Images created with OpenAI native image generation. Delivery files preserve the complete composition through proportional resizing. No creator, license, publication, or approval claims are inferred.</footer></body></html>'''
    page=page.replace('<a href="README.md">Delivery notes</a>', '<a href="README.md">Delivery notes</a> · <a href="ART-DIRECTION.md">Art direction</a> · <a href="independent-visual-review.md">Visual review</a> · <a href="production/README.md">Blender scale stage</a>')
    write_review('index.html', page)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--social-html-only', action='store_true', help='Refresh noindex review layouts without touching rasters or provenance')
    parser.add_argument('--review-html-only', action='store_true', help='Refresh gallery and social HTML without touching production files')
    args = parser.parse_args()
    if args.review_html_only:
        rebuild_social_html()
        build_gallery(json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))['entries'])
    elif args.social_html_only:
        rebuild_social_html()
    else:
        main()
