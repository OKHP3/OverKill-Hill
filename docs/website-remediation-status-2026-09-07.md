# Website remediation integration status

September 7, 2026. A21 is the sole integration PM. This is an active acceptance ledger, not a completion claim.

## Baseline and boundaries

- Isolated worktree: `/Users/okh/.codex/worktrees/6b42/OverKill-Hill`.
- Branch: `codex/a21-release-integration`.
- Initial clean baseline: `98922aebf71d90b2b18ecc34c8b00a041fff51c7`. A01/A02 are already included; do not duplicate them.
- No push, PR, main merge, deployment, account change, or sibling synchronization is authorized.
- The owner checkout is read-only context. Shared Git metadata changes only support the isolated branch.
- Historical production `ca38d5b9` is not assumed current. Architect relays A19 observation of schema 3 at `98922aeb`; A21 live-byte verification remains pending.

## Integration ownership

Runtime order: A03, then A04, then A13. Workflow order: A07, then A08, then A10, then A17, with T01 reconciled explicitly before freeze. Content dependencies: A06 before A11, A11 before A12; A14 selection before dependent presentation implementation. W13 policy review coordinates with A16 measurements. A18 `.replit` deployment changes must preserve A08 runtime changes.

Each incoming commit requires clean/known worker status, source review, focused tests and explicit acceptance limits. Integrate authoritative source changes; regenerate HTML, search, universe, CSP and fingerprints with owning tools. Never hand-merge generated conflicts. Proposal-only presentation and infrastructure deliverables do not authorize applying their alternatives.

## Package ledger

| Package | Task ID | Handoff status | Integration status |
| --- | --- | --- | --- |
| A03 | `01a07aaf-0dfd-7e83-911b-710fe5f1ef0c` | Pending reviewed handoff | Not integrated |
| A04 | `01a07aaf-0e5b-7a32-9aa2-19994121f75f` | Pending reviewed handoff | Not integrated |
| A05 | `01a07aaf-0dfd-7e83-911b-70ec8de457e1` | Pending reviewed handoff | Not integrated |
| A06 | `01a07aaf-0dfd-7e83-911b-70cbac70080a` | Pending reviewed handoff | Not integrated |
| A07 | `01a07aaf-0e55-7e51-9720-3a8e5ad36deb` | Pending reviewed handoff | Not integrated |
| A08 | `01a07aaf-5674-7bc3-b036-6968cb60db9b` | Pending reviewed handoff | Not integrated |
| A09 | `01a07aaf-58b6-7fb1-b286-2876960fdba5` | Pending reviewed handoff | Not integrated |
| A10 | `01a07aaf-5ba9-7d53-940f-84bfb3b54667` | Pending reviewed handoff | Not integrated |
| A11 | `01a07aaf-5ba9-7d53-940f-8490678d2bcd` | Pending reviewed handoff | Not integrated |
| A12 | `01a07aaf-5bfc-7a40-a63b-5214a7bbc8e7` | Pending reviewed handoff | Not integrated |
| A13 | `01a07aaf-5d32-7d93-a007-600994bdcd21` | Pending reviewed handoff | Not integrated |
| A14 | `01a07aaf-5f84-7e00-8322-2de95f2e05fd` | Pending reviewed handoff | Not integrated |
| A15 | `01a07aaf-662f-7321-a2df-5fc96ec56fae` | Pending reviewed handoff | Not integrated |
| A16 | `01a07aaf-6a21-74b1-a0dc-3b88375b1212` | Pending reviewed handoff | Not integrated |
| A17 | `01a07aaf-6e61-7733-8687-d917fb7d81d5` | Pending reviewed handoff | Not integrated |
| A18 | `01a07aaf-7155-7460-a693-eb4f4cb66f87` | Pending reviewed handoff | Not integrated |
| A19 | `01a07aaf-73f5-7830-a79b-c84f52a17f9f` | Pending reviewed handoff | Not integrated |
| A20 | `01a07aaf-7618-7fa1-8a56-226f7cc702a3` | Pending reviewed handoff | Not integrated |
| W13/SD09 | `01a07ab1-726e-7d52-9859-7f0a65c98dad` | Analytics policy and data-flow review in progress | Not integrated |
| T01-T06 | IDs pending complementary Architect | Awaiting scope/registry | Not integrated |

## A21 verification ledger

All results below are local at initial baseline, not combined-candidate CI or live verification.

| Status | Check | Actual result |
| --- | --- | --- |
| PASS | `python3 tests/test-release-package.py` | Nine tests pass |
| PASS | `python3 -m unittest tests/test_verify_live_edge.py` | Nine tests pass |
| BLOCKED | `python3 scripts/build-site.py --check` | System Python lacks Beautiful Soup; existing pinned requirements need isolated setup |
| RECORDED | Environment | Node 26.0.0; Python 3.14.5; A08 supported-runtime handoff pending |
| NOT RUN | Combined candidate suite | No worker candidate integrated yet |
| NOT RUN | A20 frozen acceptance | A20 preparing baseline; native Safari request timed out, actual VoiceOver/NVDA/phone not verified |
| NOT RUN | CI retry/event behavior | Requires authorized external run |
| NOT RUN | Candidate publication/live readback | No publication authorized |

## Freeze and release conditions

Select reviewed packages without presenting unselected proposals as implemented. Regenerate and pass required combined gates, commit the candidate, create and verify the exact SHA-bound allowlisted artifact, retain manifest digest and payload inventory, and hand that frozen SHA to A20. Changes after freeze require relevant revalidation and a new frozen identity. Keep a rollback reference to the actual previously deployed revision after fresh verification. Publication is a separate owner decision on the concrete candidate.
