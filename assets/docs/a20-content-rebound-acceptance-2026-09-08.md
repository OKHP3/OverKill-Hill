# A20 content acceptance after main merge

**ACCEPT WITH LIMITS for `f0b2eb5bb0e99ec5ea6bb4cdf8f97dc115ca24f7`.** Independent byte verification carries forward the scoped content-wave acceptance from `ed9a47d0e7e247977de8bd58ba10ac9376fa1ed5`. This does not claim hosted success, publication authorization, or full A20 completion.

## Identity and scope

Reviewed September 8, 2026 in isolated `C:/Users/jamie/.codex/worktrees/269e/overkill-hill`, branch `codex/a20-content-rebound`, created from the exact new candidate. Prior evidence commit `99d897864d1de17672b1a1bf44c17faff4071328` remains preserved on `codex/a20-content-acceptance`. Its report and three machine records contain the original content/locale/browser/preservation adjudication. This new commit adds only this rebind report and one JSON record; candidate files remain unchanged.

The complete Git delta from the reviewed candidate is 12 added files: three FoundRy review documents under `assets/docs/`, six handoff records under `docs/handoffs/coop-pertition-2026-09-07/`, and three FoundRy test files. No HTML, authoring source, runtime, asset, locale state, or workflow changed. All 12 paths are absent from the release package. The exact list is retained in [independent rebind evidence](../audit/a20-content-rebind-2026-09-08.json).

Supplied package: `C:/Users/jamie/.codex/worktrees/ace6/overkill-hill/.local/a21-evidence/content-release-rebound`, copied into A20's ignored `.local/a20-content/rebound` directory.

Manifest `assets/audit/release-manifest.json` SHA-256: `f8c3a9a727d9096ba15303988ae3c05d630f0827628386dc47a3480a37f4f3c7`.

`py -3 -X utf8 scripts/build-release.py --verify --output .local/a20-content/rebound --commit f0b2eb5bb0e99ec5ea6bb4cdf8f97dc115ca24f7` passes: **56 HTML pages, 372 files**.

A separately authored verifier confirms the supplied manifest hash, exact commit, inventory and integrity-map membership, every payload length/digest, and the 12-file Git delta. All **371 served payload files are byte-identical** to the package independently tested at `ed9a47d0`; only the manifest differs. Browser, content, locale, installation, and preservation evidence therefore carries forward through exact byte identity, not assumption. No new browser sessions are invented for unchanged pages, and the local manifest is not an independent signature or proof of a future hosted artifact's bytes.

## Newly added tests independently executed

| Command | Result |
| --- | --- |
| `python3 tests/test-foundry-feature-contract.py -v` | Six current-contract tests PASS. Two opt-in future parity diagnostics SKIP: named project slots and recovery import/export controls. |
| `python3 tests/test-foundry-launch-routes.py -v` | Four current route/source tests PASS. One proposed automatic legacy redirect check SKIP. |
| `node --test tests/foundry-embed-acceptance.test.mjs` | Two tests PASS: sandbox/direct fallback affordances and keyboard/reload controls. This does not prove external workbench operation. |
| `git diff --check` | PASS. |

The three skips remain explicit unavailable/future coverage, not passes or shipped features. Existing page contracts are checked without importing the proposed implementation.

## Carried-forward limits and adjudication

The previous content review independently passed five visitor tasks in Chromium and Firefox, package integrity, status consistency, bounded locale checks, pinned installation, and continuing art/narrative protections. WebKit visibility and search pass, while ordinary-link Tab traversal retains its independently isolated environment limitation. Actual Safari/VoiceOver/NVDA, physical-phone/touch, human/audio-backed sessions, native macOS checks, full zoom/short-height/real-font coverage, and fresh performance trials remain unperformed.

Historical English/French homepage whole-text equality against the fallback-only revision remains FAIL, as explicitly authorized content changes supersede that premise. It is not treated as passing or dismissed because it is outside CI. Continuing image alt/title equality, original PNG bytes, decoded RGBA parity, and 11 protected narrative/unrelated main-text comparisons passed independently and remain valid on identical payloads. The historical test remains unchanged.

French review remains AI-reviewed with human/native approval false and condensed-scope omissions retained. Regional pages remain machine-drafted, noindex, human/native false and release-acceptance false. Source-described project status does not become operational proof. Optional presentation/disclosure and other deferred work stay outside this acceptance.

A21 reports hosted reruns launching; A20 has not independently checked their completion or deployed bytes. A21 retains responsibility for required hosted gates, authorization, publication and live acceptance. Any subsequent SHA/package must be rebound again, with affected tests rerun if served bytes change.
