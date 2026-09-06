# MurderBird story page: local validation

## Current expansion release candidate: September 6, 2026

This section supersedes the historical local-draft receipt below. The release
candidate is on `codex/murderbird-era-expansions`, based on
`b9bfcacd74ab80d76e1bfce88325bcee7c4fd98d`. Commit-specific CI, squash-merge,
and deployment receipts are recorded by the associated GitHub pull request
and Pages workflow; this document does not predeclare their success.

- Story: 5,266 whitespace-delimited words in 73 narrative paragraphs.
- Era One: 1,728 words. Era Two: 1,745 words. The later awakening and ending
  remain unchanged. Paragraphs remain 63-77 words; supporting roles remain
  unnamed and genderless. Reading estimate: 21-27 minutes.
- Era One adds uncertain fossil reconstruction, failed flight experiments,
  and conflict with the court. No real Babylonian terror-bird find is claimed.
- Era Two now begins with a fictional illicit excavation in 1853, private
  transport and collecting, then English mechanical restoration in 1873.
  Its buyer, broker, transactions, and discovery are fictional, not allegations
  against named historical people or institutions.
- Historical background: [British Museum transport account](https://www.britishmuseum.org/blog/introducing-assyrians)
  and [Metropolitan Museum excavation history](https://www.metmuseum.org/essays/the-rediscovery-of-assyria).
  Fossil anatomy reference: [Pachystruthio study](https://doi.org/10.1080/02724634.2019.1605521).
- Source, generated HTML, reading estimate, and generated search index are
  updated together. Existing article/social metadata remains intact. Optional
  word-count and modification-date JSON-LD additions were withdrawn because
  their global CSP hash churn unnecessarily invalidated locale baselines.
  No new imagery, styles, dependencies, or security policy changes.

Local browser checks against the repository preview on port 5027 passed:
310 responsive cases across 31 routes and ten widths (320-1920px), all 31
public routes at 320px, and accessibility checks across four representative
pages plus 31 public routes. External resources are blocked by these local
suites, so they do not prove analytics receipt or third-party availability.
Structural, generated-page/index, cache, internal-link, static-audit, and
contrast checks passed during the expansion review. Existing locale warnings
remain outside this story change. There are 31 sitemap routes and 24
intentional noindex exclusions, with no broken internal links.

Prior archive refs, stashes, and unrelated recovery history are preservation
holds, not cleanup targets. Only the verified merged feature branch should
be removed after release. Unavailable historical image binaries and further
image/video work remain separate from this prose release.

## Historical delivered-page receipt (before the era expansions)

- Title: The MurderBird: What the Water Kept.
- Route: `/writings/murderbird/`.
- Authoring source: `site-src/pages/writings/murderbird/index.main.html`.
- Page metadata: `site-src/pages.json`; structured data: adjacent `index.extras.html`.
- Generated output: `writings/murderbird/index.html`.
- Revised story prose: **2,967 whitespace-delimited words**, within the requested 2,400-3,200 range. The original release contained 2,444 words under its earlier token-count method.
- Current count method: BeautifulSoup selects the article's `p:not(.manifesto-og-label)` elements and splits their text on whitespace. Headings, era labels, hero, navigation, captions, and footer are excluded.
- Editorial continuity revision: 42 narrative paragraphs, 63-77 words each, with four or five sentences per paragraph. Related actions and observations now develop together; chapter anchors, typography, artwork, and the following sidebar remain unchanged. Desktop 1440px and mobile 390px layouts passed local overflow checks.
- Three eras remain explicit: Bronze Age Mesopotamia, 1873, and 2025. The third supplies independent onboard power and processing, while retaining ancient bronze and industrial machinery.
- Supporting characters remain unnamed and genderless, identified by role. A case-insensitive whole-word check found no he/she/him/his/her/hers/man/woman/boy/girl in story prose.

## Style and integration

Applied the OverKill Hill brand profile v1.1.0 through existing shared classes, not a new stylesheet. Matched the GitHub manifesto source's hero, blueprint, stripes, typography, sidebar, and gallery vocabulary. Preserved the manifesto narrative; added a story link in its hero and a card in the writings hub. Added the page to the sitemap and regenerated search data.

Existing local artwork is reused and identified as the original sigil and a September 2026 study. No imagery was generated. Future media insertion points are HTML comments, not empty players. Video handoff requires native controls, no autoplay, a local poster, captions for speech, and an adjacent transcript.

## Environment and checks

Local working tree on `main`, based on `bd11085dc639481fc52933221384f552b5825ae6`. This is uncommitted local work, not a deployed release. GitHub plugin read the canonical manifesto source. Existing unrelated staged `.playwright-cli/` files and the index were left alone.

Python command below means `C:/Users/jamie/AppData/Local/Python/bin/python.exe`, with `PYTHONUTF8=1`. Browser base URL: `http://127.0.0.1:5011`.

| Status | Command | Evidence |
|---|---|---|
| PASS | `python .agents/skills/okhp3-site-release-validation/scripts/inventory-routes.py --root . --sitemap sitemap.xml` | 31 public routes, including MurderBird |
| PASS | `python scripts/build-site.py --check` | 36 generated pages current |
| PASS | `python scripts/build-search-index.py --check` | 160 entries current |
| PASS | `python scripts/validate-site.py` | No errors or new voice warnings; existing locale/voice warnings remain |
| PASS | `python scripts/audit-site.py --quiet` | Zero issues; `assets/docs/audit-report.md` |
| PASS | `python scripts/check-links.py` | Zero broken links; 31 sitemap URLs; `assets/audit/links-report-2026-09-05.json` |
| PASS | `python scripts/cache-bust.py --check` | No stale fingerprints |
| PASS | `python scripts/check-csp.py` | Policies verified for 59 pages |
| PASS | `python assets/scripts/check-contrast.py` | Declared light/dark token pairs pass |
| PASS | `node scripts/phone-overflow-qa.mjs --base-url=http://127.0.0.1:5011` | All 31 public routes at 320px |
| PASS | `node scripts/responsive-qa.mjs --base=http://127.0.0.1:5011` | Playwright mode; 310/310 checks, 31 routes at 320, 360, 375, 390, 430, 768, 1024, 1280, 1440, 1920px; zero failures |
| PASS | `node scripts/accessibility-qa.mjs --base-url=http://127.0.0.1:5011` | Four representative pages and 31 public routes; keyboard, focus, ARIA, reduced-motion suite |
| PASS | `git diff --check` | Working-tree whitespace check |
| NOT RUN | CI, merge, deployment, live-edge checks | No commit, push, or publication performed |

Responsive details: `assets/docs/responsive-qa/results.json`. External resources are deliberately blocked by that suite, so this does not establish third-party font, analytics, or embed availability. Twenty-four intentional noindex exclusions remain outside the sitemap; their exact routes and reasons are in the link report.

The CLI browser also exercised the story link and theme switch. Local screenshots under `assets/audit/screenshots/murderbird-story-*.png` document desktop reading and mobile light/dark views. These screenshots are ignored QA artifacts, not website assets.

## Handoff

The working tree is the current result. Some earlier story files were already staged at intake; the index can therefore differ from these validated working-tree files. Review and stage only the coherent page change before a future branch/PR publication. Do not include unrelated browser artifacts. Recheck publication dates if release occurs after September 5, 2026.
