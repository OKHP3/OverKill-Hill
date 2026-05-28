# OverKill Hill P³™ — overkillhill.com

## Project Overview

Static portfolio/documentation site for OverKill Hill P³™ (overkillhill.com). Built with HTML, CSS, and vanilla JS. Coordinated with GitHub repo `OKHP3/OverKill-Hill` (website source) and `OKHP3/first-diagram-is-a-liar` (methodology archive).

## Server

Python simple HTTP server via `server.py` — serves the static site from root.

**Workflow:** `Start application` → `python3 server.py`

## Architecture

- Root `/` — home page, site-wide assets
- `/assets/css/theme.css` — single global stylesheet (dark theme + OKH design tokens). **Organized in 4 sections in this order: GLOBAL → OKH → GLEE → ASKJAMIE.** See "CSS file structure" below.
- `/assets/js/app.js` — vanilla JS, sectioned `1. progress bar · 2. nav/year/theme/scroll-reveal/anchors · 3. GLEE construction overlay · 4. sticky TOC`
- `/assets/img/` — favicons, logos, OG images
- `/writings/` — article pages
- `/projects/` — project pages (`mermaid-theme-builder/`, `bpmn-for-mermaid/`)
- `/universe/`, `/manifesto/`, `/about/`, `/contact/`, `/legal/` — brand pages
- `/_replit/` — non-served dev tooling. **Not** part of the static site; the deployment `publicDir = "."` setting still serves it as files but it has no inbound links.
  - `_replit/mermaid-theme-builder-preview/` — **dev preview app only** (React + Vite + Tailwind v4). Used for local prototyping of the MTB project page layout; migrated 2026-05-03 from the retired `Project-Page-Mermaid-Theme-Tool` Repl. Standalone — not in a pnpm workspace. Run with `cd _replit/mermaid-theme-builder-preview && npm install && PORT=5173 BASE_PATH=/ npm run dev`. Build verified working (vite 6). **The React app's build output is never deployed** — the live project page is the static HTML at `projects/mermaid-theme-builder/index.html`.

## Key CSS Design Tokens (theme.css)

