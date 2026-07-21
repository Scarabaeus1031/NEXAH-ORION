# Explain Validation Outcome

- Session ID: `validation-validation-outcome`
- Format: `orientation-session/1`

## Human Request

> Validate the existing Stellar Projection → Calendar Projection report.

## LYRA Translation

- Vocabulary: `Validate`
- Source: existing report validation
- Target: validation explanation
- Clarifications: none

## ORION Input

Existing report only. Validation has already been performed by ORION.

## ORION Result

- Validation: `invalid`
- Checks: object immutability, explicit graph, selected `T13`, contract edge
  compatibility, invariant preservation, provenance completeness and evidence
  completeness
- Errors: the report's missing operator and renderer reasons

## LYRA Explanation

LYRA reports `Validation summary: invalid` and reproduces every check and error
from the existing `TransformationValidation`.

## Boundary Check

LYRA did not run, change or override validation and did not convert invalid to
valid.
