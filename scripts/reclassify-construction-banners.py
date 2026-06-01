#!/usr/bin/env python3
"""Reclassify construction banners on branch pages.

Decision rule:
  COMPLETE content (full copy, all Tool-ette links live) → replace heavy
    construction-overlay div with slim inline construction-badge--slim.
  INCOMPLETE content (href="#" placeholders or stub sections) → keep overlay.
  NO overlay → skip.

2026-05-27 status:
  01-discovered-careers  → SLIM  (all 6 tool-ettes have real GPT links)
  02-treasured-finds     → SLIM  (all 7 tool-ettes have real GPT links, 02c fixed)
  03-tasty-tracker       → SLIM  (all 5 tool-ettes have real GPT links)
  04-travelers-guide     → SLIM  (all 5 tool-ettes have real GPT links, 04d+04e fixed)
  05-organized-life      → SKIP  (no overlay present)
  06-healthy-bee-ing     → SLIM  (all 6 tool-ettes now have real GPT links — Task #6)
  07-identity-known      → SLIM  (all 7 tool-ettes have real ChatGPT URLs)
"""
from pathlib import Path
import re

ROOT = Path(__file__).parent.parent

SLIM_BRANCHES = [
    "toolbox/01-discovered-careers/index.html",
    "toolbox/02-treasured-finds/index.html",
    "toolbox/03-tasty-tracker/index.html",
    "toolbox/04-travelers-guide/index.html",
    "toolbox/06-healthy-bee-ing/index.html",
    "toolbox/07-identity-known/index.html",
]

SLIM_MARKER_START = "<!-- AUTOGEN:CONSTRUCTION-SLIM -->"
SLIM_MARKER_END   = "<!-- /AUTOGEN:CONSTRUCTION-SLIM -->"

SLIM_BADGE_TEMPLATE = """{start}
    <div class="construction-badge--slim" role="status" aria-label="Page status: pre-opening">
      <span class="construction-badge--slim__icon" aria-hidden="true">🌱</span>
      <strong>Pre-opening flutter</strong> — this branch is almost ready.
      A few finishing touches are in progress; all links are live.
    </div>
{end}""".format(start=SLIM_MARKER_START, end=SLIM_MARKER_END)

# Pattern to match the full construction-overlay block (multiline)
OVERLAY_PATTERN = re.compile(
    r'\s*<!-- 🔧 Glee.*?under construction gate -->\s*',
    re.DOTALL
)

changed = 0
skipped = 0

for rel_path in SLIM_BRANCHES:
    path = ROOT / rel_path
    if not path.exists():
        print(f"  MISSING: {rel_path}")
        continue

    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")

    # Already converted
    if SLIM_MARKER_START in text:
        print(f"  SKIP (already slim): {rel_path}")
        skipped += 1
        continue

    # No overlay to replace
    if "construction-overlay" not in text:
        print(f"  SKIP (no overlay): {rel_path}")
        skipped += 1
        continue

    # Replace the full overlay block including surrounding comments
    # The block starts with "<!-- 🔧 Glee‑fully..." and ends with "<!-- 🔧 end under-construction gate -->"
    start_marker = "<!-- 🔧 Glee"
    end_marker = "<!-- 🔧 end under"

    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print(f"  WARN: could not locate overlay block in {rel_path}")
        continue

    # end_idx points to start of closing comment, extend past it
    end_of_block = text.find("-->", end_idx) + 3
    # Consume trailing newline
    if end_of_block < len(text) and text[end_of_block] == "\n":
        end_of_block += 1

    text = text[:start_idx] + SLIM_BADGE_TEMPLATE + "\n" + text[end_of_block:]
    path.write_bytes(text.encode("utf-8"))
    print(f"  SLIMMED: {rel_path}")
    changed += 1

print(f"\nDone. {changed} branch(es) converted to slim badge, {skipped} skipped.")
