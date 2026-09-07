# MurderBird integration checkpoint

**Current checkpoint:** the lead-authorized nine-page review relocation below resolves the earlier structural blocker. Structural, audit, search, universe, generated HTML, links, and whitespace checks now pass. Earlier failure sections remain a chronological record, not the current gate result. No release or new-art acceptance is implied.

Date: 2026-09-06. Local preparation only; no commit, staging, merge, deployment, or candidate-image acceptance.

## Authority and baseline

Coordinating brief: [murderbird-unified-direction.md](../../docs/murderbird-unified-direction.md), v1.1, owned by the lead. Include that unchanged document in the future coordinated review packet. Jamie remains final authority. The lead's 2.0 m neutral upright floor-to-crown target guides production, not a numerical claim inserted into the fiction. Preserve earlier 1.8 m studies and original provenance.

Baseline: main at `2d7e92d23fcbe875c7421d4509109bffd22b0c48`; sole listed worktree is the canonical Windows checkout. GitHub main matched that SHA at the initial checkpoint; PR 53 was merged and no open PRs were listed. Concurrent candidate libraries and reports were already untracked and remain preserved.

## Executed source change

Authoring owner: `site-src/pages/writings/murderbird/index.main.html`. Generated owner: `scripts/build-site.py` -> `writings/murderbird/index.html`. SEO record: `site-src/pages.json`; shared chrome: `assets/partials/`; search owner: `scripts/build-search-index.py`; universe owner: `scripts/sync-universe-map.py`. Never author the generated story HTML directly.

Applied the seven localized replacements recorded in `murderbird-scale-series-continuity-2026-09-06.md`: industrial line follows a reinforced assembly platform; wound steps leave that platform; support replaces a hand beneath the breast; modern walking crosses the floor; the Bird lowers its head toward the bench-supported CRT; bracket removal uses the beak with weight on the sound leg; and the ending places the weight on the floor beside the computer. Ordinary workbench references remain. Historical artwork and its accurate perched-bird alt text remain unchanged; its caption now identifies a symbolic composition rather than a physical scale diagram.

Seven paragraph/caption lines changed in source and generated HTML (two corrections share one paragraph). Parsed narrative: 5,278 whitespace-delimited words in 73 paragraphs. No exact height added; reading-time label remains 21–27 minutes. No new images, CSS, JavaScript, navigation, or metadata changes.

## Exact scene anchors and next dependencies

All anchors below already exist on `/writings/murderbird/`. No new scene anchors were invented or inserted in this patch.

| Beat | Existing anchor and insertion cue | Dependency before illustration |
|---|---|---|
| Opening | `#murderbird`, current figure `#media-hero` | Approved identity/scale reference and approved hero crop |
| Fossil/eagle dispute | `#the-maker`; fossil discussion precedes paragraph beginning “The bones never became part of the mechanism.” | Missing dedicated fragmentary-fossil scene; no complete skull or embedded bones |
| Maker | `#the-maker`; construction/inspection sequence after the dispute | Reconciled `01-maker`, anonymous human, compact wings, era-correct body |
| Water | `#the-water` | Reconciled `02-water`; inert Bird and dark optics |
| Recovery | `#the-mechanic`; opening “In 1853, a shovel struck the bird’s beak.” | Reconciled `03-recovery`; credible slings/load |
| Transport | `#the-mechanic`; paragraph beginning “The river carried it toward Basra” | Separate missing transport image/map, explicitly fictional route |
| Industrial restoration | `#the-mechanic`; paragraph beginning “For nearly twenty years, labels followed it” marks 1873 transition | Reconciled `04-mechanic`; no modern autonomy or optics |
| Modern arrival | `#the-builder` | Optional contextual still; do not duplicate heart scene gratuitously |
| Energy | `#the-heart` | Reconciled `05-heart`; finite onboard energy, no decorative reactor |
| Processing | `#the-mind` | Distinct explanatory detail if supplied; power is not a substitute for a mind |
| Judgment | `#first-choice`; “During an ordinary test, the bird adjusted its stance” | Reconciled `06-choice`; anticipate loose support with supported weight transfer |
| Ending | `#the-sentinel` | Reconciled `07-sentinel`; floor-supported beside CRT |
| Historical lineage | `#visual-record`, `#media-crt`, `#media-awakening` | Preserve historical asset/alt; distinguish any later study by date/status |