- `--okh-orange` — primary brand accent (#c46a2c or similar)
- `--okh-amber` — secondary accent (lighter warm tone)
- `--color-surface` — card/widget backgrounds
- `--color-border-subtle` — borders
- `--color-muted` — body/secondary text
- `--color-fg` — primary text
- `--radius-md` — card border-radius

**CSS cache-bust:** Currently at `?v=15`

## CSS file structure (theme.css)

`assets/css/theme.css` is **organized in 4 banner-separated sections in canonical order**:

1. **GLOBAL** — tokens, reset, base, shared utilities + components used by all 3 sites
2. **OVERKILL HILL** — site-specific (default brand). Scoped via `body:not(.glee-main):not(.askjamie-main)` OR uses OKH-only component classes (`.article-*`, `.heat-*`, `.diagram-*`, `.bfs-hero`, `.gpt-hero`, `.brand-stripes--okh`, etc.)
3. **GLEE-FULLY** — `.glee-main`-scoped overrides + `--glee` BEM modifiers
4. **ASKJAMIE** — `.askjamie-main`-scoped overrides + `--jamie` BEM modifiers

**Maintenance:** edit rules wherever you want, then run

```
python3 assets/scripts/reorg-theme-css.py             # in-place reorg
python3 assets/scripts/reorg-theme-css.py --dry-run   # report classifier output + flag GLOBAL blocks containing brand tokens
```

The reorg script tokenizes every top-level rule, classifies it by selector, and re-emits in canonical order. Within-brand source order is **always preserved** so cascade winners for same-selector duplicates stay intact. Brace balance is verified after every run.

After running the reorg, copy `assets/css/theme.css` and `assets/js/app.js` to the sibling sync drops (see "Cross-Site Foundation Files" below).

## Current Feature: Article — The First Diagram Is Usually a Liar

Path: `/writings/first-diagram-is-a-liar/`

**Version:** v0.5 — The Council Scores the Field (2026-05-24)

### Article Sections
- `#visual-edition` — v0.3 Visual Edition overview (deck framing, scoring bracket, what v0.3 adds)
- `#poll-schedule` — 9-row poll schedule table (Apr 21 through v0.4)
- `#scoring-model` — 3-lane scoring grid (Audience / Architect / Council)
- `#pivot` — From Drawing to Modeling (intro)
- `#roy` — ROY: Return on Your Words
- `#what-mermaid-actually-is` — What a Mermaid diagram actually is
- `#mermaid-syntax-vs-platform` — Mermaid vs Mermaid.ai distinction
- `#one-that-should-have-won` — Mermaid.ai premature rendering analysis
- `#council-origin` — v0.4: Why I Built a Council of AIs (added Task #15)
- `#council` — Council of AIs (scorecard table + roles)
- `#why-one-model` — Why One Model Is Not Enough ← NEW in v0.4
- `#crude-manual-process` — The Crude Manual Process (fan out / compare / adjudicate / synthesize) ← NEW in v0.4
- `#co-opetition` — Co-opetition and What the Platforms Are Now Building ← NEW in v0.4
- `#council-seats` — Why Each Seat Existed ← NEW in v0.4
- `#council-synthesis` — What the Council Produced That a Single Model Could Not ← NEW in v0.4
- `#round1` — Round 1: Copilot
- `#round2` — Round 2: Claude
- `#prompts` — Prompts in the Wild
- `#v1-diagrams` — V1 First-Pass diagram gallery (7 cards, confirmed Mermaid.ai links)
- `#v2-diagrams` — V2 Revised diagram gallery (8 cards, confirmed Mermaid.ai links)
- `#v03-deck` — Download deck (Square + Wide, PDF + PPTX)
- `#v03-field-guide` — Heat guide cards (links to 4 static heat guide pages)
- `#council-scoring` — The Council Scores the Field ← NEW in v0.5
- `#model-interviews` — The Models Interview Themselves ← NEW in v0.5
- `#artifacts` — Launch Artifacts (LinkedIn artifact cards)
- `#thesis` — Thesis

### v0.3 Heat Guide Pages
- `/writings/first-diagram-is-a-liar/v03/v1-heat-a/` — ChatGPT, Claude, Gemini, Perplexity (V1)
- `/writings/first-diagram-is-a-liar/v03/v1-heat-b/` — Copilot, Notion, Replit (V1)
- `/writings/first-diagram-is-a-liar/v03/v2-heat-a/` — ChatGPT, Copilot, Gemini, Notion (V2)
- `/writings/first-diagram-is-a-liar/v03/v2-heat-b/` — ChatGPT Pro, Claude, Replit, Perplexity (V2)

All 15 confirmed Mermaid.ai diagram links are real (no placeholders). Poll URLs are TODO placeholders (not yet published on LinkedIn). v0.4 added ~700 words of new prose across 5 sections; v0.5 adds #council-scoring and #model-interviews. Search index is at 58 entries.

### Sidebar Widgets
1. About This Article (series badge)
2. The Repository (GitHub links)
3. Council Snapshot (scorecard table)
4. The Diagrams (15 Mermaid links)
5. v0.3 Field Guides (4 heat page links) ← NEW in v0.3
6. On This Page (TOC)

## Site-Wide Banner
All 19 non-article pages + the article page itself have a site-wide "HOT OFF THE FORGE" banner.
- **Non-article pages (19):** Link to `/writings/first-diagram-is-a-liar/#council-scoring`, text: "v0.5 is live: the Council of AIs scored each other — every model was harder on itself than the architect was. Read it →" (updated Task #28)
- **Article page:** Links to `#council-scoring`, text: "v0.5 is live: the Council of AIs scored each other — every model was harder on itself than the architect was. Read it →"

## Mermaid Theme Builder Project Page

Path: `/projects/mermaid-theme-builder/`

**Current version:** v0.5.0 — shipped May 2026. Active sprint: v0.5.x SKILL.md Hardening.

**Live tool:** `okhp3.github.io/mermaid-theme-builder/` — browser-only, no login, MIT licensed.

### Page Sections

| Section ID | Heading | Notes |
|---|---|---|
| `#embed-tool` | *(embedded iframe)* | Live tool iframe at top of page; reload button included |
| `#release` | Current Release | v0.5.0 metadata card — version, active sprint, license, runtime, live tool link, source link |
| `#what-it-is` | A governance workbench, not a diagram editor | Is/Is-Not grid — two-column comparison of what the tool is and isn't |
| `#why-this-exists` | What you get here that you don't get from prompting an LLM | Why-grid — LLM prompting vs. MTB side-by-side |
| `#since-v03` | What changed between v0.3 and v0.5 | 7 change cards: Renderer Intelligence, Look API Support, Reference Capability Registry, SKILL.md Agent Packaging, Multi-Diagram Splitting, Shareable URL State, Vitest 4 Test Suite |
| `#features` | What the builder does | Feature card grid — 16 cards covering all major capabilities |
| `#roadmap` | Where the build is going | Progress track — 10 entries: V0.1–V0.4 Shipped ✓, v0.5.0 Shipped ✓, v0.5.x SKILL.md Hardening ▶ (active), v0.6.x Native Capability + Ko-fi Artifacts, v0.7.x Session Persistence + Multi-Diagram Canvas, v0.8.x Collaboration + Governance Hardening, v1.0 Production Release (planned) |
| *(no ID — collapsibles block)* | User Guide / Palette Reference / FAQ | Three collapsible `<details>` sections: 6-step User Guide, 21-row Palette Reference variable table, FAQ with 11 Q&A pairs |
| *(no ID — builder's note + dev update)* | *(closing)* | Builder's Note blockquote, Development Update (May 2026), BPMN for Mermaid sibling link, builder sign-off |

### Sidebar Widgets

1. **Start Now** — CTA button linking to the live GitHub Pages tool
2. **Project Info** — meta card: Status, Build Phase, License, Type, Cost, Maintained by, Mermaid.js compat (v11.15.0); GitHub links (View, Issues, Contribute)
3. **Related Resources** — live app (Compose tab), GitHub repo, BPMN for Mermaid, Mermaid.js theming docs, themeVariables reference, FDIAL article, all projects

### Dev preview vs. live page

The static HTML at `projects/mermaid-theme-builder/index.html` **is** the live page. The React app at `_replit/mermaid-theme-builder-preview/` is a dev-only prototyping tool — its build output is never deployed. See Architecture section above for run instructions.

### MTB release update procedure

On every MTB version bump, run the one-command release helper — it patches `VERSION_CONFIG`, auto-fixes all 11 structured version strings, promotes roadmap pills, and verifies everything in a single invocation.

**One-command release (preferred):**

```
python3 assets/scripts/release-mtb.py \
    --version v0.6.0 \
    --date "August 2026" \
    --sprint v0.6.x \
    --sprint-name "Ko-fi Artifacts" \
    --prev-sprint v0.5.x
```

| Flag | Purpose |
|---|---|
| `--version` | Released version tag, e.g. `"v0.6.0"` |
| `--date` | Month + year shipped, e.g. `"August 2026"` |
| `--sprint` | New active sprint series, e.g. `"v0.6.x"` |
| `--sprint-name` | Sprint short name, e.g. `"Ko-fi Artifacts"` |
| `--prev-sprint` | Sprint being closed out — triggers roadmap pill promotion (omit if no sprint change) |
| `--dry-run` | Preview all changes without writing any files |

The script: (1) rewrites `VERSION_CONFIG` in `check-mtb-version.py`, then (2) delegates to `check-mtb-version.py --update` to patch all target files and verify all 11 checks. Exits 0 only when everything passes.

**Lower-level tool (check only / manual fix):**

```
python3 assets/scripts/check-mtb-version.py              # check only
python3 assets/scripts/check-mtb-version.py --update     # backup + patch + re-verify
python3 assets/scripts/check-mtb-version.py --update --prev-sprint v0.5.x
python3 assets/scripts/check-mtb-version.py --dry-run    # preview fixes, no writes
```

The `--update` flag auto-promotes the roadmap pills when `--prev-sprint` is supplied. `--prev-sprint` can also be set permanently in `VERSION_CONFIG["prev_sprint"]`.

**Manual checklist — locations auto-patched by the release script:**

| Location | What changes |
|---|---|
| Hero tag | `v{sprint} Alpha Active` |
| `#release` card `<h2>` | `v{version} — Shipped {Month YYYY}` |
| `#release` Version meta-val | `v{version} — shipped {Month YYYY}` |
| `#release` Active Sprint meta-val | `v{sprint} {sprint-name}` |
| `#roadmap` — `▶` marker + `Active` pill | Auto-promoted via `--prev-sprint`. Marker classes: `progress-marker--active` / `progress-marker--done`; pill classes: `phase-pill--active` / `phase-pill--shipped` |
| Sidebar · Status meta-val | `v{sprint} Alpha Active` |
| Sidebar · Build Phase meta-val | `v{sprint} {sprint-name}` |

**Also update in `replit.md` (not auto-patched — edit manually):**

- The `**Current version:**` line in this section (line ~116)
- The `#release` row in the Page Sections table (line ~125)
- The `#roadmap` row in the Page Sections table (line ~130)

## Internal Search Engine

Static, client-side search across the entire site. Consolidated 2026-05-03.

- `/search/` — dedicated results page (URL-shareable: `/search/?q=foo`). Body class `search-page` activates the JS page initializer.
- **All search logic lives in `assets/js/app.js` Section 5** (consolidated from the retired `assets/js/search.js`). Ctrl/Cmd+K or `/` opens overlay; Esc closes; ↑↓ navigate; ↵ follows.
- **All search CSS lives in `assets/css/theme.css`** under the `SECTION · OKH SEARCH` banner (consolidated from the retired `assets/css/search.css`).
- `assets/data/search-index.json` — generated index (48 entries as of 2026-05-15). `INDEX_URL` in `app.js` points to `/assets/data/search-index.json`.
- `assets/scripts/build-search-index.py` — Python re-builder. Walks all `*.html`, skips `noindex`, extracts title + description + headings + body excerpt, plus per-section deep links for the FDIAL article. Re-run any time content changes:
  ```
  python3 assets/scripts/build-search-index.py
  ```

### Adding deep-link entries for project page sections

The script **auto-detects** which sections to index on any `/projects/*/` page. No code changes are needed — just add `data-search-index` to the opening tag of any `content-block` div (or section/article) you want surfaced as an independent search result:

```html
<div class="content-block" id="my-section" data-search-index>
```

The attribute value is ignored; its presence is the signal. The script discovers all such elements across all project pages on every run. See `discover_sentinel_sections()` in the script for implementation details.

- Sitelinks Searchbox JSON-LD (`SearchAction`) on every page points at `/search/?q={search_term_string}`.

### Cross-site search prompt

`docs/cross-site-search-prompt.md` — a self-contained prompt (780+ lines) for the Glee-fully.tools and AskJamie.bot Replit agents to implement functionally identical search on their sites. Covers: index builder adaptation, CORS setup, `app.js` tuning, CSS brand-color overrides, the `/search/` page template, and the peer-results feature (each site shows its own results first, then a secondary section of top results from the other two sibling sites with absolute cross-domain links).

## SEO / Metadata Status

- `sitemap.xml` — rebuilt with all 18 indexable URLs (was 8). Includes writings hub, all writings, all 4 v03 field guides, projects hub, both indexable projects, and `/search/`.
- `robots.txt` — explicit opt-ins for GPTBot, ChatGPT-User, OAI-SearchBot, Google-Extended, ClaudeBot, anthropic-ai, PerplexityBot, CCBot, Applebot-Extended, Bytespider; crawl-delay for AhrefsBot/SemrushBot.
- `site.webmanifest` — fixed (was empty name + broken icon paths). Now: name "OverKill Hill P³™", short_name "OKHP³", correct favicon paths, dark theme color #111827.

### Proposed but not yet implemented (deferred)
- BreadcrumbList JSON-LD on article + project + heat pages
- Sitewide Organization JSON-LD with sameAs (LinkedIn/Fiverr/X/YouTube/Facebook/Ko-fi)
- `og:type=article` + `article:published_time` on writings pages (currently `website`)
- Per-page OG landscape images (most pages still use the 1024² sentinel; article uses a landscape image correctly)
- `prev`/`next` rel links on the four v03 field-guide pages
- "Recent Writings" surfacing block on the home page so magnus-saga and biases-as-constants aren't dropdown-only

## Cross-Site Foundation Files

`overkillhill.com`, `glee-fully.tools`, and `askjamie.bot` each live in their own GitHub Pages repo but share three byte-identical foundation files:

- `assets/css/theme.css`
- `assets/js/app.js`
- `assets/js/mermaid-init.js`

**OverKill-Hill is the source of truth.** When making a change to any of these three files, edit it here, then propagate to the siblings.

### Propagation workflow

After editing any of the three foundation files:

```bash
mkdir -p dist/sync/glee/assets/{css,js} dist/sync/askjamie/assets/{css,js}
for repo in glee askjamie; do
  cp assets/css/theme.css      dist/sync/$repo/assets/css/theme.css
  cp assets/js/app.js          dist/sync/$repo/assets/js/app.js
  cp assets/js/mermaid-init.js dist/sync/$repo/assets/js/mermaid-init.js
done
cd dist && python3 -c "
import zipfile, os
with zipfile.ZipFile(f'okh-cross-repo-sync-$(date +%F).zip', 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, _, files in os.walk('sync'):
        for f in sorted(files):
            p = os.path.join(root, f); zf.write(p, p)
    if os.path.exists('MIGRATION.md'): zf.write('MIGRATION.md', 'MIGRATION.md')
"
```

Then drop the per-repo subdirectories into the corresponding sibling clones and commit there with `chore(sync): align foundation files with overkillhill.com canonical (YYYY-MM-DD)`.

### Site-specific divergence is expressed via class hooks, not separate files

The shared `theme.css` already scopes site-specific styling via class selectors on `<body>`:

- `.glee-main` — Glee-fully.tools pages
- `.askjamie-main` — AskJamie.bot pages
- `body:not(.glee-main):not(.askjamie-main)` — OverKill Hill pages

Add new site-specific styles inside one of those scopes — never as a parallel file.

### Theme switching mechanism (do not regress)

The shared `app.js` sets `data-theme` on the `<html>` element (`document.documentElement`), **not on `<body>`**. The matching CSS uses `html[data-theme="…"] body { … }`. If you ever see `body[data-theme="…"]` rules creeping in, those are dead code — the selector will never match.

## Template Library

Path: `assets/templates/`

10 production-ready HTML templates following the `template--[slug].html` naming
convention. Index and full token reference: `assets/templates/index.md`.

| Template | Slug | Key Pages |
|----------|------|-----------|
| `template--homepage.html` | homepage | `index.html` |
| `template--interior-single.html` | interior-single | about, legal, manifesto, universe, prompt-forge |
| `template--interior-form.html` | interior-form | contact |
| `template--hub.html` | hub | projects/index, writings/index |
| `template--project-detail.html` | project-detail | all `/projects/*/`, found-ry, biases-as-constants, magnus-saga |
| `template--article.html` | article | writings/first-diagram-is-a-liar |
| `template--article-study.html` | article-study | v03/v1-heat-a, v1-heat-b, v2-heat-a, v2-heat-b |
| `template--utility.html` | utility | search |
| `template--error.html` | error | 404.html |
| `template--holding.html` | holding | under-construction.html |

**Validation exclusion:** `assets/templates/` is in `SKIP_DIRS` inside
`assets/scripts/validate-site.py` so `[[token]]` placeholders don't cause false
positives during the site audit.

**Status:** Complete (2026-05-04). Post-audit fixes applied:
- `template--project-detail.html` — `robots` corrected from `noindex, nofollow` to the standard `index, follow` block (+ googlebot / bingbot / revisit-after), matching published project pages.
- `template--article-study.html` — About submenu fixed to canonical 4-item cluster (Universe / About / Contact / Legal); Contact and Legal were erroneously top-level nav items.

**Spec:** `attached_assets/TEMPLATE-SYSTEM-PROMPT_1777919852480.md`

## Out of Scope for This Session
- LinkedIn poll URLs (not yet published; TODO comments in heat pages)
- GitHub Mermaid source `.mmd` file links (not yet verified)
- PNG thumbnail images for diagram cards
- glee-fully.tools and askjamie.bot (separate Replit projects)
