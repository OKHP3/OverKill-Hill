#!/usr/bin/env python3
"""
update-placeholder-dimensions.py
---------------------------------
Run this script after uploading real artwork for any of the four tool-ette
pages that currently carry placeholder width/height attributes.

For each entry in TARGETS the script:
  1. Checks whether the image file now exists on disk.
  2. If yes: reads its intrinsic pixel dimensions (PNG header or SVG viewport).
  3. Updates width= and height= on the matching <img> tag in the HTML page.
  4. Reports what changed (or what is still pending).

Safe to re-run at any time — only files with matching artwork are touched.
Exit code 0 always (pending artwork is not an error).
"""

import re
import struct
import sys
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).parent.parent

# (html_page, img_src_prefix, artwork_path)
TARGETS = [
    (
        ROOT / "toolbox/01-discovered-careers/01f-career-seeker/index.html",
        "/assets/img/toolbox/career-seeker-illustration.svg",
        ROOT / "assets/img/toolbox/career-seeker-illustration.svg",
    ),
    (
        ROOT / "toolbox/03-tasty-tracker/03b-menu-conductor/index.html",
        "/assets/img/tool-ettes/menu-conductor-illustration.svg",
        ROOT / "assets/img/tool-ettes/menu-conductor-illustration.svg",
    ),
    (
        ROOT / "toolbox/02-treasured-finds/02c-present-hoarder/index.html",
        "/assets/img/toolbox/02-treasured-finds/02c-present-hoarder.png",
        ROOT / "assets/img/toolbox/02-treasured-finds/02c-present-hoarder.png",
    ),
    (
        ROOT / "toolbox/04-travelers-guide/04e-memento-log/index.html",
        "/assets/img/toolbox/04-travelers-guide/04e-memento-log.png",
        ROOT / "assets/img/toolbox/04-travelers-guide/04e-memento-log.png",
    ),
]


def png_dimensions(path: Path) -> tuple[int, int]:
    """Read width, height from PNG IHDR chunk (bytes 16-24)."""
    with path.open("rb") as f:
        sig = f.read(8)
        if sig != b"\x89PNG\r\n\x1a\n":
            raise ValueError(f"Not a valid PNG: {path}")
        f.read(4)  # IHDR length
        f.read(4)  # 'IHDR'
        w, h = struct.unpack(">II", f.read(8))
    return w, h


def svg_dimensions(path: Path) -> tuple[int, int]:
    """
    Extract intrinsic width/height from SVG.
    Tries width/height attributes first, then falls back to viewBox.
    Returns integer pixel dimensions (strips 'px' suffix if present).
    """
    tree = ElementTree.parse(path)
    root = tree.getroot()
    ns = {"svg": "http://www.w3.org/2000/svg"}

    def to_int(val: str) -> int:
        return int(float(val.replace("px", "").strip()))

    w_attr = root.get("width")
    h_attr = root.get("height")
    if w_attr and h_attr:
        try:
            return to_int(w_attr), to_int(h_attr)
        except (ValueError, AttributeError):
            pass

    vb = root.get("viewBox")
    if vb:
        parts = vb.strip().split()
        if len(parts) == 4:
            return int(float(parts[2])), int(float(parts[3]))

    raise ValueError(f"Cannot determine dimensions from SVG: {path}")


def get_dimensions(artwork: Path) -> tuple[int, int]:
    suffix = artwork.suffix.lower()
    if suffix == ".png":
        return png_dimensions(artwork)
    elif suffix == ".svg":
        return svg_dimensions(artwork)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")


def update_img_dimensions(html_path: Path, src_prefix: str, w: int, h: int) -> bool:
    """
    Replace width="NNN" height="NNN" on the <img> tag whose src contains
    src_prefix. Returns True if the file was modified.
    """
    text = html_path.read_text(encoding="utf-8")

    # Find the <img … src="…src_prefix…" … > block
    # Strategy: locate the src attribute, then find the enclosing <img tag
    src_pattern = re.compile(
        r'(<img\b[^>]*?src="[^"]*' + re.escape(src_prefix) + r'[^"]*"[^>]*?>)',
        re.DOTALL,
    )
    match = src_pattern.search(text)
    if not match:
        print(f"  ⚠️  Could not find <img> with src containing '{src_prefix}' in {html_path.name}")
        return False

    old_tag = match.group(1)

    # Replace width and height attributes within the tag
    new_tag = re.sub(r'\bwidth="\d+"', f'width="{w}"', old_tag)
    new_tag = re.sub(r'\bheight="\d+"', f'height="{h}"', new_tag)

    if new_tag == old_tag:
        print(f"  ✓  {html_path.name} — dimensions already correct ({w}×{h})")
        return False

    new_text = text.replace(old_tag, new_tag, 1)
    html_path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    pending = []
    updated = []
    already_correct = []

    for html_path, src_prefix, artwork_path in TARGETS:
        label = f"{html_path.parent.name}/{html_path.name}"
        art_label = artwork_path.name

        if not artwork_path.exists():
            pending.append(art_label)
            print(f"  ⏳  {art_label} — not yet uploaded (placeholder dimensions kept)")
            continue

        try:
            w, h = get_dimensions(artwork_path)
        except Exception as e:
            print(f"  ❌  {art_label} — could not read dimensions: {e}", file=sys.stderr)
            continue

        print(f"  📐  {art_label} — intrinsic size {w}×{h}")
        changed = update_img_dimensions(html_path, src_prefix, w, h)
        if changed:
            updated.append(label)
            print(f"      → updated {label}")
        else:
            already_correct.append(label)

    print()
    print("=== Summary ===")
    print(f"  Updated:         {len(updated)} page(s)")
    print(f"  Already correct: {len(already_correct)} page(s)")
    print(f"  Pending artwork: {len(pending)} file(s)")
    if pending:
        print()
        print("  Still waiting on:")
        for name in pending:
            print(f"    - {name}")
        print()
        print("  Upload the artwork file(s) to the paths shown above, then re-run:")
        print("    python3 scripts/update-placeholder-dimensions.py")


if __name__ == "__main__":
    main()