The character owner's candidate01 is on HOLD per lead review: long hanging wing plates and ambiguous shoulder band. Do not integrate it or derive poses. Scene acceptance follows the corrected shared reference, not the presence of a matching filename.

## Review-boundary defect and scoped fix

The untracked mixed package contains nine development HTML pages. Initially its eight social layouts lacked robots noindex. The normal search rebuild included those eight candidates (160 -> 168 entries), and universe generation propagated them. Only this run's generated contamination was reversed; candidate files were untouched. A transient Windows invalid-argument write error on `universe/index.html` cleared on one retry; cause is unknown.

The lead then authorized the local owning-generator fix. `assets/murderbird/v2/build-library.py` now uses one `social_layout()` template with robots noindex for both full builds and `--social-html-only`. The latter reads the existing package manifest and refreshes only social HTML: it never writes masters, derivatives, social rasters, gallery, or provenance. It was run twice. All eight layouts retain noindex; search and universe return to their original public inventory. No broad indexer changes were made.

Remaining failure: `scripts/validate-site.py` still scans `assets/murderbird/v2/index.html` and `social/01-maker.html` through `08-hero.html`. Its `SKIP_DIRS`/HTML inventory does not distinguish this development folder; noindex affects sitemap eligibility, not shared-shell/source-manifest requirements. The result is 44 errors, all on these nine review pages (down from 52 before noindex). Do not add fake analytics, public metadata, or site chrome to card-rendering templates to satisfy a scanner. Lead must approve a documented development-path relocation/boundary correction.

## Manifest adoption and relocation proposal — not executed

Reuse `assets/murderbird/v2/coordination/asset-register.json` and its `build-register.py`; both inspected. Preserve `assets/murderbird/v2/manifest.json` as package provenance. Video task authored the original eight-scene library and Blender stage; illustration ownership is subsequent stewardship. Do not relabel original authorship.

The consolidated register is a snapshot, not an acceptance list. Its cutout status is filename-derived and its hasAlpha field only checks band presence; these are not substitutes for independent pixel-alpha verification. Before publication, extend the same record with accepted reference version, anatomical landmarks, scene anchors, actual public paths, derivatives, captions/transcripts, audio status, and review decisions. Refresh existing hardcoded paths only after relocation is approved.

| Current material | Proposed destination | Release implication |
|---|---|---|
| Image masters/references | `assets/img/library/murderbird/` with stable descriptive filenames | Current release builder includes image extensions under assets/img; choose preservation/publication deliberately |
| Generated WebP | `assets/img/webp/` | Regenerate through owning pipeline, proportional sizes, no upscale |
| Generated JPEG/social PNG | `assets/img/library/murderbird/` | Keep original/master relationship explicit; captions remain real page text |
| Human Markdown reports | `assets/docs/murderbird/` | Non-runtime documentation |
| Production and register tooling | `scripts/` with murderbird-prefixed kebab-case names | Update relative-path assumptions and preserve attribution |
| QA/register snapshot | `assets/audit/murderbird/` | Not public runtime data; retain package metadata alongside preserved production sources |
| HTML review gallery/social render templates | `.local/murderbird-review/` | Existing scanner exclusion; local review only, retain noindex; preserve original package before approved move |
| Blender/original motion/audio | Existing `C:/Users/jamie/Documents/murderbird-production/2026-09-06/` pending preservation plan | Not website runtime; no blind commit of large originals |
| Accepted web clips/tracks | Proposed `assets/video/murderbird/` and `assets/audio/murderbird/` | NOT currently included by `scripts/build-release.py`; explicit allowlist extension and regression test required before integration |

Do not execute moves while another lane is producing against existing paths. Require old-to-new hash mapping, dependency rewrite, rebuild, and owner/lead-approved preservation before cleanup. The current release builder allowlists assets/css, data, downloads, img, js, vendor, and .well-known; it does not deploy `assets/murderbird/v2/`, video/audio folders, or Blender files. Keeping candidates out of sitemap is not sufficient to guarantee a working media release.

## Local checks

Commands use `C:/Users/jamie/AppData/Local/Python/bin/python.exe` with PYTHONUTF8=1; scripts are those at the baseline SHA, with the scoped untracked builder edit above. These checks are local, not CI or live-edge evidence.

