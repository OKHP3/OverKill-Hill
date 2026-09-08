#!/usr/bin/env python3
"""Build the lossless ETCH-AI-SKETCH delivery derivative; retain the PNG master."""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/img/etch-ai-sketch-using-a-council-to-design-at-velocity.png"
OUTPUT = ROOT / "assets/img/webp/etch-ai-sketch-using-a-council-to-design-at-velocity-lossless.webp"


def main():
    with Image.open(SOURCE) as image:
        source = image.convert("RGBA")
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        source.save(OUTPUT, "WEBP", lossless=True, exact=True, method=6)
    with Image.open(OUTPUT) as image:
        assert image.size == source.size, "Derivative dimensions changed"
        assert image.convert("RGBA").tobytes() == source.tobytes(), "Derivative pixels changed"
    assert OUTPUT.stat().st_size < SOURCE.stat().st_size, "Derivative is not smaller"
    print(f"Lossless RGBA parity: {source.width}x{source.height}; "
          f"{SOURCE.stat().st_size} -> {OUTPUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
