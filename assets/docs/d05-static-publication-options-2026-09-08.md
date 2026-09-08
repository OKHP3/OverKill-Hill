# D05 static publication options

## Evidence

The repository contains an allowlisted release builder at
`scripts/build-release.py`. Its CLI requires an output directory and a full
40-character commit SHA. The exact build invocation is:

```text
python3 scripts/build-release.py --output .local/site-release --commit <validated-40-character-sha>
```

The builder copies published HTML, required root files, and approved runtime
assets. It rejects unsafe paths and verifies that source files such as
`server.py`, `site-src/pages.json`, `AGENTS.md`, and build/test tooling are not
in the package. The existing release and preview tests exercise this boundary.

This proposal branch changes `.replit` to declare:

```toml
[deployment]
deploymentTarget = "static"
publicDir = ".local/site-release"
```

The proposal now supplies `build = "python3 scripts/build-replit-release.py"`.
Official Replit documentation describes a Static Deployment public directory and
optional build command ([deployment types](https://docs.replit.com/features/publishing/deployment-types));
the configuration reference defines the deployment `build` string
([configuration](https://docs.replit.com/features/project-setup/configuration)).
This verifies the configuration model, but does not verify this workspace's
deployment settings until the owner inspects them. Replit availability of Git
metadata during the deployment build is not verified; the wrapper therefore
fails closed unless `REPLIT_RELEASE_SHA` matches `HEAD` in a clean checkout.
The current `origin/main` checkout and the observed Replit deployment still use
`publicDir = "."`; the `.local/site-release` setting exists only in this unpublished
proposal branch.

The regression test is wired into the existing GitHub Actions workflow and has
been run locally with the release-package and preview-server tests.

The available public probes are status-only evidence: `/server.py` returned
HTTP 200 with Python source and `/site-src/pages.json` returned HTTP 200 with
JSON. Those observations identify the current exposure but do not establish
the complete deployed file inventory or deployment provenance.

## Options

1. **Retire the existing Replit route.** This removes the exposure, but
   interrupts users of that URL. The exact deployment intent, usage, and
   deployment identifier are not recorded in this repository. The Replit UI
   exposes a “Shut down” control that says the published app will cease to
   exist and billing will be canceled; no such action is authorized here.

2. **Republish from a verified staged package.** First arrange an owner-approved
   process that runs the exact builder command above and places its output at
   the configured `.local/site-release` directory. Then inspect the resulting static
   deployment and verify the public edge. Current UI inspection did not expose
   a build field, so the owner must verify that the documented build setting is
   honored before publication.

3. **Keep the route unchanged pending an owner decision.** This preserves the
   current public state while leaving the known root-publication exposure
   unresolved. It is not a hardened publication outcome.

## Limits and owner gate

The current Replit UI reports Static, Public, `publicDir` as `.`, and
`over-kill-hill.replit.app` published 13 days ago. It exposes a “Change
deployment type” action and a “Shut down” control that cancels billing and
removes the published app. Site usage
intent and the exact deployment ID remain unknown.

This D05 work does not deploy, unpublish, push, or mutate Replit. That boundary
comes from the A21 integration directive for the A08/D05 separate proposal; it
is an explicit task restriction, not an inferred skill approval requirement. A
parent/owner decision is required between retirement and an owner-approved
republish path.

## Authorized remediation and staging behavior

On September 8, the parent relayed the owner's explicit instruction to fix the
public source exposure. This supersedes the earlier no-deployment restriction
for this narrow repair; retirement is not selected. Repository sources remain
intact. Publication still requires reviewed code and successful checks.

The deployment wrapper requires `REPLIT_RELEASE_SHA` to be deliberately set in
the deployment environment to the accepted, CI-validated commit. It verifies
that HEAD matches and the checkout is clean; these checks do not independently
attest that GitHub CI passed. Missing Git metadata or the variable fails closed.
There is no repository-root fallback.

Before building, previous public output moves into unique private recovery
storage under `.local/replit-release-*/previous`. Failed preflight, build, or
package verification leaves `.local/site-release` absent. Successful build and
manifest verification promote only the new package. Recovery and failed staging
bytes remain private for inspection; no recursive deletion is performed.

The existing `.local/` ignore and source-scanning exclusions apply to both the
public package and private staging. The release builder uses explicit public
route and asset allowlists and cannot recursively package these directories.
Actual publishing must confirm the effective directory, deployment variable,
build execution, and successful public/negative route probes.
