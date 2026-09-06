# MurderBird story page: local validation

## Delivered page

- Title: The MurderBird: What the Water Kept.
- Route: `/writings/murderbird/`.
- Authoring source: `site-src/pages/writings/murderbird/index.main.html`.
- Page metadata: `site-src/pages.json`; structured data: adjacent `index.extras.html`.
- Generated output: `writings/murderbird/index.html`.
- Confirmed story prose: **2,444 words**, within the requested 2,400-3,200 range.
- Count method: BeautifulSoup selects the article's `p:not(.manifesto-og-label)` and `pre` elements; regex counts word tokens with internal apostrophes and hyphens retained. Headings, era labels, hero, navigation, captions, and footer are excluded.
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
