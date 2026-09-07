# A20 independent acceptance: frozen wave one

## Exact disposition

**Selected-wave local acceptance: ACCEPT WITH LIMITS for `6a122cad4126d52cbce3639e1fea70ff6488bd21`.** Independent tests confirm that X01, X02, and X03 are corrected in the supplied package. The first frozen candidate, `daa3ebd84f7401e2e179dffa5ceee8307f34730f`, failed French locale freshness. The replacement corrects only review/state metadata; A20 independently verified its passing locale gate, new manifest binding, and all 370 unchanged payload files. Required hosted checks, actual assistive-technology evidence, and release authorization remain separate.

The reviewed wave includes A03/A04/A05/A07/A08/A09/A10/A17/A18 and A19 decision evidence. A06/A11/A12/A13-A16 content, status, locale interaction, and presentation work is deferred. Those original findings remain open; this batch does not silently complete them. A19 decision evidence does not imply a hosting change.

Baseline evidence remains preserved at commit `fb0aadda13269c7f56dc468e2f54d12bb2631cae` on `codex/a20-accessibility-acceptance`. The browser review began on `codex/a20-wave-one-acceptance` at the first frozen SHA; final evidence uses `codex/a20-wave-one-rebound`, created directly from the replacement SHA. No candidate file or supplied package was modified. Only this report and four machine evidence files are added.

## Candidate and artifact identity

- Candidate: `daa3ebd84f7401e2e179dffa5ceee8307f34730f`, supplied by A21 from `codex/a21-release-integration`; baseline `98922aebf71d90b2b18ecc34c8b00a041fff51c7`.
- Supplied artifact: `C:/Users/jamie/.codex/worktrees/ace6/overkill-hill/.local/a21-evidence/wave-one-release`. Copied read-only into this isolated checkout at `.local/a20-wave-one/release`.
- Manifest: `assets/audit/release-manifest.json`, SHA-256 `0dee5a155e921d205374fec4c36c66adb0080367c476e61fc2fabdce9317cc22`.
- `py -3 -X utf8 scripts/build-release.py --verify --output .local/a20-wave-one/release --commit daa3ebd84f7401e2e179dffa5ceee8307f34730f`: PASS, 56 HTML pages and 371 files.
- A separately authored Python verifier checked the exact file inventory, all 370 payload byte lengths and SHA-256 digests, the externally supplied manifest hash, and every payload against `git show <candidate>:<path>`. There were 214 exact Git-blob matches and 156 line-ending-only differences, with zero other differences. This distinguishes Windows checkout packaging bytes from raw Git blobs; it does not claim a bit-identical Linux CI package. See [independent integrity evidence](../audit/a20-wave-one-integrity-2026-09-07.json).

The manifest's own digest is checked against A21's supplied value; it cannot contain its own digest. This is integrity/provenance evidence, not an independent signature or deployment proof. Each browser task also checked that the HTTPS root response exactly matched the copied package root bytes.

### Replacement binding

Final candidate `6a122cad4126d52cbce3639e1fea70ff6488bd21` was copied from A21's `.local/a21-evidence/wave-one-rebound` to `.local/a20-wave-one/rebound`. Its verified manifest SHA-256 is `f7c30eb978a16dd23021581015c79d6c8a76a1359c638f12975a8ae1dedd2cf2`. The package verifier again passes 56 HTML/371 files. An independent byte comparison confirms identical inventories and **370 byte-identical payload files**, with only `assets/audit/release-manifest.json` changed. All replacement byte lengths and digests pass. See [replacement integrity evidence](../audit/a20-wave-one-rebound-2026-09-07.json).

The exact Git diff contains only `i18n/pilot/fr/wave1-fingerprint-review-2026-09-07.json`, `i18n/sync-state.json`, and `assets/docs/release-integration-ledger-2026-09-07.md`. Therefore the earlier browser/install observations apply to identical payload bytes in the replacement. The locale provenance explicitly says AI-reviewed and `native_or_human_approval: false`; this review does not promote it to human approval. The actual locale check passes locally on the replacement, leaving only eight existing advisory German/Spanish stale records.

