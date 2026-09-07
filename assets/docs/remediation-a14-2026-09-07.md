# A14: Phone hierarchy and selected-work proposals

Disposition: **PREPARED PENDING SELECTION AND INTEGRATION**, September 7, 2026.
Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`, initially clean and detached.
Branch: `codex/a14-phone-proposals`. No production SHA was assumed or verified.
Worktree: `/Users/okh/.codex/worktrees/a1a8/OverKill-Hill`.

## Reviewable result

Eight local rendered pages cover two alternatives across homepage, project
shelf, Mermaid Theme Builder detail and Contact. Open the
[comparison page](http://127.0.0.1:5144/.local/a14/index.html) while the local preview is running.
The generated HTML and screenshots remain in `.local/a14/`; they are deliberately
excluded from publication and Git. The committed generator and template recreate
the pages. Run QA to recreate the screenshots before viewing the comparison.

| Direction | Proposed hierarchy | Tradeoff |
| --- | --- | --- |
| A: Forge front door | Concise description and task choices, accepted MurderBird art, selected work | Preserves the large illustration near the top; selected evidence requires more scrolling |
| B: Work first | Concise description and task choices, compact selected-work rows, accepted art | Brings evidence into the initial phone screen; the large illustration appears farther down |

Both preserve the motto and existing artwork, provide a common 20px phone
content gutter, retain the full project shelf, and use one primary link per
new selected-work card. New copy and status examples are explicitly proposed.
Three examples distinguish a documented release, a prototype and published
writing. These are illustrative labels based on assessment/source evidence,
not an alternative status registry or a fresh external tool certification.

The detail preview retains its complete source main body and anchors, adding
only a release-evidence jump. Contact retains its complete main body and art,
with early email and Contact/Support jumps. Inquiry prompts remain A15 scope.
The shared production navigation, theme controls, search and TOC controllers
are not loaded into the review shell. This shell previews hierarchy, not the
final integrated runtime. Static detail TOC anchors remain available; working
production TOC behavior is untouched and needs regression after integration.

## Reproduction and observations

Local Chromium 151.0.7922.34, 390×844, normal baseline load:

| Measure | Baseline | A | B |
| --- | --- | --- | --- |
| Homepage heading x | 0px | 20px | 20px |
| Task entry y | Start heading 1563px | Task links 380px | Task links 362px |
| Selected work y | Heading 2332px | Section top 812px | Section top 486px |

These are geometry observations, not a controlled conversion experiment.
The baseline uses heading positions and proposals use section/nav positions;
the proposal review banner and simplified navigation also affect vertical
coordinates. The two review banners differ by one wrapped line at 390px.
All eight proposal page headings align at x=20px at phone widths.

Visual inspection of phone entry captures identified and corrected duplicate
template output, inherited shelf minimum-height whitespace, and extra detail
container padding. Final phone and desktop entry/full-page captures are named
`a-home-390-entry.png`, `b-projects-1280.png`, etc., under
`.local/a14/evidence/`. The accepted illustration is reused without modification.

Task observations are automated analyst walkthroughs, not recruited-user results:

- Both variants: keyboard Skip to content reaches `#main` with JavaScript disabled.
- Both variants: Inspect projects reaches the local shelf, Inspect project reaches
  the local detail, and the release jump reaches the preserved `#release` anchor.
- Both variants: Contact exposes the expected `mailto:contact@overkillhill.com`.
  No email was sent. The direct Try a tool destination is a link only; external
  tool behavior was not exercised.

## Validation

See the generated [compact QA record](../audit/a14-proposal-qa-2026-09-07.json).

