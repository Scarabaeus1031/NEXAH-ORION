# Navigate Observation → Calendar Projection

- Session ID: `canonical-full-round-trip`
- Format: `orientation-session/1`

## Human Request

> I want to understand how this observation reaches the calendar.

## LYRA Translation

- Vocabulary: `Navigate`, `Explain`
- Source: `Observation`
- Target: `Calendar Projection`
- Clarifications: none

## ORION Input

Existing `OrientationObject` plus existing `RepresentationTarget`; no additional
runtime fields.

## ORION Result

- Type: `TransformationReport`
- Status: `blocked`
- Path: `T02 → T04 → T06 → T08 → T11 → T13`
- Evidence: `E0 → E0 → E0–E1 → E0 → E0 → E0–E1`
- Provenance: source and six contract steps retained
- Validation: `invalid`
- Issues: `MissingOperator` and `MissingRenderer` for every path edge
- Alternative paths: seven registered alternatives
- Produced representation: none

## LYRA Explanation

LYRA reports the blocked status, selected route, all registered alternatives,
issues with their evidence, validation fields, source and transformation
provenance, invariants, and that no target representation was produced.

## Boundary Check

LYRA invented and changed nothing and performed no planning. ORION interpreted
no language and produced no explanation. The exact report remains attached to
the explanation.