## Five visitor tasks and results

Environment: Windows, Node v24.11.1, Playwright 1.62.1, headless Chromium 151.0.7922.34, Firefox 153.0, and WebKit 26.5. Desktop viewport 1280 x 800; compact navigation 390 x 844. The unchanged package was served over loopback HTTPS at `https://127.0.0.1:5221` using an ephemeral self-signed certificate. Browser contexts used `ignoreHTTPSErrors: true` for that local certificate only. No certificate was installed in an account trust store, and no CSP or page content was bypassed or rewritten. External requests were aborted to isolate first-party behavior; these checks do not establish external fonts, Analytics, embeds, or public-host availability.

| Visitor task and acceptance observation | Chromium | Firefox | WebKit |
| --- | --- | --- | --- |
| T1: Read homepage purpose despite unavailable enhancements. Heading ancestor opacity stays 1 and hero art loads in normal, no-JS, blocked-app, missing-observer, observer-constructor failure, observe failure, stalled observer, and reduced-motion contexts. | PASS, eight modes | PASS, eight modes | PASS, eight modes |
| T2: Skip repeated navigation. From fresh root, Tab focuses skip link, Enter updates `#main`, next Tab reaches a link inside main. | PASS | PASS | QUALIFIED / NOT ACCEPTED: Tab skips ordinary links in this runtime, also reproduced on a plain control fixture. |
| T3: Reach Contact at compact width using keyboard. Tab to nav toggle, Enter expands with `aria-expanded=true`, Tab to Contact and Enter; correct heading and no horizontal overflow. | PASS | PASS | QUALIFIED / NOT ACCEPTED: ordinary links are skipped by this runtime's Tab traversal. |
| T4: Find Mermaid work and open MurderBird. Wait for search-input focus, type `mermaid`, ArrowDown focuses a real result link; snippets have no closing-tag fragments; ArrowUp returns to input, another ArrowUp selects last result, ArrowDown remains bounded at last result; Escape restores opener. Dedicated `MurderBird` search plus Enter opens the story. | PASS | PASS | PASS |
| T5: Begin the long story through its reading shortcut. Keyboard activates `Read the story`; `#the-maker` receives section focus; next Tab stays in main. | PASS | PASS | QUALIFIED / NOT ACCEPTED: ordinary reading-shortcut link is skipped by Tab traversal. |

All five task runs in Chromium and Firefox reported no unexpected page errors. T1 deliberately injected observer failures in separate contexts. Chromium's no-JS screenshot was visually inspected: heading, description, links, and accepted hero art are painted, unlike the baseline blank-hero observation. The local screenshot uses fallback fonts because external requests were blocked; it is visibility evidence, not typography acceptance.

The candidate now uses ordinary focused result links. The baseline absence of `aria-activedescendant` is therefore no longer a failure: DOM focus actually moves to the destination. This verifies focus semantics, not what VoiceOver or NVDA speaks.

See [all task observations](../audit/a20-wave-one-tasks-2026-09-07.json). Machine status retains the initial WebKit FAIL assertions; the interpretation above is based on the separately retained control experiment, not deletion of failures.

### WebKit limitations isolated from product failures

HTTPS removed the earlier SSL asset-loading blockage, enabling styled runtime and search tests. It did not solve keyboard traversal: an independent page containing only `<a>`, `<button>`, `<a>` cycles between button and body under both Tab and Alt+Tab. The site similarly cannot reach ordinary links by those keys. This confirms the behavior is not specific to the candidate, but does not establish the precise platform preference or engine cause. No operating-system/browser account setting was changed to force a pass.

