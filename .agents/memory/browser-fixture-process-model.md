---
name: Browser fixture process model
description: Constraint for browser QA tests that serve deterministic pages from an in-process local HTTP server.
---

When a browser QA test starts its fixture HTTP server in the same Node process,
launch the QA command asynchronously rather than with a synchronous child
process call.

**Why:** A synchronous child-process call blocks the parent Node event loop, so
the fixture server cannot answer the browser and the test appears to hang until
the child timeout.

**How to apply:** Use an async child-process helper, keep the fixture server
alive for the duration of the child, and assert the child exit status and
diagnostic output after it closes.