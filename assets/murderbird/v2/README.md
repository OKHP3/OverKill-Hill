# MurderBird visual library — review edition

Open `../../../.local/murderbird-review/index.html` for the collection after generating review HTML. Review HTML now lives only under that excluded local directory, not under assets. `manifest.json` records actual file dimensions, bytes and SHA-256 hashes; missing masters are shown explicitly rather than fabricated. Its earlier `socialCard.layout` paths are historical until an approved full rebuild; the current local layouts are under `.local/murderbird-review/social/` from the repository root.

## Rebuild

From the repository root, with Python, Pillow, and Beautiful Soup available:

```powershell
py -3 assets/murderbird/v2/build-library.py
```

To refresh only the local review gallery and social layouts without re-encoding images or modifying manifest provenance, use `py -3 assets/murderbird/v2/build-library.py --review-html-only`. Use `--social-html-only` for just the eight layouts. Both modes retain noindex, and normal full builds also write HTML exclusively to `.local/murderbird-review/`. Full rebuilds update derivatives and manifest; coordinate them with the integrator before running.

Masters are matched by prefixes `01-maker`, `02-water`, `03-recovery`, `04-mechanic`, `05-heart`, `06-choice`, `07-sentinel`, and `08-hero`. A prefix with multiple masters is reported as ambiguous. Existing masters are never modified. Exact generation prompts, alt text, era and limitations come from the `assets` arrays in `masters/*-metadata.json`; optional per-image records under `prompts/` are also linked.

`derivatives/` contains uncropped, proportionally resized WebP and JPEG encodings at widths up to 480, 960 and 1600 pixels. No upscaling is applied. JPEG is omitted when genuine transparency would be lost. Metadata text and proposed placements are review drafts, not machine-verified descriptions of every visible detail.

`social/` retains the social PNGs. The 1200 × 630 HTML layouts are now in the repository's `.local/murderbird-review/social/` directory. The complete art uses `object-fit: contain` above a separate typography band. Browser screenshots provide social raster files without altering or cropping the generated art. After approved rasterization, coordinate a full rebuild so it can include the finished social files in the manifest. Intended public URLs in JSON-LD and Open Graph snippets are **not yet live**. No creator, license, copyright, or publication date is invented.

See `placement-map.md` for source locations and integration dependencies. The 1.8 m scale is a working proposal. Final editorial review must reconcile the story's workbench and computer-casing language before adopting these full-height scenes as canon.

## Social rendering and browser checks

The original delivery used a separate local Playwright CLI browser without user browser accounts. After relocation, serve the repository root on `127.0.0.1:5379` using a local-only server that permits `.local/`, then open `/.local/murderbird-review/index.html`. Relative links resolve back to the unchanged v2 images and documents. Do not serve only the v2 directory. For an approved re-render, run `rasterize-social.js` using the CLI's `run-code --filename` option; it reads local review layouts and writes PNGs to the unchanged v2 social directory. Its output path is explicit; update it if moving the repository. Coordinate a rebuild afterwards to refresh social hashes and snippets. Historical desktop and 390-pixel mobile screenshots remain under ignored `output/playwright/`. The byte-preserved pre-relocation HTML is in `.local/murderbird-review/backup-2026-09-06-pre-relocation/`; these backup files retain historical relative links and are not the active preview.
