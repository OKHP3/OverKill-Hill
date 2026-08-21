---
name: Playwright system libraries
description: Local Chromium runtime requirements for browser QA in this Replit project.
---

The cached Playwright Chromium binary does not start in the base development
runtime unless the Nix environment includes `libgbm` and `cups`.

**Why:** The Playwright package and browser cache can both be present while
Chromium still exits before creating a page when these shared libraries are
not exposed.

**How to apply:** Keep `libgbm` and `cups` in the project Nix package list and
restart the application workflow after changing that list before running
browser QA.