| Check | Status | Evidence / limitation |
|---|---|---|
| `scripts/build-site.py --check` | PASS | 36 generated pages current |
| `scripts/build-search-index.py --check` | PASS after noindex fix | 160 entries; normal owning rebuild, no candidate URLs |
| `scripts/sync-universe-map.py` through search build | PASS | Universe current, no retained universe diff |
| Skill `scripts/inventory-routes.py --root . --sitemap sitemap.xml` | PASS | 31 sitemap routes, including MurderBird |
| `scripts/validate-site.py` | FAIL | 44 errors on nine development-only v2 HTML pages; no MurderBird story error reported |
| `scripts/check-links.py` | PASS | Zero broken links; report `assets/audit/links-report-2026-09-06.json` |
| `scripts/cache-bust.py --check` | PASS | Zero substitutions across 155 scanned HTML files at execution |
| `assets/scripts/check-contrast.py` | PASS | Existing theme token audit; not a rendered-media contrast claim |
| `scripts/audit-site.py --quiet` | WARN | Initial run reported 121 issues while development pages were present; not an acceptance gate pass. Its tracked default report overwrite was reversed to preserve the standing report |
| `git diff --check` | PASS | No whitespace errors; platform line-ending warnings are separate |
| Browser/mobile/light-dark/keyboard/reduced-motion/media failure | NOT RUN | Structural gate remains blocked; no new layout or media implemented |
| CI/Pages/live edge | NOT RUN | No release authorized at this checkpoint |

Final retained tracked diff is source and generated story only. Search and universe have no content diff; the excerpt-based story search entry is unchanged because edited paragraphs occur beyond its excerpt. That is expected, not evidence that later paragraphs are full-text indexed. Additional lane-owned changes are this report, the untracked builder and eight social HTML layouts. Existing concurrent libraries, lead brief, reports, and output files are not staged or altered by this lane. Machine link-check output is generated evidence, not hand-edited.

## Next illustrated release

First resolve the review-directory scanner boundary. Then accept one character reference and a small coherent scene set through the lead. Add poster-quality stills at chapter transitions, retaining uninterrupted paragraphs and original history. Add a restrained homepage invitation and matching story social metadata only within the next approved scope; verify locale parity explicitly. Do not publish all studies or replace unrelated project identity.

Motion follows approved stills, prioritizing first choice. Require actual playable files, correct weight/props/era, local posters, appropriate captions and descriptive transcripts, explicit play controls, silence/stillness default, independent sound control, and no competing tracks. Complete prose survives missing media, disabled JavaScript, and reduced motion. Optional three-era exploration uses keyboard-operable controls and explanatory text, not geometry morphs between inconsistent studies.

Return source/generated diff, consolidated asset evidence, unchanged unified brief, browser results, structural/search/release-boundary checks to the lead for one coordinated release. No publication readiness is claimed by this checkpoint.

## Follow-up: review boundary resolved

The lead authorized relocation of only nine development HTML files. Before mutation, every resolved source, destination, and backup path was checked to remain below C:/Users/jamie/OKH-Local/04_GitHub_Mirrors/overkill-hill/. Destination and backup collisions were checked and would fail the operation. No directory tree was moved or deleted.

For each relative path below, the exact mapping is:

- Old: `assets/murderbird/v2/<relative-path>`.
- Active: `.local/murderbird-review/<relative-path>`.
- Byte-preserved backup: `.local/murderbird-review/backup-2026-09-06-pre-relocation/<relative-path>`.

After copying each backup, SHA-256 was checked against the old source. After moving each source to its active destination, SHA-256 was checked again. All nine matched. Subsequent HTML-only generation updated active relative links; the backup retains exact original bytes and historical links. No artwork, raster, metadata, or Blender file moved.

| Relative path | Original = backup = immediately moved SHA-256 |
|---|---|
| `index.html` | `bf415dd0c774f989f8f8d8be559f96d0231fadbc1f5150c23e43bf20385c1073` |
| `social\01-maker.html` | `1ef9a185113711aa130b28d250c894073852781e4e49dfcc2f9e0d5380125e69` |
| `social\02-water.html` | `809e3b2ab9d846b4edb5c3199ec59c4ecea8a1f57d6eb0c0f84dd08d110d1c76` |
| `social\03-recovery.html` | `89814b455ef9d856297218dc330c2c78cd3fc56e234fcca4c59c7155182a7331` |
| `social\04-mechanic.html` | `392c8a97c42d19e97c29807d2ab07519cccd56ac682e3d6103c20aee501736d3` |
| `social\05-heart.html` | `34aa2c4304f263011ad40b1b8a9f350d559041672c45343bba1ea7ded6fb7e6c` |
| `social\06-choice.html` | `2e675a720473641d9bbe4dbba030bab0a0f189397e9961272c1883bd6e2fd779` |
| `social\07-sentinel.html` | `ad0c8eec2a46b885ab1db6cfece4935d5626bdf18b8084a082684f8d33f96356` |
| `social\08-hero.html` | `1d03dc75c3831ed4328287a73ba71520ccf3ad26cbadf33acb0b7e8006adf1ef` |

