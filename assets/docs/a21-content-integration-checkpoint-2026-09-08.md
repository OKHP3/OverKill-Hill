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
