# ORION Core Compatibility Report

## Decision state

**Owner decision required. No compatibility change has been made.**

## Exact revisions

| Item | Revision |
|---|---|
| ORION configured Core pin | `9f79bb06210402c40c9ef7d9937ca00d86c092b1` |
| Connected NEXAH Framework checkout | `7daa0ecc2ec106b5709fa99e53c88d57a8ab1b6c` at the verification point |
| Difference | Connected checkout is newer; exact-pin gate correctly fails |

The connected checkout is clean. `./scripts/check-workspace` passes architecture,
boundary and Architecture Plate checks and reports one failure only: the
connected Core revision is not the configured revision.

## Meaning

The newer Framework revisions contain Governance and publication preparation.
That fact does not prove or disprove ORION compatibility. ORION's exact pin is
an authority boundary and cannot be updated merely because a newer checkout is
available.

## Valid owner choices

1. **Keep the current pin.** Verify the ORION candidate against a clean detached
   checkout of `9f79bb06210402c40c9ef7d9937ca00d86c092b1`. No compatibility record or
   pin change is required.
2. **Approve a newer Core baseline.** First run the complete compatibility and
   release checks against the chosen immutable Framework revision, record the
   result under `docs/releases/compatibility/`, then update the pin through the
   existing cross-repository governance process.

Operations does not choose between these alternatives. The Release Gate must
not be weakened, bypassed or changed to accept the currently connected branch.

## Reproduction

```sh
./scripts/check-workspace
./scripts/release-check --development
```

Expected current result: all repository-local architecture checks pass and the
workspace gate stops at the exact Core revision comparison.
