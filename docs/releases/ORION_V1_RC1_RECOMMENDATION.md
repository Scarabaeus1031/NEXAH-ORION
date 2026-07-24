# ORION Version 1 RC1 Recommendation

## Decision

**ORION Version 1 — Release Candidate Accepted**

**Pending external dependency synchronization only.**

## Basis

Repository-owned verification passes: isolated tests, Phase VI, Phase VII,
architecture consistency, frozen responsibility boundaries, Architecture
Plates, internal reference integrity and onboarding review. The reviewed scope
contains no architecture, behavior, contract, Runtime, Gateway or version
change introduced by RC1 preparation.

## Remaining action

Connect or explicitly approve the exact NEXAH Core dependency required by
`workspace.yaml`, rerun the complete development Release Gate, then create the
immutable release commit and metadata through the existing publication process.
No ORION implementation change is required.
