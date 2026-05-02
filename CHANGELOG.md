# Changelog

All notable changes to the **OverKill Hill P³™** public repository should be recorded here.

## [v0.3 — 2026-04-21] — The First Diagram Is Usually a Liar: Visual Edition

### Added
- **v0.3 Visual Edition section** (`#visual-edition`) — deck-is-live framing, key quote pull-quote, What v0.3 Adds list, Public Scoring Bracket, and three-lane scoring model overview.
- **Poll Schedule table** (`#poll-schedule`) — seven-row schedule covering April 21 through post-close debrief (v0.3.1.1 through v0.3.3).
- **Scoring Model section** (`#scoring-model`) — three-lane grid: Audience Scoring, Architect Scoring (seven-point rubric), and Council-Assisted Scoring.
- **V1 First-Pass Diagram gallery** (`#v1-diagrams`) — seven diagram cards with quick-reads and confirmed Mermaid.ai live links for all seven models (Copilot, Claude, ChatGPT, Perplexity, Gemini, Notion, Replit).
- **V2 Revised Diagram gallery** (`#v2-diagrams`) — eight diagram cards including ChatGPT V2 Pro, with confirmed Mermaid.ai live links for all eight.
- **Deck download section** (`#v03-deck`) — Square and Wide formats each with PDF and PPTX links to the public GitHub repository.
- **v0.3 High-Resolution Field Guide section** (`#v03-field-guide`) — four heat guide cards linking to dedicated field guide pages.
- **Four new static heat guide pages** — `v03/v1-heat-a/`, `v03/v1-heat-b/`, `v03/v2-heat-a/`, `v03/v2-heat-b/` — each with poll question, competitor quick-reads, Mermaid.ai links, back-to-article navigation, and a separate Mermaid referral CTA.
- **v0.3 Field Guides sidebar widget** — fourth sidebar widget listing all four heat guide pages.
- **New CSS classes** — `.schedule-table`, `.scoring-lanes`/`.scoring-lane`, `.diagram-gallery`/`.diagram-grid`/`.diagram-card`, `.download-options`/`.download-format`, `.heat-guide-grid`/`.heat-guide-card`, `.heat-guide-hero`, `.heat-actions`, `.mermaid-cta` — all using OKH design tokens.

### Updated
- Article version throughout: `v0.2` → `v0.3` (eyebrow, subtitle, protoform notice, sidebar badge, meta tags, JSON-LD `dateModified`).
- Protoform notice: removed coming-soon language; updated to v0.3 Visual Edition Live summary.
- Article banner: Mermaid hook → Visual Edition hook, link target `#what-mermaid-actually-is` → `#visual-edition`.
- JSON-LD `dateModified`: `2026-04-16` → `2026-04-21`.
- CSS cache-bust: `?v=14` → `?v=15`.
- TOC sidebar: seven new entries added (Visual Edition, Poll Schedule, Scoring Model, V1 Diagrams, V2 Diagrams, v0.3 Deck, Field Guide).
- About This Article sidebar widget: updated to reference v0.3 additions.
- Site-wide announcement banner on 19 pages: `"Updated v0.2: …Plus: Mermaid.ai explained →"` → `"v0.3 Visual Edition: The First Diagram Is Usually a Liar →"`.
- Home page article card blurb updated to reference v0.3 Visual Edition and scoring bracket.
- Writings index article card blurb updated to reference v0.3 Visual Edition.

---

## [v0.2 — 2026-04-16] — The First Diagram Is Usually a Liar

### Added
- **"What a Mermaid Diagram Actually Is"** — new section (`#what-mermaid-actually-is`) establishing that Mermaid is a text syntax, not an AI format. Includes raw code example and the Notepad test.
- **"Mermaid the Syntax vs Mermaid.ai the Platform"** — new section (`#mermaid-syntax-vs-platform`) disambiguating the open-source JS library from the commercial AI product. Reframes the council comparison.
- **"The One That Should Have Won"** — new section (`#one-that-should-have-won`) covering Mermaid.ai's premature rendering failure and the Think Mode product recommendation.
- **Replit** added to the council scorecard in the article body (was already in sidebar).
- **LinkedIn Post v0.2** artifact card — Mermaid.ai, premature rendering, and the missing Think Mode.
- **LinkedIn Comment v0.2** artifact card — Mermaid syntax vs Mermaid.ai platform clarification.

