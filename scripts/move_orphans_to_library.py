#!/usr/bin/env python3
"""
Move every unreferenced asset under assets/img/* into assets/img/library/.
Preserves a brand media kit while removing dead weight from the deploy footprint.

Detection uses the same logic as the audit pass:
  - scans every HTML/CSS/JS/JSON/XML/TXT/MD/webmanifest file
  - collects every src/href/content/url/srcset reference
  - normalizes via URL-decoding + literal-³ comparison

Skips:
  - assets/img/library/        (already archived)
  - assets/img/favicons/       (referenced via the manifest+rels system)
  - assets/img/favicons/source/ (build artifact)

Idempotent: re-runs are no-ops once orphans are archived.
Supports --check (exits 1 if any orphans remain in the live tree).
"""
from __future__ import annotations
import re, sys, shutil
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"_replit", ".local", "attached_assets", "node_modules", "dist", ".git"}
LIBRARY = ROOT / "assets" / "img" / "library"
EXEMPT_DIRS = {LIBRARY, ROOT / "assets" / "img" / "favicons"}
SCAN_SUFFIXES = {".html", ".css", ".js", ".json", ".xml", ".txt", ".webmanifest", ".md"}
ASSET_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".ico", ".gif"}
REF_RE = re.compile(
    r'(?:src|href|content|url|srcset)\s*[=:]\s*["\']?([^"\'\s)>,]+\.'
    r'(?:png|jpg|jpeg|webp|svg|ico|gif))'
)


def collect_references() -> set[str]:
    refs: set[str] = set()
    for p in ROOT.rglob("*"):
        if not p.is_file() or p.suffix not in SCAN_SUFFIXES: continue
        if set(p.relative_to(ROOT).parts) & SKIP_DIRS: continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for m in REF_RE.finditer(text):
            raw = m.group(1).split("?")[0].split("#")[0].lstrip("/")
            refs.add(Path(raw).as_posix())
            refs.add(Path(unquote(raw)).as_posix())
    return refs


def find_orphans() -> list[Path]:
    refs = collect_references()
    orphans: list[Path] = []
    for img in (ROOT / "assets" / "img").rglob("*"):
        if not img.is_file(): continue
        if img.suffix not in ASSET_SUFFIXES: continue
        if any(parent in EXEMPT_DIRS for parent in img.parents): continue
        rel = img.relative_to(ROOT).as_posix()
        if rel not in refs:
            orphans.append(img)
    return sorted(orphans)


def main(check: bool = False) -> int:
    orphans = find_orphans()
    if not orphans:
        print("✓ no orphans in live image tree.")
        return 0

    total = sum(o.stat().st_size for o in orphans)
    print(f"  detected {len(orphans)} orphan(s), {total // 1024 // 1024} MB total.")
    if check:
        print("--check: orphans present in live tree. Re-run without --check to archive.")
        return 1

    LIBRARY.mkdir(parents=True, exist_ok=True)
    moved = 0
    for o in orphans:
        dest = LIBRARY / o.name
        # On collision, suffix with parent dirs
        if dest.exists():
            stem = "_".join(o.relative_to(ROOT / "assets" / "img").with_suffix("").parts)
            dest = LIBRARY / (stem + o.suffix)
        shutil.move(str(o), str(dest))
        moved += 1
    print(f"✓ moved {moved} orphan(s) → assets/img/library/ ({total // 1024 // 1024} MB archived)")

    # Drop a README in the library so its purpose is self-documenting
    readme = LIBRARY / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Brand image library\n\n"
            "Generated brand-image variants and unused source renders, archived from the\n"
            "live tree on 2026-05-03 by `scripts/move_orphans_to_library.py`. None of\n"
            "these files are referenced by any production page.\n\n"
            "**Disposition options:**\n\n"
            "- Keep here as a media kit (current state).\n"
            "- Exclude from deploy by adding `assets/img/library/` to your build's\n"
            "  ignore list (Cloudflare Pages: `.cfignore`; Netlify: handled by\n"
            "  `_redirects` or build settings).\n"
            "- Delete entirely: `rm -rf assets/img/library/`.\n",
            encoding="utf-8",
        )
        print(f"  ✓ wrote {readme.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(check="--check" in sys.argv))
