---
name: External health CSP merge
description: How browser CSP-blocked requests must be classified when external dependency results are merged across routes.
---

The external-health merger must ignore the browser-generated CSP request failure when classifying a CSP-only dependency, while giving any real HTTP error or non-CSP network failure outage precedence across routes.

**Why:** Chromium reports a CSP-blocked request through the request-failure channel with an error marker of `csp`. Treating every request failure as an outage makes policy-only checks appear operationally unavailable; treating CSP as dominant hides a real 4xx/5xx response from another route using the same URL.

**How to apply:** Keep CSP diagnostics and dependency failures in the report for evidence, but classify merged state using HTTP error responses or non-CSP failures first, then CSP blocking, then successful/no-response states. Preserve both route references and response evidence in regression fixtures.