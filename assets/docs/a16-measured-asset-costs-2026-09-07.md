# A16: measured asset and runtime costs

## Disposition

Ready for A21 integration review, with regional source-receipt reconciliation
still required. No merge or deployment was performed. Baseline:
`98922aebf71d90b2b18ecc34c8b00a041fff51c7`.

The homepage's ETCH-AI-SKETCH PNG was the largest measured first-party
contributor after scrolling. A lossless WebP reduces that image from 2,494,141
to 1,862,704 file bytes (631,437 bytes, about 25.3%). The original PNG remains
unchanged and is still the fallback and social-image URL. Only the existing
homepage image receives a `picture`/`source` wrapper. Its dimensions, alt text,
lazy loading, link, accepted illustration, and all user-facing copy stay intact.
No CSS, browser runtime, font, analytics, or locale policy changed.

## Method and scope

Retained machine receipts: [baseline transfers](../audit/a16-before-2026-09-07.json),
[candidate transfers](../audit/a16-after-2026-09-07.json),
[rendered parity](../audit/a16-parity-2026-09-07.json), and
[final harness check](../audit/a16-harness-check-2026-09-07.json).

`scripts/measure-page-costs.mjs` used Chromium 151.0.7922.34, Node 24.11.1,
Windows, and the existing Playwright dependency. Three independent contexts
per route/device each performed a cold visit and a warm revisit through
`about:blank`. Cache stayed enabled. Desktop: 1280x800, DPR 1, CPU factor 1.
Phone emulation: 390x844, DPR 3, touch/mobile enabled, CPU factor 4.
Both used CDP 20 Mbps download, 5 Mbps upload, and 40 ms latency, light mode,
and reduced motion. This is Chromium phone emulation, not a physical phone.

The dedicated loopback fixture served this checkout with gzip level 6 for
text and `public, max-age=3600` for responses. This intentionally differs from
the project's no-cache preview server and does not claim to reproduce Pages
headers, Brotli, HTTP/2, CDN geography, or actual visitor connections.
External requests were live and unmodified. The initial window ended two
seconds after `load`; scrolling advanced 800 pixels every 100 ms through the
initial document height, followed by another two seconds. These are fixed
experiment windows, not an exhaustive interaction or lazy-media inventory.

Bytes are CDP `loadingFinished.encodedDataLength`, including response overhead.
First-party and external totals are separate. Failed and incomplete requests
are retained, never assigned invented completed lengths. Only the page CDP
target is observed; out-of-process iframe traffic and CPU may be absent.
The embed totals therefore cannot establish the embedded application's full
cost. Request query strings and analytics parameters are omitted from receipts.

The baseline/candidate receipts undercount memory-cache hits in the `cached`
flag because a later response event overwrote the earlier cache event. The
final runner preserves that flag. A fresh one-trial pair on both devices
verified 11 warm cache hits and reproduced every candidate first-party byte
total. The measured byte totals were unaffected; do not use the older receipts'
cache-hit counts as complete inventories.

Baseline has 48 visits across home, the long First Diagram article, MurderBird,
and the Mermaid Theme Builder page. After-change evidence repeats the 12 home
visits because that is the only changed page. All homepage baseline visits
finished before the homepage edit; other baseline pages stayed unchanged.
The receipts' `sourceCommit` is the baseline HEAD; `after` explicitly measures
the uncommitted candidate source and derivative subsequently committed with
this report, not a different released commit.

## Observed homepage transfer

The first-party counts below were identical across all three trials in each
cell. Scrolled counts are cumulative, including initial requests.

| Device and cache | Before initial bytes | After initial bytes | Before scrolled bytes | After scrolled bytes |
| --- | ---: | ---: | ---: | ---: |
| Desktop cold | 2,651,420 | 2,020,003 | 2,651,420 | 2,020,003 |
| Phone cold | 255,534 | 255,553 | 2,749,865 | 2,118,448 |
| Desktop warm | 0 | 0 | 0 | 0 |
| Phone warm | 0 | 0 | 0 | 0 |

Desktop initial and phone scrolled transfers decreased by 631,417 bytes.
Phone initial transfer increased by 19 bytes of compressed markup. The PNG
was outside the phone's initial lazy-loading window. There is no demonstrated
phone initial-transfer improvement or warm-transfer saving.

