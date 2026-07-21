# Canonical Orientation Sessions

These versioned sessions are executable documentation for the Phase 6C
Human → LYRA → ORION → LYRA → Human boundary. They introduce no
architecture, contract, route or runtime authority. Each session uses the
canonical Phase 6A vocabulary and the Phase 6B deterministic implementation.

- Session format: `orientation-session/1`
- Vocabulary: `orion.lyra-vocabulary/0.1`
- Repository version: `0.3.0-dev.0`
- LUCY: outside the execution path

## Index

| Category | Session | Expected outcome |
|---|---|---|
| Canonical | [`canonical/full_round_trip.md`](canonical/full_round_trip.md) | blocked report faithfully explained |
| Navigation | [`navigation/existing_route.md`](navigation/existing_route.md) | registered route `T13` |
| Explanation | [`explanation/planned_identity.md`](explanation/planned_identity.md) | valid planned identity route |
| Blockers | [`blockers/blocked_route.md`](blockers/blocked_route.md) | blocked six-transition plan |
| Blockers | [`blockers/missing_operator.md`](blockers/missing_operator.md) | missing executable operator |
| Blockers | [`blockers/missing_renderer.md`](blockers/missing_renderer.md) | missing renderer |
| Blockers | [`blockers/unknown_representation.md`](blockers/unknown_representation.md) | `UnknownRepresentation` before ORION |
| Canonical | [`canonical/clarification_required.md`](canonical/clarification_required.md) | `ClarificationRequired`, no guessing |
| Canonical | [`canonical/unsupported_vocabulary.md`](canonical/unsupported_vocabulary.md) | `UnsupportedIntent` |
| Comparison | [`comparison/report_comparison.md`](comparison/report_comparison.md) | explicit field comparison of two reports |
| Inspection | [`inspection/report_metadata.md`](inspection/report_metadata.md) | versions, evidence and provenance retained |
| Validation | [`validation/validation_outcome.md`](validation/validation_outcome.md) | invalid outcome faithfully explained |
| Alternatives | [`alternatives/registered_alternatives.md`](alternatives/registered_alternatives.md) | registered alternative `T12 → T14` |

## Required format

Every session uses the same seven sections: Title, Human Request, LYRA
Translation, ORION Input, ORION Result, LYRA Explanation and Boundary Check.
`tests/test_orientation_sessions.py` enumerates every linked session, checks this
shape and executes its documented result. A new Markdown session without a test
case fails the suite; a test case without a listed document also fails.

Reports remain authoritative. Explanation text is a projection of report fields,
not a replacement. Exception sessions end at LYRA and explicitly confirm that
ORION received no input.
