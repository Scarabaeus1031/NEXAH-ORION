# Explain a Blocked Route

- Session ID: `blockers-blocked-route`
- Format: `orientation-session/1`

## Human Request

> Navigate Observation → Calendar Projection

## LYRA Translation

- Vocabulary: `Navigate`
- Source: `Observation`
- Target: `Calendar Projection`
- Clarifications: none

## ORION Input

Existing Observation object and Calendar Projection target.

## ORION Result

- Type: `TransformationReport`
- Status: `blocked`
- Path: `T02 → T04 → T06 → T08 → T11 → T13`
- Evidence: six entries retained
- Provenance: source plus six contract steps retained
- Validation: `invalid`
- Issues: twelve capability blockers
- Alternative paths: seven

## LYRA Explanation

LYRA states that the deterministic plan is blocked and lists every issue from
the report. It states that no target representation was produced.

## Boundary Check

No blocker, evidence value, alternative, validation field or provenance step is
removed or upgraded. LYRA did not attempt a different route.
