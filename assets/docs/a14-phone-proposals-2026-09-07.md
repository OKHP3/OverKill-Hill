# A14 phone presentation studies

Status: RENDERED PROPOSALS READY FOR OWNER REVIEW. X04/X08 remain open until
selection and implementation acceptance. Neither direction is approved for
production. This revision supersedes the preliminary layout checkpoint.

Architect refinement: concise visitor status with expandable provenance. This
updates both existing alternatives; it neither chooses A/B nor issues another
selection prompt. A11 reviewed the proposal-only contract in the task handoff.

Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`. A01/A02 are committed
in this baseline. The old audit description of uncommitted work is historical.

Verified A11 source contract: `73019eadafe25e1d763e6ef6dd223a5b67942202`,
the optional disclosure followup to `9bfe170badf3133fab8119643aafeb1f04d2d0c9`,
including its A06 source corrections. The builder reads that exact commit's
source fragments, registry and renderer into its own ignored preview directory.
It validates the 18-record registry and renders canonical summaries without
copying handwritten facts. It calls `render(..., disclosure=True)` and uses
`visitor_summary(record)` for verification. A14 adds only scoped classes and a
project-specific accessible summary name; it maintains no parallel wording
function. Every full summary retains source description scope,
review date, immutable evidence link and `Delivery: unknown` inside native
`details`, opened with "Status and source". One primary
action per project card is styled separately from supporting source links.

The visible line preserves `record.maturity` verbatim and adds "Operation
unverified" for software or "Delivery unverified" for other records. Unknown
shelf entries also retain the external-link or access-inquiry context. The
workbench retains its dated readiness and exact benchmark/RAG evidence summary
outside the disclosure because that limitation is material; the shared helper
does not add a redundant generic delivery phrase to that record. No independent
status table, shortened prototype qualification or stronger delivery claim was
introduced. On cards, the visitor description precedes the concise status.
The canonical node, source URL and review date are unchanged, available without
JavaScript, and excluded from the primary-action styling.

## Two directions

| Study | Treatment | Tradeoff |
| --- | --- | --- |
| A: Project-led | Compact, ruled project rows; selected work immediately follows the shorter hero; practical links appear above the accepted art on phones | Easier scanning, less visual separation between projects |
| B: Editorial | Existing dimensional project cards; selected work followed by featured writing before the longer orientation section | More editorial character, more scrolling below the selected set |

Both reuse the current static page shells, shared theme, Alfa Slab One / DM Sans /
JetBrains Mono roles, Forge colors, existing URLs, and accepted MurderBird picture.
Brand skill profile 1.1.0 was consulted; current canonical CSS supplies actual
tokens where the older seed profile differs. No new artwork or font was added.
The shared stylesheet and browser runtime are unmodified. Original manifesto,
locale boundaries, and article text/TOC are unmodified.

New homepage introduction is proposed: "AI tools, working methods, and the
evidence behind them." Longer original introduction and forge explanation
remain in the preview's native "More from the forge" disclosure. This is a
layout study, not a finalized preservation or editorial acceptance claim.

The verified A12 contract at `2074a969825e81e742d728b6816fb0adb364b445`
supplies "Featured from the Forge", "Featured writing", and its descriptive
subcopy. The selected article, dates, artwork and URLs remain unchanged.
Both Contact previews insert A15's exact optional prompt fragment from
`e9154af71eb8248cad2efcf2d44fa5d06bd0ad06` after the Central Time paragraph.
The email destination and support section remain intact; no email was sent.

## Rendered evidence

Screenshots capture the initial viewport, not the entire long page. Selected
work has a separate scrolled capture. Chromium 151.0.7922.34, reduced motion,
390 x 844 phone and 1280 x 800 desktop. Automated overflow checks also cover
320 x 844. These are emulated browsers, not physical phones or human sessions.

| Surface | A phone | A desktop | B phone | B desktop |
| --- | --- | --- | --- | --- |
| Homepage | [View](../audit/screenshots/a14-phone-proposals/a-home-390.png) | [View](../audit/screenshots/a14-phone-proposals/a-home-1280.png) | [View](../audit/screenshots/a14-phone-proposals/b-home-390.png) | [View](../audit/screenshots/a14-phone-proposals/b-home-1280.png) |
| Selected work | [View](../audit/screenshots/a14-phone-proposals/a-selected-390.png) | [View](../audit/screenshots/a14-phone-proposals/a-selected-1280.png) | [View](../audit/screenshots/a14-phone-proposals/b-selected-390.png) | [View](../audit/screenshots/a14-phone-proposals/b-selected-1280.png) |
| Expanded source | [View](../audit/screenshots/a14-phone-proposals/a-status-open-390.png) | Phone detail | [View](../audit/screenshots/a14-phone-proposals/b-status-open-390.png) | Phone detail |
| Project shelf | [View](../audit/screenshots/a14-phone-proposals/a-projects-390.png) | [View](../audit/screenshots/a14-phone-proposals/a-projects-1280.png) | [View](../audit/screenshots/a14-phone-proposals/b-projects-390.png) | [View](../audit/screenshots/a14-phone-proposals/b-projects-1280.png) |
| Skillz detail | [View](../audit/screenshots/a14-phone-proposals/a-projects-skillz-390.png) | [View](../audit/screenshots/a14-phone-proposals/a-projects-skillz-1280.png) | [View](../audit/screenshots/a14-phone-proposals/b-projects-skillz-390.png) | [View](../audit/screenshots/a14-phone-proposals/b-projects-skillz-1280.png) |
| Contact | [View](../audit/screenshots/a14-phone-proposals/a-contact-390.png) | [View](../audit/screenshots/a14-phone-proposals/a-contact-1280.png) | [View](../audit/screenshots/a14-phone-proposals/b-contact-390.png) | [View](../audit/screenshots/a14-phone-proposals/b-contact-1280.png) |

The generator writes only `.local/a14/`: eight HTML previews, one shared
preview stylesheet, source-hash manifest, expected summaries and a pinned
contract source snapshot. It does not write production
pages, authoritative sources or a competing production stylesheet. Every
preview has noindex/nofollow and a visible pending-status notice. The release
builder's existing allowlist excludes previews, this report, scripts and the
retained screenshots. No sitemap, search index or locale change is needed.

The dedicated `serve-phone-proposals.py` server stages a fresh tree from the
release builder's explicit inventory, then adds only the eight proposal pages
and preview stylesheet. Its URL space is `/proposals/`, never `/.local/`.
The server binds only `127.0.0.1`; it serves exact allowlisted files, rejects
private/dot/traversal paths and untrusted Host values, checks symlinks/reparse
points, and supports only GET/HEAD. It has no directory listing or report-writing
endpoint. The staging allowlist and contract source stay outside its HTTP root.
This corrects the initial reproduction instructions, which used the old
repository server. A18's hardened `server.py` intentionally rejects private
paths and is not changed or bypassed by modifying its configuration.

## Observations and checks

Confirmed local 390px measurements, including the review notice in proposals:

| Measurement | Baseline | A | B |
| --- | --- | --- | --- |
| Heading left edge | 0px | 16px | 16px |
| Early practical links | No equivalent hero group | y585 to y681 | y585 to y681 |
| Selected work heading | y2332 | y1026 | y1026 |

The existing task section begins at y1563 in the baseline. Both previews
move its practical links earlier, but retain the full existing section lower
down. Removing that duplication is a pending editorial decision. Geometry
supports earlier access, not a claim about conversions or task success.

- PASS: eight preview routes at each of three widths; 24 preview samples plus
  three baseline samples, no document overflow or page JavaScript errors.
- PASS: every rendered status summary and evidence URL matches the pinned
  A11 renderer; shelf record count matches registry membership; one primary
  action on every project card. An initial test expected 15 shelf records;
  that incorrect test assumption was corrected to derive the count from the
  registry, which declares 14. No product change was made to satisfy that count.
- PASS: each concise status is visible with its disclosure closed; keyboard
  Enter opens and closes every disclosure in the standard matrix, exposing the
  canonical text and leaving focus on its summary. No primary action is inside
  a disclosure. Supplemental checks also open/close the first disclosure on
  applicable pages with JavaScript disabled. These are scoped control checks,
  not a full keyboard journey or assistive-technology acceptance session.
- PASS: the five focused tests shipped with A11's pinned disclosure contract,
  executed in the ignored contract snapshot. They cover exact canonical content,
  visible material limits, record-driven wording, opt-in/idempotent rendering,
  and visitor description/action placement. Production default stays unchanged.
- PASS: eight additional phone samples with dark mode and JavaScript enabled,
  plus eight with JavaScript disabled and a requested dark system preference;
  no overflow or hidden reveal content. Disabled-script samples retain the
  stylesheet fallback because theme initialization requires JavaScript.
- PASS: accepted homepage image loaded with the same 480w phone / 960w desktop
  source as baseline. No source image file changed.
- PASS: generated HTML freshness for 36 pages; search-index freshness;
  universe-map freshness; whitespace diff check.
- PASS: allowlisted release build, 56 HTML pages / 371 files; no A14 preview
  or evidence files packaged. This is a local boundary check, not a deployment.
- Visual inspection: desktop homepage and shelf, phone selected-work differences
  and Contact; the retained complete surface matrix supports further review.
- PASS: dedicated server boundary tests, eight passed and one real-symlink test
  skipped because Windows denied symlink creation. Independent mocked symlink
  and Windows reparse guards pass. Exact page/query/HEAD serving, denied directory
  listings/unlisted files, private/encoded traversal, hostile Host, and denied POST
  are covered. All 43 browser samples were rerun on the dedicated server.

Machine records: [geometry](../audit/phone-proposals-2026-09-07.json),
[supplemental checks](../audit/phone-proposals-supplemental-2026-09-07.json), and
[source hashes](../audit/phone-proposals-source-2026-09-07.json).

Reproduce from this checkout, with the repository's existing Playwright package
or the already bundled runtime package available to Node:

```powershell
py -3 scripts/build-phone-proposals.py
py -3 scripts/serve-phone-proposals.py
# In another terminal in this checkout:
py -3 tests/test-phone-proposal-server.py
node scripts/phone-proposals-qa.mjs
```

Open `http://127.0.0.1:5145/proposals/a/` or the corresponding `b/` path.
Only four routes per variant are previewed; other existing links lead to the
staged release baseline. The "Current site" review link returns
to the baseline. The A11 commit must be present in the local Git object store.
Rebuild after updating the pinned contract to a reviewed integrated candidate;
the builder intentionally expects these existing page structures. Shell metadata
and shared runtime still come from this checkout's unchanged generated baseline.
Restart the dedicated server after rebuilding previews; it deliberately serves
its fixed staged snapshot. Stop it with Ctrl+C. It creates a unique ignored
preview tree for each run and does not delete prior trees or alter other servers.

