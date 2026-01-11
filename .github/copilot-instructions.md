# Copilot instructions (Jamie’s personal repo defaults)

## Goals
- Optimize for correctness, clarity, and maintainability.
- Prefer small, reviewable commits over big rewrites.

## How to respond
- Start with a 3–6 step plan.
- Then show the code changes.
- Then show how to run / test.

## Coding conventions
- Follow existing project structure and naming.
- Prefer pure functions and clear boundaries.
- Don’t introduce new dependencies unless necessary (and explain why).

## Safety
- Never print, log, or hardcode secrets.
- Use environment variables for credentials.
- Validate untrusted inputs.

## Deliverables checklist
- ✅ Code compiles / runs
- ✅ Tests added or updated when appropriate
- ✅ Notes on edge cases
- ✅ Minimal diffs (no drive-by refactors)
