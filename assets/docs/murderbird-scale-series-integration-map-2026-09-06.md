# MurderBird scale series integration map

Date: 2026-09-06

## Status and scope

The scale-correct series is a first-wave candidate collection. This document maps existing consumers to possible future placements. It does not approve an image, replace published artwork, or establish that any candidate has been deployed. Proposed dimensions below are delivery targets, not claims about files already generated.

This inventory was checked against local source files. It is not a live-deployment verification. English published pages are generated from `site-src/`; edits to generated HTML alone would not be durable.

## Existing consumer matrix

Paths are relative to the repository root. Existing icon PNG dimensions were measured. Hero and social dimensions below are declared by the source HTML or page metadata unless otherwise stated.

| Priority | Role | Existing asset | Source consumers |
|---|---|---|---|
| P1 | Homepage hero | `assets/img/murderbird-frontal-attack-2026-09-05.png`, 1254 x 1254; `assets/img/webp/murderbird-frontal-attack-2026-09-05-{512,1024}.webp` | `site-src/pages/index.main.html`; localized homepages `fr/index.html`, `de/index.html`, `es/index.html`, `es-mx/index.html`, `en-gb/index.html` |
| P1 | Story hero and awakening panel | `assets/img/webp/murderbird-frontal-attack-2026-09-05-1024.webp`, 1024 x 1024 | `site-src/pages/writings/murderbird/index.main.html` |
| P1 | Story social image and Article image | Same frontal-attack 1024 WebP | `site-src/pages.json`, `site-src/pages/writings/murderbird/index.extras.html` |
| P1 | Shared brand social card | `assets/img/library/over-kill-hill-p3-title-left-comp-right-wide-1536.png`, 1536 x 1024 | Fifteen English route entries in `site-src/pages.json`, listed below |
| P2 | Navigation mark | `assets/img/murderbird-v2-icon-nav-96.png`, displayed at 40 x 40 | `assets/partials/header.html`; generated pages, locale pages, and page templates |
| P2 | Browser icons | `assets/img/favicons/murderbird-v2-icon-browser-{16,32,48}.png`, measured matching square sizes; `murderbird-v2-icon.ico` | `assets/partials/head.html`; generated and localized heads; `assets/templates/template--*.html` |
| P2 | Apple home-screen icon | `assets/img/favicons/murderbird-v2-icon-opaque-180.png`, measured 180 x 180 | `assets/partials/head.html` and downstream page heads |
| P2 | Android and PWA icons | `assets/img/favicons/murderbird-v2-icon-{opaque,maskable}-{192,512}.png`, measured matching square sizes | `site.webmanifest`, with separate `any` and `maskable` entries |
| P2 | Organization structured-data logo | `assets/img/favicons/murderbird-v2-icon-1024.png`, measured 1024 x 1024 | `assets/partials/head.html`, `scripts/build-site.py` |
| P3 | Generic fallback social image | `assets/img/over-kill-hill-p3-sentinel-waiting-square-1024.png`, 1024 x 1024 | Eight English route entries in `site-src/pages.json`, listed below |
| P3 | Other visible legacy sentinel | Same sentinel PNG and WebP | `site-src/pages/legal/index.main.html`, displayed at 260 x 260; historical diagram in `site-src/pages/writings/first-diagram-is-a-liar/v03/v2-heat-b/index.main.html` |

Shared brand social-card routes:

- `/`, `/about/`, `/contact/`, `/legal/`
- `/projects/`, `/projects/abrahamic-reference-engine/`, `/projects/bpmn-for-mermaid/`, `/projects/kierans-lifetrkr/`, `/projects/mac-studio-local-ai-workbench/`, `/projects/mermaid-theme-builder/`, `/projects/skillz/`
- `/prompt-forge/`, `/universe/`, `/vault/`, `/writings/`

Generic fallback social-image routes:

- `/404.html`, `/search/`, `/under-construction.html`
- `/projects/hometools/`, `/projects/pathscrib-r/`, `/projects/un-nocked-truth/`
- `/writings/biases-as-constants/`, `/writings/magnus-saga/`

Localized homepage heroes already reference the same frontal-attack asset family. A future approved change must preserve that parity and update localized alternative text through the applicable translation workflow. Shared source changes do not, by themselves, prove localized HTML or social metadata has been updated.

## Historical preservation boundaries

