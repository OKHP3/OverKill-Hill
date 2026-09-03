---
name: SEO source/render boundary
description: Why SEO validation must distinguish manifest intent from generated HTML and separately maintained locale pages
---

SEO guardrails should validate both the source manifest and the generated document. The renderer may intentionally normalize legacy fields, while localized pilot pages may be maintained outside the English manifest.

**Why:** A rendered-page-only check can miss source drift, and a source-only check can reject an intentional compatibility transform or accidentally change locale indexing boundaries.

**How to apply:** Keep source-contract checks focused on manifest-owned pages, compare generated metadata after rendering, and explicitly document any maintained surfaces that are outside the manifest.