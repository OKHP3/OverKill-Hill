# MurderBird placement map

This is a candidate replacement plan, not a record of changes to the live site.

| Surface | Current local evidence | Candidate | Integration notes |
|---|---|---|---|
| Homepage hero | `site-src/pages/index.main.html:45` uses frontal-attack WebP plus PNG | `08-hero` | Full composition; use explicit dimensions and responsive sizes. A wide image may require a deliberate hero layout adjustment. |
| French, German, Spanish, Mexican Spanish homepages | `fr/`, `de/`, `es/`, `es-mx/` currently share frontal-attack image with translated alt text | `08-hero` | Change canonical authoring/generator inputs together; update alt translations and verify generated parity. |
| Story hero | `site-src/pages/writings/murderbird/index.main.html:19` uses frontal-attack square | `07-sentinel` or `08-hero` | Retain full silhouette and independent computer scale cue. |
| Story chapter illustrations | Story currently has no full eight-stage sequence | `01-maker` through `07-sentinel` | Keep 1853 recovery separate from 1873 restoration; modern power and independent choice are separate moments. Use lazy loading below the hero. |
| Story lineage figures | Same source lines 149 and 153 preserve original perch and revised attack versions | Existing historical assets | Keep as explicitly historical design evidence; do not silently present old anatomy as current canon. |
| About | `site-src/pages/about/index.main.html` has a text-led hero | `06-choice` or `07-sentinel` | Optional companion figure, not a mandatory new hero image. |
| Manifesto | `site-src/pages/manifesto/index.main.html:376` contains historical perch artwork | `07-sentinel` companion | Retain historical artwork in its editorial context; any replacement needs text alignment. |
| Story OG/Twitter | `site-src/pages.json` has square frontal-attack image and dimensions | `07-sentinel` social card | Update records and `site-src/pages/writings/murderbird/index.extras.html` Article image together. |
| Brand/general social | `site-src/pages.json` uses title-left/computer-right blueprint across many routes | `08-hero` social card where editorially relevant | Do not replace article-specific graphics or project marks indiscriminately. |
| Navigation icon | Localized navigation uses `assets/img/murderbird-v2-icon-nav-96.png` | Separate head-only icon review | A full-body scene is not a legible navigation icon. Keep current icon pending dedicated tiny-size comparison. |
| Favicon/PWA | `site.webmanifest` points to opaque and maskable 192/512 head assets | Separate icon deliverable | Preserve transparent/opaque purpose and maskable safe area. Do not auto-crop the new body scenes into icons. |

## Continuity gates

- Approximately 1.8 m is a **proposed** fictional standing-height target, not a published canon measurement or a species identification.
- One body persists across eras. Repairs, corrosion and power change; physical scale does not grow between chapters.
- The Maker studies leg/joint fragments; no complete fossil skull or fossil parts in the machine.
- Human-scale doors, workers and furniture establish size. The floor or a credible cradle supports the body, never an ordinary CRT casing.
- The commissioned hooked bill and folded ornamental wings are not evidence for flight. Keep substantial terrestrial legs and coherent joint geometry.
- Captions and alt text in this library are editorial drafts until each finished master is visually reviewed.

## Publication boundary

This folder supplies masters, delivery encodings, social layouts, provenance and draft metadata. No existing route, social record, story sentence, favicon, or deployment was changed by the packaging script.
