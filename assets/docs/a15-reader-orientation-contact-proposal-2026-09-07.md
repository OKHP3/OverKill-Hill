# A15 reader orientation and contact proposal

Status: PROPOSAL. Prepared September 7, 2026 against baseline
`98922aebf71d90b2b18ecc34c8b00a041fff51c7`. This packet supplies optional copy
and an integration contract for X07/C07. It does not close visitor acceptance
or select an A14 presentation. No published or authoritative page was edited.
A01/A02 are committed in this baseline; the assessment's uncommitted wording
is historical.

## Current source findings

| Claim | Tier | Evidence | Consequence if false | Next check |
| --- | --- | --- | --- | --- |
| Contact has a direct email address and Central Time context, followed by a separate creator-support section; it has no inquiry prompts. | Confirmed | `site-src/pages/contact/index.main.html`, `#contact-details`, `#support`, `#ko-fi` | Redundant copy or a disrupted support boundary | Recheck the A14 selected Contact source before insertion |
| The diagram essay already offers argument, scoring, archive and version-history jumps. | Confirmed | `site-src/pages/writings/first-diagram-is-a-liar/index.main.html`, `nav[aria-label="Jump to article sections"]` | A replacement menu could remove useful entry points | Preserve all four existing links and labels |
| The essay supplies scoring criteria, first-pass/revised galleries, sample-qualified findings and historical artifacts. | Confirmed | Same source, `#scoring-model`, `#v1-diagrams`, `#v2-diagrams`, `#council-scoring`, `#artifacts` | New guidance could overstate what readers can inspect | Verify each target against the integrated candidate; external artifact operation remains unverified |
| MurderBird already offers a reading estimate, story/imagery entry links and chapter navigation. | Confirmed | `site-src/pages/writings/murderbird/index.main.html` | Another orientation block could crowd a working introduction | Retain existing entry aids; no A15 fiction edit proposed |
| Shared same-page anchor handling moves focus, records a changed hash and honors reduced motion. | Confirmed at source level | `assets/js/app.js`, smooth-anchor handler | Added links could disrupt keyboard continuation or history | Browser checks on the final shared runtime; source inspection is not behavioral acceptance |
| A short guided sequence may help readers inspect the experiment without reading the full essay first. | Inferred | Existing essay length and current jump menu; C07 in `audit-experience-content-2026-09-07.md` | More introductory copy could increase friction | Observe the reader task below on the selected rendered presentation |
| The following additions are suitable for publication. | Proposal | Copy in this packet only | Unselected presentation or unsupported positioning could ship | A11 contract verification, A14 selection and A21 review |
| A11's final contract and an owner-selected A14 direction are accepted. | Unknown | Neither is supplied in the assigned baseline or this task | Premature application or competing status claims | Obtain exact upstream revisions and selection evidence before source edits |

## Optional Contact copy

Proposed placement: inside the existing Contact card, immediately after the
email/location paragraph. Retain the current heading, mascot introduction,
email link and visible address, existing closing copy, and creator-support
section. This is an insertion, not a replacement of the owner's text.

```html
<h3>What are you trying to untangle?</h3>
<p>A few details can help start the conversation. Share whatever is useful:</p>
<ul>
<li>The problem you want to solve.</li>
<li>How the process works today, and where it gets stuck.</li>
<li>What a useful result would look like.</li>
<li>Constraints that matter, such as tools, timing, or budget.</li>
</ul>
<p>No finished brief needed. If a page here prompted your inquiry, include its link.</p>
<p>If the email link does not open your mail app, copy contact@overkillhill.com into a new message.</p>
```

The prompts are optional context, not required fields or an intake commitment.
Keep `mailto:contact@overkillhill.com` unchanged. Do not add a prefilled body,
new form, tracking, booking route, response promise, pricing or service list.
The support section keeps its own heading, narrative and donation action;
do not turn creator support into a prerequisite for inquiry.

## Optional evidence route

Proposed placement: immediately after the existing four-link article jump
menu and before the first autobiographical paragraph. A14 determines final
spacing and presentation. Reuse the existing typography and shared stylesheet.
Keep the current 45-minute estimate; this route has no invented duration.

```html
<p><strong>Want to inspect the evidence first?</strong>
Start with the <a href="#scoring-model">criteria and scoring lanes</a>,
compare the <a href="#v1-diagrams">first-pass diagrams</a> with the
<a href="#v2-diagrams">revisions</a>, then read
<a href="#council-scoring">where the council agreed and split</a>.
These findings describe this sample. The
<a href="#version-history">version history</a> puts the experiment in context.</p>
```

