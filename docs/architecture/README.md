# Architecture Records

This directory contains the accepted ORION architecture and the evidence used to establish it.

```text
architecture/
├── ORION_ARCHITECTURE.md        accepted target architecture
├── REPRESENTATION_ARCHITECTURE.md  Phase 3A rendering specialization
├── transformations/             Phase 3B cartography and Phase 3C contracts
│   └── contracts/               versioned TransitionContract specifications
├── baselines/                   recovered current-state records
└── evidence/                    reviews and source analyses
```

Authority order:

1. Accepted ADRs govern explicit decisions.
2. `ORION_ARCHITECTURE.md` describes the current coherent architecture.
3. `REPRESENTATION_ARCHITECTURE.md` specializes the accepted Lyra and
   representation boundaries without implementing them.
4. `transformations/` maps the hypothesized coordinate transitions, invariants,
   evidence gaps and lossiness without introducing new geometry. Its `contracts/`
   directory formalizes each registered edge without implementing it.
5. Baseline records describe pinned external states.
6. Evidence explains how conclusions were reached but is not itself normative.

Do not edit an evidence document to change architecture. Create an ADR and update the current architecture after acceptance.
