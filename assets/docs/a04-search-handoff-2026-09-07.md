# A04 search implementation handoff

Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`.
Scope: search IIFE in `assets/js/app.js`, section extraction in
`scripts/build-search-index.py`, and focused regressions. No sibling changes.

## Confirmed behavior

- Baseline failed both new focused-link browser regressions and all three
  initial parser regressions. The generator cut closing tags before their
  final bracket, counted markup inside comments/scripts, and duplicated headings.
- The section parser now finds complete matching elements with HTMLParser
  events. TextExtractor supplies plain text and inserts each heading only once.
  Incomplete sections are omitted. Existing URLs and result counts are retained.
- Result links retain their ordinary link semantics and list wrappers. Down
  from input focuses the first link; Up focuses the last. Link arrows move
  actual focus, clamp at the last link, and return to input above the first.
  Native Tab and Enter work. Enter from input opens the first result.
  Overlay Escape restores the opener. Input text is preserved.
- Loading, failed, empty-index, and no-match states remain distinct while
  typing. Retry retains the current query. Category and query history remain.

## A13 English string and DOM contract

The exact search IIFE is the authoritative complete string inventory. No
locale translation or locale markup changed here.

| Change | Exact English text |
| --- | --- |
| Added empty-index message, both surfaces | `No indexed pages are available.` |
| Existing overlay loading text now used on initial fetch and retry | `Loading search index…` |
| Dedicated loading text retained | `Loading index…` |
| Removed simulated selection announcement | `Selected: ` |

All existing error, retry, count, category, brand hint, regional fallback,
full-search, and ARIA label strings remain unchanged. Focused native links
replace the removed selection announcement. Keep the existing list wrappers,
live status region, result class, input hooks, and query/category URLs.

## Verification

Windows, Node 24.11.1, Playwright Chromium, existing lockfile installed with
`npm ci --ignore-scripts`; no new dependencies.

| Check | Result |
| --- | --- |
| `node --test tests/search-page.test.mjs` | PASS, 13 tests before final test-only additions |
| `node --test --test-name-pattern='focuses ordinary\|Enter from' tests/search-page.test.mjs` | PASS, 3 final keyboard tests including direct input Enter |
| `py -3 -B -X utf8 tests/test-search-sections.py` | PASS, 4 tests including published fragment scan |
| `node --test tests/search-index.test.mjs tests/search-index-locale.test.mjs` | PASS, 3 tests |
| `scripts/build-site.py --check` | PASS, 36 pages |
| English/French search freshness | PASS, 160/4 entries; both regenerated |
| Regional generation | PASS, en-gb/es-mx remain 0 entries and unchanged |
| `node --check assets/js/app.js`, `git diff --check` | PASS |
| `scripts/validate-site.py` | FAIL, 56 stale app.js fingerprints; no new voice warnings |
| `scripts/cache-bust.py --check` | FAIL, 66 files/66 substitutions needed |

## Integration boundaries

A03's exact `6a0a6aaea1ae9adafc5fdc146b55ed785814d813` app.js diff was
inspected: section 2 reveal only, disjoint from this section 5 search change.
A21 must test the combined candidate and regenerate shared cache references.
Search index output is committed separately as reproducible evidence; A21
should regenerate it from the combined source instead of hand-merging JSON.
The universe generator reported current after regeneration.

Wire the new Python fixture into the combined CI gate. Screen-reader speech,
actual Safari/VoiceOver/NVDA sessions, sibling deployments, live behavior,
and full release acceptance are not verified here. No merge or deployment.
