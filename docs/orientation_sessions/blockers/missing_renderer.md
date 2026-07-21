# Explain a Missing Renderer

- Session ID: `blockers-missing-renderer`
- Format: `orientation-session/1`

## Human Request

> Navigate Stellar Projection → Calendar Projection

## LYRA Translation

- Vocabulary: `Navigate`
- Source: `Stellar Projection`
- Target: `Calendar Projection`
- Clarifications: none

## ORION Input

Existing Stellar Projection object and Calendar Projection target.

## ORION Result

- Type: `TransformationReport`
- Status: `blocked`
- Path: `T13`
- Evidence: `E0–E1`
- Provenance: `T13` contract step retained
- Validation: `invalid`
- Issues: `MissingOperator(T13)`, `MissingRenderer(T13)`
- Alternative paths: `T12 → T14`

## LYRA Explanation

LYRA explicitly names `Missing Renderer at T13` and preserves its report reason
and evidence. It does not render a representation.

## Boundary Check

Renderer absence remains a blocker. LYRA did not substitute an image, renderer
or visualization-only projection.