- Preserve the manifesto's historical narrative artwork and sharing imagery. This boundary is recorded in `assets/docs/murderbird-v2-delivery-status-2026-09-05.md`.
- The protected image is `assets/img/library/over-kill-hill-p3-title-low-right-bird-perch-comp-square-1024.webp`, declared 1024 x 1024, used by `site-src/pages/manifesto/index.main.html` and the manifesto metadata in `site-src/pages.json`.
- The same image appears in `site-src/pages/writings/murderbird/index.main.html` as the explicitly labeled original sigil. Preserve it as a historical comparison rather than silently replacing it with the new physical-scale interpretation.
- Historical diagrams and unrelated project-specific imagery are not blanket replacement targets. Client brands, sibling brands, and project-specific social cards retain their own identity.
- Shared navigation and platform icons are separate from historical narrative art. Their previous v2 adoption does not authorize rewriting the historical image record.

## Proposed candidate array and derivative targets

| Candidate or derivative | Proposed target | Intended use and constraint |
|---|---|---|
| Full-height workshop portrait | 1536 x 2048 master; 768 x 1024 derivative | Establish imposing terrestrial scale against a normal-height workbench and ordinary CRT. The computer does not support the bird's body weight. |
| Landscape workshop hero | 2400 x 1600 master; 1536 x 1024 and 768 x 512 derivatives | Responsive homepage or editorial hero, with enough margin for complete feet and crown. |
| Brand social card | 1200 x 630 | Purpose-composed wide image with crop-safe subject and optional separately typeset title. Do not assume a square crop is sufficient. |
| Story social card | 1200 x 630 | Story-specific composition; may share a master with the hero if the crop retains scale evidence. |
| Square editorial card | 1024 x 1024; 512 x 512 | Listings and small card placements. Avoid cropping away every scale reference. |
| Transparent full-body pose | Native generated master plus reviewed responsive derivatives | Actual alpha required. A painted checkerboard or white background is not transparency. |
| Frontal action and lateral stride | Native landscape or portrait masters | Grounded weight transfer, mechanical articulation, limited left-wing travel, and coherent anatomy. Still poses are not animation frames. |
| Repair and heart detail | 1536 x 1024 target | Explain layered construction without turning the everyday bird into a permanently open cutaway. |
| Head/icon master | 1024 x 1024 or larger square | Preserve recognizable bill, crown, and optic. Fine detail must survive small-size review. |
| Browser derivatives | 16, 32, and 48 square PNG; multi-size ICO | Evaluate each at actual display size. A resized detailed portrait may not be legible. |
| Navigation derivative | 96 x 96 PNG | Review at the current 40 x 40 display size on light and dark themes. |
| Apple derivative | 180 x 180 opaque PNG | Deliberate opaque background and comfortable margins. |
| PWA derivatives | 192 and 512 square PNG, separate opaque and maskable versions | Verify mask-safe content in the dedicated maskable versions. Do not reuse a tightly cropped head without checking masks. |
| Organization logo | 1024 x 1024 PNG | Consistent identity and metadata dimensions; distinct from a social scene. |

Do not enlarge a smaller generated image and describe it as a higher-detail original. Record native dimensions separately from derivative dimensions.

## Metadata and acceptance requirements

Each candidate and approved derivative should have a portable record containing:

- Stable asset ID, role, relative path, MIME type, byte size, pixel dimensions, and file hash.
- Native generated dimensions, transparency status, and any conversion or resizing history.
- Reference asset IDs and relative paths, exact generation prompt, tool used, and generation date. Do not invent an exact model identifier if the tool does not expose one.
- Candidate or approved status, approval evidence, and intended route or component. A file in the repository is not evidence of deployment.
- Focal point, crop-safe area, applicable background, and mask-safe assessment where relevant.
- en-US alternative text describing the visible image rather than invisible lore; localized alternatives for localized consumers.
- Social-card title, description, image alternative text, width, height, and MIME metadata where used. Keep Open Graph, Twitter, and applicable structured-data image references consistent.
- Story-continuity review: scale cues, fossil-informed terrestrial proportions, preferred hooked bill and crown, aged bronze, historically layered repairs, self-contained modern power, and purposeful behavior.
- Known limitations, including uncertain mechanical connections, inconsistent markings between poses, failed alpha, or missing scale references.

## Future integration gate

1. Review the candidate masters against the story and owner feedback before creating a broad production derivative set.
2. Keep candidate source assets in the brand library and generation records in `assets/docs/`. Do not overwrite historical masters.
3. For an approved integration, update the authoring source, shared partials, page metadata, locale consumers, platform manifest, and structured-data consumers explicitly within the approved scope.
4. Use current active tooling from `scripts/README.md`. Several legacy image conversion commands are now in `scripts/archive/`; their names in older guidance do not make them active production commands.
5. Verify generated HTML and search freshness, locale links and hero parity, image dimensions and alpha, small-icon rendering, social metadata, and light/dark responsive behavior.
6. After an authorized release, separately verify the deployed revision and live asset consumers. Until then, this collection remains staged first-wave candidates, not a completed site-wide rollout.
