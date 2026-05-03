# OverKill Hill P³™ — Template Library
**Location:** `/assets/templates/`  
**Last updated:** May 2026

## Purpose
Structural clones of every page layout on overkillhill.com, stripped of
page-specific content and ready to use as starting points for new pages.
All templates are complete, valid HTML files. Navigation and footer are
live. CSS and JS are functional. All asset paths are root-relative
(starting with `/`) so they resolve correctly from this subdirectory.

## Template Inventory

| Template File | Covers These Pages | Layout Type |
|---|---|---|
| `home-template.html` | `/` | Homepage |
| `writings-hub-template.html` | `/writings/` | Content hub / index |
| `writings-article-template.html` | `/writings/biases-as-constants/`, `/writings/magnus-saga/`, `/writings/first-diagram-is-a-liar/` | Long-form article |
| `writings-article-study-template.html` | `/writings/first-diagram-is-a-liar/v03/v1-heat-a/`, `/writings/first-diagram-is-a-liar/v03/v1-heat-b/`, `/writings/first-diagram-is-a-liar/v03/v2-heat-a/`, `/writings/first-diagram-is-a-liar/v03/v2-heat-b/` | Article variant / heat-test study |
| `projects-hub-template.html` | `/projects/` | Content hub / index |
| `projects-project-template.html` | `/projects/abrahamic-reference-engine/`, `/projects/bfs-framing-intelligent-futures/`, `/projects/hometools/`, `/projects/mermaid-theme-builder/`, `/projects/pathscrib-r/`, `/projects/un-nocked-truth/` | Individual project page |
| `universe-template.html` | `/universe/` | Brand universe |
| `about-template.html` | `/about/` | About / brand page |
| `contact-template.html` | `/contact/` | Contact / form page |
| `legal-template.html` | `/legal/` | Legal / policy page |
| `manifesto-template.html` | `/manifesto/` | Manifesto / editorial |
| `prompt-forge-template.html` | `/prompt-forge/` | Tool / resource page |
| `found-ry-template.html` | `/found-ry/` | Foundry / studio brand page |
| `search-template.html` | `/search/` | Search results / utility page |
| `404-template.html` | `/404.html` | Error page |
| `under-construction-template.html` | `/under-construction.html` | Placeholder / stub |

## Usage Protocol
1. Identify which template matches the layout type of the page you're building
2. Copy the template file to the correct directory path
3. Rename to `index.html`
4. Replace every `[PLACEHOLDER]` token with real content
5. Populate all `<head>` meta, OG tags, and canonical URL
6. Validate HTML before committing (`python3 scripts/validate_site.py`)
7. Update this README with any new templates added

## Placeholder Token Reference
| Token | Where Used |
|---|---|
| `[PAGE TITLE]` | `<title>` tag |
| `[PAGE META DESCRIPTION — 120-160 chars]` | `<meta name="description">` |
| `[OG TITLE]` / `[OG DESCRIPTION]` / `[OG IMAGE PATH]` | Open Graph meta |
| `[TWITTER TITLE]` / `[TWITTER DESCRIPTION]` | Twitter card meta |
| `[CANONICAL URL]` | `<link rel="canonical">` and `og:url` |
| `[PAGE HEADLINE]` | First `<h1>` on page |
| `[SECTION HEADING]` | `<h2>` section headers |
| `[SUBSECTION HEADING]` | `<h3>` subheaders |
| `[BODY CONTENT]` | Body `<p>` elements (HTML comment placeholder inside `<p>`) |
| `[IMAGE-FILENAME.ext]` | `<img src>` and `<picture><source srcset>` |
| `[Descriptive alt text for image]` | `<img alt>` attributes |
| `[LINK URL]` | In-content `<a href>` (nav/footer hrefs are preserved) |
| `[PUBLICATION DATE]` / `[ISO DATE]` | Visible dates and `<time datetime>` |
| `[VERSION BADGE]` | Article version indicators (e.g. v0.3) |
| `[AUTHOR NAME]` | Author bylines + `meta name="author"` |

## What's preserved (chrome)
- Site `<header>`, `<nav>`, and `<footer>` blocks (live links and labels)
- Skip-to-content link
- Hot-forge / announcement banner (`.site-specials`)
- All `<head>` `<link>`/`<script>` references and CSS/JS
- Every layout `<div>`, `<section>`, `<article>`, `<aside>` wrapper and class
- In-page anchor `href="#…"` links (they belong to the page outline)

## What's stripped (content)
- All `<title>`, meta description, OG, Twitter, canonical values
- Visible `<h1>` / `<h2>` / `<h3>` / `<h4>` text
- All `<p>` body text (tag preserved, content replaced with HTML comment)
- Image `src`, `srcset`, and `alt` (favicons/OG images preserved)
- In-content `<a>` `href` values (text preserved as written)
- `<time>` datetime + visible date text
- JSON-LD string values (replaced with `[KEY_NAME]` placeholders; `@context` / `@type` preserved)