## Unresolved gates and next handoff

1. A11 status/action dependency is now satisfied for these proposals. Its source
   contract is not external functional proof; delivery remains unknown. The
   selected writing card is editorial content, not a software registry record.
   A11's current production browser fixture expects the full canonical block
   visible. Any eventual disclosure adoption must coordinate that fixture change
   with A11, asserting visible concise limits plus keyboard-accessible full
   evidence. A14 does not waive that production assertion or modify its fixture.
2. A21 must refresh the chosen proposal against its combined source and shell
   metadata before implementation. Preserve A16's future picture/source
   optimization when updating the pinned source; A14 does not add that asset.
3. Owner chooses A's compact rows or B's editorial cards, or requests a specific
   revision. The status/action contract is ready for that comparison. No choice
   is inferred from delivery or elapsed time.
4. Human newcomer tasks remain NOT RUN: find an available tool; explain its
   maturity/evidence; distinguish a concept from a usable artifact; locate the
   featured essay; prepare a useful inquiry. Record completion, wrong turns,
   and what the person believes is available, without sending a message.
5. Full integrated regression, keyboard/focus/history, contrast, default motion,
   failed-initialization, short height, zoom, screen-reader and physical-phone
   acceptance remain NOT RUN. Scoped light/dark and disabled-script checks above
   do not substitute for them. Preview-only reveal visibility
   does not test or close A03's production runtime issue.

A21 may retain this proposal package, but must not merge it as a production
redesign or mark A14/X04/X08 complete. After selection, the implementation scope
would be authoritative homepage/project-shelf sources and canonical theme rules,
with A15 owning Contact insertion and A21 owning generated outputs. No production
patch is included in this proposal deliverable.
