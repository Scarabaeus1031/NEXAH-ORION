# Compare Two Existing Reports

- Session ID: `comparison-report-comparison`
- Format: `orientation-session/1`

## Human Request

> Compare the existing Observation → Observation and Stellar Projection → Calendar Projection reports.

## LYRA Translation

- Vocabulary: `Compare`
- Source: two existing `TransformationReport` records
- Target: explicit report fields only
- Clarifications: none

## ORION Input

Two independently produced existing reports; LYRA sends no new planning request.

## ORION Result

- Report A: status `planned`, validation `valid`, empty path and issues
- Report B: status `blocked`, validation `invalid`, path `T13`
- Report B evidence: `E0–E1`
- Report B issues: `MissingOperator(T13)`, `MissingRenderer(T13)`
- Report B alternative: `T12 → T14`

## LYRA Explanation

The comparison states only these field differences. It does not infer why the
systems differ beyond the issues already present in Report B.

## Boundary Check

LYRA performed no new route selection or validation. Each underlying report and
its separate explanation remain intact and authoritative.