This labels a route through existing evidence; it does not certify model
rankings, statistical validity, external tools or present-day software maturity.
Readers can still choose the original argument, archive or full essay.
No project status badge is introduced. If A14 adds a related-project action,
its status and availability must come from the final A11 contract, with no
handwritten competing claim in this block.

## Source ownership and preservation contract

Only the following authoritative files would need A15 insertions after the
dependencies are verified:

- `site-src/pages/contact/index.main.html`
- `site-src/pages/writings/first-diagram-is-a-liar/index.main.html`

All existing text nodes, element IDs, links and their order remain intact.
Do not rename a heading anchor, wrap the essay in a collapsed control, split
the archive into new routes, or add a new anchor controller. Preserve
`#roy`, `#council-scoring`, `#artifacts`, `#version-history` and every other
current fragment identifier. Native links must remain usable without scripts.
The original manifesto, MurderBird text/art, locale pages, shared CSS/JS and
project-status records are outside this patch's source ownership.

A14 owns the rendered alternatives across homepage, shelf, detail and Contact.
This packet supplies copy to those alternatives; it is not a third presentation.
Before implementation, record A11's accepted revision and A14's selected
variant/revision here or in the integrator's acceptance record. Re-read both
source files at that candidate to avoid duplicating an upstream insertion.

A21 owns the combined generated HTML, search, universe, CSP and fingerprints.
After selected source insertion, regenerate with the repository's current
pipeline and run HTML/search/universe freshness, structural and internal-link
gates. Identify the new English strings for exact-pair locale review without
promoting any regional draft or changing noindex boundaries.

## Acceptance tasks for the selected candidate

| Task | Required observation |
| --- | --- |
| Evidence route | A reader finds the criteria, compares V1/V2 and reaches the council findings; they can describe the sample limitation without treating the page as a current model leaderboard. Record wrong turns as well as completion. |
| Existing long-form routes | Original four-link menu, sidebar TOC, direct fragment URLs and version history remain reachable. Compare baseline text/ID/link inventories before and after the insertion. |
| Keyboard and history | Tab to each added link, activate it, check visible focus and keyboard continuation at the destination; use Back/Forward and reload a fragment URL. Check modified-click behavior and no duplicate history entry when activating the current fragment. |
| Script failure and motion | Test normal, reduced-motion, disabled-script and blocked-app.js conditions. Text and links stay visible and native hash navigation works without JavaScript. Coordinate any baseline reveal failure with A03. |
| Inquiry | A reader can locate and copy the address, describe what context to include and distinguish inquiry from creator support. Inspect the email destination without sending a message or making a donation. |
| Layout | Review Contact and the essay at phone and desktop widths, short height, zoom, and light/dark themes within the selected A14 direction; check wrapping, gutters, focus visibility and added introductory height. |

## Validation and handoff

This is a documentation-only proposal. No site behavior or output has changed.
Checks run in this isolated checkout on September 7, 2026:

| Check | Result | Scope of evidence |
| --- | --- | --- |
| Proposed-fragment inspection with Python standard-library HTMLParser | PASS | Two HTML fragments; all five proposed evidence links resolve to unique existing IDs; four original jump destinations and current email verified |
| New-copy guardrail scan and editorial review | PASS | No em dash or prohibited filler in this packet; US English, optional prompts and sample limits reviewed |
| `py -3 scripts/build-site.py --check` | PASS | Baseline generated HTML current for 36 pages |
| `py -3 scripts/build-search-index.py --check` | PASS | Baseline generated search index current |
| `py -3 scripts/sync-universe-map.py --check` | PASS | Baseline universe map current |
| `git diff --check` and staged scope review | PASS | Only this proposal document is included; authoritative and published pages remain unchanged |

Rendered alternatives,
user task observations, browser history/focus acceptance, assistive-technology
sessions, external link operation, locale translation and live publication are
NOT RUN for this packet. They must not be inferred from baseline freshness.

Next action: A14 can incorporate this proposed copy into its two alternatives.
Apply only the selected insertion after verifying A11/A14, then hand the exact
source diff and generation requirements to A21. X07/C07 remain open until
the integrated candidate meets the acceptance tasks above.