### Updated
- Article version throughout: `v0.1` → `v0.2` (eyebrow, subtitle, protoform notice, sidebar badge, meta tags, JSON-LD schema description).
- Read time: `~12 min` → `~18 min`.
- JSON-LD `dateModified`: `2026-04-10` → `2026-04-16`.
- CSS cache-bust: `?v=9` → `?v=10`.
- TOC sidebar: three new entries added (What a Mermaid Diagram Is, Mermaid vs Mermaid.ai, The One That Should Have Won).
- About This Article sidebar widget: updated to reflect v0.2 additions.
- Site-wide announcement banner on 19 pages: `"New: …ROY, Mermaid, and a Council of AIs →"` → `"Updated v0.2: …Plus: Mermaid.ai explained →"`.
- Home page article card blurb updated to reference v0.2 content and Mermaid.ai.
- Writings index article card blurb updated to flag Mermaid.ai exclusion.

---

## [Unreleased]

### Added
- **Internal search engine** — new `/search/` results page plus a sitewide `Ctrl/Cmd+K` (or `/`) overlay injected into the primary nav of every page via `assets/js/search.js`. Results highlight matched terms, support category filters, and link directly to article sections.
- **Per-section deep-link indexing** for `/writings/first-diagram-is-a-liar/` — 23 article sections now individually searchable (e.g. searching "ROY", "council", or "mermaid" returns specific in-article anchors, not just the parent page).
- `assets/scripts/build-search-index.py` — re-runnable Python script that walks all `*.html`, skips `noindex`, and produces `assets/search-index.json` (39 entries).
- `assets/css/search.css` — overlay + results-page styles using OKH design tokens.
- New artifact cards: **LinkedIn Post v0.3.2** and **LinkedIn Comment v0.3.2** in `#artifacts`.

### Updated
- **`sitemap.xml`** — rebuilt with all 18 indexable URLs (previously 8). Now includes the `/writings/` hub, both other writings, all four v03 field guides, the Mermaid Theme Builder project, and `/search/`.
- **`robots.txt`** — explicit allow opt-ins for GPTBot, ChatGPT-User, OAI-SearchBot, Google-Extended, ClaudeBot, anthropic-ai, PerplexityBot, CCBot, Applebot-Extended, Bytespider. Crawl-delay 10 for AhrefsBot and SemrushBot. `Disallow: /404.html` added.
- **`site.webmanifest`** — fixed (was previously empty `name`/`short_name` and pointed at non-existent root favicons). Now includes name, short name, description, scope, dark theme color #111827, and correct `/assets/img/favicons/` icon paths including 192/512 maskable variants.
- **JSON-LD `SearchAction`** on 18 pages — phantom `https://overkillhill.com/?s={search_term_string}` replaced with the real `https://overkillhill.com/search/?q={search_term_string}` pattern.

### Planned (deferred follow-up)
- BreadcrumbList JSON-LD on article + project + heat pages
- Sitewide Organization JSON-LD with `sameAs` social links
- `og:type=article` and `article:published_time` on writings pages
- Per-page landscape (1200×630) Open Graph images
- `prev`/`next` `rel` links across the four v03 field-guide pages
- "Recent Writings" home-page block surfacing magnus-saga and biases-as-constants

## [Current Public Baseline]

### Established
- Core brand README
- Public website source for overkillhill.com
- Writings section and related feature pages
- Public-facing companion pages for ecosystem properties including Glee-fully and AskJamie

### Notes
- This repository serves as the main public source for the OverKill Hill web presence and brand artifacts.