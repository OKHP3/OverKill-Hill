# A13 French interaction implementation

Status: implemented and AI-reviewed in the isolated branch; A21 integration and native-language acceptance remain separate.

## Source and scope

Source contract: A04 `007787fd032679cc44ba3197f2e1779084fe1297`, locally cherry-picked as `22844623`. A21 should use A04's original commit and then the A13 implementation commit, not cherry-pick this entire branch history.

`assets/js/app.js` now selects France French display text for French documents. Search controls, keyboard instructions, loading/error/retry/empty/result-count messages, metadata labels, and theme actions are translated. Query values and category keys are preserved. A04's ordinary-link focus model is unchanged; no simulated selection announcement returns.

The four French pages now use `Langue : Français (France)` for their language control. Language autonyms and their language attributes remain intact. The French overlay states its limited French catalog scope, offers French catalog suggestions, and labels `/search/` as an English-content destination. The dedicated search route stays English. There is no new route or sitemap/indexability promotion.

## Pair record and linguistic limits

The `i18n/pilot/fr/interactions/` directory contains the en-US and fr-FR text-resource pair, exact-pair manifest, source voice record, unchanged seed dictionary, and translation record. The record identifies A04's source revision/hash, resource hashes, dictionary version, AI provenance, source-scope adaptations, and unresolved dictionary approval.

Direction: `en-US -> fr-FR`, using `okhp3-translation-en-us-fr-fr@1.1.0`. The source uses direct plainspoken UI instructions. French uses `vous`; action labels use infinitives. The introduction adapts the source to the actual four-route French catalog, and the full-search label makes the English fallback explicit. Query fragments preserve the query and count. Terminology received AI semantic review, not native or human certification. Non-seed proposed terms are recorded as unresolved dictionary approvals, not silently added as approved entries.

## Verification

- Existing dependency installation: `npm ci --ignore-scripts`; no new dependency or lockfile change.
- `node --test tests/search-page.test.mjs`: 14 passed, including English/shared-brand behavior, focus, history, empty/loading/error/retry, and query handling.
- `node --test tests/french-interactions.test.mjs`: 3 passed. Covers French singular/plural/no-result text, accent matching, safe query rendering, focused links, Escape return, explicit English fallback/query retention, 390-pixel overlay overflow, retry recovery, all four language controls, and all three theme actions.
- Exact-pair validator: passed manifest, structure, and protected-token checks.
- Exact-pair planner: passed, one source artifact and zero missing targets.
- JavaScript syntax: passed.
- Locale-link check after source integration: reports stale French search index. A21 owns regeneration. No locale policy failure was reported.

These are automated Chromium/source checks. Actual screen-reader speech, native French review, full integrated release checks, and live publication were not performed here.

## Integration requirements

A21 combines A03/A04/A13 before generating HTML/cache fingerprints, English and French search indexes, universe output, and any resulting CSP metadata. Re-run locale-link checks and the two browser suites on that candidate. Preserve every regional noindex boundary and retain the existing French release policy. Do not infer release approval or whole-page linguistic freshness from these resource hashes.

Homepage A06/A12 review is a separate follow-up commit so this interaction change can integrate independently.
