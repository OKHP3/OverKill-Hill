# A04: Search interaction and parsed snippets

Status: implemented and locally tested; integration acceptance remains pending.
Branch: `codex/a04-search-interaction`.
Initial baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`.
Reviewed A03 dependency: `f9ebeb99`, cherry-picked here as `624c6449` before
this package commit. A21 owns final runtime integration and release readiness.
No deployment SHA is assumed, and nothing was published.

## Reproduction and repair

The baseline search handlers selected results using `data-active` while keeping
focus in the query input without an active-descendant relationship. The parser
sliced section HTML through `</div`, then attempted to strip only complete tags.
A fresh public search-index GET on September 7 still contained that fragment in
31 entry bodies, including BPMN and Mermaid Theme Builder resources. The rebuilt
local index has zero such bodies. Live keyboard behavior was documented in the
linked assessment; this package verified keyboard behavior locally in Chromium.

Search now uses ordinary focused links inside the existing list wrappers.
ArrowDown or ArrowUp from the query focuses the first destination. Within results,
arrows move focus, the last result clamps, and ArrowUp from the first returns to
the query. Native link Enter and Tab work; Enter in the dedicated input still
opens its first result. The overlay traps Tab and Escape returns to its opener.
Visual active state follows actual link focus. Query changes preserve typing,
reset the input's Enter target, and keep loading, failure, empty catalog, and no
matches distinct. Query/category history, accents, and safe text escaping remain.

The index generator now uses HTMLParser element boundaries for project and
article sections, parses text only inside those bounds, resolves nested labels,
and avoids appending headings twice. This is a generator correction, not a
renderer filter for a specific fragment.

## Changed paths and generation ownership

Authoritative sources: `assets/js/app.js` (Section 5 only),
`scripts/build-search-index.py`.
Regression sources: `tests/search-page.test.mjs`, `tests/test-search-sections.py`.
Generated outputs: `assets/data/search-index.json` and
`assets/data/search-index.fr.json`, from the owning index generator. English
retains 160 entries; French retains four. German, Spanish, British English, and
Mexican Spanish indexes were regenerated and remain unchanged and empty.
No English page authoring content, artwork, locale indexing policy, CSS, or URLs
were changed by A04. A03 CSS/runtime changes are in the preceding dependency
commit, not this package diff.

## Validation

- PASS: 16 tests with `node --test tests/search-page.test.mjs tests/search-index.test.mjs tests/search-index-locale.test.mjs`, repeated after A03 incorporation. Covers brand vocabulary, loading/query races, failure/retry, empty indexes, no matches, clearing, bounds, focused links, Enter, Tab, Escape/opener focus, category/Back, accents and escaping.
- PASS: four parser fixtures with `python3 tests/test-search-sections.py`: nested uppercase blocks, inline tags/entities, heading duplication, comments/script/void elements, truncated tag syntax, nested article sections, and nested accessible labels.
- PASS: all 20 inherited A03 desktop/phone visibility cases against this worktree on loopback port 18404. The first attempt failed because the default port 18303 had no preview server; it did not exercise page behavior. Rerun command: `REVEAL_BASE_URL=http://127.0.0.1:18404 node --test tests/reveal-visibility.test.mjs`.
- PASS: `scripts/build-site.py --check` (36 English generated pages), all six index freshness checks, `node --check assets/js/app.js`, and `git diff --check`.
- PENDING: structural validator reports stale shared CSS/script cache references after the source changes. Final fingerprints are deliberately left to A21 after A13. No new voice warnings beyond the existing baseline.
- NOT RUN: human assistive-technology sessions, Firefox/WebKit, full-site browser gates, sibling synchronization, and final production acceptance.

Existing owner-clone Node dependencies were read through a temporary symlink,
removed after tests. No packages were installed. Default Python lacked bs4;
existing `/private/tmp/okh-overkill-hill-qa-venv-20260906/bin/python` ran the English
build and validator. Browser and loopback execution required sandbox escalation.

## A13 strings and A21 acceptance

A13 received the final interaction model and new string:
`No searchable pages are available.` Existing loading strings remain
`Loading search index…` (overlay) and `Loading index…` (page). Removed
`Selected: ` because actual link focus now exposes the selected destination.
Other English error, ready, suggestion, and result-count strings are unchanged.

A21 must integrate A04 after A03 and before A13, then run `scripts/cache-bust.py`,
`scripts/build-site.py`, and the owning search-index generator for each affected
locale. Recheck generation, cache freshness, structural validation and these
regressions on the frozen combined candidate, then send it to A20. Do not
hand-merge generated indexes or intermediate page fingerprints. This package
needs no new owner content decision; release acceptance remains with A21/A20.
