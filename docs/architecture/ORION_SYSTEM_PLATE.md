# ORION System Plate

## Certified Core and Expression Architecture

Status: Canonical certified assembly
Baseline: Vertical Slice IV after WP30
Certified STOP: `at_slice_iv_certified`

```mermaid
flowchart TB
    representation["Representation"]
    understand["UNDERSTAND"]
    relations["Relations"]
    navigation["Navigation"]
    orientation_map["Orientation Map"]

    core_gate["CERTIFIED ORIENTATION CORE<br/><code>at_slice_iii_certified</code>"]

    expression_contract["Expression Contract"]
    expression_construction["Expression Construction"]
    expression_conformance["External Expression Conformance"]
    expression_certification["Expression Certification"]

    expression_gate["CERTIFIED EXPRESSION LAYER<br/><code>at_expression_certified</code>"]
    slice_iv_gate["VERTICAL SLICE IV CERTIFIED<br/><code>at_slice_iv_certified</code>"]

    representation --> understand
    understand --> relations
    relations --> navigation
    navigation --> orientation_map
    orientation_map --> core_gate

    core_gate --> expression_contract
    expression_contract --> expression_construction
    expression_construction --> expression_conformance
    expression_conformance --> expression_certification
    expression_certification --> expression_gate

    expression_gate --> slice_iv_gate

    classDef certified fill:#101b33,stroke:#b2832f,stroke-width:2px,color:#f7f3e9;
    class core_gate,expression_gate,slice_iv_gate certified;
```

| Certified boundary | Responsibility | Work packages |
|---|---|---:|
| Certified Orientation Core | Deterministic structural Orientation through the immutable Orientation Map | WP1–WP25 |
| Certified Expression Layer | Deterministic Contract, Construction, External Conformance, and Expression Certification | WP26–WP29 |
| Vertical Slice IV Certified | Certification of the complete Core-to-Expression boundary | WP30 |

The plate is an assembly view. It introduces no component, authority, behavior,
or execution path. Runtime, Gateway, LYRA, SIRIUS, applications, presentation,
and semantic interpretation remain outside the certified chain shown here.
