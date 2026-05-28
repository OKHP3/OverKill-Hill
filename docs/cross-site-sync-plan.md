# OKHP3 Universe — Cross-Site CSS/JS Sync Plan

**Date:** 2026-05-28  
**Author:** OverKill Hill P³  
**Status:** Active — Phase 1 (Audit complete; Phase 2 decisions pending)

---

## Overview

Three sites share a common `theme.css` and `app.js`:

| Site | Repo | URL |
|------|------|-----|
| OverKill Hill P³ | `OKHP3/OverKill-Hill` | overkillhill.com |
| Glee-fully Tools | `OKHP3/Glee-fullyTools` | glee-fully.tools |
| AskJamie | `OKHP3/AskJamie` | askjamie.bot |

OKH is the **source of truth**. Sync flows outward: OKH → Glee → Jamie.  
However, siblings have accrued independent additions that must be absorbed
into OKH before the next sync cycle.

The tool for running audits and building sync drops is:

```
python3 assets/scripts/cross-site-sync.py --audit
python3 assets/scripts/cross-site-sync.py --build-drop
python3 assets/scripts/cross-site-sync.py --build-drop --dry-run
```

---

## Phase 1 — Audit (Completed 2026-05-28)

### File sizes at time of audit

| File | OKH | Glee | Jamie |
|------|-----|------|-------|
| `theme.css` lines | 5,559 | 5,551 | 4,839 |
| `theme.css` bytes | 138,679 | 145,388 | 114,691 |
| `app.js` lines | 716 | 1,060 | 1,114 |
| `app.js` bytes | 28,530 | 41,036 | 45,152 |

### CSS divergences

#### Category A — OKH-only additions (siblings are behind)

These exist in OKH but not in sibling files. They will be propagated in the
next sync drop automatically once OKH is the unified superset.

| Item | Detail |
|------|--------|
| Sprint 2 semantic alias tokens | `--color-text-heading`, `--color-link`, `--color-link-hover`, `--font-mono`, `--radius-sm` |
| Spacing scale tokens | `--space-xs` through `--space-xxl` |
| Transition tokens | `--transition-fast`, `--transition-normal` |
| `.header-controls` wrapper CSS | Flex wrapper that holds search trigger + theme toggle |
| `.okh-search-trigger` light-mode overrides | Lines 200–212; keeps search button readable on dark OKH header |
| 3-state theme toggle CSS | `.theme-toggle` SVG icon states (system / light / dark) |
| Warm light-mode surface colors | `--color-surface: #f6f2ee` (warm paper) vs siblings' `#ffffff` |

#### Category B — Sibling-only additions (must be absorbed into OKH superset)

These exist only in sibling repos. OKH must absorb them before the next sync.

| Item | Source | Detail |
|------|--------|--------|
| Glee brand header variants | Glee CSS | `.glee-main` hero layering, paper effect pages |
| Glee Mermaid refined skin | Glee CSS | Supersedes earlier Glee Mermaid block |
| Glee tool-ette hub icon cards | Glee CSS | `.card--tool-ette` |
| Cross-site sync utilities block | Glee + Jamie | `/* CROSS-SITE SYNC */` block (lines ~1804 Glee, ~2212 Jamie) |
| AskJamie BFS hero section | Jamie CSS | BFS Framing Intelligent Futures hero (~111 lines) |
| AskJamie system pages | Jamie CSS | 404 + under-construction page styles (~231 lines) |
| AskJamie mid-century teal Mermaid | Jamie CSS | (~84 lines) |
| GPT Hero Card BFS variant | Jamie CSS | (~11 lines) |

#### Category C — Conflicts (human decision required before next sync)

| Item | OKH value | Sibling value | Decision needed |
|------|-----------|---------------|-----------------|
| Light-mode `--color-bg` | `#eff2f5` (warm grey) | `#f9fafb` (cool grey) | Which shade? |
| Light-mode `--color-surface` | `#f6f2ee` (warm paper) | `#ffffff` (pure white) | Which? |
| Light-mode `--color-surface-soft` | `#f0ebe5` (warm) | `#f3f4f6` (cool grey) | Which? |
| Search CSS class namespace | `okh-search-*` | `glee-search-*` / `site-search-*` | Standardise to one namespace |
| Section banner format | OKH box-drawing style | Glee / Jamie use different formats | Standardise in OKH reorg script |

---

### JS divergences

#### Category A — OKH-only additions (siblings are behind)

| Item | Detail |
|------|--------|
| 3-state theme toggle | System / Light / Dark with SVG icons; siblings have 2-state emoji or older |
| `.header-controls` wrapper injection | JS creates the wrapper div between nav and hamburger |
| `injectTrigger()` targets `.header-controls` | Siblings inject into nav or elsewhere |
| OKH search class names | `okh-search-trigger`, `okh-search-modal` |

#### Category B — Sibling-only additions (must be absorbed into OKH superset)

