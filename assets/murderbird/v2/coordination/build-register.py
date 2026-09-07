"""Read-only cross-collection inventory; write this coordination register only."""
from pathlib import Path
import hashlib, json, subprocess
from PIL import Image

root = Path(__file__).resolve().parents[4]
out = Path(__file__).resolve().parent
tracked = set(subprocess.check_output(['git','ls-files'],cwd=root,text=True).splitlines())
head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
accepted_scenes = {
 'maker': ('93966eb269ae9f8d8d00e05e913cbb23f7656204e6f3fdf7fd26e8a39ca0cbb9', 'Quiet inspection of completed floor-standing body by back-view hooded Maker with intact lowered hammer; not the hammer-breaking event or exact historical attire certification'),
 'mechanic': ('0bd7c79510be9eeef024f8861a7576b777a7f5de5710523e8d2ab039d03c65f9', 'Industrial repairs fitted around ancient bronze; floor-supported body; no autonomous awakening claim'),
 'water': ('0db88f0529288a9c6032662a9fb9e62d1ae077322241c4d9bd2c5a8eb915c117', 'Inert partly submerged body and mineral history; no exact chemistry or internal-mechanism claim'),
 'heart': ('9430f91e3cd3fc8223297720a0f57ec1c46e9c8245cfba91495e9c362029fea9', 'Power assembly inspection; not completed heart and mind'),
 'sentinel': ('d6153907884045e824e3be9cd02a7a446fb75f6e8b35a246918cf11ac620667e', 'Floor-standing Bird watching operator beside CRT; no invisible screen text claim'),
}
groups = {
 'unified-scenes': [root / f'assets/img/library/murderbird-unified-{scene}{"-clean" if scene == "maker" else ""}-candidate-2026-09-06.png' for scene in accepted_scenes],
 'narrative': sorted((root/'assets/murderbird/v2/masters').glob('[0-9][0-9]-*.png')),
 'human-scale': [root/'assets/img/library'/name for name in (
  'murderbird-floor-master-landscape-1536-2026-09-06.png',
  'murderbird-camera-advance-square-1254-2026-09-06.png',
  'murderbird-social-hero-wide-1774-2026-09-06.png',
  'murderbird-head-avatar-square-1254-2026-09-06.png',
  'murderbird-profile-stride-landscape-1536-2026-09-06.png',
  'murderbird-repair-detail-landscape-1536-2026-09-06.png',
  'murderbird-rear-view-landscape-1536-2026-09-06.png',
  'murderbird-standing-cutout-candidate-portrait-1024-2026-09-06.png')],
 'scale-series': sorted((root/'assets/img/library').glob('murderbird-scale-*-2026-09-06.png')),
 'unified-reference': [root/'assets/img/library/murderbird-unified-master-candidate-03-2026-09-06.png'],
}
records=[]
for group,paths in groups.items():
 for p in paths:
  rel=p.relative_to(root).as_posix()
  entry={'collection':group,'path':rel,'exists':p.is_file(),'gitTracked':rel in tracked,'publicationStatus':'unverified'}
  if p.is_file():
   data=p.read_bytes()
   with Image.open(p) as im:
    im.load()
    entry.update(width=im.width,height=im.height,mode=im.mode,hasAlpha='A' in im.getbands())
   entry.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),reviewStatus='rejected-transparent-use' if 'cutout' in p.name else 'candidate')
  if rel == 'assets/img/library/murderbird-unified-master-candidate-03-2026-09-06.png':
   expected = '538c51bcdbf5bfce95a0932fdbbb0f5868b446f4985346d15e6cacd32430e633'
   if entry.get('sha256') != expected:
    raise SystemExit('Accepted reference bytes changed; renewed lead review required.')
   entry.update(id='murderbird-unified-reference-03',reviewStatus='lead-accepted-illustrative-production-reference',publicationStatus='local-story-hero-preview-only',acceptance={'authority':'coordinating-lead','brief':'docs/murderbird-unified-direction.md','briefVersion':'1.2','scope':['head','body silhouette','compact folded wing and rear contour','modern materials','floor-supported staging'],'limitations':['Not Jamie final-art approval or deployment acceptance','Not certified 2.0 m geometry or an animation rig','Hidden mechanisms and close-up shoulder topology are not certified','Modern hardware must not be copied into earlier eras']},placements=['/writings/murderbird/#media-hero'],derivativeBuilder='scripts/build-murderbird-hero.py')
   entry['placements'] += ['/#forge', '/fr/#forge', '/de/#forge', '/es/#forge', '/es-mx/#forge']
   entry['publicationStatus']='local-story-and-homepage-preview-only'
   entry['derivatives']=[]
   for derivative in sorted((root/'assets/img/webp').glob('murderbird-unified-master-03-2026-09-06-*.webp')):
    data=derivative.read_bytes()
    with Image.open(derivative) as picture:
     dimensions=picture.size
    entry['derivatives'].append({'path':derivative.relative_to(root).as_posix(),'width':dimensions[0],'height':dimensions[1],'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'processing':'proportional resize and WebP encoding; no crop or upscale'})
  for scene, (expected, scope) in accepted_scenes.items():
   variant = '-clean' if scene == 'maker' else ''
   if rel != f'assets/img/library/murderbird-unified-{scene}{variant}-candidate-2026-09-06.png':
    continue
   if entry.get('sha256') != expected:
    raise SystemExit(f'Accepted {scene} bytes changed; renewed lead review required.')
   entry.update(id=f'murderbird-unified-{scene}',reviewStatus='lead-accepted-local-illustrated-preview',publicationStatus='not-published',acceptance={'authority':'coordinating-lead','brief':'docs/murderbird-unified-direction.md','scope':[scope],'limitations':['Local preview acceptance, not Jamie final-art or deployment approval','No numeric height, engineering, chemistry, or hidden mechanism certification']},placements=[f'/writings/murderbird/#media-{scene}'],derivativeBuilder=f'scripts/build-murderbird-hero.py --asset {scene}',derivatives=[])
   for derivative in sorted((root/'assets/img/webp').glob(f'murderbird-unified-{scene}{variant}-2026-09-06-*.webp')):
    data=derivative.read_bytes()
    with Image.open(derivative) as picture:
     dimensions=picture.size
    entry['derivatives'].append({'path':derivative.relative_to(root).as_posix(),'width':dimensions[0],'height':dimensions[1],'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'processing':'proportional resize and WebP encoding; no crop or upscale'})
  records.append(entry)
social=root/'assets/img/og/murderbird-story-share-2026-09-06.png'
if social.is_file():
 data=social.read_bytes()
 with Image.open(social) as picture:
  dimensions=picture.size
 records.append({'id':'murderbird-story-share','collection':'story-social-composition','path':social.relative_to(root).as_posix(),'width':dimensions[0],'height':dimensions[1],'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'gitTracked':social.relative_to(root).as_posix() in tracked,'source':'assets/img/library/murderbird-unified-master-candidate-03-2026-09-06.png','sourceSha256':'538c51bcdbf5bfce95a0932fdbbb0f5868b446f4985346d15e6cacd32430e633','generator':'scripts/build-murderbird-story-social.mjs','reviewHtml':'.local/murderbird-review/social/murderbird-story-share.html','reviewStatus':'local-review-candidate','publicationStatus':'not-published','placements':['/writings/murderbird/ Open Graph','/writings/murderbird/ Twitter card','/writings/murderbird/ Article image'],'processing':'Full uncropped accepted illustration with real Alfa Slab One, DM Sans and JetBrains Mono typography; 1200x630 PNG'})
video_dir=Path('C:/Users/jamie/Documents/murderbird-production/2026-09-06')
videos=[]
for p in sorted(video_dir.glob('*-original.mp4')):
 data=p.read_bytes()
 videos.append({'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'inRepository':False,'reviewStatus':'legacy-scale-study-not-current-narrative-media','metadataRecord':str(video_dir/'video-metadata.json')})
standalone=[p.relative_to(root).as_posix() for base in ('assets','context') for p in (root/base).rglob('*') if p.is_file() and p.suffix.lower() in ('.wav','.mp3','.ogg','.m4a','.flac')]
register={'scope':'snapshot, not an approval or publication manifest','sourceRevision':head,'collections':{k:len(v) for k,v in groups.items()},'imageMasters':records,'videoOriginals':videos,'standaloneAudioInAssetsAndContext':standalone,'audioNote':'Downloaded videos have AAC tracks per verified metadata. Artistic suitability has not been audited; no accepted soundtrack inferred.','githubCheck':{'path':'assets/murderbird/v2/manifest.json','ref':'main','result':'GitHub connector returned404 at review time'},'provenanceDocuments':['assets/murderbird/v2/manifest.json','assets/docs/murderbird-human-scale-library-2026-09-06.md','assets/docs/murderbird-scale-series-catalog-2026-09-06.md']}
(out/'asset-register.json').write_text(json.dumps(register,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'collections':register['collections'],'images':len(records),'untracked':sum(not x['gitTracked'] for x in records),'videoOriginals':len(videos),'videoBytes':sum(x['bytes'] for x in videos),'standaloneAudio':len(standalone)},indent=2))
