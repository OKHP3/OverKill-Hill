# Release evidence contract

Use these tiers in every report:

- **Confirmed:** command output, parsed artifact, browser observation, or commit
  identity captured during this run.
- **Inferred:** a conclusion derived from confirmed evidence; name the inference.
- **Unknown:** unavailable because a tool, route, credential, or third party was
  not reachable.
- **Not run:** intentionally skipped; give the reason.

Each check records `id`, `command`, `status`, `commit`, `evidence`, `artifact`,
and `limitations`. A report may recommend a fix, but validation does not apply
it. Browser success with external requests blocked is not evidence that embeds
work in production.