The original source budget of 5,451,266 bytes included unused responsive
candidates and fallback assets. The new inventory is 7,314,112 bytes because
it now includes both the preserved PNG and the WebP. The budget rises by the
exact inventory delta, 1,862,846 bytes, to 7,630,014; the original 315,902-byte
headroom is unchanged. This is not a network-budget relaxation disguised as
an optimization. Other route budgets are unchanged.

## Runtime and external costs

Cold homepage external completed bytes were approximately 250.5 KB in both
versions: approximately 174.1 KB Google tag JavaScript and 76.3 KB observed
Google font CSS/fonts. The desktop selected the 960-pixel MurderBird WebP;
the DPR-3 phone selected the 1536-pixel derivative. These existing responsive
choices and all font requests remain intact.

The baseline receipts include all four routes, request-level costs, browser
image choices, long tasks, and navigation timings. These runtime observations
are diagnostic only. For example, desktop median `load` changed from about
1,634 to 1,532 ms while median accumulated long-task duration increased from
117 to 154 ms. Phone median `load` changed from 8,063 to 3,286 ms even though
its initial bytes barely changed. Shared-machine contention, live external
responses, browser decode behavior, and the small sequential sample prevent
attributing timing differences to this patch. No LCP, INP, CLS, field,
conversion, or general speed improvement is claimed.

Analytics collection requests reported `net::ERR_ABORTED` in the observed
windows. That is retained as a failed request, not proof of successful
collection or an analytics-policy defect. Account retention, usefulness,
advertising settings, and dashboard results were not inspected. Before any
future policy decision, useful questions would be whether visitors reach a
usable tool, follow a source/evidence link, or initiate contact, and whether
those measures actually inform an owner decision. This patch adds no tracking
and does not infer authorization to change the accepted policy.

## Artwork and rendered parity

`scripts/build-etch-webp.py` uses the existing Pillow dependency, lossless
encoding, and `exact=True`. It verifies all 1536x1024 decoded RGBA pixels,
including hidden RGB values. The original PNG matches the baseline Git blob.

- PNG SHA-256: `785299b7d50f1280771bd97740da442945df18e2ec886ca6c499fbc15e98d1c8`
- WebP SHA-256: `f1611e5c143430997da38bcfcb1b4b908b4b46f2ba4e4d5514088a9610ecabc2`

`scripts/check-etch-parity.mjs` tests the actual generated candidate in light
and dark themes at both device sizes. It captures the WebP, removes its source
wrapper to exercise the PNG fallback, and compares geometry and image crops.
All four geometries match exactly. Browser-scaled RGB differences are at most
1/255 per channel, with mean differences below 0.05/255. Source pixels are
exact; rendered screenshots are not byte-identical. Visual inspection found
the same composition, labels, proportions, and colors. The parity test blocks
external requests and only certifies the image crop, not full-page font parity
or external availability. Captures remain under `.local/a16/parity/`.

## Verification and remaining acceptance

PASS: lossless builder validation; four browser image comparisons; generated
HTML (36 pages); search freshness (160 entries); cache fingerprints; CSP
generation (56 pages); structural validation (existing warnings retained);
static audit (zero issues); internal links (zero broken); locale links;
five performance-budget unit tests; five homepage hero-parity tests; and
JavaScript syntax checks.

FAIL requiring A21: `scripts/check-regional-drafts.py` reports the homepage
canonical source stale against both regional release receipts. The English
change contains no new strings. Reconcile the receipt against the frozen
integrated source after review; do not claim translation acceptance or publish
the regional drafts. The named receipt is
`i18n/pilot/source-hashes-murderbird-stills-2026-09-06.json`.

NOT RUN: full integrated browser/accessibility matrix, CI, real Safari or
physical-device checks, field metrics, and production before/after delivery.
A21 owns integration, generated-output reconciliation, and any release. A14
was notified to retain the picture/source in presentation variants. No upstream
runtime edit is needed for this bounded change.

Reproduce locally after installing only the existing locked dependencies:

```text
node scripts/measure-page-costs.mjs --label=baseline --trials=3
py -3 scripts/build-etch-webp.py
py -3 scripts/build-site.py
node scripts/measure-page-costs.mjs --label=candidate --trials=3 --routes=/
node scripts/check-etch-parity.mjs --base=http://127.0.0.1:8166
```

Run the baseline command on the baseline revision and the candidate commands
on the candidate revision. The parity command expects an already running
loopback preview on the supplied port. Measurements start and close their own
ephemeral loopback servers. On non-Windows systems use `python3` instead of
`py -3`.
