# ADR-0009: Adopt the reconciled ORION Master Architecture partition

- Status: Accepted
- Date: 2026-08-11
- Decision owner: ORION Architecture Owner
- Integration authority: ORION repository maintainer / architecture integrator
- Affected repositories: nexah-orion only; external boundaries are informative and unchanged
- Supersedes: none
- Superseded by: none

## Context

The accepted F1 decisions and artifacts preserve the development history of a
broad ORION architecture. The current Version 1 release subsequently certified
a narrower deterministic structural chain and classified retained Runtime,
Gateway, Public Contract, LYRA, transformation and experimental work outside
that certified responsibility.

The Phase 1 reconciliation separated current fact, historical implementation,
scientific evidence, proposed architecture, implemented behavior and certified
product responsibility. Phase 2 exposed the resulting architecture choices to
the Owner. The Owner then recorded an explicit disposition for all 17 choices
and authorized a controlled documentation-only canonicalization pass.

## Decision

ORION adopts this cross-status Master Architecture partition:

```text
ORION
├── CERTIFIED CORE
├── SEPARATELY ADOPTED EXTENSION PROFILES
│   └── NONE CURRENTLY ADOPTED
└── EXTERNAL RESEARCH
    └── Science Lab
```

**ADOPTED EXTENSION PROFILES: NONE**

The partition is architecture. It is not an Extension Profile, capability,
interface, implementation, certification or scientific result. Every future
Extension Profile requires its own explicit Owner adoption and every applicable
semantic, validation, certification, release and governance process.

The Certified Core remains the current certified Version 1 chain from the
confirmed source through Structural Representation, UNDERSTAND Inventory,
Structural Summary and Statistics, Relations, Structural Navigation,
Structural Orientation Map and Expression certification. Its certified STOP
remains `at_slice_iv_certified`.

## Owner decision accounting

| ID | Disposition | Canonical architectural effect |
|---|---|---|
| OA-01 | ADOPT | The certified deterministic structural chain is the ORION V1 Core. |
| OA-02 | ADOPT | Human intention, interpretation, decision, consent and STOP remain Human-owned. |
| OA-03 | ADOPT | Science Lab remains External Research authority, separate from ORION product authority. |
| OA-04 | ADOPT | O8/B1 remain Research and are not ORION V1 capabilities. |
| OA-05 | ADOPT | Interface V1 remains `MEMBRANE_V1_APPROVED_NOT_IMPLEMENTED`. |
| OA-06 | ADOPT | LYRA remains inactive and outside the certified ORION V1 Core. |
| OA-07 | ADOPT | TransformationEngine, T01–T15 and Operator Registry remain outside certified V1 unless separately adopted. |
| OA-08 | ADOPT | F1 Runtime, Gateway and Public Contract remain historical or separately governed, not certified V1. |
| OA-09 | DEFER | IRIS remains unresolved and is not instantiated by assumption. |
| OA-10 | DEFER | SIRIUS remains unresolved; no single authoritative runtime definition is adopted. |
| OA-11 | ADOPT | Research cannot self-promote into product capability, certification or canonical architecture. |
| OA-12 | ADOPT | Certification means deterministic software/conformance certification within declared scope, not general scientific validation. |
| OA-13 | ADOPT | The Version 1 STOP remains `at_slice_iv_certified`. |
| OA-14 | ADOPT | ORION meaning ownership applies to exported ORION objects only; OLS normative authority and Human meaning/decision authority remain unchanged. |
| OA-15 | ADOPT | Legacy Public Contract/Gateway and Interface V1 are distinct boundaries with separate evidence. |
| OA-16 | ADOPT WITH CHANGE | Only the Certified Core / Separately Adopted Extension Profiles / External Research partition is adopted; no profile or candidate is adopted. |
| OA-17 | ADOPT | Untracked Runtime/deployment work remains noncanonical pending separate review. |

