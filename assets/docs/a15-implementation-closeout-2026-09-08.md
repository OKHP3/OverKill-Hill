# A15 reader orientation and Contact implementation

September 8, 2026. Implementation baseline:
`6071bc2b0c748fde88b1d5ef1302e039e256444b`. The owner requested completion
after selecting Option B. A14's layout is retained. The earlier A15 proposal
packet is historical preparation, not the current implementation disposition.

## Delivered change

Contact adds optional prompts for the problem, current process, desired result
and constraints after the existing address/location paragraph. It also explains
how to copy the email address when a mail app does not open. No message was sent,
no service or response time is promised, and creator support remains separate.

The diagram essay adds five inline evidence links after its existing four-link
jump menu. The route covers criteria, first-pass diagrams, revisions, council
findings and version history, with an explicit sample limitation. All original
prose, anchors, links and history mechanisms remain. No CSS, JavaScript, art,
project-status fact or layout changed.

French Contact receives only the corresponding inquiry block. The exact-pair
translation record and independent AI review retain native/human approval false.
The essay is outside the configured translation inventory. German and Spain
Spanish drafts remain unchanged. The UK-English and Mexican-Spanish Contact
drafts receive the corresponding bounded addition to satisfy their structural
and source-freshness gate, retaining noindex and human/native approval false.

## Verification

| Check | Result |
| --- | --- |
| Exact baseline preservation after removing marked insertions | PASS for two authoritative fragments and three published pages, normalizing CRLF only |
| Generated HTML check | PASS, 36 English pages |
| English and French search freshness; universe freshness | PASS |
| Structural validation | PASS, zero errors and 32 existing warnings; no new voice warnings |
| Internal links | PASS, zero broken links and zero style issues |
| Locale links and regional draft unit tests | PASS; four draft unit tests; these alone did not prove the actual regional release gate |
| Published-locale freshness | PASS, all four French routes current; eight German/Spanish draft routes remain nonblocking drift |
| CSP and cache checks | PASS; no policy or fingerprint changes required |
| French changed-unit validator and independent semantic review | PASS, AI-reviewed only; see `i18n/pilot/fr/a15-contact-translation-2026-09-08.json` and `a15-contact-review-2026-09-08.json` |
| Focused browser acceptance | See `a15-browser-acceptance-2026-09-08.md` and `tests/test-reader-orientation.mjs` |

Generator CSP normalization briefly rewrote unrelated locale metadata; those
local-only side effects were discarded and the retained policy passes the CSP
checker. An intermediate search freshness check failed before the final rebuild;
both final indexes pass. No failure is represented as a passing first attempt.

The first hosted run failed `scripts/check-regional-drafts.py`: the new Contact
heading changed canonical source freshness and h3 coverage in both regional
drafts. The earlier four unit tests passed but did not cover this final source
state. The correction adds the exact-pair inquiry text to both drafts and
records reviewed source/target hashes without publishing them. Final gate
results and baseline reconciliation are recorded with the release handoff.

## Release boundary

This record describes the tested local implementation. A21 retains PR review,
integration and publication ownership. Hosted CI and live readback must be
verified on the merged revision before reporting release completion. No human
assistive-technology session or native French certification is claimed. These
program-wide limits are separate from the scoped automated browser checks.
