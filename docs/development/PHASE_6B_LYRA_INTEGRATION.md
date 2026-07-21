# Phase 6B: First LYRA Language Integration

- Status: implemented development baseline
- Scope: deterministic Human → ORION → Human boundary
- Repository version: `0.3.0-dev.0`

## Purpose

Phase 6B makes the Phase 6A language boundary executable without transferring
authority to LYRA. A canonical human request is translated into the existing
`OrientationObject` and `RepresentationTarget` planning inputs. The unchanged
`TransformationEngine` creates its report. LYRA then projects that exact report
into human-readable sentences.

```text
HumanLanguageRequest
        ↓ translate only
PlanningTranslation(OrientationObject, RepresentationTarget)
        ↓ ORION-owned composition
TransformationEngine
        ↓ unchanged
TransformationReport
        ↓ explain only
LyraExplanation(source_report = exact report)
```

LYRA does not plan, validate, route, execute, infer, call a provider or mutate
the supplied object. `LyraOrientationExecutor` is an ORION-owned composition
root outside `src/orion/lyra/`; it does not give the language package Engine
authority.

## Package layout

```text
src/orion/
├── lyra/
│   ├── __init__.py       public language-boundary exports
│   ├── vocabulary.py     canonical Phase 6A vocabulary
│   ├── models.py         immutable language projections
│   ├── translator.py     explicit deterministic mappings
│   ├── explanation.py    faithful report projection
│   └── exceptions.py     provider-neutral language failures
└── lyra_execution.py         ORION-owned end-to-end composition
```

## Input model

`HumanLanguageRequest` contains only:

- a non-empty utterance;
- an existing immutable `OrientationObject`.

The first baseline supports three explicit planning forms:

```text
Navigate <Source> → <Target>
Project <Source> → <Target>
Plan <Source> → <Target>
```

ASCII `->` is accepted as the same separator. The documented Phase 6A sentence
is also an explicit mapping:

```text
I want to understand how this observation reaches the calendar.
```

It maps to `Navigate + Explain`, Source `Observation`, Target
`Calendar Projection`. This is not a general natural-language parser. There is
no fuzzy matching and no inferred source or target.

Unknown vocabulary raises `UnsupportedIntent`. A known but incomplete or
multi-target request raises `ClarificationRequired`. Unknown sources and targets
raise `UnknownRepresentation` and `UnknownTarget` respectively. The named source
must match the supplied Orientation Object.

## Translation output

`PlanningTranslation` retains the exact `HumanLanguageRequest` and contains:

- one or more canonical `OrientationIntent` values;
- the resolved registered source name;
- the existing `RepresentationTarget` model;
- the fixed vocabulary version `orion.lyra-vocabulary/0.1`.

It is a language-boundary projection, not a new universal request contract.

## Output model

`LyraExplainer` accepts an existing `TransformationReport`. Its explanation
covers:

- planned or blocked status;
- explicit success wording only when the report status is `planned`;
- selected path and registered alternatives;
- unsupported paths and missing contracts, operators or renderers;
- invariant and compatibility failures;
- validation checks and errors;
- evidence chain;
- source references and source provenance;
- transformation provenance;
- required and preserved invariants;
- the absence of a produced Target Representation.

`LyraExplanation.source_report` is the exact report instance. Structured
properties expose status, evidence, provenance, blockers and alternatives
without reparsing prose. Consequently the explanation may simplify wording but
cannot erase or replace the authoritative result.

## Example

```python
from orion import (
    HumanLanguageRequest,
    LyraOrientationExecutor,
    OrientationObject,
    RepresentationRef,
)

source = OrientationObject(
    orientation_object_id="orientation-1",
    orientation_object_version="orientation-object/1",
    representation=RepresentationRef(
        representation_id="observation-1",
        representation_type="Observation",
        representation_version="representation/1",
        coordinate_profile="observation/1",
    ),
    source_references=("source:example",),
    provenance=("source:example@revision-1",),
    epoch="epoch-1",
)

interaction = LyraOrientationExecutor().execute(
    HumanLanguageRequest(
        "Navigate Observation → Calendar Projection",
        source,
    )
)

assert interaction.explanation.source_report is interaction.report
print(interaction.explanation.text)
```

The present registry has no executable transformation operators or renderers.
The normal result for a non-empty route is therefore a faithful blocked report,
not a generated Target Representation.

## Verification

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  python3 -m unittest tests.test_lyra
make test
make release-check
```

Tests cover the vocabulary, supported and unsupported input, clarification,
unknown representations, immutable models, blocked and planned reports, every
required issue class, alternatives, validation, evidence, provenance and exact
report retention across the round trip.

## Architecture Plate workflow

Architecture Plates are generated artifacts. Sources under
`docs/architecture/plates/src/` are canonical SVG; adjacent PNG files are
documentation output and must never be edited directly.

```bash
./scripts/generate-architecture-plates
./scripts/check-architecture-plates
```

When a plate changes, edit its SVG, regenerate the PNG, and review the plate
together with every Markdown document that embeds it. Plate 08 was reviewed
against this Phase 6B boundary; the Markdown remains authoritative.

## Out of scope

No LLM, prompt template, chat interface, Web UI, CLI, Builder Hub, memory, LUCY,
AI reasoning, mathematical operator, renderer execution, provider integration,
persistence, Kernel mutation or new planning behavior is introduced.
