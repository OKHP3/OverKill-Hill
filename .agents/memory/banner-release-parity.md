---
name: Banner release parity
description: Cross-artifact release validation required before repairing site-wide featured-article banners.
---

The banner checker must reject a source/generated featured-article release disagreement before scanning or writing any banner file.

**Why:** Repairing against each artifact's local release can make source and generated pages advertise different featured releases while reporting both representations as individually valid.

**How to apply:** Validate that both article artifacts have exactly one release label, then compare the normalized releases and fail with both artifact paths and the featured route before entering any update or dry-run repair loop.