Builder changes: all gallery/social writes now pass through `write_review()` into `.local/murderbird-review/`, retargeting href/src/srcset to existing v2 assets/documents. Direct HTML writes under the production package are rejected. Full builds share this destination and emit current review layout paths in future manifests. The existing provenance manifest was not rewritten; its old HTML layout pointers are explicitly documented as historical in README. `--review-html-only` refreshes all nine pages; `--social-html-only` refreshes eight. README and `rasterize-social.js` now use a repository-root local server and excluded review URL; raster output remains in the original v2 social directory. No rasterization was performed.

`tests/test-murderbird-review-boundary.py` exercises a real full build in an isolated temporary fixture, repeats markup-only regeneration, resolves generated local links, checks image and manifest byte stability for markup-only runs, rejects direct public-package HTML writes, and runs the real search scanner to prove review output is absent. It passes. Production rasters were not regenerated to test the full build; the temporary test uses an eight-by-six-pixel fixture, not candidate artwork.

The real nine relocated pages retain noindex, all 70 inspected href/src/srcset targets resolve, no HTML remains beneath `assets/murderbird/v2/`, and all 64 production image records still match manifest hashes. Original bytes remain recoverable in the dated local backup; `.local` is ignored and excluded from the Pages artifact.

### Current post-relocation checks

| Check | Result |
|---|---|
| Boundary behavioral regression | PASS, one test covering full and markup-only generation |
| `scripts/validate-site.py` | PASS, exit 0; no scanner exclusions or public validation rules changed |
| `scripts/audit-site.py --quiet --report .local/murderbird-review/audit-report.md` | PASS, 60 pages, zero issues; standing tracked audit report untouched by this follow-up |
| `scripts/build-search-index.py --check` | PASS, 160 entries; story present, no candidate URLs |
| `scripts/build-site.py --check` | PASS, 36 generated pages |
| `scripts/sync-universe-map.py --check` | PASS, current |
| `scripts/check-links.py` | PASS, zero broken links; existing noindex boundaries retained |
| `git diff --check` | PASS; CRLF advisories are not whitespace errors |

Post-relocation lane file delta: two story files; this checkpoint; untracked v2 `build-library.py`, `README.md`, and `rasterize-social.js`; new `tests/test-murderbird-review-boundary.py`; nine relocated/regenerated ignored HTML files and nine ignored backups. No metadata/raster/Blender mutation, staging, branch switch, publication, or candidate02 integration. Candidate02 remains HOLD per the lead. Browser-rendered review and CI/live release are not claimed for that boundary checkpoint; the subsequent hero browser check follows below.

## Follow-up: candidate03 local story hero

Authority: unified-direction v1.2 and explicit lead assignment. Candidate03 is accepted as an illustrative production reference only: head, silhouette, compact wing/rear contour, modern materials, and floor staging. It is not Jamie's final-art approval, certified 2.0 m geometry, a mechanical rig, or deployment acceptance. Its shoulder remains a narrative constraint without inventing a cross-wing strap or asserting hidden details.

Source: `assets/img/library/murderbird-unified-master-candidate-03-2026-09-06.png`, independently viewed and SHA-256 checked: `538c51bcdbf5bfce95a0932fdbbb0f5868b446f4985346d15e6cacd32430e633`. Source dimensions are 1536 x 1024. The source was not altered.

The old hero conversion script is archived, not an active pipeline. Added `scripts/build-murderbird-hero.py` as the narrow owning delivery pipeline. It refuses a changed source hash, applies proportional resize/WebP encoding only, does not crop or upscale, and supports a read-only source/dimension/format check. Outputs under `assets/img/webp/`:

