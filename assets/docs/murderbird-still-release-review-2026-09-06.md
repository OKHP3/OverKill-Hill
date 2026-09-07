# MurderBird aligned stills — draft release review

## Scope and authority

This isolated draft selects the accepted still-image subset from the shared story/visual coordination work. It does not publish, merge, translate the whole story, or deliver audio/video. Selection began from freshly fetched origin/main at `2d7e92d23fcbe875c7421d4509109bffd22b0c48`. The primary main checkout, six existing stashes, archive branch, held art and exploratory package were preserved without staging, reset or cleanup.

The coordinating task explicitly accepted the six source images and rendered homepage/story/share layouts for local review, then authorized a draft PR. This is not Jamie final-art approval, native-language approval, engineering certification, or release approval. `docs/murderbird-unified-direction.md` contains the acceptance receipts and boundaries. Its references to held files are historical local-working records, not claims those files are shipped in this PR.

## Selected dependency closure

- Six exact source PNGs: accepted master03; clean Maker; Water; Mechanic; Heart; Sentinel.
- Eighteen proportional480/960/1536 WebPs plus one1200x630 story share PNG. No image crop or edited master; real site-font typography in the social composition.
- Exact paths, accepted source SHA256 values, derivative hashes/dimensions/bytes, placements and limited acceptance scopes are recorded in `assets/audit/murderbird-still-release-register.json`. This is a **derived release subset**, not a competing editorial catalog. The original mixed `assets/murderbird/v2/coordination/asset-register.json` and its provenance remain preserved in the primary checkout and are intentionally absent from this release tree.
- Reproduction requires only committed source PNGs, `requirements-qa.txt` (including Pillow), existing Node lockfile dependencies and the three `scripts/build-murderbird-*.{py,mjs}` builders. Review HTML is generated only under ignored `.local/murderbird-review/`. No hidden exploratory input or old Blender/video package is required.
- Story main/extras sources, story-specific page metadata, generated story, scoped shared CSS, homepage source/generated English homepage and FR/DE/ES/ES-MX/EN-GB homepage units are selected. Existing historical gallery/nav imagery is retained.
- Locale generator mappings and regressions preserve all-six-homepage image parity and accurate regenerated EN-GB/ES-MX alt/CTA. New source-fingerprint receipt replaces the active pointer while retaining the historical receipt unchanged. No locale lifecycle/noindex/hreflang-cluster/sitemap promotion occurs.
- Required generated collateral: English/FR search excerpts, CSS fingerprints across existing HTML/templates/partial, canonical CSP declarations and affected meta tags. Article JSON-LD changes its inline-script hash, so canonical policy regeneration is necessary. No policy permission was broadened.
- Selected QA/provenance: existing homepage parity test plus new accepted-dependency/placement test; workflow invokes subset validation and verifies a built package; script inventory, coordination direction, historical integration checkpoint, this review report, fallback locale receipt, new source hashes and accepted subset register.

## Deferred, preserved and deliberately not copied

The following new experimental filenames are excluded: `murderbird-unified-maker-candidate-2026-09-06.png`, `murderbird-unified-maker-candidate-02-2026-09-06.png`, `murderbird-unified-master-candidate-2026-09-06.png`, `murderbird-unified-master-candidate-02-2026-09-06.png`, and `murderbird-first-choice-opening-candidate-2026-09-06.png`. All new scale-series, human-scale studies, candidate cutouts and old exploratory `assets/murderbird/v2/` content remain outside the selected tree. No old MP4, standalone audio, native Blender package, output directory, browser snapshot, or review HTML is selected.

The old review-boundary generator/test depended on the omitted exploratory v2 package, so it is not included as a dead dependency. Its original corrected copies and byte-verified backups remain in the primary checkout. The selected social generator and built-release checks enforce the relevant local-review boundary independently.

Video remains blocked on the user's browser-extension file-access permission. No Generate click, new media-service action, credit spend, or placeholder player is part of this PR.

## Language review limit

Only homepage image descriptions and short invitations changed. FR/DE/ES/ES-MX units were independently model-translated directly from en-US under the coordinator's bounded fallback; EN-GB was adapted for the existing parity contract. These are explicitly **model-translated/adapted; native review not performed**. Required full exact-pair profiles/records were missing or provisional; no full-skill PASS, owner-approved profile or native certification is claimed. Existing locale editorial content and draft status remain unchanged. All localized invitations explicitly identify the English story destination.

`i18n/pilot/murderbird-homepage-preview-2026-09-06.json` contains the exact units, hashes, protected terms, source revision and limitations for six homepages. The source-fingerprint record permits mechanical regeneration of this bounded revision; it is not editorial approval of all page copy.

## Verification on isolated selection

Checks ran against a dedicated server at127.0.0.1:5397 serving this isolated tree, not the shared main preview. No live-deployment result is inferred.

| Gate | Result |
|---|---|
| Source copy and regeneration |22 exact selected source/doc/asset files hash-compared after copy;18 WebPs regenerated from six committed-source candidates; no exploratory package present |
| Focused browser |36 homepage combinations plus30 chapter combinations; successful English-story link transitions; no overflow/page errors; light/dark and reduced-motion |
| Full responsive |31 sitemap routes x10 viewports =310 checks, zero failures |
| Phone overflow |31 public routes at320px passed |
| Accessibility |4 representative pages plus31 routes passed bounded keyboard/focus/ARIA checks |
| CSP browser |31 routes,21 Mermaid diagrams, zero route failures; cross-origin requests intentionally blocked, not external-availability proof |
| Structural/static |56 HTML pages, zero errors,32 standing locale warnings; static audit zero issues |
| Generated outputs |36 English pages,160 search records, FR index, universe, CSS fingerprints and56-page CSP policy checks passed |
| Locale boundaries |FR/DE/ES locale-link gate and EN-GB/ES-MX regional noindex/draft gate passed |
| Regressions |Homepage parity/regeneration5 tests; accepted still dependency/placement3 tests; release-package3 tests passed |
| Performance/contrast |Representative asset budgets passed; all existing contrast-token pairs passed using UTF-8 console mode |
| Social reproduction |1200x630 PNG449979 bytes, SHA256 `d6fefa4a22b07f4427a73c1e55ba236c05771bac1b8394274475c343f2d86a14`; byte-identical rerender on Chromium151.0.7922.34 with actual site fonts |

Social byte reproducibility depends on pinned browser/font rendering environment; generator fails on unloaded required font families and changed accepted art. CI's committed-byte subset check does not claim to certify another font renderer. Screenshot/raw browser evidence remains local; the selected reports summarize observed checks, not full WCAG or hidden-mechanism certification. Thirty-two existing locale GA4/JSON-LD warnings are not newly repaired here. `_headers` is a repository declaration, not evidence that GitHub Pages serves headers.

The final PR description records commit/ref, built artifact inspection and current CI state. No main-branch change, merge, pruning, branch deletion, or deployment is authorized by this draft.
