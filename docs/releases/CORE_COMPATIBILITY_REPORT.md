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

## Configured-pin verification

Launch Control created isolated clean clones, checked the Framework clone out
at the unchanged configured pin, connected it to ORION, and ran:

```sh
./scripts/release-check --development
```

Verified revisions and result on 21 July 2026:

```text
ORION  0a9c031e3d71b75abd007e12b493acc93d8e4cc8
Core   9f79bb06210402c40c9ef7d9937ca00d86c092b1
Workshop checks passed.
75 tests passed; 1 optional integration test skipped.
Development Release Gate passed.
```

This proves that the committed ORION baseline remains reproducible with its
declared Core pin. It does not declare the newer connected Framework checkout
compatible.

## Meaning

The newer Framework revisions contain Governance and publication preparation.
That fact does not prove or disprove ORION compatibility. ORION's exact pin is
an authority boundary and cannot be updated merely because a newer checkout is
available.

## Valid owner choices

1. **Keep the current pin.** The clean verification above is complete. Owner
   approval may adopt this tested pair without a pin change.
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

Against the currently connected newer Framework checkout, the workspace gate
stops at the exact Core revision comparison. Against the configured pin in an
isolated clean workspace, the complete development Release Gate passes.
