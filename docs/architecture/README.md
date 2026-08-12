# Architecture Records

This directory contains the accepted ORION architecture and the evidence used to establish it.

ORION architecture is subordinate to the adopted
[NEXAH Ecosystem Constitution v1.0](https://github.com/Scarabaeus1031/NEXAH/blob/main/GOVERNANCE/ECOSYSTEM_CONSTITUTION.md).
The Constitution defines the ORION House and its authority; this directory
describes how deterministic navigation is structured within that boundary.

```text
architecture/
├── MACHINE_READABLE_ORIENTATION_ARCHITECTURE.md
│                                  proposed semantics-to-carrier architecture
├── OLS_1_0_REPOSITORY_ARCHITECTURE_EXTRACTION.md
│                                  cross-repository OLS synthesis and map
├── ORION_MASTER_ARCHITECTURE.md canonical cross-status architecture map
├── ORION_SYSTEM_PLATE.md        canonical certified Core + Expression assembly
├── ORION_CORE_PLATE.md          canonical certified cross-layer assembly
├── ORION_V1_ARCHITECTURE_FREEZE.md historical F1 freeze record
├── ORION_V1_ARCHITECTURE_REVIEW.md historical F1 review summary
├── ORION_ARCHITECTURE.md        preserved broad F1 architecture
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

[`OLS_1_0_REPOSITORY_ARCHITECTURE_EXTRACTION.md`](OLS_1_0_REPOSITORY_ARCHITECTURE_EXTRACTION.md)
maps the published OLS 1.0 suite to ORION and the wider ecosystem without
redefining either. It is an informative navigation document, not an item in the
authority order below. The canonical OLS release in the NEXAH Research &
Framework repository remains semantic authority.

[`MACHINE_READABLE_ORIENTATION_ARCHITECTURE.md`](MACHINE_READABLE_ORIENTATION_ARCHITECTURE.md)
proposes the missing boundaries between OLS semantics, carriers, processors,
records, representation mappings, media, packages, and Human experience. It is
informative Stage-0 architecture: it does not amend OLS 1.0, reopen ORION
Version 1, or define a production format.

Authority order:

1. Accepted ADRs govern explicit decisions.
2. [`ORION_MASTER_ARCHITECTURE.md`](ORION_MASTER_ARCHITECTURE.md) is the
   canonical cross-status architecture map adopted by ADR-0009. It separates
   the Certified Core, the empty category of separately adopted Extension
   Profiles, and External Research without changing certified scope.
3. [`ORION_SYSTEM_PLATE.md`](ORION_SYSTEM_PLATE.md) assembles the certified
   Orientation Core and certified Expression Layer through the final WP30
   `at_slice_iv_certified` STOP. It is the current one-page system view and
   introduces no new responsibility.
4. [`ORION_CORE_PLATE.md`](ORION_CORE_PLATE.md) assembles the certified
   Foundation and Vertical Slices I–III into the canonical frozen cross-layer
   reference after WP25. It does not replace the detailed architecture of any
   individual responsibility.
5. The current
   [`Version 1 Classification Report`](../releases/ORION_V1_VERSION_CLASSIFICATION.md)
   and [`Version 1 Reading Order`](../releases/ORION_V1_READING_ORDER.md)
   govern current release scope and the interpretation of retained files.
6. [`ORION_ARCHITECTURE.md`](ORION_ARCHITECTURE.md), the F1 freeze/review and
   earlier phase records preserve the broad historical architecture. They are
   not rewritten and do not enlarge the certified Version 1 baseline.
7. `REPRESENTATION_ARCHITECTURE.md` specializes the accepted representation
   boundaries without implementing them.
8. [`SLICE_III_RESPONSIBILITY_MATRIX.md`](SLICE_III_RESPONSIBILITY_MATRIX.md)
   coordinates the canonical
   [`Relations`](SLICE_III_RELATIONS.md),
   [`Navigation`](SLICE_III_NAVIGATION.md), and
   [`Orientation Map`](SLICE_III_ORIENTATION_MAP.md) architecture after the
   certified Slice II STOP. These specifications introduce no implementation
   and do not reopen Slice II.
9. [`SLICE_IV_EXPRESSION_ARCHITECTURE.md`](SLICE_IV_EXPRESSION_ARCHITECTURE.md)
   defines the Expression Boundary after the certified Core. Its
   [`Responsibility Matrix`](SLICE_IV_RESPONSIBILITY_MATRIX.md),
   [`Boundaries`](SLICE_IV_BOUNDARIES.md), and
   [`Execution Chain`](SLICE_IV_EXECUTION_CHAIN.md) assign no implementation
   authority and do not reopen the Core Plate.
10. `transformations/` maps the hypothesized coordinate transitions, invariants,
   evidence gaps and lossiness without introducing new geometry. Its `contracts/`
   directory formalizes each registered edge without implementing it.
11. `operators/` contains the Version 1 Orientation Policies and Operators; its
   earlier capability inventory remains historical.
12. [`lyra/LYRA_ARCHITECTURE.md`](lyra/LYRA_ARCHITECTURE.md) specializes the
   existing LYRA Translation-/Representation-Boundary for faithful human-facing
   language. Phase 6B makes translation executable without adding runtime
   authority.
13. [`plates/`](plates/README.md) contains generated visual companions. Canonical
   SVG sources produce the PNG documentation artifacts; linked Markdown and
   accepted ADRs remain authoritative.
14. Baseline records describe pinned external states.
15. Evidence explains how conclusions were reached but is not itself normative.
16. External Research, including Science Lab, remains outside ORION product
    authority. Research enters product architecture only through an explicit
    Research-to-Architecture Adoption Gate and Owner decision.

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
