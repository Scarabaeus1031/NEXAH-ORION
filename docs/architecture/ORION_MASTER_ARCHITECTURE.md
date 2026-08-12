# ORION Master Architecture

- Status: Canonical cross-status architecture map
- Adopted by: ADR-0009
- Date: 2026-08-11
- Certified Core STOP: `at_slice_iv_certified`
- Adopted Extension Profiles: **NONE**

## 1. Purpose and authority

This document maps current certified product authority, separately adoptable
extension space and External Research without collapsing their status. It
introduces no implementation and changes no certified responsibility.

Present architectural precedence is:

```text
accepted architecture decisions
→ ORION Master Architecture
→ certified System and Core Plates
→ current Version 1 classification and reading order
→ preserved historical architecture
→ External Research
```

Historical documents and code remain preserved. File presence, implementation,
testing, scientific evidence or visual similarity does not grant present
product authority.

## 2. Adopted architecture

```text
ORION
├── CERTIFIED CORE
│   ├── confirmed source boundary
│   ├── immutable Structural Representation
│   ├── UNDERSTAND Inventory
│   ├── Structural Summary and Statistics
│   ├── certified Relations
│   ├── Structural Navigation
│   ├── Structural Orientation Map
│   ├── Expression
│   └── conformance, certification, provenance, replay and STOP
├── SEPARATELY ADOPTED EXTENSION PROFILES
│   └── NONE CURRENTLY ADOPTED
└── EXTERNAL RESEARCH
    └── Science Lab
```

**ADOPTED EXTENSION PROFILES: NONE**

An Extension Profile category is not a capability. No retained implementation,
Research result, candidate schema, interface, operator family or proposed
profile occupies this category until an explicit Owner decision names and
adopts it and all applicable semantic, validation, certification, release and
governance requirements are satisfied.

## 3. Four independent status axes

| AXIS | QUESTION | EXAMPLES OF VALUES |
|---|---|---|
| Semantic status | Is meaning and ownership defined? | undefined, defined, ambiguous, loss-aware |
| Software status | Does code exist and has it been exercised? | absent, implemented, tested |
| Scientific/evidence status | What scoped evidence exists? | untested, supported, refuted, invalid, unresolved |
| Product/certification status | Has the Owner adopted and the release certified it? | proposed, adopted, certified, historical, deferred |

`DEFINED`, `IMPLEMENTED`, `TESTED`, `VALIDATED`, `CERTIFIED` and `ADOPTED` are
not synonyms and do not form an automatic progression. Each state requires its
own authority and evidence.

## 4. Certified Core

The Certified Core is the deterministic Version 1 structural chain recorded by
the Certified Baseline and System/Core Plates. It begins at a Human-confirmed
source and ends at:

`at_slice_iv_certified`

The STOP is unchanged. The Core owns only its declared immutable artifacts,
construction, external conformance, certification, provenance and replay
responsibilities.

The following qualifications are normative:

- Structural Navigation is deterministic movement over certified Relations;
  it is not general, physical or dynamical navigation, recommendation, action,
  intervention or control.
- Structural Orientation Map is a certified structural artifact; it is not
  Human interpretation or general ecosystem orientation.
- Expression is the certified bounded Expression artifact; it is not generated
  language or LYRA explanation.
- Replay establishes deterministic reproducibility within its contract; it is
  not scientific truth.
- Certification is deterministic software/conformance certification within
  declared scope; it is not universal scientific validation.

## 5. Separately Adopted Extension Profiles

There are no adopted Extension Profiles.

A future profile requires at minimum:

1. an exact proposition, owner, inputs, outputs and boundary;
2. semantic/type authority and explicit ambiguity, loss and undefined behavior;
3. provenance and forbidden-inference rules;
4. compatibility with the Certified Core and its STOP;
5. scoped software and scientific evidence review;
6. an explicit Owner disposition;
7. applicable implementation, validation, certification, release and
   governance acts performed separately.

No step authorizes the next by implication.

## 6. External Research

Science Lab is External Research authority. It owns its questions, methods,
preregistrations, implementations, data, controls, failures, negative results,
replays and Labreports. It does not own ORION product adoption.

O8/B1 remain Research and are not ORION V1 capabilities. A Research PASS does
not become a product capability, certified capability or canonical architecture
statement.

