# A20 bounded visual closeout

**Result: PASS for the feasible automated sample on `https://overkillhill.com`, candidate `f4a353`.** `CNAME` resolves to `overkillhill.com`. Existing installed Playwright ran 24 samples: Chromium and Firefox across the homepage, search, contact, and First Diagram writing route at a 390×240 short-height viewport plus 640×844 and 320×844 CSS viewport reflow equivalents for 200% and 400% zoom from a 1280 CSS-pixel baseline.

Every sample returned HTTP 200. `document.fonts.ready` completed with `document.fonts.status === "loaded"`. Document and body `scrollWidth` matched `clientWidth` in all 24 samples, so no horizontal overflow was observed. Results are preserved in [the audit record](../audit/a20-closeout-visual-2026-09-08.json). The disposable local probe output remains ignored.

This is viewport emulation and responsive reflow evidence. Playwright did not control native browser zoom, so it cannot close actual 200%/400% browser-zoom acceptance. Human AT, native macOS, VoiceOver/NVDA, physical touch, real-font visual judgment, and audio-backed checks remain outside this automated result.
