# A20 selected-wave acceptance: mandatory locale gate

**ACCEPT WITH LIMITS for `23e78e0dae0c441a0b42f11d01a0af6748c1de1c`.** The mandatory locale gate correction is verified, and all previously tested visitor-facing payload bytes remain unchanged. This is scoped local acceptance, not merge/deployment authorization, hosted success, full accessibility conformance, or completion of A20's actual assistive-technology evidence.

## Scope and preservation

Independent review ran on September 7, 2026 in `C:/Users/jamie/.codex/worktrees/269e/overkill-hill`, branch `codex/a20-wave-one-gated`, created directly from the named candidate. No candidate source or package file was changed. This commit adds only this report and its machine integrity evidence.

Prior accepted candidate: `6a122cad4126d52cbce3639e1fea70ff6488bd21`. Its review commit `2d00450d7dcef2c6c6672e34048529784bf3ed66` remains preserved on `codex/a20-wave-one-rebound`; detailed five-task observations and limits are in that commit's `assets/docs/a20-wave-one-acceptance-2026-09-07.md` and four linked JSON files. Baseline review `fb0aadda13269c7f56dc468e2f54d12bb2631cae` remains preserved separately.

The exact Git delta from the prior accepted candidate is only:

- `.github/workflows/validate.yml`: six added lines, adding workflow regression execution and the actual blocking locale freshness command before release packaging.
- `tests/test-i18n-workflow.py`: four regression tests.
- `assets/docs/release-integration-ledger-2026-09-07.md`: integration evidence update.

No deferred content, presentation, locale interaction, or project-status wave was imported. A06/A11/A12/A13-A16 findings remain outside this batch and open.

## Artifact identity and independent comparison

Supplied package: `C:/Users/jamie/.codex/worktrees/ace6/overkill-hill/.local/a21-evidence/wave-one-gated`. A20 copied it into its own ignored `.local/a20-wave-one/gated` directory for read-only verification.

Manifest: `assets/audit/release-manifest.json`, SHA-256 `fdf39bd8e240ccd46122d75378011676ef1c798d71eda4745981e217ca070142`.

`py -3 -X utf8 scripts/build-release.py --verify --output .local/a20-wave-one/gated --commit 23e78e0dae0c441a0b42f11d01a0af6748c1de1c` passes: **56 HTML pages, 371 files**.

A separately authored verifier confirms the exact manifest digest, candidate commit, file inventory, integrity-map inventory, all 370 payload byte lengths and SHA-256 digests, and the three-file Git delta. Comparison against A20's preserved `6a122cad` package finds **370 byte-identical payload files**. Only the release manifest differs. See [machine rebind evidence](../audit/a20-wave-one-gated-rebind-2026-09-07.json).

The earlier package had already been independently compared to browser-tested `daa3ebd8`, also with all 370 payload files identical. The five visitor-task results therefore carry forward through exact byte identity; browser sessions were not rerun or invented for this metadata/workflow-only change. A trusted manifest is not an independent signature. Local Windows package bytes do not prove the byte identity of a later hosted Linux artifact.

## Independently executed gate checks

| Exact command | Result |
| --- | --- |
| `python3 tests/test-i18n-workflow.py -v` | PASS, four tests. Current reviewed French passes; stale French fails; stale German/Spanish drafts stay advisory; Pages depends on reusable validation and the actual gate precedes artifact creation/upload. |
| `python3 tests/test-ci-concurrency.py -v` | PASS, seven tests covering PR identity, rapid pushes/reruns, dispatch isolation, reusable validation, monitor isolation, summaries, and deployment cancellation boundary. |
| `python3 scripts/check-i18n-release.py --mode check --format json` | PASS, exit 0. This is the literal added workflow command, executed against current inputs without mutation. |
| `python3 scripts/check-i18n-release.py --mode check --format text` | PASS; no blocking French records; eight existing German/Spanish stale records remain advisory. |
| `git diff --check` | PASS. |

The added gate has no `if`, `continue-on-error`, alternate shell, or working-directory override. The regression executes the real detector in copied sites and checks that it leaves files unchanged. These local tests establish the declared dependency and command behavior; they do not demonstrate a hosted workflow run or deployment attempt.

## Carried-forward visitor evidence and explicit limits

On byte-identical payloads, Chromium 151.0.7922.34 and Firefox 153.0 passed all five tasks: homepage visibility under enhancement failure, skip-link continuation, compact keyboard navigation to Contact, accessible focused search links with clean excerpts and working Enter/Escape behavior, and the long-story reading shortcut. WebKit 26.5 passed visibility and search over an unchanged HTTPS preview; ordinary-link Tab traversal failed both on the site and on a trivial independent anchor/button fixture. WebKit skip/navigation/story keyboard acceptance therefore remains qualified, not silently passed. The earlier HTTP-to-HTTPS asset transport failure is a separate resolved local-preview limitation.

The previous review independently passed pinned package installation and preservation tests (5), search browser cases (14), reveal scenarios (10), accessibility checks (4 representative samples plus all 56 shipped routes), and Chromium accessibility-tree checks (6 pages). Copying and generator checks do not prove Claude Code or Copilot activation.

Actual Safari/VoiceOver, NVDA/Firefox, physical-phone/touch, audio-backed speech, human participant, and native macOS sessions were **not performed**. A 390-pixel viewport is not a physical-phone test, WebKit is not Safari, and an accessibility tree is not a screen-reader speech session. Full zoom/text enlargement, short-height, rendered light/dark contrast, external font/Analytics/embed availability, and complete real-device acceptance remain outside the five bounded probes.

A21 reported hosted checks launching for this candidate. A20 has not independently inspected their completion or a deployed artifact. A21 owns required hosted checks, publication authorization, release artifact verification, and live-byte/task acceptance. Any later candidate must be rebound again, with affected behavior retested if served bytes change.