The minimum Research-to-Architecture Adoption Gate is:

```text
closed and scoped Research evidence
→ exact candidate proposition
→ authority and conflict review
→ semantic and boundary review
→ explicit ORION Owner decision
→ optional separately authorized implementation/validation/certification/release
```

Negative, failed and invalid results remain Research evidence. No numerical
product threshold is invented by this architecture.

## 7. Ecosystem authority boundaries

| AUTHORITY | OWNS | DOES NOT TRANSFER TO ORION |
|---|---|---|
| Human | intention, interpretation, meaning, decision, consent and STOP | personal authority or authorization |
| NEXAH Framework | shared Orientation Space and ecosystem boundaries | ORION product/certification authority |
| OLS | normative semantics, definitions, contracts and conformance rules | Human meaning or Research truth |
| Kernel | deterministic execution of released contracts | normative, scientific or Human authority |
| ORION | declared ORION objects, Certified Core responsibilities and explicitly adopted future profiles | OLS semantics, Human decisions or external source truth |
| Science Lab | Research evidence and scientific provenance | product adoption or certification |
| Interface V1 | versioned transport semantics only | ORION meaning, NEXAH consumption authority or product implementation |

At Interface V1, “ORION owns meaning” means ORION owns the meaning of exported
ORION objects. It does not supersede OLS normative authority, source authority
or Human meaning and decision authority.

## 8. ORION↔NEXAH Interface V1

Current status:

`MEMBRANE_V1_APPROVED_NOT_IMPLEMENTED`

Interface V1 is approved architecture, not an operational integration. It does
not convert ORION objects into NEXAH actions, episodes, navigation, reachability
or control objects.

The Legacy Public Contract/Gateway and Interface V1 are distinct boundaries.
Implementation or consumer evidence for one does not prove compatibility,
conformance or implementation of the other.

## 9. Retained historical and separately governed components

TransformationEngine, T01–T15, Operator Registry, F1 Runtime, Gateway, Public
Contract and LYRA remain outside the Certified Core unless separately adopted.

LYRA remains inactive and outside certified V1. Its retained historical
translator/explainer implementation does not activate, certify or adopt it.

Pre-existing untracked Runtime and deployment material remains:

`NONCANONICAL / PENDING SEPARATE REVIEW`

No authority follows from its presence.

## 10. Deferred and future Research concepts

- IRIS: `DEFERRED / UNRESOLVED`; no component is instantiated by assumption.
- SIRIUS: `DEFERRED / UNRESOLVED`; no single authoritative runtime definition
  is adopted.
- Operator-family reconciliation: `FUTURE_RESEARCH_CANDIDATE` only.

No equivalence is asserted among T01–T15, O8, JANUS, historical Codex, NEXAH
operators or transformation grammars.

## 11. Change control

- A future Extension Profile requires an explicit Owner adoption record.
- A certified Core change requires the applicable release/certification change
  process and cannot be performed through an extension.
- Cross-repository contracts require affected-owner acknowledgement.
- Interface V1 changes remain subject to its own frozen owner/change-control
  model.
- Research evidence remains immutable within its governing record and is not
  rewritten to support product adoption.

## 12. Explicit non-capabilities

This Master Architecture adds no general navigation, intervention, control,
recommendation, universal representation invariance, general scientific
validation, LYRA execution, Interface implementation, O8/B1 product capability,
IRIS/SIRIUS system or adopted Extension Profile.

## References

- [`ADR-0009`](../adr/0009-orion-master-architecture-adoption.md)
- [`ORION System Plate`](ORION_SYSTEM_PLATE.md)
- [`ORION Core Plate`](ORION_CORE_PLATE.md)
- [`Version 1 Certified Baseline`](../releases/ORION_V1_CERTIFIED_BASELINE.md)
- [`Version 1 Classification Report`](../releases/ORION_V1_VERSION_CLASSIFICATION.md)
- [`Version 1 Reading Order`](../releases/ORION_V1_READING_ORDER.md)
- [`Ownership Map`](../governance/OWNERSHIP.md)
- [`Cross-Repository Governance`](../governance/CROSS_REPOSITORY_GOVERNANCE.md)

