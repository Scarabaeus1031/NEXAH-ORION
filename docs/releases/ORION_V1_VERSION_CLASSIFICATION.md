# ORION Version 1 Classification Report

- Status: authoritative Phase VIII document classification
- Rule: classification describes current authority, not file age or quality

## Classification meanings

| Class | Meaning |
|---|---|
| Version 1 | required to understand, execute or verify the stable baseline |
| Future Version | specified or reserved work outside implemented Version 1 scope |
| Research | inquiry without runtime or architectural authority |
| Experimental | executable exploration without supported public API status |
| Historical | immutable decision or phase evidence; not current guidance |

## Version 1

- `docs/releases/ORION_V1_CERTIFIED_BASELINE.md`;
- `docs/architecture/ORION_SYSTEM_PLATE.md` and `ORION_CORE_PLATE.md`;
- the frozen Representation and Structural Representation specifications;
- the frozen Markdown Structural Representation Profile and Projection
  Specification;
- Slice II–IV architecture, implementation, conformance, proof, and
  certification records;
- the corresponding Structural Representation, UNDERSTAND, Relations,
  Navigation, Orientation Map, Expression, and Slice certification modules;
- `docs/governance/` and the current release policy;
- Version 1 proof and certification tests.

The certified release ends at `at_slice_iv_certified`. No earlier or adjacent
module becomes part of Version 1 merely because it remains in the repository.

## Future Version

- Wonder, Compare, Connect, Explore, Build and Reflect Runtime implementations;
- transition operator implementations and renderers;
- approved transport encodings that may eventually occupy `schemas/`;
- persistence, network transport and additional consumer integrations;
- open transformation architecture questions explicitly marked for later
  decision.

These items have no current executable or public-interface authority.

### Future-document inventory

| Document or item | Classification | Reason |
|---|---|---|
| `docs/architecture/transformations/OPEN_ARCHITECTURE_QUESTIONS.md` | Future Version | deferred architecture questions; no accepted behavior |
| Wonder chapter in `ORION_ORIENTATION_OPERATORS.md` | Future Version | canonical behavior, Runtime absent |
| Compare chapter in `ORION_ORIENTATION_OPERATORS.md` | Future Version | canonical behavior, Runtime absent |
| Connect chapter in `ORION_ORIENTATION_OPERATORS.md` | Future Version | canonical behavior, Runtime absent |
| Explore chapter in `ORION_ORIENTATION_OPERATORS.md` | Future Version | canonical behavior, Runtime absent |
| Build chapter in `ORION_ORIENTATION_OPERATORS.md` | Future Version | canonical behavior, Runtime absent |
| Reflect chapter in `ORION_ORIENTATION_OPERATORS.md` | Future Version | canonical behavior, Runtime absent |
| Future renderer/operator references in T01–T15 and `TRANSITION_CARDS.md` | Historical | describe the earlier draft transform program, not a Version 1 commitment |

## Research

- everything under `docs/architecture/lucy/`;
- `docs/architecture/evidence/NEXAH_REASONING_ARCHITECTURE_REVIEW.md` as source
  research supporting earlier decisions;
- research templates and local `.workspace/research/` material.

LUCY remains a future reflection inquiry, not an ORION component.

### Research-document inventory

| Document | Classification |
|---|---|
| `docs/architecture/lucy/README.md` | Research |
| `docs/architecture/lucy/LUCY_CONCEPT.md` | Research |
| `docs/architecture/lucy/LUCY_CONCEPT_REVIEW.md` | Research |
| `docs/architecture/lucy/REFLECTION_MANIFEST.md` | Research |
| `docs/architecture/lucy/REFLECTION_BOUNDARY_DIAGRAM.md` | Research |
| `docs/architecture/lucy/FUTURE_RESEARCH.md` | Research |
| `docs/architecture/lucy/OPEN_QUESTIONS.md` | Research |
| `docs/architecture/evidence/NEXAH_REASONING_ARCHITECTURE_REVIEW.md` | Historical research evidence |

The word “future” inside these LUCY files denotes a research horizon, not a
Future Version commitment.

## Experimental

- `orion.ollama_backend` and its opt-in integration test;
- draft backend/context/execution prototypes retained at explicit module paths;
- local `.workspace/experiments/` content;
- any provider-specific execution outside the certified Version 1 proof chain.

Experimental code may remain reproducible, but it is not a Version 1 public
interface and cannot define observable ORION behavior.

## Historical

- `docs/development/PHASE_*.md` implementation records;
- `docs/orientation_sessions/` Phase 6C documentation-backed scenarios;
- `docs/architecture/baselines/` and the earlier F1 freeze/review snapshots;
- the Phase VIII audit, cleanup, freeze, RC1, release-candidate, and
  publication-baseline documents that describe an earlier repository state;
- ADRs when read as chronology (accepted decisions remain normative);
- legacy transition contracts and registry code at `0.1-draft`.

Earlier Public Contract, Runtime, Gateway, report, presentation, evaluation,
and LYRA implementation slices are historical or separately governed. They are
not certified Version 1 responsibilities. Earlier aggregate imports retained
for repository compatibility do not grant them certified authority.

Historical artifacts retain their original wording. Current status is resolved
through the Version 1 reading order rather than by rewriting history.

The exact earlier freeze documents
`ORION_V1_ARCHITECTURE_FREEZE.md`, `ORION_V1_ARCHITECTURE_REVIEW.md` and
ADR-0008 are Historical records of the F1 decision. ADR-0008's accepted
boundary remains normative; its old inventory and counts do not supersede the
Phase VIII audit. All named `PHASE_*.md` files and files under
`docs/orientation_sessions/` are Historical. No item in those collections is an
unclassified current or future interface.

## Ambiguity rule

If a document conflicts with this classification or uses future tense that is
no longer current, this report and the Version 1 reading order govern. A file
cannot acquire Version 1 authority merely because it resides under
`docs/architecture/`; it must be named above or incorporated by a named
canonical document.
