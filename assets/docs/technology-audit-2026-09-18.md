# Technology audit, September 18, 2026

## Result and scope

The deployed solution is a generated static HTML/CSS/JavaScript site. Python
builds and validates it; Node.js runs browser QA. It does not have a Vite,
Tailwind, React, or TypeScript production build. Three preserved TSX mockups
import React, but have no package manifest, lockfile, or installed-version
contract of their own. This distinction comes from executable files and
manifests, not the generic sibling-app examples in AGENTS.md.

This audit covers repository commit
`52a747a9` and the local tracking changes prepared on
`codex/technology-version-tracking`. Sources were retrieved September 18 in
America/Chicago, September 19 UTC. It inventories the public runtime, build/QA,
GitHub workflows, Replit declarations, and preserved media authoring tools.
It does not claim to inspect running Replit or Mac environments or the internal
stacks of separately hosted iframe applications.

The [complete generated version table](../audit/technology-version-inventory-2026-09-18.md)
and [machine-readable evidence](../audit/technology-versions-2026-09-18.json)
contain every npm lock location, direct Python requirement, action SHA/tag,
runtime selector, and the upstream Mermaid package's dependency constraints.
These local generated files are intentionally ignored by Git; future watcher
runs publish equivalents as GitHub Actions artifacts. The durable upgrade
instructions are in [the update policy](../../docs/technology-update-policy.md).

## Main version comparison

These are confirmed repository declarations and live publisher results.
Selectors such as Python `3.11` are not exact installed patch versions.

