# A14 phone presentation studies

Status: PRELIMINARY RENDERED PROPOSALS. X04/X08 remain open. Neither direction
is selected or approved for production. A11's final registry contract is a
required dependency, not satisfied by its inventory checkpoint.

Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`. A01/A02 are committed
in this baseline. The old audit description of uncommitted work is historical.

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
| Project shelf | [View](../audit/screenshots/a14-phone-proposals/a-projects-390.png) | [View](../audit/screenshots/a14-phone-proposals/a-projects-1280.png) | [View](../audit/screenshots/a14-phone-proposals/b-projects-390.png) | [View](../audit/screenshots/a14-phone-proposals/b-projects-1280.png) |
| Skillz detail | [View](../audit/screenshots/a14-phone-proposals/a-projects-skillz-390.png) | [View](../audit/screenshots/a14-phone-proposals/a-projects-skillz-1280.png) | [View](../audit/screenshots/a14-phone-proposals/b-projects-skillz-390.png) | [View](../audit/screenshots/a14-phone-proposals/b-projects-skillz-1280.png) |
| Contact | [View](../audit/screenshots/a14-phone-proposals/a-contact-390.png) | [View](../audit/screenshots/a14-phone-proposals/a-contact-1280.png) | [View](../audit/screenshots/a14-phone-proposals/b-contact-390.png) | [View](../audit/screenshots/a14-phone-proposals/b-contact-1280.png) |

The generator writes only `.local/a14/`: eight HTML previews, one shared
preview stylesheet and a source-hash manifest. It does not write production
pages, authoritative sources or a competing production stylesheet. Every
preview has noindex/nofollow and a visible pending-status notice. The release
builder's existing allowlist excludes previews, this report, scripts and the
retained screenshots. No sitemap, search index or locale change is needed.

## Observations and checks

Confirmed local 390px measurements, including the review notice in proposals:

| Measurement | Baseline | A | B |
| --- | --- | --- | --- |
| Heading left edge | 0px | 16px | 16px |
| Early practical links | No equivalent hero group | y569 to y665 | y569 to y665 |
| Selected work heading | y2332 | y1010 | y1010 |

The existing task section begins at y1563 in the baseline. Both previews
move its practical links earlier, but retain the full existing section lower
down. Removing that duplication is a pending editorial decision. Geometry
supports earlier access, not a claim about conversions or task success.

- PASS: eight preview routes at each of three widths; 24 preview samples plus
  three baseline samples, no document overflow or page JavaScript errors.
- PASS: accepted homepage image loaded with the same 480w phone / 960w desktop
  source as baseline. No source image file changed.
- PASS: generated HTML freshness for 36 pages; search-index freshness;
  universe-map freshness; whitespace diff check.
- PASS: allowlisted release build, 56 HTML pages / 371 files; no A14 preview
  or evidence files packaged. This is a local boundary check, not a deployment.
- Visual inspection: desktop homepage and shelf, phone selected-work differences
  and Contact; the retained complete surface matrix supports further review.

Machine records: [geometry](../audit/phone-proposals-2026-09-07.json) and
[source hashes](../audit/phone-proposals-source-2026-09-07.json).

Reproduce from this checkout, with the repository's existing Playwright package
or the already bundled runtime package available to Node:

```powershell
py -3 scripts/build-phone-proposals.py
$env:HOST = '127.0.0.1'
$env:PORT = '5144'
py -3 server.py
# In another terminal in this checkout:
node scripts/phone-proposals-qa.mjs
```

Open `http://127.0.0.1:5144/.local/a14/a/` or the corresponding `b/` path.
Only four routes per variant are previewed; other existing links lead to the
current site in this local checkout. The "Current site" review link returns
to the baseline. Rebuild after verified upstream source/generation changes;
the builder intentionally expects these existing page structures.

## Unresolved gates and next handoff

1. A11 final implementation and tests are unavailable. Inherited project labels,
   claims and multiple card links are visibly provisional. Replace them from
   the accepted availability/maturity/evidence record, then finish exactly one
   primary action per card. Do not derive software readiness from "Live".
2. A06/A12 remaining metadata corrections are not applied here. Refresh previews
   from the integrated source after A21 verifies those commits. Preserve A16's
   future picture/source optimization; the generator keeps featured media markup.
3. Owner chooses a specific revised direction only after the status/action
   contract is complete. No selection is inferred from this preliminary packet.
4. Human newcomer tasks remain NOT RUN: find an available tool; explain its
   maturity/evidence; distinguish a concept from a usable artifact; locate the
   featured essay; prepare a useful inquiry. Record completion, wrong turns,
   and what the person believes is available, without sending a message.
5. Full integrated regression, keyboard/focus/history, contrast, light/dark,
   default motion, disabled/failed JavaScript, short height, zoom, screen-reader
   and physical-phone acceptance remain NOT RUN. Reduced-motion geometry and
   source freshness do not substitute for them. Preview-only reveal visibility
   does not test or close A03's production runtime issue.

A21 may retain this proposal package, but must not merge it as a production
redesign or mark A14/X04/X08 complete. After selection, the implementation scope
would be authoritative homepage/project-shelf sources and canonical theme rules,
with A15 owning Contact insertion and A21 owning generated outputs. No production
patch is included in this checkpoint.
