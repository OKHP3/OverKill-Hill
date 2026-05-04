# OverKill Hill P³™ — Page Template Library

> **Brand:** OverKill Hill P³™ · Precision · Protocol · Promptcraft  
> **Theme:** Espresso `#2a2320`  
> **Created:** 2026-05-04  
> **Spec:** `attached_assets/TEMPLATE-SYSTEM-PROMPT_1777919852480.md`

---

## Template Inventory

All templates live at `assets/templates/` and follow the `template--[slug].html`
naming convention. Copy the appropriate file, rename to `index.html` (or the
required HTML filename), then replace every `[[ ]]` token before publishing.

| File | Type Slug | Described Purpose | Source Page |
|------|-----------|-------------------|-------------|
| `template--homepage.html` | `homepage` | Full hero, multi-section, multi-CTA home page | `index.html` |
| `template--interior-single.html` | `interior-single` | Hero + prose sections, no card grid, no form | `about/index.html` |
| `template--interior-form.html` | `interior-form` | Interior page whose primary element is a form or contact block | `contact/index.html` |
| `template--hub.html` | `hub` | Section index with card grid of child items | `writings/index.html` |
| `template--project-detail.html` | `project-detail` | Individual project page; includes WIP construction overlay | `projects/abrahamic-reference-engine/index.html` |
| `template--article.html` | `article` | Long-form article with breadcrumb, author meta, TOC sidebar, reading-progress bar, Mermaid support | `writings/first-diagram-is-a-liar/index.html` |
| `template--article-study.html` | `article-study` | Article sub-page for diagram heat comparisons; multi-competitor Mermaid card grid, poll box, breadcrumb trail back to parent | `writings/first-diagram-is-a-liar/v03/v1-heat-a/index.html` |
| `template--utility.html` | `utility` | Functional tool page (search, calculators, generators) — no standard hero, tool interface is the primary content | `search/index.html` |
| `template--error.html` | `error` | HTTP error page (404, 410, etc.) — `noindex, nofollow`, hero + navigation cards | `404.html` |
| `template--holding.html` | `holding` | Coming-soon / under-construction holding page — `noindex, nofollow` | `under-construction.html` |

---

## Page Type → Template Map

| Live Page | Template |
|-----------|----------|
| `index.html` | `template--homepage.html` |
| `about/index.html` | `template--interior-single.html` |
| `legal/index.html` | `template--interior-single.html` |
| `manifesto/index.html` | `template--interior-single.html` |
| `universe/index.html` | `template--interior-single.html` |
| `prompt-forge/index.html` | `template--interior-single.html` |
| `contact/index.html` | `template--interior-form.html` |
| `projects/index.html` | `template--hub.html` |
| `writings/index.html` | `template--hub.html` |
| `projects/abrahamic-reference-engine/index.html` | `template--project-detail.html` |
| `projects/bfs-framing-intelligent-futures/index.html` | `template--project-detail.html` |
| `projects/hometools/index.html` | `template--project-detail.html` |
| `projects/mermaid-theme-builder/index.html` | `template--project-detail.html` |
| `projects/pathscrib-r/index.html` | `template--project-detail.html` |
| `projects/un-nocked-truth/index.html` | `template--project-detail.html` |
| `found-ry/index.html` | `template--project-detail.html` |
| `writings/biases-as-constants/index.html` | `template--project-detail.html` |
| `writings/magnus-saga/index.html` | `template--project-detail.html` |
| `writings/first-diagram-is-a-liar/index.html` | `template--article.html` |
| `writings/first-diagram-is-a-liar/v03/v1-heat-a/index.html` | `template--article-study.html` |
| `writings/first-diagram-is-a-liar/v03/v1-heat-b/index.html` | `template--article-study.html` |
| `writings/first-diagram-is-a-liar/v03/v2-heat-a/index.html` | `template--article-study.html` |
| `writings/first-diagram-is-a-liar/v03/v2-heat-b/index.html` | `template--article-study.html` |
| `search/index.html` | `template--utility.html` |
| `404.html` | `template--error.html` |
| `under-construction.html` | `template--holding.html` |

---

## Token Reference

All page-specific values are marked with `[[UPPERCASE-KEBAB-CASE]]` tokens.
Replace every token before publishing a page derived from these templates.

### Universal Tokens (all templates)

