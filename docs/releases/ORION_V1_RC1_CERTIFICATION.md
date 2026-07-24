# ORION Version 1 RC1 Certification Statement

## Purpose

ORION Version 1 provides the stable, model-independent navigation and validation
boundary between a Human Orientation Request and a structured, evidence-bound
Orientation Report with meaningful Continuation Options.

## Implemented scope

Version 1 contains the frozen Orientation Policies, Orientation Operators and
Public Contract Suite 1.0; executable contract models and validation; one
deterministic Understand Runtime; a thin Gateway; presentation mapping; one live
orientation trace; and a versioned twelve-document evaluation corpus.

All observable Runtime outcomes are Version 1.0 public contracts. NEXAHEDRON
does not import Runtime internals, and no private Runtime object crosses the
Gateway boundary.

## Explicit non-scope

Version 1 does not implement Wonder, Compare, Connect, Explore, Build or Reflect.
It contains no provider integration, prompt system, transport API, retrieval
service, persistence, authentication, streaming, sessions, production SLA,
LUCY Runtime, Library mutation, Atlas mutation or Human decision authority.

## Evidence

- accepted architecture and public-contract freezes;
- 128 passing isolated tests and one intentionally skipped optional integration;
- one complete Phase VI live journey;
- 12 complete Phase VII evaluation sessions;
- complete contract and lineage validation;
- architecture, boundary and Architecture Plate verification;
- Phase VIII audit finding no justified architecture or contract change;
- RC1 dead-reference and reproducibility audits.

## Verification

The candidate is reproducible with Python 3.10+, a POSIX environment and
librsvg. It requires no third-party Python runtime dependency or live reasoning
provider. Exact commands and expected outputs are recorded in the
[`RC1 Checklist`](ORION_V1_RC1_CHECKLIST.md) and
[`Reproducibility Report`](ORION_V1_RC1_REPRODUCIBILITY_REPORT.md).

## Known release blocker

The configured Core pin is
`9f79bb06210402c40c9ef7d9937ca00d86c092b1`; the currently connected checkout is
`64d1c817f7661e518dcc217bd56f34d272807372`. The exact dependency guard correctly
stops publication verification. ORION has not changed the pin, weakened the gate
or asserted compatibility with the connected revision.

## Certification

Within its explicit scope, ORION Version 1 is coherent, contract-valid,
reproducible and suitable as the canonical reference baseline. RC1 acceptance
does not publish a package or broaden the Version 1 claim.