| Filename suffix after `murderbird-unified-master-03-2026-09-06-` | Dimensions | Bytes |
|---|---|---|
| `480.webp` | 480 x 320 | 19,800 |
| `960.webp` | 960 x 640 | 75,222 |
| `1536.webp` | 1536 x 1024 | 173,666 |

Changed only the story's existing `#media-hero` image in authoring source and regenerated HTML, retaining earlier reviewed prose. It now has the three-size srcset, explicit 1536 x 1024 dimensions, accurate visible alt text, eager/high-priority loading, and sizes matching the unchanged shared hero layout (260px mobile, 320px desktop). Both feet and the CRT remain in the uncropped composition. Historical gallery artwork is unchanged. No social derivative was chosen, so head/Article social image references intentionally remain the existing truthful historical image rather than claiming a new share-card release.

The existing consolidated `coordination/build-register.py` now registers this exact path AND expected hash, with explicit lead authority, v1.2 scope, limitations, local story placement, and delivery provenance. Regenerated the same `asset-register.json` (24 master records including one unified reference); no third catalog or filename-based approval of other studies. Package `manifest.json` remains preserved as original provenance.

### Browser QA

Flow: local story loads -> theme control changes theme -> full-body image remains legible and proportionate -> Read the story reaches `#the-maker`.

Used existing OverKill Hill design tokens and hero classes only (no CSS/JS changes or supporting style profile). CSS signal extraction and source inspection confirmed the current declared styles. Browser plugin/skill absent; existing Playwright CLI used, with no new browser dependency installation. URL: `http://127.0.0.1:5387/writings/murderbird/`, dedicated local no-cache server. Chromium viewport matrix: 1440 x 1000, 390 x 920, 320 x 920, each in dark and light mode.

All six states: correct page title/content; no blank page or framework overlay; horizontal document width equals viewport; image ratio remains 3:2; no crop; visible hero brand phrase does not split; theme control changes actual data-theme. Console warning/error query: zero messages, pageerror listener: zero. Read the story changes URL to `#the-maker` and the Maker heading is visible. An initial test assumed a two-state theme toggle and timed out; corrected test follows the actual system/light/dark cycle, then passed without changing site behavior.

Visual review: desktop dark and narrow light screenshots inspected directly. Both feet, compact rear contour, head and CRT remain visible. At 320px the existing stacked hero places the illustration below the first viewport; a scrolled screenshot confirms full-body framing. At current shared dimensions the artwork is intentionally modest (320 x 213 desktop, 260 x 173 mobile), not a full-width cinematic redesign. Close-up shoulder topology cannot be assessed at this display size. No claim of exact scale or mechanical validation.

Evidence directory outside repo: `C:/Users/jamie/.codex/visualizations/2026/09/06/01a0744b-8fb9-7b10-9925-72b509f1c05e/`. Files: `murderbird-hero-{1440,390,320}-{dark,light}.png`, plus `murderbird-hero-320-light-scrolled.png`; repeatable local QA driver `murderbird-hero-qa.js`. Screenshot viewport/frame observations do not certify every site brand-name occurrence or other browser engine.

Post-change checks: hero delivery `--check` PASS; generated HTML freshness PASS (36); search freshness PASS (160); structural validator PASS (56 HTML pages, zero errors, existing warnings); diff whitespace PASS. Browser evidence covers the hero and two interactions only, not the later media player, reduced-motion media failure, full-site accessibility, cross-browser/locale parity, CI, or live deployment. No media beyond the hero, no water/heart/sentinel selection, no staging/commit/merge/publication.

## Follow-up: balanced hero and three-scene illustrated preview

The lead authorized a story-only visual correction after reviewing the thumbnail-sized first hero. All new hero CSS is scoped to `#murderbird` in the existing `assets/css/theme.css`; other heroes retain their rules. The two-column layout now gives the complete illustration 514.4 x 342.9 pixels at a 1440-pixel viewport and 499.8 x 333.2 at 1080. The former 72vh minimum is removed for this story; vertical padding is bounded. Stripes are reduced to 8% opacity, blueprint to 20%, and those decorative animations are disabled for this hero. Existing brand tokens/fonts remain; text uses theme foreground colors. No absolute text overlays.

Below 1025px the layout stacks with 24px side margins and full available image width (342px at390,272px at320). The full composition is preserved. A brand-name split exposed by the narrower text column was fixed with nonbreaking spaces plus a story-scoped nowrap span. Title size is bounded to retain comfortable narrow margins. Real links/buttons remain; focus-visible has a 3px accent outline. No forced above-fold layout at320.

