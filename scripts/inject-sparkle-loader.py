#!/usr/bin/env python3
"""
inject-sparkle-loader.py  — RETIRED

This script is no longer functional and must not be re-run.

What it did:
  Injected <script src="/assets/js/sparkle-loader.js" defer></script>
  and data-sparkle-link attributes into every page with a sparkle banner.

Why it was retired (task #57, 2026-05-28):
  sparkle-loader.js no longer exists as a standalone file.
  The sparkle banner logic was merged into assets/js/app.js during the
  task-47 governance fix. Re-running this script would inject a broken
  <script> reference into all 61 pages, causing silent 404 network errors.

Current approach:
  - Banner content is controlled via assets/data/sparkle.json
  - The loader runs automatically from assets/js/app.js (already on every page)
  - To update the banner site-wide, edit assets/data/sparkle.json only

If you see this script referenced in documentation, that reference is
historical — no action is needed and this script should not be executed.
"""
import sys

print(
    "ERROR: inject-sparkle-loader.py has been retired.\n"
    "The sparkle loader is now part of assets/js/app.js — already present\n"
    "on every page. To update the banner, edit assets/data/sparkle.json.\n"
    "See script docstring for full context."
)
sys.exit(1)
