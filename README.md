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
| Search | Client-side index in `assets/data/search-index.json` |
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
│   ├── data/search-index.json       Generated search index
│   ├── templates/                   10 production HTML scaffolds
├── scripts/                         All dev + CI maintenance scripts
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
python3 scripts/validate-site.py
```

Checks every HTML page for: title, meta description, canonical, single H1, JSON-LD, sitemap inclusion, broken internal links, broken asset references, external `target="_blank"` links missing `rel="noopener"`, placeholder hrefs, `P3` (without superscript) brand violations, and old-tagline regressions. Run before every commit.

For the browser-level phone layout check used in CI:

```bash
npm ci
npx playwright install chromium
python3 server.py &
npm run test:phone-overflow
```

This opens the manifesto, Mac Studio workbench, and First Diagram article at
320px and fails on document overflow, inaccessible final table columns, or
diagram grids that escape the viewport.

## Build / maintenance scripts

All scripts in `scripts/` are pure Python, dependency-light (Pillow + bs4 + lxml), and **idempotent** — re-running them on an already-processed repo is a no-op. Each supports `--check` where documented.

| Script | Purpose |
|---|---|
| `validate-site.py` | Editorial + structural validator (run before every commit) |
| `png-to-webp.py` | Bulk PNG → WebP conversion (q=82, method=6) for assets ≥ 200 KB |
| `picture-upgrade.py` | Wraps `<img src=".png">` in `<picture>` with a `<source type="image/webp">` sibling |
| `cache-bust.py` | Appends `?v=<sha256[:8]>` to local CSS/JS refs in HTML |
| `extract-templates.py` | Derives stripped layout templates into `/assets/templates/` from one donor per layout; requires `beautifulsoup4` locally |
| `build-search-index.py` | Refreshes `/assets/data/search-index.json` from live HTML. `--check` compares the expected index in memory and exits non-zero when stale without writing the JSON. |
| `modernize-pages.py` | Idempotently injects 2026 baselines into every page: `color-scheme` meta, skip-link, Speculation Rules API prefetch, jsdelivr preconnect + mermaid `modulepreload` (mermaid pages only); `--check` for CI |
| `move-orphans-to-library.py` | Moves any unreferenced asset under `assets/img/` into `assets/img/library/` (preserves the file as a media-kit archive, removes from deploy hot path); `--check` for CI |

Templates produced by `extract-templates.py` are **scaffolds, not pages** — they're disallowed in `robots.txt` and skipped by `validate-site.py`.

### Continuous integration

`.github/workflows/validate.yml` runs `validate-site.py` and the non-mutating
`build-search-index.py --check` on every push and pull request to `main`. It
also runs the comprehensive static audit, internal-link/sitemap check, shared
asset fingerprint check, phone browser QA, and contrast audit. On a push to
`main`, it deploys the checked-out commit only after that validation job
succeeds.

## Editing guidance

- **Brand name** is `OverKill Hill P³™` (Unicode `³`, not `P3`). The script will fail the build if `P3` slips into a title or meta tag.
- **Tagline** is `Precision · Protocol · Promptcraft` — never `Precision. Power. Presence.` (the pre-2026 form).
- **Sub-brands** (AskJamie™, Glee-fully Personalizable Tools™) are separate; do not collapse them into OverKill Hill copy.
- **`AutoCAD 10`** is a deliberate locked literal in the manifesto — leave it alone.
- When adding an indexable page, also add a `<url>` entry to `sitemap.xml`.
  Redirects and WIP pages marked `noindex` stay out of the sitemap and are
  reported as intentional exclusions by `check-links.py`.
- After changing searchable content, refresh and verify the committed index:
  `python3 scripts/build-search-index.py` followed by
  `python3 scripts/build-search-index.py --check`.

## Related projects

- **AskJamie™** — <https://askjamie.bot> — mid-century AI helpdesk persona
- **Mermaid Theme Builder** — `/projects/mermaid-theme-builder/` — live tool, MIT-licensed
- **Prompt Forge** — `/prompt-forge/` — protocol-driven prompt engineering workshop

## Known limitations

- Image-format optimization is script-based rather than automatic: use the PNG-to-WebP and picture-upgrade scripts, then review the generated diff.
- `_headers` provides a report-only CSP and related security headers; enforcement and live edge behavior still require deployment-specific verification.
- Search index (`assets/data/search-index.json`) is committed. Refresh it after
  searchable content changes, then use `build-search-index.py --check` to
  verify the generated file without rewriting it.
- Publishing authentication: use the GitHub Actions Pages workflow for normal
  releases. If a controlled API publish is required from Replit, store a
  fine-grained GitHub credential as the `GITHUB_PAT` workspace secret and run
  `GITHUB_TOKEN="$GITHUB_PAT" python3 scripts/push-to-github.py`. Never put the
  credential in a remote URL, repository file, shell history, or chat. The
  helper sends it only in an HTTPS Authorization header and exits on any API
  failure. See `docs/publishing.md`.

## Contact

Project inquiries, collaboration, or audit reports: <contact@overkillhill.com>

---

*This repo is the artifact, not the product. The product is whatever the page tells you it is.*