Measured contrast using computed foreground/solid CTA colors and theme background with each 8%-opacity stripe: primary CTA minimum4.63:1; secondary CTA14.33:1 dark/16.03:1 light; hero ordinary text11.45:1 dark/13.67:1 light; eyebrow minimum5.58:1 dark/5.79:1 light. The text model does not sample individual blueprint-grid pixels; visual screenshots separately show its restrained treatment. Existing finite theme transitions are allowed to settle before screenshots/measurements; initial transitional captures were replaced, not presented as settled contrast evidence.

Eight settled hero states passed:1440/1080/390/320px in both themes, correct page identity, no blank/overlay, no overflow,3:2 full image, intact hero brand phrase, and no console/page errors. Read the story navigates to `#the-maker`. Keyboard focus from Read the story followed by Tab reaches Explore the imagery with visible3px outline; Enter reaches `#visual-record`. Final screenshots are `murderbird-hero-balanced-{1440,1080,390,320}-{dark,light}.png` in the evidence directory above. Desktop light/dark and narrow dark were directly inspected.

### Three narrowly accepted scenes

Lead acceptance is local illustrated preview only, not Jamie final-art approval, certified engineering/chemistry, or public release. All three sources were directly viewed and independently checked against the authorized hash. Added them to the same owning delivery pipeline using `--asset water|heart|sentinel`, and to the same consolidated register using explicit path/hash/scope records. There are now27 master records, with exactly these three new scene acceptances; no filename-derived broad approval.

| Scene source under `assets/img/library/` | Accepted SHA-256 | Placement and caption boundary |
|---|---|---|
| `murderbird-unified-water-candidate-2026-09-06.png` | `0db88f0529288a9c6032662a9fb9e62d1ae077322241c4d9bd2c5a8eb915c117` | `#media-water`, after `#the-water` prose; inert partly submerged body and sediment/mineral history, no exact chemistry/internal construction claim |
| `murderbird-unified-heart-candidate-2026-09-06.png` | `9430f91e3cd3fc8223297720a0f57ec1c46e9c8245cfba91495e9c362029fea9` | `#media-heart`, after power discussion immediately before `#the-mind`; power inspection, not completed heart plus mind |
| `murderbird-unified-sentinel-candidate-2026-09-06.png` | `d6153907884045e824e3be9cd02a7a446fb75f6e8b35a246918cf11ac620667e` | `#media-sentinel`, after ending prose inside `#the-sentinel`; watches operator beside CRT, no invisible screen-text claim |

Each has480x270,960x540,1536x864 WebP variants under `assets/img/webp/murderbird-unified-<scene>-2026-09-06-<width>.webp`. No crop/upscale/master modification. Bytes by ascending size: water22514/92500/188054; heart23908/88482/179112; sentinel19858/71104/149086. Hashes and dimensions are in the consolidated generated register. All three delivery `--check` runs passed.

Semantic figure/figcaption, truthful alt text, explicit dimensions, lazy loading and async decoding are used. Scene CSS is scoped to their story sections and `.murderbird-scene`, with width100%, height auto, restrained2rem margins and theme-aware captions. Browser measurements confirm content-column widths744.2px desktop,342px at390,272px at320; full16:9 frames remain uncropped. All73 narrative paragraphs and previous anchors remain. Historical sigil unchanged. Zero video players, no visible placeholders, no autoplay/audio.

Scene QA:18 combinations (three scenes x1440/390/320 x dark/light), all decoded, no horizontal overflow, correct full-column image ratio, alt/caption/loading present, intended section parents, Heart immediately before `#the-mind`. Reduced-motion state retains all73 paragraphs and three figures. Screenshots `murderbird-scene-<water|heart|sentinel>-<1440|390|320>-<dark|light>.png`; desktop heart/light, mobile sentinel/dark and water/light inspected directly. Tiny mobile views show scene composition, not a claim that close-up engineering details are legible.

### Consolidated local verification and generated collateral

