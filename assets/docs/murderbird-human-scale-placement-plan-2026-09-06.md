# MurderBird human-scale asset placement plan

Date: 2026-09-06

Status: First candidate batch. Not deployed. This document records a read-only local consumer audit and proposed export requirements. It does not approve an image, replace published artwork, or establish copyright ownership.

## Direction and scope

Use the owner's human-scale terror-bird direction: approximately two meters upright, substantial floor-bearing legs, a heavy torso, compact folded wings, and the recognizable curved bill and circular orange optic. Treat the height as the current fictional design direction, not a measured fact about every member of Phorusrhacidae.

The normal-sized CRT remains a visual scale reference and interface beside the bird. It must not look like the load-bearing perch for the full automaton. Preserve the story's ancient body, Victorian mechanical repair, and discreet modern heart and mind. Scale, historical layer, posture, and behavior need visual review together.

## Proposed deliverable matrix

All dimensions below are pending export targets, not verified dimensions of new candidate files. Crop intentionally without stretching; retain original masters.

| Asset role | Proposed exports | Placement |
| --- | --- | --- |
| Floor-standing sentinel with normal CRT | Portrait master; transparent PNG if suitable; WebP at 512, 1024, and 1536 widths when source resolution permits | Homepage and translated homepage heroes |
| Wide workshop sentinel | Wide master; 1200 x 630 social card; 1200 x 675 preview | General brand Open Graph and Twitter imagery |
| Story scale-establishing scene | Wide or portrait master plus dedicated 1200 x 630 card | MurderBird article hero, gallery, and article metadata |
| Front attack, profile stride, rear three-quarter | Separate full-body source masters and matching responsive exports | Character library, future gallery, and movement references |
| Construction-era details | Ancient bronze, Victorian repairs, modern concealed systems | Future story chapter illustrations |
| Simplified head mark | 1024 master; browser 16/32/48; navigation 96; Apple 180; Android 192/512; separate maskable 192/512; ICO | Navigation, browser tabs, and installed PWA surfaces |
| Portable asset metadata | Exact prompts, references, dimensions, alpha evidence, focal point, alt-text drafts, era, approval state, intended consumers | Cross-platform handoff and provenance |

The small head mark should preserve identity, not attempt to convey full-body scale at 16 pixels. Do not regenerate functional icon families until the new master is approved and native-size readability is checked.

## Verified current consumers

Paths are relative to the repository root. The audit inspected local source and generated files; public deployment was not checked.

### Homepage and article

- `assets/img/murderbird-frontal-attack-2026-09-05.png`: current master, 1254 x 1254, 1,509,199 bytes.
- `assets/img/webp/murderbird-frontal-attack-2026-09-05-512.webp` and `assets/img/webp/murderbird-frontal-attack-2026-09-05-1024.webp`: current responsive variants.
- `site-src/pages/index.main.html`: English homepage hero source.
- `index.html`, `fr/index.html`, `de/index.html`, `es/index.html`, `es-mx/index.html`, and `en-gb/index.html`: published homepage hero consumers.
- `site-src/pages/writings/murderbird/index.main.html`: article hero and September 2026 study gallery image.
- `site-src/pages/writings/murderbird/index.extras.html`: Article structured-data image.
- `site-src/pages.json`: article Open Graph and Twitter image configuration.
- `writings/murderbird/index.html`: generated article consumer.
- `assets/img/library/murderbird-story-sentinel-portrait-2026-09-06.png`: existing 1024 x 1536 candidate, 2,547,951 bytes; not the current homepage hero.

### General rich-meta imagery

The English page configuration contains 15 routes using `assets/img/library/over-kill-hill-p3-title-left-comp-right-wide-1536.png` (1536 x 1024, 2,957,445 bytes):

`/`, `/about/`, `/contact/`, `/legal/`, `/projects/abrahamic-reference-engine/`, `/projects/bpmn-for-mermaid/`, `/projects/`, `/projects/kierans-lifetrkr/`, `/projects/mac-studio-local-ai-workbench/`, `/projects/mermaid-theme-builder/`, `/projects/skillz/`, `/prompt-forge/`, `/universe/`, `/vault/`, and `/writings/`.

Eight routes use `assets/img/over-kill-hill-p3-sentinel-waiting-square-1024.png` (1024 x 1024, 1,903,649 bytes):

`/404.html`, `/projects/hometools/`, `/projects/pathscrib-r/`, `/projects/un-nocked-truth/`, `/search/`, `/under-construction.html`, `/writings/biases-as-constants/`, and `/writings/magnus-saga/`.

These mappings identify review candidates, not blanket replacement authority. Project-specific artwork on other routes stays project-specific. A dedicated social composition should not depend on a square hero surviving arbitrary platform cropping.

### Shared navigation and installed surfaces