Decision totals: 14 ADOPT, 2 DEFER, 1 ADOPT WITH CHANGE, 0 REJECT.

## Authority boundaries

- Human authority is unchanged.
- NEXAH Framework and OLS retain their ecosystem and normative semantic
  authority. The Kernel retains deterministic execution authority for released
  contracts.
- ORION owns the meaning of its declared and exported ORION objects. This does
  not supersede OLS normative semantics, source authority or Human meaning and
  decision authority.
- Interface V1 owns transport only. NEXAH owns registered consumption only.
- Science Lab owns Research evidence. A result, including a successful result,
  does not acquire product or certification authority without the
  Research-to-Architecture Adoption Gate and an explicit Owner decision.

## Retained and deferred material

Historical ADRs and F1 artifacts remain preserved. They are not rewritten by
this decision. Their current product status is read through this ADR, the
Master Architecture, the Version 1 Classification Report and the Version 1
Reading Order.

TransformationEngine, T01–T15, Operator Registry, Runtime, Gateway, Public
Contract and LYRA are not silently adopted. Existing implementations remain at
their already declared historical, experimental, separately governed or
unknown-authority status. Untracked Runtime and deployment material is
`NONCANONICAL / PENDING SEPARATE REVIEW`.

IRIS and SIRIUS remain unresolved. Operator-family reconciliation remains a
`FUTURE_RESEARCH_CANDIDATE`; no equivalence is asserted among T01–T15, O8,
JANUS, historical Codex, NEXAH operators or transformation grammars.

## Interface distinction

The earlier Public Contract/Gateway boundary and ORION↔NEXAH Interface V1 are
not interchangeable and do not validate one another. Interface V1 remains:

`MEMBRANE_V1_APPROVED_NOT_IMPLEMENTED`

No adapter, producer, consumer, schema, conformance result or operational
integration is created by this ADR.

## Consequences

### Positive

- Current certified architecture, retained history and External Research have
  one explicit precedence and status map.
- Extension categories can no longer imply adopted capabilities.
- Scientific, implementation, adoption and certification states remain
  independent.

### Constraints

- Structural Navigation is not general navigation.
- Structural Orientation Map is not Human or ecosystem orientation.
- Expression is not LYRA explanation.
- Replay is not scientific truth.
- Certification is not universal scientific validation.
- Research PASS is not product capability.

## Non-actions

This decision changes no code, tests, schemas, Runtime, interface,
certification scope, scientific result, closed Labreport or external
repository. It does not activate LYRA, implement the membrane, adopt O8/B1,
resolve IRIS/SIRIUS, adopt an Extension Profile or begin operator-family
reconciliation.

## Provenance

- Phase 1 manifest SHA-256:
  `b30be0af5298cca0c603dabef884f030691471b428a75fe00684e4a809bd8f34`
- Phase 2 Owner Adoption package manifest SHA-256:
  `c564a2907718ab9acdfcc64ad69a187f8382e0f8f219d75f10f4e0d57ca5310d`
- Phase 3 canonicalization proposal manifest SHA-256:
  `b639f766fd990e0d4353d340cc5192ea016fe33aaa934b72b9ef0c1b49a659d6`

## References

- [`../architecture/ORION_MASTER_ARCHITECTURE.md`](../architecture/ORION_MASTER_ARCHITECTURE.md)
- [`../architecture/ORION_SYSTEM_PLATE.md`](../architecture/ORION_SYSTEM_PLATE.md)
- [`../architecture/ORION_CORE_PLATE.md`](../architecture/ORION_CORE_PLATE.md)
- [`../releases/ORION_V1_VERSION_CLASSIFICATION.md`](../releases/ORION_V1_VERSION_CLASSIFICATION.md)
- [`../releases/ORION_V1_READING_ORDER.md`](../releases/ORION_V1_READING_ORDER.md)
- [`../governance/OWNERSHIP.md`](../governance/OWNERSHIP.md)