| Item | Source | Detail |
|------|--------|--------|
| GA4 analytics bootstrap | Jamie | `window.dataLayer`, `gtag()`, `gtag('config', 'G-MT9Y10YY0G')` — runs immediately on parse |
| `_gtag_event()` helper | Jamie | Wraps all gtag calls with a null-guard |
| GA4 search event tracking | Jamie | `search_open` / `search_submit` events |
| Self-initialising module structure | Jamie | Each feature is an IIFE that runs without DOMContentLoaded wait |
| Dedicated `/search/` page wiring | Jamie (1b) | Category chips, URL sync — more complete than OKH |

#### Category C — Conflicts (human decision required)

| Item | OKH | Sibling | Decision needed |
|------|-----|---------|-----------------|
| GA4 tracking ID | Not present | `G-MT9Y10YY0G` (Jamie only) | Does OKH want analytics? Separate file or shared? |
| Search modal class names | `okh-search-modal` | `glee-search-modal` / `site-search-modal` | Standardise namespace |
| Module init pattern | DOMContentLoaded wrapper | IIFEs (Jamie) / inline (Glee) | One pattern for all |

---

## Phase 2 — Superset Assembly (Pending)

Before the next sync drop, these decisions and edits must happen **in OKH's repo**:

### 2a. Resolve Category C conflicts (human decisions)

1. **Light-mode surface colors** — choose warm paper or cool grey, then lock in
   the `:root[data-theme="light"]` block in OKH's `theme.css`.
2. **Search CSS class namespace** — standardise to `okh-search-*` everywhere
   (recommended: OKH owns the shared pattern, siblings get brand-scoped aliases
   via their body class selectors).
3. **GA4 analytics** — options:
   - Option A: Keep analytics in a separate `analytics.js` per site (current Jamie approach, cleanest)
   - Option B: Embed in `app.js` gated by a per-page config object (`window.OKH_CONFIG.ga4Id`)
   - **Recommended: Option A** — analytics is site-specific, not a shared concern.
4. **Module init pattern** — standardise on DOMContentLoaded for DOM-dependent
   code, IIFE for self-contained utilities (search overlay can be IIFE; toggle
   stays inside DOMContentLoaded). This is closer to OKH's current structure.

### 2b. Absorb Category B items into OKH theme.css

The OKH `theme.css` already contains GLEE and ASKJAMIE sections. These
sibling-only additions need to be merged into those sections:

1. Audit each Category B block against what OKH already has in its GLEE/ASKJAMIE sections
2. Paste missing blocks into the appropriate section in OKH's `theme.css`
3. Run `python3 assets/scripts/reorg-theme-css.py --dry-run` to verify placement
4. Run `python3 assets/scripts/reorg-theme-css.py` to canonicalise order

### 2c. Absorb Category B items into OKH app.js

1. Add `_gtag_event()` helper to OKH `app.js` (guard-wrapped so it's a no-op if
   `gtag` is not loaded on that site)
2. Wire GA4 `search_open` / `search_submit` events through `_gtag_event()`
3. Do NOT embed the `gtag('config', …)` call — that stays in per-site analytics files

---

## Phase 3 — Sync Drop (Repeatable)

Once Phase 2 is complete, the sync drop is a single command:

```bash
python3 assets/scripts/cross-site-sync.py --build-drop
```

This packages `theme.css`, `app.js`, and `mermaid-init.js` from OKH into a zip
with per-repo subdirectory structure. Commit the per-repo subdirectory contents
to each sibling repo with:

```
chore(sync): align foundation files with overkillhill.com canonical (YYYY-MM-DD)
```

---

## Phase 4 — Ongoing Governance

### Edit workflow (all future changes)

1. Edit `theme.css` / `app.js` in OKH
2. Run `python3 assets/scripts/cross-site-sync.py --audit` to verify no new drift
3. Run `python3 assets/scripts/cross-site-sync.py --build-drop` to create sync zip
4. Commit sibling repos

### Audit cadence

Run `--audit` before every non-trivial PR. The script exits non-zero if it
detects known-dangerous drift (e.g., siblings missing Sprint-level tokens).

### What the audit script checks

| Check | Pass condition |
|-------|---------------|
| Sprint tokens present in OKH | All 6 tokens found |
| Sibling CSS byte size within ±20% of OKH | Files not severely truncated |
| Sibling JS byte size within ±50% of OKH | Accounts for legitimate size differences |
| 3-state toggle present in OKH JS | `"system", "light", "dark"` found |
| `.header-controls` present in OKH CSS | Selector found |
| Search trigger overrides in OKH CSS | `.okh-search-trigger` light-mode rules found |

---

## Open Questions

- [ ] **Light-mode surface warmth** — warm paper or cool grey? (affects all body content, not just header)
- [ ] **GA4 on OKH** — does overkillhill.com want analytics? If yes, what tracking ID?
- [ ] **Search namespace** — standardise across all three, or accept per-brand class names in CSS/JS?
- [ ] **mermaid-init.js** — not audited in this plan; add to Phase 1 next cycle

---

*Tool:* `assets/scripts/cross-site-sync.py`  
*Audit last run:* 2026-05-28  
*Next scheduled sync drop:* After Phase 2 decisions resolved
