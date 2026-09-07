# A13 French interaction audit

Status: X06 reproduced in source; implementation pending the verified A04 final-string contract and shared-runtime handoff. This is an audit checkpoint, not an A13 completion or release approval.

## Baseline and scope

Inspected isolated checkout at `98922aebf71d90b2b18ecc34c8b00a041fff51c7`, matching fetched `origin/main` on September 7, 2026. The checkout was clean before this report. A01/A02 are already committed in this baseline; the advancement plan's uncommitted wording is historical.

Read `AGENTS.md`, `replit.md`, the advancement plan, the experience/content audit, current runtime and locale records, and `okhp3-translation-en-us-fr-fr@1.1.0` with its contract, voice guidance, seed dictionary, and manifest example. Direction is exclusively `en-US -> fr-FR`.

## Confirmed current findings

| Surface | Current source evidence | Required follow-through |
| --- | --- | --- |
| Theme | `assets/js/app.js:198` defines English action names for system, light, and dark states; the button reads this table on creation and change. | Translate all three action names while retaining state identifiers and cycling behavior. |
| Language | All four `fr/**/index.html` pages have `aria-label="Language: Français (France)"`. | Translate the control's English prefix. Preserve language autonyms, destination URLs, and their language attributes. |
| Search scope | `app.js:621` selects the French index, but `searchCopy()` still selects brand-specific English copy. | French dialog name, placeholder, introduction, and useful suggestions must match the actual four-route catalog. |
| Overlay controls | `app.js:829-840` hardcodes Search, Close search, Search results, keyboard instructions, and Open full search. | Localize accessible and visible labels together after A04 settles semantics. |
| Errors and status | `app.js:873-885`, `925`, and `953-966` hardcode error/retry/loading, ready, no-match, and singular/plural result announcements. | Translate complete message units with query/count placeholders preserved and safely escaped. Include A04's final selection announcements. |
| Result metadata | `renderResultHtml()` emits category values directly and maps publication states to English. | Localize display labels only; retain canonical category/state values for filtering and history. |
| Full-search destination | Overlay footer routes to `/search/`, preserving a query when present. There is no French full-search route in the four-route pilot. | Explain the English destination in French and retain the existing URL/query contract. Do not imply that it continues searching the French catalog. |
| Dedicated search | Its loading, empty, result-count, and Selected messages also live in the shared runtime. | Inventory A04's complete contract. The existing English destination must remain English unless an explicitly scoped French route is added later. |

These observations reproduce the generating cause against current source. The previous audit's live Edge session is historical evidence, not a browser session repeated in this task.

## Translation and review contract

The current French review record (`i18n/pilot/fr/review-record-2026-09-05.json`) explicitly says `ai-reviewed`, `native_or_human_approval: false`, uses `vous`, and calls for labeled English destinations. Its older page hashes do not cover new runtime strings.

Before drafting the final microcopy, create a scoped plainspoken en-US text-resource inventory from A04's verified commit, a separate fr-FR resource, the exact-pair manifest, source voice record grounded in the owner's instructions/current English controls, and a project copy of the pair dictionary. Do not reuse the provisional es-MX profile: it contains example paths and target-specific instructions. Record absent terminology as unresolved; seed entries and AI review are not owner-approved dictionary additions.

Record source revision and hashes, target hash, skill/profile/dictionary versions, protected placeholders, AI authorship/review, and remaining native review. Do not adopt unrelated page hashes or claim native certification. The skill states: "A clean script result, model agreement, back-translation, or a dictionary match cannot certify native French."

## Required implementation validation

1. Recheck the frozen A04 source contract and serialize the shared `app.js` change with its owner.
2. Exercise French overlay empty/loading/error/retry/no-result/singular/plural/selection states, query escaping, accent matching, Enter, Escape, Tab, and focus return. Match A04's actual interaction model.
3. Verify all three French theme actions and the four language controls. Check labels at narrow viewport sizes and in the accessibility tree.
4. Verify the full-search link visibly explains English content, retains the query, and reaches the existing English search page. Preserve English brand behavior.
5. Run the exact-pair validator/planner and locale checks. Distinguish linguistic judgment from mechanical results.
6. Hand generator/cache/CSP requirements to A21 for combined regeneration and review. Preserve French's existing indexing status and every regional draft/noindex boundary.

## Evidence at checkpoint

- `py -3 scripts/check-locale-links.py`: passed for the current fr/de/es pilot contract.
- Source inspection: confirms X06 remains unresolved; no runtime or translated page changes made.
- Native/human language review, new browser testing, combined release checks, and publication: not performed.
- A04 final strings and runtime handoff: requested from the coordinating task; not yet received at this checkpoint.

Only this audit document is changed. Resume implementation in this branch when the upstream contract is available; A21 remains the sole integrator.
