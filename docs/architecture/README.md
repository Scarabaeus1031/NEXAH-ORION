# Architecture Records

This directory contains the accepted ORION architecture and the evidence used to establish it.

```text
architecture/
├── ORION_ARCHITECTURE.md        accepted target architecture
├── baselines/                   recovered current-state records
└── evidence/                    reviews and source analyses
```

Authority order:

1. Accepted ADRs govern explicit decisions.
2. `ORION_ARCHITECTURE.md` describes the current coherent architecture.
3. Baseline records describe pinned external states.
4. Evidence explains how conclusions were reached but is not itself normative.

Do not edit an evidence document to change architecture. Create an ADR and update the current architecture after acceptance.
