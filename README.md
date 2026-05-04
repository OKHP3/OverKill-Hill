# OverKill Hill P³™

**Precision · Protocol · Promptcraft**

The public site and source materials for **OverKill Hill P³™** — the digital forge behind protocol-driven promptcraft, custom GPT architecture, AI system design, and structured visual communication.

- **Live site:** <https://overkillhill.com>
- **Status:** Active build zone (forge mode, not museum mode)
- **License:** [CC BY 4.0](LICENSE)
- **Contact:** <contact@overkillhill.com>

---

## What this repo is

A static HTML/CSS/JS site, hand-authored, hosted on GitHub Pages with a Cloudflare-fronted custom domain (`overkillhill.com`). No build step. No framework. No tracking beyond the analytics declared on the relevant pages.

The repo also serves as the public artifact archive for OverKill Hill P³ writings, projects, and the surrounding ecosystem (AskJamie™, Glee-fully Personalizable Tools™, Mermaid Theme Builder, Prompt Forge).

## Stack

| Layer | Choice |
|---|---|
| Markup | Plain HTML 5 |
| Styling | Hand-authored CSS in `assets/css/theme.css` (token-driven) |
| Scripting | Vanilla JS (`assets/js/app.js`, `mermaid-init.js`) |
| Diagrams | [Mermaid](https://mermaid.js.org/) loaded from CDN on the v0.3 article |
| Search | Client-side index in `assets/search-index.json` |
| Hosting | GitHub Pages with `CNAME` + Cloudflare |
| Local preview | `python3 server.py` (port 5000, no-cache headers) |

## Local development

```bash
python3 server.py
# then open http://localhost:5000
```

The server is dev-only. It serves the repo root with no caching so edits are immediately visible. Production routing (404, redirects) is handled by GitHub Pages and Cloudflare, not by this script.

## Repository layout

```
.
├── index.html                       Homepage
├── 404.html                         Brand-styled 404
├── under-construction.html          Forge-in-progress shell
├── about/                           About OverKill Hill
├── contact/                         Contact + social
├── legal/                           Legal notice + usage disclaimer
├── manifesto/                       The manifesto (canonical declaration)
├── universe/                        Ecosystem map (parent/child relationships)
├── search/                          Client-side site search
├── prompt-forge/                    The Prompt Forge tool entry
├── found-ry/                        Found-Rᵧ meta-framework page
├── projects/
│   ├── index.html                   Projects hub
│   ├── mermaid-theme-builder/       Live tool + landing
│   ├── bfs-framing-intelligent-futures/
│   ├── abrahamic-reference-engine/
│   ├── hometools/                   Homestead-R
│   ├── pathscrib-r/                 Narrative copilot
│   └── un-nocked-truth/             Inclusive archery program
├── writings/
│   ├── index.html                   Writings hub
│   ├── first-diagram-is-a-liar/     Featured essay (v0.3 Visual Edition)
│   │   └── v03/                     v1/v2 heat pages (poll bracket)
│   ├── biases-as-constants/
│   └── magnus-saga/                 Speculative fiction series
├── assets/
│   ├── css/theme.css                Single stylesheet, token-driven
│   ├── js/app.js                    Mobile nav + year setter + search
│   ├── img/                         Logos, hero images, favicons
│   └── search-index.json            Generated search index
├── scripts/
│   └── validate_site.py             Static-site validation harness
├── sitemap.xml                      All canonical public URLs
├── robots.txt                       Crawler policy + AI-bot opt-ins
├── site.webmanifest                 PWA manifest
├── server.py                        Dev preview server
├── CNAME                            overkillhill.com
└── _replit/                         Workspace-internal previews (not deployed)
```

## Major routes

Brand: `/`, `/about/`, `/manifesto/`, `/universe/`, `/contact/`, `/legal/`
Projects: `/projects/`, `/projects/mermaid-theme-builder/`, `/projects/bfs-framing-intelligent-futures/`, `/projects/abrahamic-reference-engine/`, `/projects/hometools/`, `/projects/pathscrib-r/`, `/projects/un-nocked-truth/`
Tools: `/prompt-forge/`, `/found-ry/`, `/search/`
Writings: `/writings/`, `/writings/first-diagram-is-a-liar/` (+ four `v03/v1-heat-*` and `v03/v2-heat-*` subpages), `/writings/biases-as-constants/`, `/writings/magnus-saga/`
Utility: `/404.html`, `/under-construction.html`

## Validation

```bash
python3 scripts/validate_site.py
```

Checks every HTML page for: title, meta description, canonical, single H1, JSON-LD, sitemap inclusion, broken internal links, broken asset references, external `target="_blank"` links missing `rel="noopener"`, placeholder hrefs, `P3` (without superscript) brand violations, and old-tagline regressions. Run before every commit.

## Build / maintenance scripts

All scripts in `/scripts/` are pure Python, dependency-light (Pillow + bs4 + lxml), and **idempotent** — re-running them on an already-processed repo is a no-op. Each supports `--check` (where applicable) for dry-run mode.

| Script | Purpose |
|---|---|
| `validate_site.py` | Editorial + structural validator (run before every commit) |
| `png_to_webp.py` | Bulk PNG → WebP conversion (q=82, method=6) for assets ≥ 200 KB |
| `picture_upgrade.py` | Wraps `<img src=".png">` in `<picture>` with a `<source type="image/webp">` sibling |
| `cache_bust.py` | Appends `?v=<sha256[:8]>` to local CSS/JS refs in HTML |
| `extract_templates.py` | Derives stripped layout templates into `/assets/templates/` from one donor per layout; `--check` runs conformance asserts |
| `build_search_index.py` | Refreshes `/assets/search-index.json` from live HTML (preserves hand-curated anchor entries); `--check` for CI |
| `modernize_pages.py` | Idempotently injects 2026 baselines into every page: `color-scheme` meta, skip-link, Speculation Rules API prefetch, jsdelivr preconnect + mermaid `modulepreload` (mermaid pages only); `--check` for CI |
| `move_orphans_to_library.py` | Moves any unreferenced asset under `assets/img/` into `assets/img/library/` (preserves the file as a media-kit archive, removes from deploy hot path); `--check` for CI |

Templates produced by `extract_templates.py` are **scaffolds, not pages** — they're disallowed in `robots.txt` and skipped by `validate_site.py`.

### Continuous integration

`.github/workflows/validate.yml` runs `validate_site.py`, `extract_templates.py --check`, and `build_search_index.py --check` on every push and pull request to `main`. All three must pass green for the build to be considered deploy-safe.

## Editing guidance

- **Brand name** is `OverKill Hill P³™` (Unicode `³`, not `P3`). The script will fail the build if `P3` slips into a title or meta tag.
- **Tagline** is `Precision · Protocol · Promptcraft` — never `Precision. Power. Presence.` (the pre-2026 form).
- **Sub-brands** (AskJamie™, Glee-fully Personalizable Tools™) are separate; do not collapse them into OverKill Hill copy.
- **`AutoCAD 10`** is a deliberate locked literal in the manifesto — leave it alone.
- When adding a page, also add a `<url>` entry to `sitemap.xml` and verify the validation script passes.

## Related projects

- **AskJamie™** — <https://askjamie.bot> — mid-century AI helpdesk persona
- **Mermaid Theme Builder** — `/projects/mermaid-theme-builder/` — live tool, MIT-licensed
- **Prompt Forge** — `/prompt-forge/` — protocol-driven prompt engineering workshop

## Known limitations

- No automated image-format optimization yet (everything is PNG; WebP conversion is a follow-up task).
- No CSP header set at the edge yet (recommendation in `AUDIT_OVERKILL_HILL_REPLIT_PASS.md`).
- Search index (`assets/search-index.json`) is committed; regenerate when adding new pages.

## Contact

Project inquiries, collaboration, or audit reports: <contact@overkillhill.com>

---

*This repo is the artifact, not the product. The product is whatever the page tells you it is.*
