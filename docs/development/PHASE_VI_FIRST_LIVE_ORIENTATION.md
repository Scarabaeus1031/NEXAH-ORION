# Phase VI — First Live Understand Orientation

- Session ID: `phase-vi-first-live-understand`
- Phase: ORION Phase VI
- Date: 2026-07-22
- Format: executable in-process acceptance session
- Operator: `orion.orientation-operator/understand`
- Runtime effects: none

## Human intention

> I need to understand how ORION keeps evidence, interpretation, and Human
> authority separate before I trust an Orientation Report.

The Orientation Object is the canonical
`ORION_ORIENTATION_POLICIES.md` document at source revision
`facb20f3439d183f8494ba27d94975509ddec415`.

The Human-selected focus is the separation of evidence, interpretation and
Human authority. Execution technology and provider behavior are outside the
confirmed Scope.

## Executable session trace

Run the complete instrumented journey from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 scripts/phase_vi_live_orientation.py
```

The command emits one deterministic JSON trace containing, in order:

1. the Human intention and external request mapping;
2. the validated `OrientationRequest`;
3. the Runtime outcomes;
4. all bound `EvidenceReference` objects;
5. the `OrientationReport`;
6. the `ContinuationOption`;
7. the NEXAHEDRON presentation models.

The trace is an inspection artifact. It does not write state, influence
readiness, change Runtime behavior or bypass Gateway validation.

## Result

- Request: `phase-vi-understand-policies-01@1`
- Report: `report-phase-vi-understand-policies-01-1@1`
- Status: `complete`
- Contract Validation: `valid`
- Orientation Validation: `valid`
- Operator stages: all 11 completed
- Bound evidence: three observed, versioned canonical policy fragments
- Continuation: `inspect_evidence`, available
- Effects: none

The report identifies the confirmed focus and Scope, the canonical source and
revision, and the three policy locations that support the Understanding Frame:

- `2.1 P01 — The Human Owns Intention`;
- `2.1 P04 — Separation of Authority`;
- `2.3 P12 — Evidence Before Interpretation`.

The sensible next step is to inspect the evidence for P12 while retaining the
same report, intention, Scope, Human authority and Evidence References.

## Structured review: initial execution

The observations below classify the first execution before any Phase VI
correction. They intentionally state location and impact without proposing
solutions.

| Classification | Observation |
|---|---|
| Architecture issue | None observed. The journey crossed NEXAHEDRON mapping, Gateway, Runtime and public contracts without authority leakage. |
| Contract issue | None observed. Every Version 1.0 object and the complete lineage graph validated. |
| Runtime issue | The initial summary and conceptual structure repeated object identity and Scope but did not expose the evidence bindings in a Human-readable structure. |
| Runtime issue | `mode_payload.suggested_continuations` used an unversioned option identity while the canonical report continuation field used a versioned reference. |
| Gateway issue | None observed. Invalid or private objects were not exposed, and the validated Human intention remained unchanged. |
| Presentation issue | Evidence was initially presented only as opaque Evidence Reference identities. Source, fragment and authority were not visible in the presentation model. |
| User experience issue | The natural Human sentence was preserved, but this session still required explicit NEXAHEDRON choices for object, focus and Scope; free-language interpretation was not exercised. |
| Missing evidence | Evidence established identity, provenance, authority and source locations, but did not carry the full source statements. The result could orient to policy locations without restating their content. |
| Missing capability | No approved content-bearing Representation or retrieval capability participated in the session. Semantic explanation beyond the supplied evidence metadata was therefore not evaluated. |

## Minimal corrections justified by the session

Only the three deficiencies directly demonstrated by the initial execution were
corrected:

- the deterministic Understand report now exposes source-aware evidence
  bindings and a focus-aware summary;
- suggested continuation references now retain identity and version;
- presentation data now includes source, fragment, authority, editorial status,
  evidence class and relationship for every resolved Evidence Reference.

These corrections add no Operator, contract, Runtime concept, Gateway
responsibility or external capability. The same request and evidence complete
successfully after the corrections.

## Evaluation

| Question | Observed result |
|---|---|
| Can a Human express an intention naturally? | Yes for preservation: the sentence remains verbatim in the validated request and report. Automatic language interpretation was not tested. |
| Did the Gateway construct the correct request? | Yes. Identity, intention, Scope, authority and no-effects invariants validate. |
| Did the Runtime produce a useful report? | Yes within the deterministic scope: it provides a focused, source-aware orientation map. It does not claim semantic synthesis that the supplied evidence cannot support. |
| Is the evidence understandable? | Yes at the identity, source-location, authority, provenance and relationship levels. Full source content remains outside this session. |
| Are continuations meaningful? | Yes. `Inspect evidence` directly follows from the report and preserves complete lineage. |
| Does the flow feel coherent? | Yes as an in-process journey. Rendered interaction quality remains a NEXAHEDRON UX review question. |

## Boundary confirmation

- NEXAHEDRON supplied the external mapping and presentation need.
- The Gateway translated, validated, invoked and mapped only.
- The Runtime executed only UNDERSTAND.
- Evidence remained owned by its canonical source authority.
- The public Version 1.0 objects remained unchanged.
- The Human retained intention, Scope and continuation authority.
- No provider, prompt, retrieval, persistence, transport or session system was
  introduced.
