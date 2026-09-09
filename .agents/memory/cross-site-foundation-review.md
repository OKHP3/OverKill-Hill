---
name: Cross-site foundation review
description: Durable review rule for validating shared theme behavior across the three sibling static sites.
---

The cross-site theme audit must compare the shared foundation bytes and exercise each site's actual body and header hooks from an immutable reviewed revision when one is supplied. A local workspace may not contain the sibling checkouts, so the ordinary fixture regression and the three-site audit are intentionally separate modes.

**Why:** The three repositories can drift independently, and a local OverKill Hill checkout alone cannot prove what Glee or AskJamie publish.

**How to apply:** Use the reviewed revision input for release evidence; require site name, revision, asset fingerprint, and markup-hook context in any drift failure.

The shared `app.js` search-index URL must remain stable across sites; cache-busting belongs in each site's published HTML and service-worker references rather than in the byte-identical runtime.

**Why:** Glee's site-specific cache-buster and the cross-site browser fixtures otherwise disagree about the runtime URL, creating either foundation drift or false loading failures.

**How to apply:** Keep the shared runtime URL unversioned, version generated page/worker references, and test both the stable runtime contract and the site-specific generated references.