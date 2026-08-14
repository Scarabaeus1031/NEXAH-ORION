# ORION Noncanonical Working-Set Index — 2026-08-14

## Purpose

This index makes the formerly untracked ORION working material reviewable
without silently adopting it. The branch is a preservation and decision
surface. ORION `main`, the certified Core, the adopted Master Architecture and
all public capability claims remain unchanged.

## Package dispositions

| Package | Contents | Disposition | Adoption gate |
|---|---|---|---|
| Runtime 1.1 candidate | service boundary, release manifest, deployment definitions, Runtime code, proofs, tests and audits | `NOT_ADOPTED / TEST_BLOCKED` | Resolve release/Core identity proof; pass focused and full suites; perform supported-Linux verification; separate Owner adoption |
| Orientation architecture studies | machine-readable architecture, OLS extraction, distilled architecture, infrastructure studies and design reviews | `RESEARCH_REFERENCE_ONLY` | Reconcile each proposal with the adopted Master Architecture; accept only through a separately scoped architecture decision |
| POA experiment packets | POA-001 through POA-003 protocols, code, renderings, results and synthesis assessment | `EXPERIMENTAL_EVIDENCE / NOT_CERTIFIED_CORE` | Independent evidence review and explicit decision about whether any result belongs in an ORION release or external research record |
| Ecosystem/NTO/structural-grammar reviews | exploratory program, dependency, grammar and information-architecture assessments | `REVIEW_REFERENCE_ONLY` | No current integration job; use only as input to a named future decision |

## Authority boundary

- A clean worktree is not evidence of adoption.
- A commit on this branch is not a release, merge approval or architecture
  decision.
- Normative language inside preserved source documents retains its historical
  local context; this index controls the current repository disposition.
- No file on this branch may be promoted to `main` through a bulk merge.
- Future work must select an exact package allowlist and rerun its relevant
  verification.

```text
BRANCH_PURPOSE = PRESERVATION_AND_REVIEW
CERTIFIED_CORE_CHANGED = NO
MASTER_ARCHITECTURE_CHANGED = NO
RUNTIME_ADOPTED = NO
POA_ADOPTED = NO
PUBLIC_RELEASE_CHANGED = NO
```
