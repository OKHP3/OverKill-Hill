# D05 static publication options

## Evidence

The repository contains an allowlisted release builder at
`scripts/build-release.py`. Its CLI requires an output directory and a full
40-character commit SHA. The exact build invocation is:

```text
python3 scripts/build-release.py --output site-release --commit <validated-40-character-sha>
```

The builder copies published HTML, required root files, and approved runtime
assets. It rejects unsafe paths and verifies that source files such as
`server.py`, `site-src/pages.json`, `AGENTS.md`, and build/test tooling are not
in the package. The existing release and preview tests exercise this boundary.

The checked-in `.replit` file declares:

```toml
[deployment]
deploymentTarget = "static"
publicDir = "site-release"
```

The repository contains no checked-in Replit static-deployment build command or
other configuration that invokes `scripts/build-release.py` before a static
deployment. The available repository evidence therefore proves the package
builder and the selected publication directory, but does not prove that a
Replit deployment will materialize `site-release` automatically.

## Options

1. **Retire the existing Replit route.** This avoids changing a public route
   whose exact deployment intent and deployment identifier are not recorded in
   this repository. The Replit UI warns that changing deployment type requires
   unpublishing and publishing again; no such action is authorized here.

2. **Republish from a verified staged package.** First arrange an owner-approved
   process that runs the exact builder command above and places its output at
   the configured `site-release` directory. Then inspect the resulting static
   deployment and verify the public edge. The current evidence does not identify
   a Replit-native build hook, so this remains a proposed integration step.

3. **Keep the route unchanged pending an owner decision.** This preserves the
   current public state while leaving the known root-publication exposure
   unresolved. It is not a hardened publication outcome.

## Limits and owner gate

The current Replit UI reports Static, Public, `publicDir` as `.`, and
`over-kill-hill.replit.app` published 13 days ago. It exposes a “Change
deployment type” action and warns that the route must be unpublished and
published again; no standalone unpublish control was observed. Site usage
intent and the exact deployment ID remain unknown.

This D05 work does not deploy, unpublish, push, or mutate Replit. A parent/owner
decision is required between retirement and an owner-approved republish path.
