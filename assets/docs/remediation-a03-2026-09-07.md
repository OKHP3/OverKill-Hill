# A03: fail-open content visibility

Status: implementation prepared and locally tested; combined runtime integration,
cache regeneration, and independent acceptance remain with A21/A20. Not deployed.

Baseline: clean detached `98922aebf71d90b2b18ecc34c8b00a041fff51c7`.
Branch: `codex/a03-fail-open-reveal`. Worktree: `3d31/OverKill-Hill`.
The package commit is the commit containing this handoff. Production SHA was not
reverified or used as an implementation baseline.

## Reproduction and correction

At localhost port 18303, Chromium at 1280 x 800 reproduced eight transparent
homepage reveal sections with JavaScript disabled and with `app.js` blocked.
Both regression tests failed before the source changes.

- `assets/css/theme.css`: reveal sections are opaque and untransformed by
  default. An observer callback can start a finite 0.5-second slide without
  hiding text, art, or links. Reduced motion, smaller screens, focused sections,
  and the existing AskJamie hero exception suppress this animation.
- `assets/js/app.js`: constructor, observation, and callback failures stop the
  optional reveal controller without interrupting the following anchor setup.
  Missing or silent observers never hide content.
- `tests/reveal-visibility.test.mjs`: repeatable browser regression, using the
  existing Playwright dependency. No package or workflow changes.

No copy, artwork, route, locale indexing, generated HTML, owner checkout, or
sibling files were changed. Shared-runtime integration must be serialized with
A04/A13 by A21; this package does not authorize sibling synchronization.

## Validation

Command: `REVEAL_BASE_URL=http://127.0.0.1:18303 node --test tests/reveal-visibility.test.mjs`
against `python3 -m http.server 18303 --bind 127.0.0.1` in this worktree.

| Check | Result |
| --- | --- |
| 20 Chromium cases, 1280 x 800 and 390 x 800 | Pass |
| Disabled JS, blocked app.js, injected initialization exception | Content, loaded hero art, and contact link pass |
| Missing observer, throwing constructor/observe/callback, silent observer | Content and contact link pass; skip-link hash and main focus pass |
| Normal and reduced motion | Pass; normal desktop animation event observed; reduced/mobile animation absent |
| Page title, meaningful h1, computed paint for all reveal sections before/after scroll | Pass |
| Page errors | None except the deliberately injected app initialization exception |
| Disabled-JS desktop and phone screenshots | Visually reviewed; meaningful content rendered, no error overlay |
| `node --check assets/js/app.js`, `git diff --check` | Pass |
| `scripts/build-site.py --check` | Pass, 36 pages, with existing `/private/tmp/okh-overkill-hill-qa-venv-20260906/bin/python` |
| `scripts/build-search-index.py --check` | Pass, 160 entries |
| `scripts/validate-site.py` | Pending regeneration: 112 stale shared-asset references; no new voice warnings |
| `scripts/cache-bust.py --check` | Pending regeneration: 67 files, 133 substitutions |

Browser plugin not available; used existing Playwright and installed Chromium.
The sandbox initially prevented browser launch and localhost binding; approved
escalated execution succeeded. System and bundled Python lacked `bs4`; an
existing QA virtual environment completed the generated HTML check. No new
dependencies were installed. Existing owner-clone Node packages were read through
a temporary worktree symlink, removed after validation. External services were
blocked in these tests, so screenshots use fallback fonts. These checks establish
local runtime behavior, not external asset health or production delivery.

Screenshot evidence from this run: `/private/tmp/a03-disabled-1280.png` and
`/private/tmp/a03-disabled-390.png` (temporary local evidence, not release assets).

## Integration acceptance still required

A21 must apply the reviewed source commit before combining A04/A13 and freeze
the final runtime. Run the owning `scripts/cache-bust.py` generator after final
CSS/JS edits, then `scripts/build-site.py` and freshness checks. If the combined
candidate changes content, regenerate search data with its owning generator too.
Do not hand-merge generated HTML or copy this package's intermediate hashes.
Run structural validation again and the 20-case browser regression against the
combined candidate, then provide that candidate to A20. No full-site browser,
Firefox/WebKit, sibling markup, or live-production acceptance is claimed here.
No owner content decision is needed for this bounded correction.
