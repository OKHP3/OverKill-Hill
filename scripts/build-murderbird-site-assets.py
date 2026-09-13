"""Build proportional delivery copies of the owner's final site-lineage revisions."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SELECTION = {
    'legal-guardian': 'murderbird-v2-legal-guardian-square-1254-2026-09-08.png',
    'contact-warning': 'murderbird-v2-contact-warning-revision-02-square-1254-2026-09-08.png',
    'under-construction': 'murderbird-v2-under-construction-revision-02-wide-1536-2026-09-08.png',
    '404-reassembly': 'murderbird-v2-404-reassembly-revision-04-wide-1536-2026-09-08.png',
}

def build():
    for role, name in SELECTION.items():
        with Image.open(ROOT / 'assets/murderbird/production/images' / name) as source:
            if role in ('legal-guardian', 'contact-warning'):
                assert source.mode == 'RGBA' and source.getextrema()[3] == (0, 255)
            for width in (480, 960):
                image = source.resize((width, round(source.height * width / source.width)), Image.Resampling.LANCZOS)
                image.save(ROOT / f'assets/img/webp/murderbird-v2-{role}-{width}.webp', quality=85, method=6)
            # Real PNG fallback, same 960px size/aspect ratio, no crop or upscaling.
            image.save(ROOT / f'assets/img/murderbird-v2-{role}-960.png', optimize=True)

if __name__ == '__main__':
    build()
