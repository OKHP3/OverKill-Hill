# OverKill Hill P³™ — overkillhill.com

## Project Overview

Static portfolio/documentation site for OverKill Hill P³™ (overkillhill.com). Built with HTML, CSS, and vanilla JS. Coordinated with GitHub repo `OKHP3/OverKill-Hill` (website source) and `OKHP3/first-diagram-is-a-liar` (methodology archive).

## Server

Python simple HTTP server via `server.py` — serves the static site from root.

**Workflow:** `Start application` → `python3 server.py`

## Architecture

- Root `/` — home page, site-wide assets
- `/assets/css/theme.css` — single global stylesheet (dark theme + OKH design tokens)
- `/assets/js/app.js` — vanilla JS (nav, reading progress, theme toggle)
- `/assets/img/` — favicons, logos, OG images
- `/writings/` — article pages
- `/projects/` — project pages
- `/universe/`, `/manifesto/`, `/about/`, `/contact/`, `/legal/` — brand pages

## Key CSS Design Tokens (theme.css)

- `--okh-orange` — primary brand accent (#c46a2c or similar)
- `--okh-amber` — secondary accent (lighter warm tone)
- `--color-surface` — card/widget backgrounds
- `--color-border-subtle` — borders
- `--color-muted` — body/secondary text
- `--color-fg` — primary text
- `--radius-md` — card border-radius

**CSS cache-bust:** Currently at `?v=15`

## Current Feature: Article — The First Diagram Is Usually a Liar

Path: `/writings/first-diagram-is-a-liar/`

**Version:** v0.3 — The Visual Edition (2026-04-21)

### Article Sections
- `#visual-edition` — v0.3 Visual Edition overview (deck framing, scoring bracket, what v0.3 adds)
- `#poll-schedule` — 7-row poll schedule table (Apr 21–after polls close)
- `#scoring-model` — 3-lane scoring grid (Audience / Architect / Council)
- `#pivot` — From Drawing to Modeling (intro)
- `#roy` — ROY: Return on Your Words
- `#what-mermaid-actually-is` — What a Mermaid diagram actually is
- `#mermaid-syntax-vs-platform` — Mermaid vs Mermaid.ai distinction
- `#one-that-should-have-won` — Mermaid.ai premature rendering analysis
- `#round1` — Round 1: Copilot
- `#council` — Council of AIs
- `#round2` — Round 2: Claude
- `#prompts` — Prompts in the Wild
- `#v1-diagrams` — V1 First-Pass diagram gallery (7 cards, confirmed Mermaid.ai links)
- `#v2-diagrams` — V2 Revised diagram gallery (8 cards, confirmed Mermaid.ai links)
- `#v03-deck` — Download deck (Square + Wide, PDF + PPTX)
- `#v03-field-guide` — Heat guide cards (links to 4 static heat guide pages)
- `#artifacts` — Launch Artifacts (LinkedIn artifact cards)
- `#thesis` — Thesis

### v0.3 Heat Guide Pages
- `/writings/first-diagram-is-a-liar/v03/v1-heat-a/` — ChatGPT, Claude, Gemini, Perplexity (V1)
- `/writings/first-diagram-is-a-liar/v03/v1-heat-b/` — Copilot, Notion, Replit (V1)
- `/writings/first-diagram-is-a-liar/v03/v2-heat-a/` — ChatGPT, Copilot, Gemini, Notion (V2)
- `/writings/first-diagram-is-a-liar/v03/v2-heat-b/` — ChatGPT Pro, Claude, Replit, Perplexity (V2)

All 15 confirmed Mermaid.ai diagram links are real (no placeholders). Poll URLs are TODO placeholders (not yet published on LinkedIn).

### Sidebar Widgets
1. About This Article (series badge)
2. The Repository (GitHub links)
3. Council Snapshot (scorecard table)
4. The Diagrams (15 Mermaid links)
5. v0.3 Field Guides (4 heat page links) ← NEW in v0.3
6. On This Page (TOC)

## Site-Wide Banner
All 19 non-article pages + the article page itself have a site-wide "HOT OFF THE FORGE" banner.
- **Non-article pages (19):** Link to `/writings/first-diagram-is-a-liar/`, text: "v0.3 Visual Edition: The First Diagram Is Usually a Liar →"
- **Article page:** Links to `#visual-edition`, text: "The diagrams are in. The polls are open. The deck is live. →"

## Internal Search Engine

Static, client-side search across the entire site.

- `/search/` — dedicated results page (URL-shareable: `/search/?q=foo`).
- `assets/js/search.js` — auto-injects a `Ctrl/Cmd+K` overlay button into the primary nav of every page; bound to `/` and `Ctrl/Cmd+K`. Reads `assets/search-index.json`.
- `assets/css/search.css` — overlay + results-page styles (loaded on demand by search.js + statically on the search page).
- `assets/search-index.json` — generated index (39 entries: 1 home, 5 brand, 1 writings hub, 1 article, **23 article-section deep links**, 4 field guides, 3 projects, 1 search page).
- `assets/scripts/build-search-index.py` — Python re-builder. Walks all `*.html`, skips `noindex`, extracts title + description + headings + body excerpt, plus per-section deep links for the FDIAL article. Re-run any time content changes:
  ```
  python3 assets/scripts/build-search-index.py
  ```
- Sitelinks Searchbox JSON-LD (`SearchAction`) on every page now points at the real `/search/?q={search_term_string}` URL pattern (was previously phantom `/?s=…`).

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
cd dist/sync && zip -qr ../okh-cross-repo-sync-$(date +%F).zip glee askjamie MIGRATION.md
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

## Out of Scope for This Session
- LinkedIn poll URLs (not yet published; TODO comments in heat pages)
- GitHub Mermaid source `.mmd` file links (not yet verified)
- PNG thumbnail images for diagram cards
- glee-fully.tools and askjamie.bot (separate Replit projects)
