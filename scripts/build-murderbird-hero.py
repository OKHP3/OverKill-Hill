"""Create proportional WebP delivery files from explicitly accepted story assets."""
import argparse
import hashlib
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets/img/library/murderbird-unified-master-candidate-03-2026-09-06.png'
EXPECTED = '538c51bcdbf5bfce95a0932fdbbb0f5868b446f4985346d15e6cacd32430e633'
PREFIX = 'murderbird-unified-master-03-2026-09-06'
SCENES = {
    'maker': (ROOT / 'assets/img/library/murderbird-unified-maker-clean-candidate-2026-09-06.png', '93966eb269ae9f8d8d00e05e913cbb23f7656204e6f3fdf7fd26e8a39ca0cbb9', 'murderbird-unified-maker-clean-2026-09-06'),
    'mechanic': (ROOT / 'assets/img/library/murderbird-unified-mechanic-candidate-2026-09-06.png', '0bd7c79510be9eeef024f8861a7576b777a7f5de5710523e8d2ab039d03c65f9', 'murderbird-unified-mechanic-2026-09-06'),
    'water': (ROOT / 'assets/img/library/murderbird-unified-water-candidate-2026-09-06.png', '0db88f0529288a9c6032662a9fb9e62d1ae077322241c4d9bd2c5a8eb915c117', 'murderbird-unified-water-2026-09-06'),
    'hero': (SOURCE, EXPECTED, PREFIX),
    'heart': (ROOT / 'assets/img/library/murderbird-unified-heart-candidate-2026-09-06.png', '9430f91e3cd3fc8223297720a0f57ec1c46e9c8245cfba91495e9c362029fea9', 'murderbird-unified-heart-2026-09-06'),
    'sentinel': (ROOT / 'assets/img/library/murderbird-unified-sentinel-candidate-2026-09-06.png', 'd6153907884045e824e3be9cd02a7a446fb75f6e8b35a246918cf11ac620667e', 'murderbird-unified-sentinel-2026-09-06'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Verify delivery dimensions and source identity without writing')
    parser.add_argument('--asset', choices=SCENES, default='hero')
    args = parser.parse_args()
    source, expected, prefix = SCENES[args.asset]
    if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
        raise SystemExit('Source identity mismatch; request renewed reference acceptance.')
    with Image.open(source) as master:
        master.load()
        widths = sorted({min(width, master.width) for width in (480, 960, 1536)})
        for width in widths:
            height = round(master.height * width / master.width)
            target = ROOT / 'assets/img/webp' / f'{prefix}-{width}.webp'
            if args.check:
                with Image.open(target) as delivered:
                    delivered.load()
                    if delivered.format != 'WEBP' or delivered.size != (width, height):
                        raise SystemExit(f'Delivery dimensions/format mismatch: {target}')
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                resized = master.resize((width, height), Image.Resampling.LANCZOS) if width != master.width else master.copy()
                resized.save(target, 'WEBP', quality=86, method=6)
            print(f'{target.relative_to(ROOT)}: {width}x{height}, {target.stat().st_size} bytes')


if __name__ == '__main__':
    main()