- 56 published HTML files reference `/assets/img/murderbird-v2-icon-nav-96.png`, displayed at 40 x 40.
- Shared icon references occur in `assets/templates/template--article-study.html`, `template--error.html`, `template--homepage.html`, `template--article.html`, `template--holding.html`, `template--interior-form.html`, `template--interior-single.html`, `template--hub.html`, `template--utility.html`, and `template--project-detail.html`.
- Browser PNGs: `assets/img/favicons/murderbird-v2-icon-browser-16.png`, `murderbird-v2-icon-browser-32.png`, and `murderbird-v2-icon-browser-48.png`.
- Browser ICO: `assets/img/favicons/murderbird-v2-icon.ico`; inspect the root `favicon.ico` compatibility surface when implementing.
- Apple touch icon: `assets/img/favicons/murderbird-v2-icon-opaque-180.png`.
- `site.webmanifest`: `murderbird-v2-icon-opaque-192.png`, `murderbird-v2-icon-opaque-512.png`, `murderbird-v2-icon-maskable-192.png`, and `murderbird-v2-icon-maskable-512.png` under `assets/img/favicons/`.
- `scripts/build-site.py`: Organization logo currently references `/assets/img/favicons/murderbird-v2-icon-1024.png`.

Opaque and maskable files currently have identical byte lengths at corresponding sizes. This observation neither proves nor disproves safe-mask compliance. Inspect actual content and mask previews before replacement.

## Protected historical illustrations

Keep `assets/img/library/over-kill-hill-p3-title-low-right-bird-perch-comp-square-1024.webp` unchanged as the historical sigil.

Protected consumers include:

- `site-src/pages/manifesto/index.main.html`: historical manifesto illustration and its description.
- `site-src/pages/manifesto/index.extras.html`: historical structured-data image.
- `/manifesto/` entry in `site-src/pages.json`: historical Open Graph and Twitter image.
- Generated `manifesto/index.html` and translated historical manifesto equivalents, where present.
- `site-src/pages/writings/murderbird/index.main.html`, figure `media-crt`: explicitly labeled original-sigil gallery entry.

Shared navigation and platform icons on those pages are separate from their protected editorial illustrations. Do not rewrite original prompts or quotations to pretend the historical image had the revised scale.

## Proposed metadata requirements

For each approved social card, record and validate:

- `og:image` and, where used, `og:image:secure_url`: absolute public HTTPS URL for the actual approved file.
- `og:image:width`, `og:image:height`, and `og:image:type`: measured exported dimensions and correct MIME type.
- `og:image:alt`: concise description of visible content, not a keyword list or an assertion that hidden machinery is visible.
- `twitter:card`: the intended card presentation, usually `summary_large_image` for these wide cards.
- `twitter:image` and `twitter:image:alt`: matching approved composition and page-language description.
- Structured-data `image`: a valid public image URL or an `ImageObject` where the existing schema and validator permit it.
- Proposed `ImageObject` fields: `@type`, `contentUrl`, `url` if needed by the owning schema, `width`, `height`, `encodingFormat`, and descriptive `caption` or `name` when useful. Keep the Organization logo distinct from article illustrations.
- Do not invent `license`, `acquireLicensePage`, `copyrightNotice`, creator attribution, or ownership claims. Add such fields only after the owner supplies or approves the relevant rights information.

The portable internal record should also retain asset ID, file hash, generation tool, exact prompt, reference roles, creation date, original output path, transformations, actual alpha evidence, historical era, focal point, crop constraints, review status, and intended consumer list. Candidate metadata must not imply publication or approval.

## Localization ownership

English alt text is authored with the approved image and source page. Locale alt text, captions, and metadata prose belong to the exact-pair translation skills for `en-US` to `fr-FR`, `de-DE`, `es-ES`, `es-MX`, and `en-GB`. Reuse language-neutral image files where appropriate, but do not mechanically copy English descriptions into translated pages or mark stale translations fresh without review. Locale image paths, dimensions, and source-set structure still require parity checks.

## Integration gates

1. Owner or designated reviewer approves the candidate's head identity, human-scale proportions, three-era continuity, CRT scale, pose, and believable load-bearing contacts.
2. Measure dimensions, format, file size, alpha channel, and crop safety. A rendered checkerboard is not transparent alpha. Check light and dark backgrounds plus native icon sizes and mask shapes.
3. Preserve full-resolution sources in the appropriate image library and generation records in `assets/docs/`. Generate WebP output through the owning image pipeline into `assets/img/webp/`.
4. Review the exact consumer list before integration. Keep protected historical imagery and unrelated project artwork unchanged.
5. Edit English authoring sources and metadata in `site-src/`; regenerate published English HTML with the existing site builder. Handle locale prose through the owning translation skills.
6. Run declared generated-HTML, search freshness, locale-link, structural, image/icon, and relevant browser checks after implementation. Verify responsive cropping, contrast, loading priority, and no layout shifts. No release checks have been run for this candidate plan.
7. Verify metadata URLs, image dimensions, JSON-LD consistency, install-icon behavior, and localized parity against the actual approved exports.
8. Commit and deploy only as a separately verified integration step. Confirm the deployed revision and live asset responses before reporting publication.

Motion, sound, Blender scenes, and video files are separate deliverables. A set of poses is not an animation, and a camera zoom over a still is not evidence of articulated automaton movement.
