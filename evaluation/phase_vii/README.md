# Phase VII Real-World Orientation Evaluation

- Corpus: `orion-real-world-understand-corpus`
- Version: `1.0.1` (document revisions refreshed during the Phase VIII documentation audit)
- Operator: UNDERSTAND only
- Documents: 12
- Runtime and Gateway: unchanged from Phase VI

## Artifacts

- [`corpus.json`](corpus.json) — versioned document identities, SHA-256
  revisions, Human intentions, Scope and exact evidence selectors.
- [`EVALUATION_LOG.md`](EVALUATION_LOG.md) — session outcomes, metrics and
  per-session classifications.
- [`CROSS_SESSION_REVIEW.md`](CROSS_SESSION_REVIEW.md) — recurring findings
  across the corpus.
- [`ARCHITECTURE_STABILITY_REPORT.md`](ARCHITECTURE_STABILITY_REPORT.md) —
  contract and architecture stability assessment.

## Execute

Run the concise evaluation log:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  python3 scripts/phase_vii_real_world_evaluation.py
```

Run the complete inspection trace for all 12 sessions:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  python3 scripts/phase_vii_real_world_evaluation.py --full-trace
```

The harness verifies every document digest and every text-quote selector before
constructing evidence. It then validates each request, public outcome, Evidence
Reference and cross-contract lineage graph. It writes no state and does not
alter Gateway or Runtime behavior.
