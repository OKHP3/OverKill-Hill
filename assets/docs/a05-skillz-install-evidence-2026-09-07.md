# A05: Skillz installation journey

Baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`.
Branch: `codex/a05-skillz-install`. Local Windows verification, September 7, 2026.

C01 reproduced in the English source: an example downloaded a nonexistent
`main/skills/family/SKILL.md` path into `.agents/skills/my-skill.md`, omitting
the package directory and supporting files. Nearby copy treated file context
as proof of native client support and promised installation within three minutes.

## Change and public evidence

The guide now installs the complete `mermaid/okhp3-universe-map` package,
version 0.1.4, maturity `draftable`, from public Skillz commit
`1a8686ce386928cccef04b53ac6bb98e0ab40b61`. A pinned source ZIP supplies all
12 package files, including `.gitattributes`, and the repository MIT license.
The Python standard-library copy recipe preserves the license and refuses
an existing destination. Users inspect the contract first, choose a named
client path, and verify files before attempting activation.

Sources read on September 7, 2026:

- [Pinned public package](https://github.com/OKHP3/skillz/tree/1a8686ce386928cccef04b53ac6bb98e0ab40b61/mermaid/okhp3-universe-map)
- [Pinned download](https://github.com/OKHP3/skillz/archive/1a8686ce386928cccef04b53ac6bb98e0ab40b61.zip)
- [Public Git tree](https://api.github.com/repos/OKHP3/skillz/git/trees/1a8686ce386928cccef04b53ac6bb98e0ab40b61?recursive=1)
- [Claude Code project skill paths and invocation](https://code.claude.com/docs/en/skills)
- [GitHub Copilot skill directories and discovery](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)

## Verification

`py -3 -X utf8 tests/test-skillz-install-guide.py --archive dist/a05-validation/skillz.zip -v`
passed five tests. The test extracts and executes the exact Python snippet
from the authoritative page, not a duplicate installer implementation.

- Public Git tree blob hashes match every downloaded package byte and LICENSE.
- Both `.claude/skills/` and `.github/skills/` installs match the complete source.
- Every backtick resource reference under scripts, references, assets, tests,
  and evals in SKILL.md resolves inside the installation.
- The package's 19 generator tests pass in each clean client-path project.
- A repeated installation refuses and preserves a modified SKILL.md and every
  other installed file; an existing file destination is also preserved.
- Missing extracted source fails without creating the client directory.

The archive is an ignored local test input, downloaded without credentials.
The test requires that ZIP and network access to GitHub's public tree API;
it does not install Python dependencies or activate an agent. It is a deliberate
integration check, not added to offline CI discovery.

Site generation and validation ran against an ignored disposable baseline
export at `dist/a05-validation/candidate/`, overlaid with the changed source.
This keeps committed generated outputs under A21 ownership.

| Check | Result |
| --- | --- |
| `py -3 scripts/build-site.py` then `py -3 scripts/build-search-index.py` | PASS; 36 pages, 160 index entries, universe refresh completed |
| Both builders with `--check` | PASS |
| `py -3 scripts/validate-site.py` | PASS with 32 existing locale metadata warnings; no new voice warnings |
| `py -3 scripts/cache-bust.py --check` | PASS; zero changes needed |
| `py -3 scripts/audit-site.py --quiet` | PASS; zero issues |
| `py -3 scripts/check-links.py` | PASS; zero broken links, 31 sitemap URLs, 24 intentional noindex exclusions |
| `py -3 -X utf8 assets/scripts/check-contrast.py` | PASS; initial Windows non-UTF-8 output failed to print, then UTF-8 run passed |
| `git diff --check` | PASS |

Locale detection used the existing i18n page-sync skill in report mode on the
baseline and generated candidate. Both report the same eight stale de/es
landing routes and four in-sync French routes. `/projects/skillz/` is outside
the declared translation scope; no corresponding detail page exists in fr,
de, es, en-gb, or es-mx. No translation or adoption was performed. A preliminary
route-filtered report mislabeled unrelated ledger entries as orphans; the full
report above is the authoritative comparison.

## Integration and unresolved boundaries

- Commit only the English source, the recipe regression test, and this record.
- A21 must regenerate HTML and search/universe artifacts on the combined
  candidate and run the combined release gates. The worker checkout's
  `build-site.py --check` deliberately reports stale `projects/skillz/index.html`
  until that generation occurs. Do not deploy this source-only commit directly.
- A06 may edit separate success-claim hunks in the same Skillz source file.
  Preserve both scopes during integration; no shared CSS/JS changes are needed.
- Claude Code and Copilot activation: NOT RUN. Documented paths and invocation
  guidance are source-backed; copying and generator tests are not activation.
- Browser, screen-reader, and phone acceptance: NOT RUN. This checkout has no
  installed Playwright package; no dependency was added. A20 owns independent
  visitor acceptance on the integrated candidate.
- The pinned package's example commands use `.agents/skills/`; the guide tells
  users to substitute their chosen installed directory. Site input configuration
  and renderer integration remain separate from installation.
- No PR, merge, deployment, sibling write, or canonical-checkout change occurred.
