---
name: SEO fixture baselines
description: How metadata regression mutations stay meaningful across source and generated fixtures
---

SEO regression mutations that exercise both source and rendered validators must differ from both baselines. Source manifests and committed generated fixtures can intentionally be out of date with one another, so a mutation equal to either baseline can make one half of the test pass without exercising the intended guardrail.

**Why:** A social-image parity regression initially used a value that matched one fixture baseline, causing the corresponding test to pass without detecting drift.

**How to apply:** When one mutation is reused for source and generated checks, compare its value with both current metadata baselines before committing the fixture.