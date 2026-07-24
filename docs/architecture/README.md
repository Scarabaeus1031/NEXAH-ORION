# Architecture Records

This directory contains the accepted ORION architecture and the evidence used to establish it.

ORION architecture is subordinate to the adopted
[NEXAH Ecosystem Constitution v1.0](https://github.com/Scarabaeus1031/NEXAH/blob/main/GOVERNANCE/ECOSYSTEM_CONSTITUTION.md).
The Constitution defines the ORION House and its authority; this directory
describes how deterministic navigation is structured within that boundary.

```text
architecture/
├── ORION_SYSTEM_PLATE.md        canonical certified Core + Expression assembly
├── ORION_CORE_PLATE.md          canonical certified cross-layer assembly
├── ORION_V1_ARCHITECTURE_FREEZE.md historical F1 freeze record
├── ORION_V1_ARCHITECTURE_REVIEW.md historical F1 review summary
├── ORION_ARCHITECTURE.md        frozen coherent architecture
├── REPRESENTATION_ARCHITECTURE.md  Phase 3A rendering specialization
├── SLICE_III_*.md               post-Slice II Relations and Navigation architecture
├── SLICE_IV_*.md                post-Core Expression Boundary architecture
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
2. [`ORION_ARCHITECTURE.md`](ORION_ARCHITECTURE.md) describes the current
   coherent architecture. The Phase VIII
   [`Architecture Audit`](../releases/ORION_V1_ARCHITECTURE_AUDIT.md) confirms
   its Version 1 consistency.
3. [`ORION_SYSTEM_PLATE.md`](ORION_SYSTEM_PLATE.md) assembles the certified
   Orientation Core and certified Expression Layer through the final WP30
   `at_slice_iv_certified` STOP. It is the current one-page system view and
   introduces no new responsibility.
4. [`ORION_CORE_PLATE.md`](ORION_CORE_PLATE.md) assembles the certified
   Foundation and Vertical Slices I–III into the canonical frozen cross-layer
   reference after WP25. It does not replace the detailed architecture of any
   individual responsibility.
5. `REPRESENTATION_ARCHITECTURE.md` specializes the accepted LYRA and
   representation boundaries without implementing them.
6. [`SLICE_III_RESPONSIBILITY_MATRIX.md`](SLICE_III_RESPONSIBILITY_MATRIX.md)
   coordinates the canonical
   [`Relations`](SLICE_III_RELATIONS.md),
   [`Navigation`](SLICE_III_NAVIGATION.md), and
   [`Orientation Map`](SLICE_III_ORIENTATION_MAP.md) architecture after the
   certified Slice II STOP. These specifications introduce no implementation
   and do not reopen Slice II.
7. [`SLICE_IV_EXPRESSION_ARCHITECTURE.md`](SLICE_IV_EXPRESSION_ARCHITECTURE.md)
   defines the Expression Boundary after the certified Core. Its
   [`Responsibility Matrix`](SLICE_IV_RESPONSIBILITY_MATRIX.md),
   [`Boundaries`](SLICE_IV_BOUNDARIES.md), and
   [`Execution Chain`](SLICE_IV_EXECUTION_CHAIN.md) assign no implementation
   authority and do not reopen the Core Plate.
8. `transformations/` maps the hypothesized coordinate transitions, invariants,
   evidence gaps and lossiness without introducing new geometry. Its `contracts/`
   directory formalizes each registered edge without implementing it.
9. `operators/` contains the Version 1 Orientation Policies and Operators; its
   earlier capability inventory remains historical.
10. [`lyra/LYRA_ARCHITECTURE.md`](lyra/LYRA_ARCHITECTURE.md) specializes the
   existing LYRA Translation-/Representation-Boundary for faithful human-facing
   language. Phase 6B makes translation executable without adding runtime
   authority.
11. [`plates/`](plates/README.md) contains generated visual companions. Canonical
   SVG sources produce the PNG documentation artifacts; linked Markdown and
   accepted ADRs remain authoritative.
12. Baseline records describe pinned external states.
13. Evidence explains how conclusions were reached but is not itself normative.

The earlier F1 freeze and review remain historical decision evidence. Current
navigation begins with the
[`Version 1 Reading Order`](../releases/ORION_V1_READING_ORDER.md).

[`lucy/`](lucy/README.md) is deliberately outside this authority order. It is a
concept exploration hosted beside the frozen architecture, not an ORION
component, accepted decision or implementation specification.

The executable documentation in
[`docs/orientation_sessions/`](../orientation_sessions/README.md) validates the
Phase 6B boundary against this architecture. Sessions are conformance evidence,
not a new authority or architecture layer.

Do not edit an evidence document to change architecture. Create an ADR and update the current architecture after acceptance.
