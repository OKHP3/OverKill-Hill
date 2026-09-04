---
name: CSP enforcement and builder parity
description: Durable constraints for the canonical CSP policy and its static-page generation boundary.
---

The canonical CSP policy is enforcing in source, while response-header
enforcement depends on the deployed edge actually applying `_headers`. The
static HTML meta policy still provides browser enforcement when the host does
not apply repository headers.

**Why:** GitHub Pages can serve the committed files while ignoring `_headers`,
so a clean repository policy must not be presented as proof that the live edge
has applied the response header.

**How to apply:** Keep edge verification separate from source-policy
validation. When changing policy generation, preserve the exact CSP meta-tag
serialization in the static builder or the builder check and CSP generator can
drift even when their policy values match. Keep the Skillz published summary
origin in `connect-src` when that runtime fetch is present. Keep browser
regression fixtures outside the published-page discovery set: their
intentionally weakened or missing policies must not be regenerated or treated
as live-page drift.