| Technology | In place | Latest stable verified | Interpretation |
| --- | --- | --- | --- |
| Node.js, repository and CI | 22.19.0 | 26.9.0 Current; 24.21.0 LTS; 22.23.2 in the existing line | Upgrade candidate: supported LTS, coordinated across all declarations. [Node release index](https://nodejs.org/dist/index.json) |
| Node.js, Replit declaration | `nodejs-24` | Same Node releases as above | Already selects the LTS major; installed patch unknown. Conflicts with repository pin |
| npm | No independent pin; Node 22.19.0 bundles 10.9.3 | 12.0.2 | Node 24.21.0 bundles 11.19.0; follow the runtime's bundled npm. [npm registry](https://registry.npmjs.org/npm/latest), [Node index](https://nodejs.org/dist/index.json) |
| Python, CI and Replit | `3.11` / `python-3.11` | 3.14.7; latest 3.11 patch is 3.11.16 | Trial newer stable interpreter before changing selectors. [Python downloads](https://www.python.org/downloads/) |
| Playwright | 1.60.0 | 1.63.0 | Direct npm QA dependency. [Publisher registry](https://registry.npmjs.org/playwright/latest) |
| Lighthouse | 13.4.1 | 13.5.0 | Direct npm QA dependency; not a browser-delivered runtime. [Publisher registry](https://registry.npmjs.org/lighthouse/latest) |
| Mermaid | 11.17.2, self-hosted bundle | 12.0.0 | Major-version review required. [Publisher registry](https://registry.npmjs.org/mermaid/latest) |
| Beautiful Soup | 4.15.0 | 4.15.0 | Current. [PyPI](https://pypi.org/pypi/beautifulsoup4/json) |
| Soup Sieve | 2.9.2 | 2.9.2 | Current; Beautiful Soup dependency pinned explicitly. [PyPI](https://pypi.org/pypi/soupsieve/json) |
| typing-extensions | 4.16.0 | 4.16.0 | Current. [PyPI](https://pypi.org/pypi/typing-extensions/json) |
| Pillow | 12.3.0 | 12.3.0 | Current; image generation/validation. [PyPI](https://pypi.org/pypi/Pillow/json) |
| NumPy | 2.5.3 | 2.5.3 | Audio/animation authoring. [PyPI](https://pypi.org/pypi/numpy/json) |
| SciPy | 1.18.1 | 1.18.1 | Audio synthesis. [PyPI](https://pypi.org/pypi/scipy/json) |
| SoundFile | 0.14.0 | 0.14.0 | Audio file generation. [PyPI](https://pypi.org/pypi/soundfile/json) |
| Mido | 1.3.3 | 1.3.3 | Editable MIDI generation. [PyPI](https://pypi.org/pypi/mido/json) |
| Blender | 5.2.1 LTS in the saved verification record | 5.2.2 LTS | Historical authoring evidence, not a verified running installation. [Blender releases](https://www.blender.org/releases/) |
| FFmpeg | Used, version not recorded | 9.0.2 | Publisher released 9.0.2 on September 18; older cached download pages still show 8.1.2. Use the [release directory](https://ffmpeg.org/releases/) |
| GarageBand, macOS | Used, application version not recorded | 10.4.14 | Native project format numbers are not app versions. [Mac App Store](https://apps.apple.com/us/app/garageband/id682658836) |

Python declarations come from `requirements-qa.txt` and
`assets/murderbird/production/audio/iron-verdict/source/requirements.txt`.
The latter preserves an audio-production recipe, not a deployed server.
There is no database, backend application framework, container build, pnpm
workspace, or root TypeScript compiler configuration in the current solution.

## GitHub Actions

All nine existing action pins resolved to the current stable publisher release
at retrieval. The detailed inventory preserves their full commit SHAs and every
workflow location; a major-only tag is not substituted for the immutable pin.

| Action | Pinned release | Latest stable source |
| --- | --- | --- |
| actions/checkout | 7.0.1 | [7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1) |
| actions/setup-node | 7.0.0 | [7.0.0](https://github.com/actions/setup-node/releases/tag/v7.0.0) |
| actions/setup-python | 7.0.0 | [7.0.0](https://github.com/actions/setup-python/releases/tag/v7.0.0) |
| actions/upload-artifact | 7.0.1 | [7.0.1](https://github.com/actions/upload-artifact/releases/tag/v7.0.1) |
| actions/download-artifact | 8.0.1 | [8.0.1](https://github.com/actions/download-artifact/releases/tag/v8.0.1) |
| actions/configure-pages | 6.0.0 | [6.0.0](https://github.com/actions/configure-pages/releases/tag/v6.0.0) |
| actions/upload-pages-artifact | 5.0.0 | [5.0.0](https://github.com/actions/upload-pages-artifact/releases/tag/v5.0.0) |
| actions/deploy-pages | 5.0.1 | [5.0.1](https://github.com/actions/deploy-pages/releases/tag/v5.0.1) |
| actions/github-script | 9.0.0 | [9.0.0](https://github.com/actions/github-script/releases/tag/v9.0.0) |

## Languages, platforms and services

| Technology | In-place contract and latest applicable reference | Update treatment |
| --- | --- | --- |
| HTML | HTML5 doctype; [WHATWG Living Standard](https://html.spec.whatwg.org/multipage/) | Browser compatibility and structural checks, not a package bump |
| JavaScript / ECMAScript | Native browser JavaScript and ES modules; no transpiler target | Latest edition is [ECMAScript 2026, edition 17](https://ecma-international.org/publications-and-standards/standards/ecma-262/); test adopted features in browsers |
| CSS | Hand-authored CSS, custom properties, responsive rules; no preprocessor | [CSS Snapshot 2025](https://www.w3.org/TR/css-2025/) is the current snapshot; modules have separate levels, not one installable CSS version |
| Bash | `scripts/post-merge.sh` and workflow shell steps; no version pin | GNU Bash [5.3](https://www.gnu.org/software/bash/manual/html_node/index.html) release line; host-managed patch/build |
| Git | Workstation 2.55.0.windows.5; CI/Replit executable versions unrecorded | Latest Windows distribution [2.55.0.windows.5](https://github.com/git-for-windows/git/releases/tag/v2.55.0.windows.5); update through host tooling |
| GitHub CLI | Workstation 2.96.0; audit/operator tool, not a site dependency | [2.101.0](https://github.com/cli/cli/releases/tag/v2.101.0); host maintenance |
| pip | Unpinned with Python; local interpreter has 25.1.1 | [26.2.1](https://pypi.org/pypi/pip/json); establish a tested host bootstrap policy |
| GitHub Actions runner / Ubuntu | `ubuntu-latest`; exact image not fixed by repository | [Ubuntu 26.04 GA migration](https://github.blog/changelog/2026-09-17-ubuntu-26-generally-available-and-latest-migration/) announced September 17. Actual per-run image comes from job logs |
| Nix / Nixpkgs on Replit | `stable-25_05`; no immutable resolved system-package lock | Upstream stable [26.05](https://nixos.org/blog/announcements/2026/nixos-2605/). Replit support for a replacement channel remains unverified |
| Replit | `web`, `nodejs-24`, `python-3.11`; static release directory | Managed platform, no single application version. [Configuration contract](https://docs.replit.com/features/project-setup/configuration) |
| GitHub Pages and Cloudflare | Pages workflow, CNAME, hosting-policy references | Managed services with no repository-controlled semantic version; current live Cloudflare routing not verified in this audit |
| Google Fonts | CSS2 API, Alfa Slab One, DM Sans, JetBrains Mono | Provider-managed font files; no pinned font revision; rendering and availability checks |
| Google Analytics | GA4 through `gtag.js` | Provider-managed script; `G-...` is an account/stream identifier, not a library version |
| JSON, JSON-LD, YAML, TOML, XML, SVG, Markdown and Web App Manifest | Data, metadata, configuration and content formats present in the tree | Validate with their consuming parsers/specifications; file-format labels are not runtime package versions |

The 19 Nix attributes declared in `.replit` are: `glib`, `nss`, `nspr`,
`libdrm`, `at-spi2-atk`, `pango`, `cairo`, `libxkbcommon`, `xorg.libX11`,
`xorg.libXcomposite`, `xorg.libXdamage`, `xorg.libXext`, `xorg.libXfixes`,
`xorg.libXrandr`, `mesa`, `libgbm`, `alsa-lib`, `cups`, and `got`.
The `web` module is separate and may supply additional dependencies. Exact
installed versions and latest versions supported by Replit are UNKNOWN without
that host's resolved package inventory. Upstream NixOS 26.05 does not establish
those package versions or authorize inventing a Replit channel.

Embedded sites belong to OverKill-Hill-FoundRy, abrahamic-reference-engine,
glee-fully-chai-chasers, kierans-lifetrkr, mermaid-diagram-bpmn,
mermaid-theme-builder, and skillz. Their iframe URLs are unversioned integration
boundaries. Their internal technology versions require audits in those repos.

## Browser bundles and transitive coverage

The root lockfile has **111 package locations**, represented as **110 distinct
name/version rows**, including 108 transitive rows. The generated appendix
checks each against the npm publisher's `latest` stable tag. A higher available
major does not mean that a parent's range can safely accept it.

Playwright 1.60.0's [publisher browser manifest](https://raw.githubusercontent.com/microsoft/playwright/v1.60.0/packages/playwright-core/browsers.json)
specifies Chromium/Headless Shell 148.0.7778.96 (revision 1223), Firefox 150.0.2
(1522), WebKit 26.4 (2287), bundled FFmpeg revision 1011, winldd 1007, and
Android helper 1001. CI installs Chromium; Firefox/WebKit and other helpers are
not claimed as installed merely because they appear in the package manifest.
Playwright 1.63.0's [corresponding manifest](https://raw.githubusercontent.com/microsoft/playwright/v1.63.0/packages/playwright-core/browsers.json)
specifies Chromium 153.0.8010.12 (1243), Firefox 155.0 (1543), and WebKit 26.6
(2359). These are the engine builds supported by that Playwright release, not
a claim about the latest consumer-browser stable channels. Update as a bundle.

Mermaid's [11.17.2 package metadata](https://registry.npmjs.org/mermaid/11.17.2)
lists 22 direct package requirements, including D3, DOMPurify, KaTeX, Cytoscape,
Marked and layout engines. The appendix lists all 22 constraints and their
latest stable versions. The checked-in bundle lacks a resolved publisher build
lock/SBOM, so exact internal versions are UNKNOWN. Requirements may include
build/type packages; they are not all separately loaded browser scripts.

The media environment has unpinned indirect dependencies: CFFI (latest
[2.1.1](https://pypi.org/pypi/cffi/json)), pycparser
([3.0](https://pypi.org/pypi/pycparser/json)), and packaging
([26.3](https://pypi.org/pypi/packaging/json)). SoundFile also relies on native
libsndfile (latest [1.2.2](https://github.com/libsndfile/libsndfile/releases/tag/1.2.2)).
The mastering recipe uses libmp3lame, whose [latest LAME release is 4.0](https://lame.sourceforge.io/).
Installed native-library versions and NumPy/SciPy BLAS/LAPACK builds depend on
the selected wheels and host and were not recorded. Capture a resolved
environment before claiming byte-reproducible rebuilds.

## Technologies mentioned but not deployed here

| Technology | In place | Latest stable checked for reference |
| --- | --- | --- |
| TypeScript | TSX mockup source only; compiler version unknown, no build manifest | [7.0.2](https://registry.npmjs.org/typescript/latest) |
| React | Imported by three preserved mockups; version unknown | [19.3.0](https://registry.npmjs.org/react/latest) |
| Vite | No build/configuration dependency | [8.3.0](https://registry.npmjs.org/vite/latest) |
| Tailwind CSS | No build/configuration dependency | [4.3.3](https://registry.npmjs.org/tailwindcss/latest) |

No package updater is added for these absent build dependencies. AutoCAD R10
is a governance constraint, not an executable site dependency. Skill package
metadata and narrative project version badges are not application library pins.

## Confirmed findings and evidence boundaries

| Claim | Tier | Evidence | Consequence and next check |
| --- | --- | --- | --- |
| Repository Node pin disagrees with Replit and the previous README wording | CONFIRMED | `.nvmrc`, `.node-version`, manifests, `.replit`, README before this change | Clean install behavior differs across hosts. Coordinate declarations; README now reports the actual pin |
| Local installed QA differs from declarations | CONFIRMED | Node 24.11.1, npm 11.6.2, installed Playwright 1.62.1; no installed Lighthouse package at inspection | Local browser results would not validate the lockfile. Use an isolated clean environment |
| Selected local Python is a prerelease | CONFIRMED | Python 3.14.0rc1; QA packages match the four pins | Passing local tests does not prove stable 3.14 or CI 3.11; run those environments before a runtime migration |
| Existing Dependabot ran monthly and omitted the nested media requirements | CONFIRMED | `.github/dependabot.yml` before this change | Daily checks and explicit media scope now prepared. Confirm logs after merge |
| Existing Mermaid watcher detects but does not update the bundle | CONFIRMED | `.github/workflows/mermaid-version-watch.yml` | Retain intentional reviewed bundle updates; 12.0.0 needs migration work |
| Stack checker contains fixed technology versions | CONFIRMED | `scripts/check-stack-conformance.py`; absent from Site Validation steps | Future PRs must co-update applicable constants; broader checker refactor remains planned |
| Running Replit/Mac versions, resolved native libraries, service internals | UNKNOWN | No connected-host inspection in this audit | Do not claim parity or a complete binary SBOM; capture host inventories |
| Automatic update machinery is operational on GitHub | UNKNOWN until merge and first successful run | Local files/tests only | Activation sequence is in the policy |

## Deliverables and next action

The online run returned 161 comparison rows: 72 current, 62 with a newer
publisher version, and 27 with unresolved exact in-place versions. All release
lookups succeeded. The 27 unknown comparisons are the 22 Mermaid publisher
constraints, three unlocked Python media dependencies, FFmpeg and GarageBand.
The 62 newer-version rows include transitive dependencies and Node Current;
they are not 62 independent upgrades that should be installed together.

Prepared a dependency-free inventory script, a daily GitHub watcher, daily
Dependabot checks for four scopes, focused tests, and a staged upgrade plan.
Validation: 15 Python regression tests and seven workflow issue-lifecycle tests
passed; the new workflow passed actionlint 1.7.12; both YAML files parsed;
generated HTML and search-index freshness checks passed; structural site
validation completed with zero errors and existing locale/voice warnings.
These are local checks on the observed local runtimes. Full remote CI,
Dependabot execution, Replit, and deployment were not exercised by this task.

No runtime, package, vendor bundle, rendered media, GitHub setting, or deployment
was upgraded by this audit. The requested update mechanism is reviewable on
the task branch; the next action is to merge it and verify its first run, then
start the coordinated Node upgrade.
