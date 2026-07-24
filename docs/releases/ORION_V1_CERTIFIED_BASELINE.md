# ORION Version 1 Certified Baseline

Status: Canonical and frozen
Baseline point: Completion of WP30
Final certified STOP: `at_slice_iv_certified`

## 1. Purpose

This document records the certified ORION Version 1 implementation baseline
reached after Vertical Slice IV. It consolidates the responsibilities,
boundaries, guarantees, and explicit exclusions already certified through
WP30. Nothing in this document creates new authority, architecture,
implementation, or behavior.

## 2. Certified Vertical Slices

| Vertical Slice | Certified responsibility | Status | Certified STOP |
|---|---|---|---|
| Slice II | Structural Representation | Certified | `at_slice_ii_complete` |
| Slice III | Relations, Navigation, Orientation Map | Certified | `at_slice_iii_certified` |
| Slice IV | Expression | Certified | `at_slice_iv_certified` |

## 3. Certified Architecture

```text
Representation
        ↓
UNDERSTAND
        ↓
Relations
        ↓
Navigation
        ↓
Orientation Map
════════════════════════════════
Certified Orientation Core
════════════════════════════════
        ↓
Expression Contract
        ↓
Expression Construction
        ↓
External Expression Conformance
        ↓
Expression Certification
════════════════════════════════
Certified Expression Layer
════════════════════════════════
        ↓
Vertical Slice IV Certified
        ↓
at_slice_iv_certified
        ↓
STOP
```

This assembly is also recorded by the
[ORION System Plate](../architecture/ORION_SYSTEM_PLATE.md).

## 4. Certified Responsibilities

Version 1 certifies only the following responsibilities:

- deterministic Structural Representation of the accepted source domain;
- immutable structural identity, ordering, locators, provenance, integrity,
  and declared lossiness;
- External Representation Conformance;
- UNDERSTAND inventory of already-declared structural elements;
- deterministic Structural Summary and Structural Statistics;
- deterministic creation of the certified structural and declared Relations;
- External Relation Conformance and Relations Certification;
- immutable Navigation contract and deterministic Navigation Construction;
- External Navigation Conformance and Navigation Certification;
- immutable Orientation Map contract and deterministic Orientation Map
  Construction;
- External Orientation Map Conformance and Vertical Slice III Certification;
- immutable Expression Contract;
- deterministic Expression Construction within the declared communicative
  scope, exclusions, and lossiness;
- External Expression Conformance;
- Expression Certification;
- Vertical Slice IV Certification.

Every responsibility ends at its certified boundary. No responsibility gains
authority from a later certification.

## 5. Explicit Non-Responsibilities

The Version 1 certified baseline does not include:

- Runtime;
- Gateway;
- LYRA execution;
- SIRIUS;
- applications;
- Human Reports;
- presentation;
- reasoning;
- semantic interpretation;
- decision making.

Their absence from this baseline is deliberate. No certified Version 1
artifact implies that any of these responsibilities executed.

## 6. Repository Guarantees

The Version 1 certified baseline guarantees:

- deterministic replay for the certified execution chain;
- canonical UTF-8 JSON serialization for certified artifacts;
- immutable certification artifacts;
- explicit and non-overlapping responsibility boundaries;
- provenance preservation across every certified transition;
- byte-identical canonical proof replay for equal accepted inputs;
- stable identity and deterministic SHA-256 integrity;
- explicit STOP boundaries;
- no mutation of certified predecessor artifacts.

These guarantees apply to the certified responsibilities recorded in this
document and do not extend authority beyond them.

## 7. Frozen Boundaries

The certified artifacts, responsibilities, provenance chains, proof conditions,
and STOP boundaries recorded here form the frozen Version 1 baseline.

Future work may extend Version 1 only outside these certified boundaries. It
must not silently reinterpret, weaken, replace, or transfer a Version 1
responsibility. Any later extension must remain distinguishable from this
baseline and preserve its certified record.

## 8. Engineering Principle

Version 1 is not defined by features.

Version 1 is defined by certified responsibility boundaries.

The architecture is frozen.

Future work begins outside those boundaries.
