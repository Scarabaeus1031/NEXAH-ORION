# ORION Source Map

The certified Version 1 implementation is the bounded deterministic chain
recorded in `docs/releases/ORION_V1_CERTIFIED_BASELINE.md`:

| Source family | Certified responsibility |
|---|---|
| Representation and Markdown Structural modules | immutable structural projection and conformance |
| `understand_*_alpha.py` modules | inventory, summary, and statistics over declared structure |
| Relation modules | immutable structural and declared Relations plus conformance and certification |
| Navigation modules | immutable Navigation construction, conformance, and certification |
| Orientation Map modules | deterministic map construction and conformance |
| Expression modules | Contract, Construction, External Conformance, and Certification |
| Slice certification modules | immutable Slice II–IV certification boundaries |

Certified modules are consumed at their explicit paths and remain governed by
their frozen profiles, proofs, and STOP boundaries. The root `orion` package
retains the earlier aggregate imports only for repository compatibility; those
imports do not enlarge the certified baseline.

Earlier Public Contract, Runtime, Gateway, context, backend, Transformation
Engine, Operator Registry, and LYRA development slices remain at explicit module
paths so their historical evidence and separate integrations remain
reproducible. They are not part of the certified Version 1 Core and are not
made certified merely by their retained aggregate imports.

This responsibility layout is governed by the
[`Version 1 Reading Order`](../docs/releases/ORION_V1_READING_ORDER.md) and
[`Ownership Map`](../docs/governance/OWNERSHIP.md). Changes to authority or
frozen contracts require Architecture Review and an accepted ADR.
