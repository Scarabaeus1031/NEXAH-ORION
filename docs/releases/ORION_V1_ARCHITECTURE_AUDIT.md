# ORION Version 1 Architecture Audit

- Status: Phase VIII consolidated audit
- Scope: repository state at the Version 1 freeze review
- Change policy: clarification and release preparation only

## Result

ORION Version 1 is internally coherent for its declared scope: one deterministic
Understand orientation exposed through frozen public contracts, a bounded
Runtime, a thin Gateway, presentation mapping and reproducible evaluation. The
audit found no repeated evidence requiring an architecture or contract change.

Two release-cleanup inconsistencies were corrected without changing behavior:

1. the root Python package had re-exported draft-era internal implementations;
2. the implemented Understand operator still identified itself as
   `0.1-draft` in otherwise Version 1 public reports.

The supported root surface is now limited to the Version 1.0 contract suite,
`OrientationRuntime`, `OrientationGateway`, its boundary, and presentation
models. The Understand operator and payload identify as `1.0`.

## Responsibility boundaries

| Authority | Version 1 responsibility | Confirmed exclusion |
|---|---|---|
| NEXAH | Orientation Layer and canonical framework authority | Laboratory interaction and ORION execution |
| ORION | navigation, validation, evidence-bound reports and continuations | Human intent, meaning and decisions; Library editorial authority; UI |
| LYRA | faithful human-language translation and explanation | reasoning, planning, validation and evidence authority |
| Library | evidence, knowledge identity and editorial authority | orientation execution and Laboratory experience |
| Human | intent, reflection and decision | no authority is silently delegated |
| NEXAHEDRON | Laboratory experience and presentation | ORION internals and NEXAH framework authority |

The dependency direction is preserved: consumer → Gateway → Runtime → Public
Contracts. Public Contracts do not import the Runtime or Gateway; the Runtime
does not import the Gateway; presentation derives only from validated public
outcomes.

## Vocabulary and naming

The public language consistently uses: Orientation Request, Clarification
Result, Orientation Report, Continuation Option, Evidence Reference and Runtime
Error. Identity fields remain type-specific (`request_id`, `report_id`,
`continuation_id`, `evidence_id`) and relationships use explicit identity and
version pairs. Scope and Intention are not treated as synonyms.

Earlier internal modules contain similarly named draft models. They remain
available only by explicit module path for historical tests and are no longer
part of the root public API. This removes the only public naming collision.

## Version consistency

| Surface | Version |
|---|---|
| Architecture baseline | `orion-architecture-v1` |
| Public Contract Suite | `1.0` |
| Understand operator and mode payload | `1.0` |
| Repository development package | `0.3.0-dev.0` pending an explicit release action |
| Historical transition and registry prototypes | `0.1-draft`, internal only |

The repository package version is release metadata, not a second contract
version. It should become `1.0.0` only through the release procedure after this
freeze recommendation is accepted.

## Lifecycle and outcome consistency

The observable lifecycle is deterministic:

1. Orientation Request validation;
2. Clarification Required or Ready;
3. Processing;
4. completed, partial or blocked Orientation Report, or a public Runtime Error;
5. zero or more report-derived Continuation Options.

Clarification Required, Invalid, Unsupported, Blocked Before Processing,
Blocked Report and Internal Failure are distinguishable public outcomes. A
blocked report means processing began and yielded a report; a blocked Runtime
Error means processing could not begin. Continuations originate from exactly
one report and preserve request, object, scope, evidence and authority lineage.

## Documentation consistency

Canonical contract headers now reflect their implemented and frozen status.
The `schemas/` reservation no longer incorrectly says that no public contract
exists, and source/ownership maps now distinguish the supported Version 1
surface from retained historical slices. Historical phase records remain
unchanged evidence of their time and are not current contributor guidance.

## Boundary leakage review

No Version 1 public contract exposes providers, prompts, transport,
orchestration plans, private reasoning, persistence or caching. Presentation
models do not replace public contracts. Runtime failures are returned as public
objects rather than implementation exceptions.

## Audit conclusion

No architecture, contract field, validator rule, lifecycle, operator behavior
or runtime capability changed during Phase VIII. The audited baseline is ready
for a stable freeze subject to the release controls in the freeze
recommendation.
