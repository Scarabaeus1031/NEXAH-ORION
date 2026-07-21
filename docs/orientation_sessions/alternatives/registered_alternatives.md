# Explain Registered Alternative Paths

- Session ID: `alternatives-registered-alternatives`
- Format: `orientation-session/1`

## Human Request

> Show Alternatives for Stellar Projection → Calendar Projection.

## LYRA Translation

- Vocabulary: `Show Alternatives`
- Source: existing Transformation Plan
- Target: `alternative_paths`
- Clarifications: none

## ORION Input

Existing report only; no route recalculation is requested.

## ORION Result

- Selected path: `T13`
- Registered alternative paths: `T12 → T14`
- Status: `blocked`
- Evidence: `E0–E1`
- Provenance: unchanged

## LYRA Explanation

LYRA states `Alternative paths: T12 → T14.` exactly from
`TransformationPlan.alternative_paths`.

## Boundary Check

LYRA did not generate, rank, select or execute the alternative. Status, evidence,
provenance and blockers remain present.
