# Architecture Records

This directory contains the accepted ORION architecture and the evidence used to establish it.

ORION architecture is subordinate to the adopted
[NEXAH Ecosystem Constitution v1.0](https://github.com/Scarabaeus1031/NEXAH/blob/main/GOVERNANCE/ECOSYSTEM_CONSTITUTION.md).
The Constitution defines the ORION House and its authority; this directory
describes how deterministic navigation is structured within that boundary.

```text
architecture/
├── ORION_V1_ARCHITECTURE_FREEZE.md official frozen baseline
├── ORION_V1_ARCHITECTURE_REVIEW.md F1 repository review summary
├── ORION_ARCHITECTURE.md        frozen coherent architecture
├── REPRESENTATION_ARCHITECTURE.md  Phase 3A rendering specialization
├── transformations/             Phase 3B cartography and Phase 3C contracts
│   └── contracts/               versioned Transition Contract specifications
├── operators/                   Phase 5A declarative capability inventory
├── lyra/                        Phase 6A/6B human-language boundary
├── lucy/                        Phase 7/7A non-normative Concept Freeze
├── plates/                      canonical visual companions and SVG sources
├── baselines/                   recovered current-state records
└── evidence/                    reviews and source analyses
```

Authority order:

1. Accepted ADRs govern explicit decisions.
2. [`ORION_V1_ARCHITECTURE_FREEZE.md`](ORION_V1_ARCHITECTURE_FREEZE.md)
   identifies the official baseline, its frozen and unfrozen scope, terminology
   and verification state.
3. `ORION_ARCHITECTURE.md` describes the current coherent architecture.
4. `REPRESENTATION_ARCHITECTURE.md` specializes the accepted LYRA and
   representation boundaries without implementing them.
5. `transformations/` maps the hypothesized coordinate transitions, invariants,
   evidence gaps and lossiness without introducing new geometry. Its `contracts/`
   directory formalizes each registered edge without implementing it.
6. `operators/` records known capability metadata without selecting, loading or
   executing an operator.
7. [`lyra/LYRA_ARCHITECTURE.md`](lyra/LYRA_ARCHITECTURE.md) specializes the
   existing LYRA Translation-/Representation-Boundary for faithful human-facing
   language. Phase 6B makes translation executable without adding runtime
   authority.
8. [`plates/`](plates/README.md) contains generated visual companions. Canonical
   SVG sources produce the PNG documentation artifacts; linked Markdown and
   accepted ADRs remain authoritative.
9. Baseline records describe pinned external states.
10. Evidence explains how conclusions were reached but is not itself normative.

[`lucy/`](lucy/README.md) is deliberately outside this authority order. It is a
concept exploration hosted beside the frozen architecture, not an ORION
component, accepted decision or implementation specification.

The executable documentation in
[`docs/orientation_sessions/`](../orientation_sessions/README.md) validates the
Phase 6B boundary against this architecture. Sessions are conformance evidence,
not a new authority or architecture layer.

Do not edit an evidence document to change architecture. Create an ADR and update the current architecture after acceptance.
