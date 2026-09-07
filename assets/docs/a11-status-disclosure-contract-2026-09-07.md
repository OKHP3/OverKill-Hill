# A11 optional status disclosure contract

Proposal-only refinement of `9bfe170b`, requested after A14 screenshot review. No registry facts, descriptions, production renderer calls, generated pages, styles, or owner design selection change in this patch.

## API and visible limits

`scripts/project-status.py` exports `visitor_summary(record)` and `disclosure_html(record)`. The optional `render(..., disclosure=True)` path applies the same wrapper, placing card descriptions before the status disclosure where a descriptive paragraph exists. Existing calls omit this option and retain the original output.

The visible brief uses `record.maturity` verbatim. Records whose maturity is Unknown also show availability and Maturity unknown. Published project/catalog and noindex concept records append Operation unverified; other records append Delivery unverified. The workbench instead retains its dated/current-readiness qualification and the exact evidence summary, keeping the RAG uncertainty visible. New delivery states fail until their visitor wording is reviewed.

Skillz therefore shows Active build; package maturity varies. Operation unverified. Abrahamic shows Reported active release v1.1. Operation unverified. Prototype, pre-production, separate service operation, and no-public-launch limits remain in the visible maturity text.

`data-project-status-disclosure` wraps a visible `data-project-status-brief` paragraph and a native, initially closed `details`. Its `summary` is Status and source. Inside is the unchanged canonical `data-project-status` paragraph, exact text, pinned source link, and review date. No custom click handler, tabindex, or substitute button role is added. Primary visitor actions remain outside the disclosure.

## Validation and adoption boundary

`py -3 tests/test-project-status-disclosure.py` passes five focused tests: unchanged canonical evidence, visible workbench limit, record-driven wording and unsupported-state rejection, opt-in/idempotent rendering, and card description/action placement. A direct comparison with `9bfe170b` confirmed byte-identical default rendering across all 17 applicable source routes with the final patch.

A14 owns rendered proposal verification: test closed-state visible limits, Enter/Space opening and closing, exact expanded canonical evidence, focus staying on the native summary, primary actions outside the disclosure, phone overflow, and operation without JavaScript. A14's independent results must identify which renderer revision they exercised. This A11 patch does not claim those browser checks ran against this revision.

The production browser fixture currently requires all canonical status blocks to be visible. Intentional closed disclosures require a coordinated fixture change upon adoption: verify the visible brief, then open the native disclosure and inspect canonical content. Do not waive the failure or apply the option to production before selection and integrated acceptance. A12 editorial descriptions remain unchanged. A21 owns eventual integration; A/B selection and human accessibility acceptance remain pending.
