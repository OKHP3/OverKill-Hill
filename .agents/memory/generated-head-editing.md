---
name: Generated head editing
description: Safe editing guidance for generated HTML heads with packed CSP and social metadata.
---

Generated static pages can place the CSP, SEO metadata, and social-card tags on one very long line. When a normal patch hunk cannot match that line safely, preserve the generated structure and remove only the exact unwanted literal rather than reformatting or regenerating the head.

**Why:** Reformatting a packed head can create unrelated CSP, cache, or metadata drift, while broad patch matching is unreliable on oversized lines.

**How to apply:** Verify the exact tag count before and after the edit, then run the page validators and inspect the diff for unintended metadata changes.