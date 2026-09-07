"""Derived accepted-stills subset, not the exploratory editorial asset catalog."""
import argparse
import hashlib
import json
from pathlib import Path
import runpy
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'assets/audit/murderbird-still-release-register.json'
BUILD = runpy.run_path(str(ROOT / 'scripts/build-murderbird-hero.py'))
SOCIAL = 'assets/img/og/murderbird-story-share-2026-09-06.png'
SCOPES = {
    'hero': 'Head, silhouette, folded wing/rear contour, modern materials and floor staging; not a certified rig or exact height.',
    'maker': 'Quiet ancient inspection, hooded back-view Maker, intact lowered hammer; not hammer breaking or exact historical attire.',
    'water': 'Inert partly submerged body and mineral history; no exact chemistry or hidden mechanism certification.',
    'mechanic': 'Industrial repairs around ancient bronze; floor supports; no autonomous awakening.',
    'heart': 'Power inspection, not a completed mind.',
    'sentinel': 'Floor-standing Bird watches operator beside CRT; no unpictured talon gesture or screen text.',
}
HELD_NAMES = [
    'murderbird-unified-maker-candidate-2026-09-06.png',
    'murderbird-unified-maker-candidate-02-2026-09-06.png',
    'murderbird-unified-master-candidate-2026-09-06.png',
    'murderbird-unified-master-candidate-02-2026-09-06.png',
    'murderbird-first-choice-opening-candidate-2026-09-06.png',
]


def describe(path, expected=None):
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if expected and digest != expected:
        raise ValueError(f'Accepted source identity changed: {path.name}')
    with Image.open(path) as image:
        image.load()
        width, height = image.size
    return dict(path=path.relative_to(ROOT).as_posix(), sha256=digest,
                bytes=len(data), width=width, height=height)


def record():
    assets = []
    for scene, (source, expected, prefix) in BUILD['SCENES'].items():
        entry = describe(source, expected)
        entry.update(id=scene, acceptanceScope=SCOPES[scene],
                     authority='Coordinating task explicit local-preview acceptance',
                     placements=['/#forge', '/fr/#forge', '/de/#forge', '/es/#forge', '/es-mx/#forge', '/en-gb/#forge', '/writings/murderbird/#media-hero'] if scene == 'hero' else [f'/writings/murderbird/#media-{scene}'],
                     generator=f'python scripts/build-murderbird-hero.py --asset {scene}',
                     derivatives=[describe(ROOT / f'assets/img/webp/{prefix}-{width}.webp') for width in (480, 960, 1536)])
        assets.append(entry)
    social = describe(ROOT / SOCIAL)
    if (social['width'], social['height']) != (1200, 630):
        raise ValueError('Social composition must be 1200x630.')
    social.update(source='hero', generator='node scripts/build-murderbird-story-social.mjs',
                  processing='Complete proportional art and separate real HTML typography; no crop',
                  placements=['Story Open Graph', 'Story Twitter card', 'Story Article image'])
    return dict(schema=1, selectionBase='2d7e92d23fcbe875c7421d4509109bffd22b0c48',
                status='draft-review-only; no deployment or final-art approval',
                lineage='Derived accepted-only subset of local exploratory assets/murderbird/v2/coordination/asset-register.json; exploratory package intentionally omitted and preserved in primary checkout, not a release dependency or published location.',
                acceptanceReceipt='docs/murderbird-unified-direction.md',
                languageReview='Model-translated or adapted, native review not performed; locale lifecycle unchanged',
                mediaStatus='Five chapter stills and one hero; no video/audio. Pilot blocked on user extension file-access permission.',
                masters=assets, social=social,
                deferred=dict(exactHeldFilenames=HELD_NAMES,
                              localOnly=['assets/murderbird/v2/', '.local/', 'output/', 'unselected scale/human-scale studies', 'external original video files']),
                reproduction='Install requirements-qa.txt and npm ci; generate six WebP sets, render social with loaded site fonts, then run this builder. --check verifies recorded bytes; --package verifies a built release.')


def verify_package(package, payload):
    selected = [payload['social']['path']]
    for master in payload['masters']:
        selected += [master['path']] + [item['path'] for item in master['derivatives']]
    for relative in selected:
        if not (package / relative).is_file():
            raise ValueError(f'Missing accepted release dependency: {relative}')
        if (package / relative).read_bytes() != (ROOT / relative).read_bytes():
            raise ValueError(f'Release bytes differ: {relative}')
    for path in package.rglob('*'):
        rel = path.relative_to(package).as_posix()
        if path.is_file() and (path.name in HELD_NAMES or rel.startswith(('assets/murderbird/', '.local/', 'output/', 'scripts/', 'docs/', 'site-src/'))):
            raise ValueError(f'Excluded exploration/source entered package: {rel}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--package', type=Path)
    args = parser.parse_args()
    payload = record()
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) + '\n'
    if args.check:
        if OUTPUT.read_text(encoding='utf-8') != rendered:
            raise SystemExit('Accepted subset record is stale.')
    else:
        OUTPUT.write_text(rendered, encoding='utf-8')
    if args.package:
        verify_package(args.package.resolve(), payload)
    print('Accepted subset verified: 6 masters, 18 WebPs, 1 social raster; exploratory inputs not required.')


if __name__ == '__main__':
    main()
