# Explain a Missing Operator

- Session ID: `blockers-missing-operator`
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

LYRA explicitly names `Missing Operator at T13` and repeats the report reason and
evidence. It does not claim an operator is available.

## Boundary Check

LYRA neither invented nor executed an operator and did not hide the independent
renderer blocker.
