# ORION Version 1 RC1 Dead Reference Report

## Scope

The audit inspected repository Markdown links, renamed paths, onboarding
navigation, release references and documents whose historical language could be
mistaken for current authority.

## Result

- Internal Markdown targets checked: no missing local targets.
- Renamed or moved Version 1 deliverables: no unresolved references.
- Phase VI and VII execution paths: present and documented.
- Public contract, Runtime, Gateway and evaluation paths: present.
- Architecture Plate sources, artifacts and checksum manifest: present.

External HTTP links were not treated as repository-controlled references; their
availability is outside a reproducible offline checkout.

## Corrections

| Location | Previous ambiguity | Documentation-only correction |
|---|---|---|
| root `README.md` | Version 1 and historical links share one index | verified that Version 1 reading, release, contract and Runtime links appear first; historical targets now carry explicit supersession notices where needed |
| `docs/architecture/README.md` | F1 freeze called the official current baseline | routed current readers to the Phase VIII audit and Version 1 reading order |
| `docs/development/WORKSPACE.md` | repository called “future”; `schemas/` described as the public contract location | aligned with the frozen contract binding and reserved transport-encoding role |
| `RELEASE_CANDIDATE.md` | earlier F1 candidate could be mistaken for RC1 | marked historical and linked to the RC1 checklist |
| `PUBLICATION_BASELINE.md` | earlier clean-state claims could be mistaken for current evidence | marked historical and linked to the RC1 recommendation |

## Historical-reference rule

Historical documents retain their original counts, versions and commands as
evidence of their phase. Their headers or current indexes identify them as
historical; they do not override the Version 1 reading order. No historical
record was rewritten to manufacture present-day results.

## Conclusion

The repository has no known dead internal documentation reference. Current,
historical, research and future navigation are distinguishable at onboarding.