| Token | Where It Goes |
|-------|---------------|
| `[[PAGE-TITLE]]` | `<title>` element |
| `[[PAGE-DESCRIPTION]]` | `<meta name="description">` content |
| `[[PAGE-KEYWORDS]]` | `<meta name="keywords">` content |
| `[[CANONICAL-URL]]` | `<link rel="canonical">` href |
| `[[OG-TITLE]]` | `og:title` meta content |
| `[[OG-DESCRIPTION]]` | `og:description` meta content |
| `[[OG-TYPE]]` | `og:type` meta content (e.g. `website`, `article`) |
| `[[OG-URL]]` | `og:url` meta content |
| `[[OG-IMAGE-URL]]` | `og:image` meta content |
| `[[OG-IMAGE-ALT]]` | `og:image:alt` meta content |
| `[[TWITTER-TITLE]]` | `twitter:title` meta content |
| `[[TWITTER-DESCRIPTION]]` | `twitter:description` meta content |
| `[[TWITTER-IMAGE-URL]]` | `twitter:image` meta content |
| `[[TWITTER-IMAGE-ALT]]` | `twitter:image:alt` meta content |
| `[[SCHEMA-JSON-LD]]` | Body of the `<script type="application/ld+json">` block |
| `[[HERO-HEADING]]` | Primary `<h1>` on the page |
| `[[HERO-SUBTITLE]]` | Subtitle or lead paragraph directly under `<h1>` |
| `[[HERO-TAGLINE]]` | Short tagline / sub-label under the subtitle |
| `[[BREADCRUMB-LABEL]]` | Eyebrow / breadcrumb label above `<h1>` |
| `[[SECTION-HEADING]]` | `<h2>` section headings in `<main>` |
| `[[CARD-OR-ARTICLE-TITLE]]` | `<h3>` card or article headings |
| `[[BODY-COPY]]` | Body paragraph placeholder text |
| `[[CTA-LABEL]]` | Call-to-action button or link label |
| `[[CTA-URL]]` | Call-to-action button or link href |
| `[[IMAGE-SRC]]` | `src` attribute of a page-specific image |
| `[[IMAGE-ALT]]` | `alt` attribute of a page-specific image |
| `[[PAGE-ANCHOR]]` | `id` attribute on a `<section>` or `<article>` |

### Template-Specific Tokens

| Token | Template(s) | Purpose |
|-------|-------------|---------|
| `[[STATUS-EYEBROW]]` | homepage | Site-status eyebrow label |
| `[[STATUS-BODY]]` | homepage | Site-status body text |
| `[[HUB-ITEM-LABEL]]` | hub | Eyebrow/pill label on a hub card |
| `[[WIP-KEY]]` | project-detail | `data-wip-key` attribute used by JS to gate the overlay |
| `[[WIP-COPY]]` | project-detail | Explanation copy inside the WIP overlay card |
| `[[WIP-DISMISS-LABEL]]` | project-detail | Button label that dismisses the WIP overlay |
| `[[IMAGE-SRC-WEBP]]` | project-detail, interior-form | WebP `srcset` path for `<picture>` element |
| `[[ARTICLE-EYEBROW-SERIES]]` | article, article-study | Series or edition label in the article eyebrow |
| `[[ARTICLE-EYEBROW-TAGS]]` | article | Topic tags in the article eyebrow |
| `[[ARTICLE-EYEBROW-VERSION]]` | article, article-study | Version string (e.g. `Article v0.3`) |
| `[[ARTICLE-AUTHOR]]` | article | Author display name |
| `[[ARTICLE-DATE-ISO]]` | article | ISO 8601 date for `<time datetime="">` |
| `[[ARTICLE-DATE-DISPLAY]]` | article | Human-readable date (e.g. `April 2026`) |
| `[[ARTICLE-READ-TIME]]` | article | Estimated read time (e.g. `~18 min read`) |
| `[[ARTICLE-PULL-QUOTE]]` | article | Pull-quote paragraph text |
| `[[SECTION-ANCHOR]]` | article | `id` attribute on `<h2>` headings for TOC links |
| `[[TOC-HEADING]]` | article | Heading label of the sidebar table of contents |
| `[[SPECIALS-URL]]` | article, article-study | `href` for the `.site-specials` banner link |
| `[[SPECIALS-COPY]]` | article, article-study | Link text for the `.site-specials` banner |
| `[[ARTICLE-EYEBROW-HEAT]]` | article-study | Heat identifier (e.g. `V1 Heat A`) |
| `[[PARENT-ARTICLE-URL]]` | article-study | URL of the parent article |
| `[[PARENT-ARTICLE-TITLE]]` | article-study | Display title of the parent article |
| `[[POLL-QUESTION-LABEL]]` | article-study | Bold label before the poll question |
| `[[POLL-QUESTION]]` | article-study | Poll question text |
| `[[POLL-COPY]]` | article-study | Explanatory copy about where/how to vote |
| `[[MERMAID-DIAGRAM-CODE]]` | article-study | Mermaid diagram syntax placed inside `.mermaid` div |
| `[[TOOL-HERO-CLASS]]` | utility | CSS class on the tool hero section |
| `[[BODY-CLASS]]` | utility | CSS class on `<body>` (e.g. `page-search`) |
| `[[TOOL-INTERFACE-HTML]]` | utility | The functional HTML for the tool (search form, results, etc.) |
| `[[ERROR-CODE]]` | error | Numeric error code used as section `id` (e.g. `404`) |
| `[[ASIDE-LABEL]]` | interior-form | `aria-label` for the aside element |
| `[[CONTACT-FIELD-LABEL]]` | interior-form | Label for a contact field (e.g. `Email`) |
| `[[CONTACT-FIELD-VALUE]]` | interior-form | Value for a contact field |

---

## Site Tooling Notes

- **Validator:** `scripts/validate_site.py` — the `assets/templates/` directory is
  excluded via `SKIP_DIRS` so template `[[token]]` placeholders don't trigger
  false positives. Run from repo root: `python3 scripts/validate_site.py`
- **Audit script note:** The spec references `tools/audit-site.py`; this project
  uses `scripts/validate_site.py` instead. `tools/audit-report.md` is in
  `.gitignore` so generated reports don't pollute the repository.
- **No build step:** This is a pure static site served by `server.py`. Templates
  are authoring tools only — they are never served directly.
- **CSS version query strings:** Live pages pin the theme stylesheet with a `?v=N`
  cache-buster. Templates use `/assets/css/theme.css` without a version string;
  add the current version when spinning up a new page.