The [minimal fixture and site keyboard evidence](../audit/a20-wave-one-webkit-keyboard-2026-09-07.json) retains the key sequence, unique focus observations, and failed destinations. A [Playwright issue about WebKit tab settings](https://github.com/microsoft/playwright/issues/5609), read September 7, 2026, provides historical context, not proof of this runtime's cause or Safari behavior. Actual Safari with its declared keyboard settings still needs testing.

## Independent installation and regression checks

The pinned ZIP was downloaded afresh from the URL published in the candidate guide. `py -3 -X utf8 tests/test-skillz-install-guide.py --archive .local/a20-wave-one/skillz.zip -v` passed all five tests. The suite executes the exact authoritative guide snippet and verifies every package byte against GitHub's public Git tree for `1a8686ce386928cccef04b53ac6bb98e0ab40b61`. Both `.claude/skills/okhp3-universe-map/` and `.github/skills/okhp3-universe-map/` install all 12 package files plus LICENSE into clean projects; supporting references resolve; each installed package's 19 generator tests pass; repeated installation preserves modified owner files; existing-file and missing-source cases remain safe. Claude Code and Copilot activation were NOT RUN and are correctly separated in the guide.

| Check executed in this review | Result |
| --- | --- |
| `py -3 scripts/build-site.py --check` | PASS, 36 English pages current. |
| `py -3 scripts/build-search-index.py --check` | PASS, 160 entries current. |
| `node --test tests/search-page.test.mjs` | PASS, 14 browser cases; loading/empty/error recovery, real result focus, query/category/history behavior, and Unicode cases included. |
| `node tests/test-reveal-browser.mjs` | PASS, 10 scenarios including injected early startup failure and working destination links. |
| `node scripts/accessibility-qa.mjs --base-url=http://127.0.0.1:5220` | PASS, four representative interaction samples plus all 56 shipped routes, zero named exceptions, on unchanged candidate checkout preview. |
| `node scripts/screen-reader-tree-audit.mjs --base-url=http://127.0.0.1:5220` | PASS, six Chromium tree samples; not a spoken screen-reader session. |
| `py -3 -X utf8 scripts/check-i18n-release.py --mode check --format text` | First SHA: FAIL, exit 1, four blocking French stale routes. Replacement SHA: PASS, exit 0, no blocking French records; eight German/Spanish stale items remain advisory. |

The installation suite and named regressions were executed independently, not accepted from worker summaries. Their ignored logs and disposable probes are under `.local/a20-wave-one/` and `output/a20-wave-one-*`. The initial manifest lookup guessed `assets/data/`; the verified actual path is `assets/audit/`. That invocation error did not alter the package. No candidate-generation command was run.

## Remaining gates and follow-up

1. **Replacement verified:** A21 resolved the four stale French records through the provenance/adoption process; A20 verified the new SHA, actual passing gate, unchanged payloads, and manifest binding above. Any subsequent changed served content needs appropriate retesting; this decision is bound only to `6a122cad4126d52cbce3639e1fea70ff6488bd21` and the supplied manifest digest.
2. **Actual AT and real-device evidence:** no Safari/VoiceOver, NVDA/Firefox, physical phone, audio-backed speech review, or human participant session occurred. Record OS/browser/AT versions, tester/date, the same five tasks, focus/announcement/error behavior, failures, and retests. WebKit cannot stand in for Safari.
3. **Broader visual acceptance:** full zoom/text enlargement, short-height, light/dark rendered focus/contrast, external fonts/embeds, and actual touch behavior remain outside these five bounded probes. Compact viewport success is not a physical-phone test.
4. **CI and delivery:** A21 reported hosted locale success for the replacement and main Site Validation still running. A20 independently reproduced local failure on the first SHA and local success on the replacement; it did not independently inspect hosted logs or a deployed artifact. A21 owns required hosted checks, publication authorization, deployment, and live-byte/task verification. Local package acceptance does not satisfy those layers. Native macOS fixture/platform execution also was not performed in this Windows review.
5. **Deferred batch:** original concept/status/content/locale-interaction findings remain open for later waves. No finding is closed because its source was outside this selected batch.

This report closes the reproduced baseline X01/X02/X03 failures only for the exact reviewed package and tested environments. It makes no WCAG conformance claim, does not mark A20 wholly complete, and is not merge or deployment authorization.
