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

## Out of Scope for This Session
- LinkedIn poll URLs (not yet published; TODO comments in heat pages)
- GitHub Mermaid source `.mmd` file links (not yet verified)
- PNG thumbnail images for diagram cards
- glee-fully.tools and askjamie.bot (separate Replit projects)
