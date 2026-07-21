# Reject an Unknown Representation

- Session ID: `blockers-unknown-representation`
- Format: `orientation-session/1`

## Human Request

> Navigate Unknown Space → Calendar Projection

## LYRA Translation

- Vocabulary: `Navigate`
- Source: unknown
- Target: `Calendar Projection`
- Clarifications: impossible without a registered source
- Result: `UnknownRepresentation`

## ORION Input

None. LYRA cannot construct existing planning inputs from an unregistered source.

## ORION Result

No `TransformationReport` is produced.

## LYRA Explanation

The source representation is unknown, so the request cannot continue.

## Boundary Check

LYRA did not invent or alias `Unknown Space`. ORION did not receive, interpret or
plan the natural-language request.
