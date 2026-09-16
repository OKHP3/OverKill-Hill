---
name: External health CSP merge
description: How browser CSP-blocked requests must be classified when external dependency results are merged across routes.
---

The external-health merger must classify CSP-only dependencies from structured `securitypolicyviolation` evidence, not browser-specific request-failure text, while giving any real HTTP error or non-CSP network failure outage precedence across routes.

**Why:** Browser updates can change request-failure markers. Treating every request failure as an outage makes policy-only checks appear operationally unavailable; treating CSP as dominant hides a real 4xx/5xx response or network failure from another route using the same URL.

**How to apply:** Capture the standard securitypolicyviolation event before navigation and correlate its normalized blocked URI and route to dependency failures. Keep console diagnostics and browser failure text in the report for evidence, but classify state using HTTP errors or failures without matching structured CSP evidence first, then CSP blocking, then successful/no-response states. Preserve both route references and response evidence in regression fixtures.

External-health route checks should track each external request until its response or failure event, then wait for a short quiet window before closing the page, with a hard upper bound for requests that never terminate.

**Why:** A fixed post-load sleep can close the page before a delayed HTTP failure arrives, turning a real outage into an incomplete no-response record.

**How to apply:** Use terminal browser events for classification and keep the settle timeout bounded so slow or hanging third-party resources cannot make monitoring unbounded.

Repeated external failures should be grouped by public route and browser reason with an occurrence count; console output should aggregate repeated reasons while the JSON report preserves route-specific groups.

**Why:** Retaining every identical event makes incident output noisy, while collapsing across routes removes the attribution needed to identify affected pages.

**How to apply:** Normalize dependency URLs before grouping, keep distinct route/reason combinations as separate records, and include the count in each grouped failure record.