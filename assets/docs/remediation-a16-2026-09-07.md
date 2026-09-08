# A16 package handoff and closeout

Verified September 8, 2026. Assigned baseline:
`98922aebf71d90b2b18ecc34c8b00a041fff51c7`.

## Accepted result

A16 is implemented and published in GitHub main
`f4a353c323fc1caa848e03f6f0aa1ea1e520210c`, through
[merged PR 65](https://github.com/OKHP3/OverKill-Hill/pull/65).
The authoritative implementation and measurement record is
[A16 measured asset costs](a16-measured-asset-costs-2026-09-07.md).
Its pre-integration disposition and unavailable CI statement are historical;
the release verification below supersedes those statements for this package.

The measured homepage contributor was the lazy ETCH-AI-SKETCH PNG after
scrolling. Its exact-RGBA WebP delivery copy reduces image file bytes from
2,494,141 to 1,862,704, a reduction of 631,437 bytes (25.3%). The original PNG
remains unchanged at its existing URL and as the picture fallback. Typography,
analytics policy, accepted source artwork, image dimensions, and prose remain
outside this optimization. There is no claimed conversion or general speed gain.

## Evidence and scope

- Four-route cold/warm baseline: [48 visits](../audit/a16-before-2026-09-07.json).
- Changed-page comparison: [12 homepage visits](../audit/a16-after-2026-09-07.json).
- [Four rendered image comparisons](../audit/a16-parity-2026-09-07.json):
  desktop/phone and light/dark geometry match; scaling differences are bounded
  by 1/255 per channel. This is image-crop parity, not full-page font parity.
- [Cache-accounting harness check](../audit/a16-harness-check-2026-09-07.json).
- Fixed conditions, live external-request failures, iframe measurement limits,
  source-budget adjustment, generator commands, and tested paths are recorded
  in the authoritative report. After-change network trials are local homepage
  evidence, not a production-wide transfer or field-performance claim.

The source change is in `site-src/pages/index.main.html`; published HTML is
owned by `scripts/build-site.py`. The derivative is owned by
`scripts/build-etch-webp.py`. A21 owns combined source receipts, generation,
cache/CSP output, and release validation. No generated file was hand-merged
in this closeout, and no sibling repository was changed.

## Current release verification

- [Site validation succeeded](https://github.com/OKHP3/OverKill-Hill/actions/runs/34231410815)
  at the exact main SHA above.
- [Pages deployment succeeded](https://github.com/OKHP3/OverKill-Hill/actions/runs/34224582972)
  at the same SHA.
- The public `assets/audit/release-manifest.json` returned schema 3 and that
  exact commit during this closeout.
- The public WebP returned 1,862,704 bytes, byte-identical to the GitHub main
  asset. SHA-256:
  `f1611e5c143430997da38bcfcb1b4b908b4b46f2ba4e4d5514088a9610ecabc2`.

These are fresh remote/live readbacks. The original implementation's image,
browser, and measurement receipts were inspected, not rerun on physical
devices. Safari, physical-phone sessions, field metrics, Analytics account
settings, and a controlled production before/after trial remain outside the
evidence. They do not justify claims that the report explicitly excludes.

## Preserved superseded work

A resumed Mac worktree independently measured 32 live trials and eight local
visits per homepage version, and explored a smaller derivative that discards
invisible RGB values under fully transparent pixels. This was superseded by
the accepted exact-RGBA implementation, not an additional required repair.
It is preserved locally on `codex/a16-measured-economics` at `c1cc1a2d`.
It was not published over the accepted implementation. An independent
small-model review reinforced the local-only transfer and image-only parity
claim boundaries. There is no open requirement to ship that alternative.

## Disposition

A16 has no remaining implementation or publication blocker. This closeout
record is a documentation handoff, not another optimization candidate.
Analytics purpose/account decisions belong to W13; combined program
acceptance belongs to A20/A21. A16 task archival does not declare those other
packages complete.
