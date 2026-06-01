#!/usr/bin/env python3
"""
fix-image-performance.py — idempotent image-performance fixer (Task #8)

Fixes two categories of image-performance issue found in the 2026-05-26 audit:

  1. Construction-overlay image loading priority
     The TitleUpperLeftButterflyMultipleUnderConstruction image sits inside a
     position:fixed overlay shown above-the-fold to first-time visitors, but was
     marked loading="lazy".  This script changes it to loading="eager" so the
     browser preload scanner treats it with normal priority.
     Marker: <!-- AUTOGEN:IMG-PERF-OVERLAY-EAGER -->

  2. Missing width/height attributes (CLS prevention)
     Twelve images across branch-hub and tool-ette pages lacked intrinsic
     width/height, preventing the browser from reserving layout space before the
     images load.  This script injects the correct attributes.
     Marker: <!-- AUTOGEN:IMG-PERF-DIMENSIONS -->

Run order: safe to run at any time; idempotent (skip-if-already-present guards).
"""

import os
import re
import sys

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def walk_html(root="."):
    """Yield every .html path under root, skipping non-page trees."""
    skip_prefixes = (
        os.path.join(root, "assets"),
        os.path.join(root, "."),
        os.path.join(root, "node_modules"),
    )
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if not d.startswith(".")
            and os.path.join(dirpath, d) not in skip_prefixes
            and not os.path.join(dirpath, d).startswith(tuple(skip_prefixes))
        ]
        for fn in filenames:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


# ---------------------------------------------------------------------------
# Fix 1: Construction-overlay image lazy → eager
# ---------------------------------------------------------------------------

OVERLAY_AUTOGEN = "<!-- AUTOGEN:IMG-PERF-OVERLAY-EAGER -->"
OVERLAY_IMG_SRC = "TitleUpperLeftButterflyMultipleUnderConstruction"

def fix_overlay_loading(path, content):
    """
    Within the construction-overlay img tag, replace loading="lazy" with
    loading="eager".  Idempotent: skips if already eager or marker present.
    """
    if OVERLAY_AUTOGEN in content:
        return content, False  # already processed

    if OVERLAY_IMG_SRC not in content:
        return content, False  # page has no construction overlay

    # Find the img tag containing the overlay src and patch loading attribute.
    # The tag spans multiple lines, so we use a DOTALL match bounded by the
    # class="construction-overlay__image" which is unique on these pages.
    pattern = re.compile(
        r'(<img\b[^>]*class="construction-overlay__image"[^>]*?)loading="lazy"([^>]*/>)',
        re.DOTALL,
    )
    new_content, n = pattern.subn(
        lambda m: m.group(1) + 'loading="eager"' + m.group(2),
        content,
    )
    if n == 0:
        # Tag might have attributes in a different order — try the src pattern
        pattern2 = re.compile(
            r'(<img\b[^>]*' + re.escape(OVERLAY_IMG_SRC) + r'[^>]*?)loading="lazy"([^>]*/>)',
            re.DOTALL,
        )
        new_content, n = pattern2.subn(
            lambda m: m.group(1) + 'loading="eager"' + m.group(2),
            content,
        )

    if n == 0:
        return content, False  # loading="lazy" not present — already eager or not set

    # Inject autogen marker just before the closing </body> tag so we never
    # re-process this file.
    new_content = new_content.replace(
        "</body>",
        f"{OVERLAY_AUTOGEN}\n</body>",
        1,
    )
    return new_content, True


# ---------------------------------------------------------------------------
# Fix 2: Missing width/height on specific images
# ---------------------------------------------------------------------------

DIM_AUTOGEN = "<!-- AUTOGEN:IMG-PERF-DIMENSIONS -->"

# Map of src fragment → (width, height) to inject.
# Actual PNG dimensions confirmed from file headers.
# SVG placeholder dimensions chosen to match typical illustration aspect ratios
# (3:2) so the browser can reserve proportionally-correct space.
IMAGE_DIMENSIONS = {
    # Branch-hub hero images (PNG 1536×1024 confirmed)
    "ButterflyLoopLeft%20Wide%201536.png": (1536, 1024),
    # Tool-ette illustrations (files are placeholders; dimensions are layout hints)
    "career-seeker-illustration.svg": (800, 534),
    "menu-conductor-illustration.svg": (800, 534),
    "02c-present-hoarder.png": (1200, 800),
    "04e-memento-log.png": (1200, 800),
}


def _inject_dimensions(img_tag, width, height):
    """
    Return img_tag with width and height attributes added.
    Inserts before the closing /> or >.
    """
    # Already has both — skip
    if 'width=' in img_tag and 'height=' in img_tag:
        return img_tag, False

    attrs = ""
    if 'width=' not in img_tag:
        attrs += f' width="{width}"'
    if 'height=' not in img_tag:
        attrs += f' height="{height}"'

    # Insert before the self-closing /> or bare >
    patched = re.sub(r'\s*(/?>)\s*$', attrs + r' \1', img_tag.rstrip(), count=1)
    return patched, True


def fix_missing_dimensions(path, content):
    """
    For each known image fragment in IMAGE_DIMENSIONS, find its <img> tag and
    add missing width/height attributes.  Idempotent via autogen marker.
    """
    if DIM_AUTOGEN in content:
        return content, 0  # already processed

    changed = 0
    for src_fragment, (w, h) in IMAGE_DIMENSIONS.items():
        if src_fragment not in content:
            continue

        # Match the complete multi-line <img … /> block containing this src fragment.
        # We capture from <img up to the nearest closing /> or >.
        def replacer(m):
            nonlocal changed
            tag = m.group(0)
            patched, did_change = _inject_dimensions(tag, w, h)
            if did_change:
                changed += 1
            return patched

        pattern = re.compile(
            r'<img\b[^>]*' + re.escape(src_fragment) + r'[^>]*/?>',
            re.DOTALL,
        )
        content = pattern.sub(replacer, content)

    if changed:
        content = content.replace(
            "</body>",
            f"{DIM_AUTOGEN}\n</body>",
            1,
        )

    return content, changed


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    overlay_fixed = 0
    dim_fixed = 0
    files_touched = 0

    for html_path in sorted(walk_html(root)):
        content = read(html_path)
        original = content

        content, overlay_changed = fix_overlay_loading(html_path, content)
        content, dims_changed = fix_missing_dimensions(html_path, content)

        if overlay_changed:
            overlay_fixed += 1
        if dims_changed:
            dim_fixed += dims_changed

        if content != original:
            write(html_path, content)
            rel = os.path.relpath(html_path, root)
            tag = []
            if overlay_changed:
                tag.append("overlay→eager")
            if dims_changed:
                tag.append(f"+{dims_changed} dim(s)")
            print(f"  fixed  {rel}  [{', '.join(tag)}]")
            files_touched += 1

    print(f"\nDone. {files_touched} file(s) touched.")
    print(f"  Construction overlay lazy→eager: {overlay_fixed} page(s)")
    print(f"  Width/height dimensions added:   {dim_fixed} img(s) across pages")


if __name__ == "__main__":
    main()
