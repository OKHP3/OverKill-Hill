# A15 browser acceptance report

Date: September 8, 2026
Base: local owned preview at `http://127.0.0.1:5016`
Scope: Contact reader-orientation copy and the first-diagram-is-a-liar evidence route.

## Result

PASS for the focused browser checks. The new Contact guidance and evidence route were visible at desktop and phone sizes, in light and dark themes, with reduced motion, with `app.js` blocked, and with JavaScript disabled. No horizontal overflow was detected. The inquiry link remained `mailto:contact@overkillhill.com`; no message was sent.

The evidence route exposed all five requested destinations: `#scoring-model`, `#v1-diagrams`, `#v2-diagrams`, `#council-scoring`, and `#version-history`. Keyboard focus and Enter activation passed for every link, each target received focus in scripted mode, and Back then Forward restored the expected URLs. The original four-link jump menu remained intact. With JavaScript disabled, native hash navigation and history still worked. The French Contact page also contained the translated block and unchanged mailto destination.

## Focused test

`tests/test-reader-orientation.mjs` ran 97 assertions across four contexts:

- desktop, light, normal motion
- 390 x 844 phone, dark, reduced motion
- desktop with `assets/js/app.js` blocked
- desktop with JavaScript disabled

The final root-reviewed run corrected the blocked-script matcher to include the version query and positively counted aborted requests. Visible-heading/route assertions also pass. Native fallback is checked without claiming scripted focus when the script is absent.

All assertions passed on Node 24.11.1 and the repository's declared Playwright dependency.

Desktop and phone Contact screenshots were retained outside the repository at `C:\Users\jamie\.codex\visualizations\2026\09\08\a15-contact-desktop.png` and `C:\Users\jamie\.codex\visualizations\2026\09\08\a15-contact-phone.png` and visually inspected. The additions were readable, wrapped within their cards, and preserved the existing support boundary.

## Limits

This is browser automation evidence only. It does not claim a human assistive-technology session, screen-reader acceptance, external mail-client operation, live deployment acceptance, or locale translation acceptance. The automated phone check covered the requested narrow viewport and overflow condition; it did not replace a full visual design review at every breakpoint or zoom level.

Reproduce with an owned preview server and `BASE_URL=http://127.0.0.1:<port> node tests/test-reader-orientation.mjs`. Screenshots are optional through `A15_SCREENSHOT_DIR`; the test has no machine-specific output path.