| Check | Actual result |
| --- | --- |
| Proposal Chromium layout matrix | 32/32 pass: A/B × four pages × 320, 390, 768, 1280px |
| Layout assertions | No horizontal overflow, expected heading gutters, no duplicate IDs, no broken completed image loads, one primary action per new selection, early home choices |
| Fonts | Alfa Slab One and DM Sans available in the rendered matrix |
| No-JS task journeys | 2/2 pass; skip, shelf/detail, release anchor, email href |
| `build-site.py --check` | Pass: 36 generated pages current, using existing QA virtual environment |
| `build-search-index.py --check` | Pass: current index |
| `validate-site.py` | Pass: 56 pages, existing warnings retained |
| `check-locale-links.py` | Pass |
| `check-links.py` | Pass: zero broken links and style issues, sitemap boundaries unchanged |
| `cache-bust.py --check` | Pass after owning generator fingerprinted only the new template |
| `tests/test-release-package.py` | 9 tests pass |
| `git diff --check` | Pass |

Initial system-Python HTML checks could not import existing `bs4`; rerunning
with `/private/tmp/okh-overkill-hill-qa-venv-20260906/bin/python` passed.
The initial `check-cache-bust.py` invocation used a nonexistent name; the actual
`cache-bust.py --check` gate above was subsequently run successfully.
Browser startup and loopback serving required sandbox approval. Playwright was
read from the existing owner-checkout dependency installation; no files were
written there and no dependency was installed. Local Node was v26.0.0, not an
A08-approved LTS environment.

Unavailable/not performed: real phone hardware, Safari/VoiceOver, NVDA/Firefox,
recruited newcomer tasks, light-mode review, 200% text/zoom and short-height
acceptance, full integrated responsive/accessibility/search/theme/TOC/embed/CSP
regressions, CI, external tool functionality, and live deployment readback.
The matrix uses the dark palette and reduced motion; external embeds are blocked
in layout cases. This is not full accessibility conformance or release acceptance.

## Exact source scope and regeneration

- `assets/templates/a14/template--preview.html`: isolated static review shell
  using current shared stylesheet/fonts; experimental inline rules are local to
  this unshipped template, not a second production stylesheet.
- `scripts/build-a14-proposals.py`: generates the eight local pages from current
  `site-src/pages/{index,projects/index,projects/mermaid-theme-builder/index,contact/index}.main.html`.
  It replaces the preview homepage entry only and preserves the original deeper
  sections. Published English main sources and all locale pages are unchanged.
- `scripts/a14-proposal-qa.mjs`: reproducible browser captures and compact QA data.
- `scripts/README.md`: classifies both commands as manual local review tools.
- This handoff and the generated dated QA record.

Recreate with `python3 scripts/build-a14-proposals.py`, serve this worktree using
`HOST=127.0.0.1 PORT=5144 python3 server.py`, then run
`node scripts/a14-proposal-qa.mjs` with the existing Playwright installation.
The loopback review server is not approved for external exposure.

After selection, A21 must incorporate reviewed A11/A12 sources, transfer only
the selected scoped CSS into canonical `assets/css/theme.css`, and edit the
four authoritative English main sources as needed. Shared runtime changes remain
serialized by A21. Rebuild with the owning HTML/search/universe/CSP/cache tools;
never merge generated alternatives into production HTML. Detect affected locales
and apply exact-pair review while retaining indexing boundaries. No sibling sync,
branch publication, PR, main merge or deployment occurred.

## Remaining acceptance and selection questions

1. Owner selects A or B, or specific elements to combine, after reviewing the
   eight pages. No direction has been accepted or applied.
2. A11/A12 reviewed commits supply canonical maturity/evidence and Featured copy.
   Current inherited shelf claims and chronology below the new entry remain
   baseline content pending those packages. This deliverable cannot close them.
3. Observe a newcomer finding a usable tool, distinguishing a prototype from a
   documented release, finding the full archive, locating release evidence, and
   reaching Contact. Record confusion and backtracking, not invented task scores.
4. A21/A20 run the full selected-candidate regression and manual acceptance,
   including A15 coordination, before any publication decision.

Selection prompt: Which ordering makes the next useful action clearer on a phone,
while still feeling like OverKill Hill? Does A preserve enough practical access,
or does B defer the MurderBird farther than you want?