- PASS: structural validator, zero errors (32 standing warnings); cache-bust freshness across146 HTML files; generated HTML freshness36; search freshness160; universe freshness; links zero broken/style issues; audit zero issues (`.local/murderbird-review/illustrated-preview-audit.md`); diff whitespace.
- PASS: `node scripts/accessibility-qa.mjs --base-url=http://127.0.0.1:5387` completed successfully:4 representative pages and31 public routes. This is the repository's bounded keyboard/focus/ARIA/reduced-motion regression, not comprehensive WCAG certification.
- CSS owning fingerprint pipeline updates67 HTML references per hash change. Independently normalized diffs confirm66 other tracked files differ only in the CSS fingerprint (includes shared head, templates, locales and published pages). The three tracked files with substantive changes are stylesheet, story authoring source, and generated story. Source/search/universe builders were run; no extra search/universe content changes.
- Untracked delivery delta includes the accepted sources owned by their lanes, twelve WebP outputs across hero+three scenes, narrow delivery builder, same register builder/output, accumulated checkpoint/test/review-boundary changes. No blanket staging of concurrent work.
- No social/Article image update, homepage feature, new motion/sound, locale story publication, CI, merge, push, or live acceptance. Existing head imagery remains accurate to historical material; social composition is a separate future choice. No Firefly session initialized in this task.

## Subsequent homepage, social, and five-scene preview checkpoint

This section supersedes the earlier three-scene/no-homepage/no-social delivery state, not its recorded history. Work remains uncommitted local preview on main at `2d7e92d23fcbe875c7421d4509109bffd22b0c48`; no push, merge, deployment, Firefly session, video upload, or audio integration occurred in this lane.

### Homepage continuity and translation boundary

English authoring source `site-src/pages/index.main.html`, generated `index.html`, and existing `fr/index.html`, `de/index.html`, `es/index.html`, `es-mx/index.html` now use accepted reference03's existing proportional WebP derivatives. Business headline, copy, project/manifesto buttons and existing layout remain unchanged. The existing hero visual maximum width is retained. One restrained story link sits below the image; all four locale invitations explicitly state that the destination story is English and link to the existing `/writings/murderbird/` with `hreflang="en"`. No localized story route, hreflang cluster, sitemap route, or language-publication status was invented. The en-GB homepage was outside this bounded assignment and remains unchanged except generated fingerprints/policy.

The four exact-pair skills were invoked but their fail-closed prerequisites did not pass: project FR/DE/ES dictionaries and approved profiles/single-pair records were absent; the existing ES-MX profile was provisional with a placeholder sample. The coordinating task expressly directed a local-preview plain-text fallback for the eight changed alt/CTA units only. Each was translated directly from en-US independently, preserving MurderBird and URLs. No owner-approved profile, native certification, completed exact-pair workflow, or approval record was fabricated. Status is **model-translated, native review not performed**. Evidence with exact source/target text, hashes, revision, direction, protected terms and missing prerequisites is `i18n/pilot/murderbird-homepage-preview-2026-09-06.json`, generated by the bounded QA runner. Native-language review remains outstanding.

### Standalone story share raster

- Output: `assets/img/og/murderbird-story-share-2026-09-06.png`, actual1200x630 PNG,449979 bytes, SHA256 `d6fefa4a22b07f4427a73c1e55ba236c05771bac1b8394274475c343f2d86a14`.
- Source: accepted03, SHA256 `538c51bcdbf5bfce95a0932fdbbb0f5868b446f4985346d15e6cacd32430e633`. Complete art is proportionally scaled to680px wide, no cropping or model-rendered typography. Separate HTML text uses the existing OKH palette and actual Alfa Slab One, DM Sans and JetBrains Mono fonts.
- Reproducible generator: `node scripts/build-murderbird-story-social.mjs`; `--check` rerenders and compares the raster byte hash. It fails if source identity, loaded font families,1200x630 canvas, image aspect ratio or text overflow checks fail. Chromium151.0.7922.34 was used. Exact reproducibility is renderer/font-environment dependent; the check does not silently certify another environment.
- Review HTML is only `.local/murderbird-review/social/murderbird-story-share.html`, noindex and outside public scanning/release boundaries. The generator embeds the accepted image in that local review file; no third asset catalog was created.
- Only MurderBird's `site-src/pages.json` social fields and `site-src/pages/writings/murderbird/index.extras.html` Article image changed. OG dimensions/type/alt, Twitter image/alt and Article image now resolve to the actual new raster. Other pages' share imagery is untouched. Browser verified the local raster serves successfully as image/png and all three records agree.

### Final two chapter stills

