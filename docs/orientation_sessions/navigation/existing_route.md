# Navigate Stellar Projection → Calendar Projection

- Session ID: `navigation-existing-route`
- Format: `orientation-session/1`

## Human Request

> Navigate Stellar Projection → Calendar Projection

## LYRA Translation

- Vocabulary: `Navigate`
- Source: `Stellar Projection`
- Target: `Calendar Projection`
- Clarifications: none

## ORION Input

Existing Stellar Projection `OrientationObject` and existing
`RepresentationTarget("Calendar Projection")`.

## ORION Result

- Type: `TransformationReport`
- Status: `blocked`
- Path: `T13`
- Evidence: `E0–E1`
- Provenance: source plus `T13` contract version retained
- Validation: `invalid`
- Issues: `MissingOperator(T13)`, `MissingRenderer(T13)`
- Alternative paths: `T12 → T14`

## LYRA Explanation

There is a registered direct route `T13`; it is blocked by the reported missing
operator and renderer. The registered alternative is `T12 → T14`.

## Boundary Check

The route and alternative came only from the Engine report. LYRA neither chose
nor executed either path and preserved status, evidence and provenance.
