#!/usr/bin/env python3
"""
activate-icons.py — Surface the per-tool / per-branch GPT icons
================================================================
The repo carries 48 purpose-built GPT icon PNGs that never reach
any rendered page.  Every tool-ette and branch-hub currently shows
a generic butterfly hero plus a butterfly Open-Graph image.

This script:
  1. Maps each tool-ette / branch folder to its GPT icon by scanning
     assets/img/Glee-fullyTools-GPTIcon-{prefix}-*-Background-
     RetroStripe-Square-1024.png.
  2. Rewrites og:image and twitter:image to that icon (with a matching
     og:image:width/height/type and og:image:alt).
  3. Replaces the hero <img> URL in the .hero-visual block (whichever
     ButterflyLoop variant is sitting there) with the same icon.

Idempotent: pages already pointing at their own GPT icon are left alone.

Usage:
    python3 scripts/activate-icons.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "assets" / "img"
SITE = "https://glee-fully.tools"

BUTTERFLY_HERO_PATTERNS = [
    "ButterflyWaiting",
    "ButterflyLoopLeft",
    "ButterflyLoopRight",
    "ButterflyHoverLeft",
    "ButterflyHoverRight",
    "ButterflyPathLeft",
    "ButterflyPathRight",
]


def find_icon(prefix: str) -> Path | None:
    """Find the matching RetroStripe-Square-1024 icon for a folder prefix.
    Prefer the non-'-alt' variant when both exist."""
    pat = re.compile(rf"^Glee-fullyTools-GPTIcon-{re.escape(prefix)}-.*-Background-RetroStripe-Square-1024(-alt)?\.png$")
    matches = sorted(p for p in IMG_DIR.iterdir() if pat.match(p.name))
    if not matches:
        return None
    # Prefer the non-alt variant
    for m in matches:
        if "-alt." not in m.name:
            return m
    return matches[0]


def encoded_url(asset_path: Path) -> str:
    """Return the absolute https URL with proper percent-encoding."""
    rel = asset_path.relative_to(ROOT).as_posix()
    return f"{SITE}/" + quote(rel, safe="/")


def encoded_path(asset_path: Path) -> str:
    """Return root-absolute path with percent-encoding (for <img src>)."""
    rel = asset_path.relative_to(ROOT).as_posix()
    return "/" + quote(rel, safe="/")


def derive_alt(prefix: str, icon_path: Path) -> str:
    """Friendly alt text for the icon."""
    # Strip 'Glee-fullyTools-GPTIcon-{prefix}-' prefix and trailing suffix
    stem = icon_path.stem
    name = re.sub(rf"^Glee-fullyTools-GPTIcon-{re.escape(prefix)}-", "", stem)
    name = re.sub(r"-Background-RetroStripe-Square-1024(-alt)?$", "", name)
    name = re.sub(r"\s+", " ", name.replace("-", " ")).strip()
    return f"Glee-fully {name} — GPT icon"


def page_prefix(rel: Path) -> str | None:
    """For toolbox/0N-branch/0Nx-tool/index.html  → '0Nx'.
       For toolbox/0N-branch/index.html           → '0N'.
       Otherwise None."""
    parts = rel.parts
    if len(parts) >= 4 and parts[0] == "toolbox" and re.match(r"^\d+[a-z]-", parts[2]):
        return parts[2].split("-", 1)[0]   # '01a'
    if len(parts) == 3 and parts[0] == "toolbox" and re.match(r"^\d+-", parts[1]):
        return parts[1].split("-", 1)[0]   # '01'
    return None


def update_meta(html: str, prop_attr: str, prop_value: str, content: str) -> tuple[str, bool]:
    """Replace an existing <meta {prop_attr}="{prop_value}" content="…"> if it
    exists, leave alone otherwise.  Returns (new_html, changed)."""
    pat = re.compile(
        rf'(<meta\s+{prop_attr}="{re.escape(prop_value)}"\s+content=")[^"]*(")',
        re.IGNORECASE,
    )
    new = pat.sub(lambda m: m.group(1) + content + m.group(2), html, count=1)
    return new, new != html


def update_meta_with_alt(html: str, prop_attr: str, image_value: str, alt_value: str,
                          width: int = 1024, height: int = 1024) -> str:
    html, _ = update_meta(html, prop_attr, "og:image", image_value)
    html, _ = update_meta(html, prop_attr, "og:image:alt", alt_value)
    html, _ = update_meta(html, prop_attr, "og:image:width", str(width))
    html, _ = update_meta(html, prop_attr, "og:image:height", str(height))
    html, _ = update_meta(html, prop_attr, "og:image:type", "image/png")
    return html


def replace_hero_img(html: str, icon_root_url: str, alt: str) -> tuple[str, bool]:
    """Find the .hero-visual <img> and rewrite its src + alt + dims.
    The hero-visual block currently uses a butterfly Wide 1536 PNG."""
    # Match the <div class="hero-visual"...>...<img src="...butterfly...">...</div>
    rgx = re.compile(
        r'(<div\s+class="hero-visual[^"]*"[^>]*>\s*'
        r'(?:<!--[^>]*-->\s*)*'
        r'<img\s+)src="[^"]*(?:Butterfly[A-Za-z]*|butterfly)[^"]*"'
        r'(\s+alt=")[^"]*(")'
        r'([^>]*?)(\s*/?>)',
        re.IGNORECASE | re.DOTALL,
    )

    def sub(m):
        prefix = m.group(1)
        alt_open, alt_close = m.group(2), m.group(3)
        rest = m.group(4)
        end = m.group(5)
        # Strip any old width/height; we'll set 1024×1024 for the square icon
        rest = re.sub(r'\s+width="\d+"', "", rest)
        rest = re.sub(r'\s+height="\d+"', "", rest)
        rest = re.sub(r'\s+loading="[^"]*"', "", rest)
        rest = re.sub(r'\s+decoding="[^"]*"', "", rest)
        return (f'{prefix}src="{icon_root_url}"'
                f'{alt_open}{alt}{alt_close}'
                f'{rest} width="1024" height="1024"'
                f' loading="lazy" decoding="async"{end}')

    new = rgx.sub(sub, html, count=1)
    return new, new != html


def process(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    prefix = page_prefix(rel)
    if not prefix:
        return False
    icon = find_icon(prefix)
    if not icon:
        print(f"  ? no icon found for prefix '{prefix}' — skipped {rel}")
        return False
    abs_url = encoded_url(icon)
    root_url = encoded_path(icon)
    alt = derive_alt(prefix, icon)

    html = path.read_text(encoding="utf-8", errors="replace")

    # Idempotence: page already references its own icon → nothing to do
    if abs_url in html and root_url in html:
        return False

    original = html
    # Update OG/Twitter image meta tags
    html, _ = update_meta(html, "property", "og:image", abs_url)
    html, _ = update_meta(html, "property", "og:image:alt", alt)
    html, _ = update_meta(html, "property", "og:image:width", "1024")
    html, _ = update_meta(html, "property", "og:image:height", "1024")
    html, _ = update_meta(html, "property", "og:image:type", "image/png")
    html, _ = update_meta(html, "name", "twitter:image", abs_url)
    html, _ = update_meta(html, "name", "twitter:image:alt", alt)

    # Swap hero-visual <img>
    html, _ = replace_hero_img(html, root_url, alt)

    if html != original:
        path.write_text(html, encoding="utf-8")
        print(f"  + {rel}  →  {icon.name}")
        return True
    return False


def main() -> int:
    edited = 0
    for path in sorted(ROOT.rglob("index.html")):
        rel = path.relative_to(ROOT)
        if any(s in rel.parts for s in {"node_modules", ".local", ".git", "attached_assets"}):
            continue
        if process(path):
            edited += 1
    print(f"\nDone. Activated icons on {edited} page(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