- `#media-mechanic`: `assets/img/library/murderbird-unified-mechanic-candidate-2026-09-06.png`, SHA256 `0bd7c79510be9eeef024f8861a7576b777a7f5de5710523e8d2ab039d03c65f9`. Placed in `#the-mechanic` after the paragraphs describing industrial repairs/lathe work, not the recovery passage. Caption identifies industrial repairs around ancient bronze and continued reliance on workshop power. No awakening claim.
- `#media-maker`: `assets/img/library/murderbird-unified-maker-clean-candidate-2026-09-06.png`, SHA256 `93966eb269ae9f8d8d00e05e913cbb23f7656204e6f3fdf7fd26e8a39ca0cbb9`. Placed late in `#the-maker`, after completed-body/internal-mechanism description and immediately before the demonstration paragraph. Back-view hooded Maker with lowered intact hammer is a quiet inspection, not the hammer-breaking event. Earlier Maker01/02 were not integrated.
- Both are explicitly lead-accepted for local illustrated preview only. New `--asset maker` and `--asset mechanic` cases in `scripts/build-murderbird-hero.py` preserve exact source hashes and produce480/960/1536 WebPs. Maker sizes480x320,960x640,1536x1024; bytes38504/134728/296716. Mechanic sizes480x270,960x540,1536x864; bytes36180/120204/236264. All image frames remain full and uncropped; no masters edited.
- Both use the established semantic figure, lazy/async loading, explicit dimensions, accurate alt/caption and narrowly scoped story CSS. The same generated asset register now records five accepted chapter scenes plus reference03 and the social composition. It retains historical collections without promoting them to canonical art. Thirty image records include the derived social composition, not thirty newly accepted masters.

### Consolidated evidence and scope

`scripts/murderbird-integration-qa.mjs` verified30 homepage combinations (five routes x1440/390/320 x dark/light), English-destination link transitions from all five pages, and30 chapter combinations (five figures x1440/390/320 x dark/light). All images decoded, ratios remained correct, no horizontal overflow occurred, two original business buttons remained on every homepage, and zero browser page errors occurred. Reduced-motion emulation remained enabled. Full screenshot set and detailed results are under `.local/murderbird-review/homepage-qa/`. Direct visual inspection included English desktop dark, French320 light, Maker desktop light/mobile dark and Mechanic mobile light. Mobile frames communicate composition, not detailed engineering legibility.

The QA record's `paragraphs:76` counts three era-label paragraphs plus73 narrative paragraphs; the narrative was not rewritten or shortened in this pass. There are five chapter figures plus the hero and historical gallery; zero video elements and no placeholder players. Prior three-scene tests are supplemented, not contradicted, by this expanded set.

PASS: structural validator56 HTML/zero errors/32 standing warnings; generated HTML36; search160; FR search regeneration and locale-link gate; CSP policy freshness56; cache freshness146 HTML/zero substitutions; universe freshness; links zero broken/style issues; whitespace diff; social deterministic render check; bounded accessibility QA4 representative pages and31 public routes. These are local checks, not live/CI/deployment or comprehensive WCAG certification.

One intermediate CSP failure was initially suspected to be unrelated because the validator named telling-forward. Inspection corrected that interpretation: `scripts/csp.py` hashes all inline scripts, including Article JSON-LD, into the shared policy. Changing this story's Article image legitimately invalidated the shared hash list. The owning CSP generator and site builder were rerun; checks are now green. No policy allowance was loosened. `_headers` remains a repository declaration, not evidence that GitHub Pages serves it.

Normalized tracked-diff classification at this checkpoint:13 substantive content/source/data/style paths, two generated CSP declarations (`_headers`, `config/csp-policies.json`), one generated link-count report, and61 other files whose only changes are stylesheet fingerprints and/or generated CSP meta. The content paths are theme CSS; English/FR search indexes; English/FR/DE/ES/ES-MX homepages; `site-src/pages.json`; homepage source; story main/extras sources; generated story. Link-count report reflects exactly five added homepage links. Existing standing audit/universe source files have no content diff. New media, builders, provenance, registry and test/report artifacts remain untracked alongside other lanes' work; no blanket staging or cleanup occurred.

Release limits: lead acceptance is not Jamie final-art approval; translations lack native review; exact2m geometry and hidden mechanisms are not certified; audio/video remain unintegrated. Firefly upload remains under the character lane and its user-permission boundary. No claim of a completed audiovisual experience or live rollout is made.
