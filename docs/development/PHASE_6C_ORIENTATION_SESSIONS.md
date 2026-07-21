# Phase 6C: Orientation Sessions

- Status: interaction-conformance baseline
- Scope: reproducible Human → LYRA → ORION → LYRA → Human scenarios
- Repository version: `0.3.0-dev.0`

## Purpose

Phase 6C validates usability of the existing Phase 6B language boundary without
changing it. The canonical collection lives in
[`docs/orientation_sessions/`](../orientation_sessions/README.md). It includes
successful planning, blocked routes, capability gaps, invalid language,
comparison, inspection, validation and registered alternatives.

Every session uses existing runtime objects and preserves the exact
`TransformationReport`. Report-view sessions operate on reports already
produced by ORION; they do not ask LYRA to plan again. Exception sessions prove
that unsupported, ambiguous or unregistered input stops before ORION.

## Conformance model

```text
versioned Markdown session
        ↕ synchronized by tests
canonical LYRA input or existing report-view intent
        ↓
Phase 6B translator / explainer
        ↓
unchanged TransformationEngine where planning is requested
        ↓
exact report, exact exception or explicit no-ORION outcome
```

`tests/test_orientation_sessions.py` verifies:

- every session file is indexed and has a conformance case;
- every case has the canonical seven-section document structure;
- every documented request produces the documented status, route, evidence,
  provenance, validation, blockers and alternatives;
- the explanation retains the exact report;
- clarification, unsupported vocabulary and unknown representations stop without
  guessing;
- comparison and inspection use existing fields only.

## Adding or changing a session

1. Reuse only the canonical vocabulary and existing runtime models.
2. Add the Markdown file under its category and keep all seven required sections.
3. Add it to the Orientation Sessions index.
4. Add a conformance case that executes the documented outcome.
5. Run the isolated and complete verification suites.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  python3 -m unittest tests.test_orientation_sessions
make test
make release-check
```

No session may introduce a representation, transition, contract, operator,
renderer, evidence level, planner behavior or explanation authority.

## Result

The repository is interaction-complete for the first deterministic human-facing
boundary: canonical input can be translated, existing ORION planning can run,
and the exact result can be translated back without authority transfer. This
does not imply transformation execution or production readiness. LUCY remains
outside the execution path and reserved for a future architecture decision.
