#!/usr/bin/env python3
"""
audit-assets.py — Asset inventory + icon-map generator
=======================================================
Walks `assets/img/` and cross-references every file against every HTML page
to determine which images are referenced and which are orphaned.

Outputs:
  assets/audit/asset-inventory-2026-05-03.json    (full inventory)
  assets/data/icon-map.json                 (best-icon mapping per tool)

Usage:
    python3 scripts/audit-assets.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"node_modules", ".local", ".git", "attached_assets"}
IMG_DIR = ROOT / "assets" / "img"

ICON_RE = re.compile(
    r"^Glee-fullyTools-GPTIcon-"
    r"(?P<prefix>0[0-7][a-z]?|0[0-7])"
    r"-(?P<name>.+?)"
    r"-Background-(?P<bg>RetroStripe|Transparent)"
    r"-Square-1024(?P<alt>-alt)?\.png$"
)


def gather_html_text() -> dict[Path, str]:
    pages = {}
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if any(s in rel.parts for s in SKIP_DIRS):
            continue
        pages[rel] = path.read_text(encoding="utf-8", errors="replace")
    return pages


def main() -> int:
    if not IMG_DIR.exists():
        print(f"!! No {IMG_DIR}", file=sys.stderr)
        return 1

    pages_text = gather_html_text()

    # --- Build inventory ---------------------------------------------------
    inventory = []
    for path in sorted(IMG_DIR.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        name = path.name
        ref_pages = sorted([
            p.as_posix() for p, text in pages_text.items() if name in text
        ])
        cls = "favicon" if rel.parts[2:3] == ("favicons",) else (
            "gpt-icon" if name.startswith("Glee-fullyTools-GPTIcon-") else (
                "butterfly" if "Butterfly" in name else "other"))
        inventory.append({
            "path": rel.as_posix(),
            "name": name,
            "size_bytes": path.stat().st_size,
            "class": cls,
            "referenced": bool(ref_pages),
            "ref_count": len(ref_pages),
            "referenced_by": ref_pages,
        })

    # --- Build icon-map ----------------------------------------------------
    by_prefix: dict[str, dict] = defaultdict(lambda: {
        "retro_stripe": None,
        "retro_stripe_alt": None,
        "transparent": None,
        "transparent_alt": None,
    })
    for asset in inventory:
        if asset["class"] != "gpt-icon":
            continue
        m = ICON_RE.match(asset["name"])
        if not m:
            continue
        prefix = m.group("prefix")
        slot = ("retro_stripe" if m.group("bg") == "RetroStripe" else "transparent")
        if m.group("alt"):
            slot += "_alt"
        by_prefix[prefix][slot] = asset["path"]

    icon_map = {prefix: {**files,
                        "primary": files["retro_stripe"] or files["transparent"]}
                for prefix, files in sorted(by_prefix.items())}

    # --- Persist -----------------------------------------------------------
    audit_dir = ROOT / "assets" / "audit"
    audit_dir.mkdir(exist_ok=True)
    inv_path = audit_dir / "asset-inventory-2026-05-03.json"
    inv_path.write_text(json.dumps({
        "generated": "2026-05-03",
        "image_root": "assets/img/",
        "total_files": len(inventory),
        "total_referenced": sum(1 for a in inventory if a["referenced"]),
        "total_orphaned": sum(1 for a in inventory if not a["referenced"]),
        "assets": inventory,
    }, indent=2), encoding="utf-8")

    map_path = ROOT / "assets" / "data" / "icon-map.json"
    map_path.parent.mkdir(parents=True, exist_ok=True)
    map_path.write_text(json.dumps({
        "generated": "2026-05-03",
        "doc": "Best GPT icon for each tool/branch prefix. "
               "'primary' is the recommended hero/og:image. "
               "Variants exist for design flexibility.",
        "tools": icon_map,
    }, indent=2), encoding="utf-8")

    print(f"Image files:        {len(inventory)}")
    print(f"  referenced:       {sum(1 for a in inventory if a['referenced'])}")
    print(f"  orphaned:         {sum(1 for a in inventory if not a['referenced'])}")
    print(f"GPT icon prefixes:  {len(icon_map)}")
    print(f"")
    print(f"Wrote:")
    print(f"  {inv_path.relative_to(ROOT)}")
    print(f"  {map_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
