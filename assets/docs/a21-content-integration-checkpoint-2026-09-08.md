# Content integration checkpoint: September 8, 2026

Status: UNPUBLISHED CHECKPOINT. Not release-ready. Baseline main:
`c2d23f088d5c29cc3df5c2e8f1b5eb9d479da61a`. A21 owns the isolated
`codex/a21-content-integration` branch; primary and sibling worktrees are untouched.

Integrated reviewed source packages:

- A06 factual corrections: `d763059a` and narrow grammar `b3b62821`.
- A12 Featured labels and aligned metadata: `2074a969`, `e4e8b085`.
- A11 registry, deterministic renderer and generated consumers: `9bfe170b`.
- A13 French interactions and bounded homepage/status deltas: `c1e56d54`,
  `30e15711`, `833c30b4`, `db082c38`.
- A16 image source, derivative, budget and measured evidence: `ee4cbbd6`;
  worker-generated root HTML was excluded before committing. A21 independently
  verified unchanged PNG bytes and exact decoded RGBA parity previously.
- Wave-one acceptance/closeout evidence and A07 publishing-guide correction.

The French project-page cherry-pick conflicted because the current runtime
fingerprint differed. A21 proved the shell outside main differed only in asset
fingerprints, retained the integrated shell and applied the exact reviewed
French main content. No whole-file overwrite or translation-policy change.

A21 regenerated English HTML, cache fingerprints, CSP, English/French search
and universe navigation from combined sources. Generated freshness, universe,
cache and CSP checks pass. Registry tests pass 7; detail/shelf/search checker
passes all 18 records; snippet tests pass 4. Combined English/French interaction
browser tests pass 17. Structural validation reports zero errors and 32 existing
warnings; all 17 current SEO fixtures and locale-link checks pass.

## Explicit remaining gates

- Actual locale wrapper FAIL: all four French routes are stale after content
  and shared runtime changes. No new hashes were adopted. Exact final combined
  source/target review and provenance are required.
- Regional draft gate FAIL: homepage and project source receipts are stale;
  project h3/article counts differ for en-gb and es-mx. Update with bounded
  language-pair review, preserving noindex, human approval false and zero public
  search entries. Do not merely replace receipt hashes.
- A14 A/B choice remains pending. Optional A11 disclosure `73019ead` and A14
  proposal implementation are not activated. The current default status renderer
  is an integration checkpoint, not an approved final presentation. The selected
  English direction must freeze before final locale review/adoption.
- A11 browser fixture still requests private source JSON, which A18 correctly
  denies. A11 has the bounded correction assignment: verify public HTML identity
  and local-registry summary values, retain visibility/overflow assertions, and
  keep private source unavailable. Do not weaken the preview boundary.
- Full combined browser/device/artifact/hosted acceptance has not run. No PR,
  merge or deployment is authorized by these partial local results alone.

Retired worker Git refs and the known missing A05/A10 raw outputs are recorded
in the wave-one closeout. Independent A21 evidence is preserved. This checkpoint
does not mark content, presentation, translation, human/device or full-program
work complete.

### Content-only freeze clarification

The architect confirmed the A14 choice does not block independently authorized
content corrections. The existing production presentation stays in use; neither
optional disclosure nor A/B proposal is activated. Freeze the combined English
content for bounded locale review, then validate this content-only wave. Any
later selected redesign will have its own source and locale review.

Standalone A11 fixture correction `0a866b6c` is integrated. Independent browser
execution now passes all 32 route/viewport cases: public response bytes match
the candidate, status/source/date match the local registry, private registry
returns 404, and existing visibility/overflow assertions pass. Four independent
image parity checks pass with exact geometry and at most 1/255 channel rounding.
This supersedes the earlier fixture and layout-choice blocking statements;
actual French/regional reconciliation remains required.

### Combined locale and browser acceptance checkpoint

English remains frozen at `a2f5f9196fd8e9bef6deeb039804882c40f17413` with
existing presentation. A13 independently reviewed all four English/French pairs
and delivered `befbfc8648b7a068b79aa31af85c2804ef8c1bf3`. A21 reviewed the
provenance, imported it and adopted only its exact hashes through the guarded
wrapper. Actual French freshness now passes; eight de/es advisories remain.
The French condensed-scope omissions are explicitly retained in that record.

A21 applied the en-US to en-GB and en-US to es-MX skills to changed units only:
claims, Featured labels, status summaries, duplicate status-card removal and
the lossless picture source. Existing prose outside those units and all page
shell/canonical/noindex boundaries remain. Exact-pair records are under each
locale's `content-wave-2026-09-08` directory. Inherited voice profiles remain
provisional under the owner's bounded draft authorization; no profile approval,
human/native review or publication promotion was invented. Source dates,
versions, evidence links and uncertainty survive. About/contact normalized
source hashes did not change. The regional receipt is updated only after those
semantic and structure checks, with links to both review records.

Both exact-pair validators and planners pass. Initial planner calls used its
working-directory default and failed to find controls; rerunning with the
explicit manifest base directory passes. Regional noindex/structure/freshness
now passes for all eight pages. Eight regional browser samples pass exact
status/source equality, noindex and overflow; the Mexican project shelf was
visually inspected with cross-origin fonts blocked, so this is fallback-font
layout evidence, not final native-language or typography acceptance.

Combined local checks pass: 560 responsive samples; 56 phone routes; four
representative accessibility samples plus all 56 public routes; 56 CSP routes
with 21 diagrams; 23 release/performance/i18n unit tests; and source inventory,
cache, generated HTML/search/universe, structural and locale-link gates noted
above. A11's 32 public-byte/status cases and four image comparisons pass.

An extra historical `tests/test-murderbird-fallback-editorial.py` invocation
FAILS because it compares current homepage text to `d112ca4e` under a
fallback-only premise. This explicitly authorized content wave changes that
text. The test is absent from the active CI workflow; its historical assertion
is left intact. Do not call it passing or use it to claim this was a
fallback-only edit. Current source, locale and image checks establish the
applicable boundaries for this wave.

A20 independent whole-candidate acceptance and hosted validation remain pending.
No new PR, merge or deployment has occurred at this checkpoint. Optional
status disclosure and both A14 alternatives remain outside the candidate.

### Historical test contract adjudication

The complete historical fallback test contains two assertions for English and
French homepages: whole-page extracted text must equal `d112ca4e`, and every
image alt/title pair must equal that revision. It also emits hashes; it does
not inspect fallback URL/type or PNG bytes, nor original article text directly.

Whole-page text equality FAILS for both pages, as expected from authorized
A06/A11/A12/A13 content edits. That failure is retained, not turned into a pass.
The image alt/title assertions still apply and independently PASS for both
pages. Continuing protections also PASS: original ETCH PNG byte identity,
exact decoded lossless derivative parity, four rendered image comparisons,
and unchanged main text on all eight existing narrative HTML pages under
writings (excluding the intentionally relabeled writings hub), plus manifesto,
about and contact. The 11 text comparisons use explicit UTF-8 and CRLF-to-LF
normalization; an initial unnormalized comparison found platform line endings,
not a narrative change. See `assets/audit/a21-content-preservation-2026-09-08.json`
for 14 passing continuing checks and two explicit historical text failures.
A20 must independently adjudicate this scope; lack of a CI invocation is not
used as the sole reason to disregard the historical premise.
