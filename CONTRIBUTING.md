# Contributing to NEXAH-ORION

Every contribution begins with ownership. A technically correct change in the wrong repository is still an invalid change.

## Before changing anything

1. Read [`docs/governance/OWNERSHIP.md`](docs/governance/OWNERSHIP.md).
2. Classify the work as documentation, decision, research, experiment, contract, implementation, test, or release.
3. Confirm that ORION owns the change.
4. Identify affected repositories and compatibility surfaces.
5. Create or update an ADR before changing stable architecture or cross-repository ownership.

## Contribution paths

| Change type | Required path |
|---|---|
| typo or clarification with no semantic effect | edit the owning document; normal review |
| architecture or ownership change | ADR first; cross-repository review if applicable |
| cross-repository contract change | ADR + compatibility record + all affected owners |
| local research | `.workspace/research/`; promote only through a reviewed proposal |
| experiment | `.workspace/experiments/`; no product claim by location |
| release | release checklist, changelog, compatibility verification and signed tag policy |
| implementation | only within an accepted contract and ownership boundary |

## Branches

Use short-lived branches:

```text
codex/<topic>      Codex-assisted work
docs/<topic>       documentation-only work
adr/<topic>        decision proposals
chore/<topic>      repository workshop maintenance
```

Do not develop directly on `main`. Keep one ownership concern per branch.

## Pull requests

A pull request must state:

- responsible repository and module owner;
- change class and scope;
- affected ADRs and contracts;
- cross-repository compatibility impact;
- evidence or validation performed;
- explicit exclusions;
- rollback or recovery path when state or release metadata changes.

Use [the pull request template](.github/PULL_REQUEST_TEMPLATE.md).

## Required checks

```bash
./scripts/test
./scripts/check-workspace
./scripts/release-check --development
```

The default checks must remain usable without downloading model runtimes. Runtime integration tests are opt-in and require an externally managed local runtime.

## Architecture rule

Accepted architecture is changed by a superseding ADR, not by silently editing historical decisions. Rejected and superseded ADRs remain in the repository.

The frozen scope and canonical terminology are listed in
[`ORION_V1_ARCHITECTURE_FREEZE.md`](docs/architecture/ORION_V1_ARCHITECTURE_FREEZE.md).
An extension must name the frozen boundary it preserves. A redefinition must
stop for Architecture Review before implementation.

## Generated and local material

Never commit:

- `.workspace/` contents;
- model weights or provider caches;
- secrets or tokens;
- raw private research sources;
- unredacted model runs;
- generated contact sheets and source-material dumps;
- independent repository working trees.

## Conduct and security

Participation follows [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). Report
security-sensitive issues through [`SECURITY.md`](SECURITY.md), never through a
public issue containing credentials or exploit details.

## Contribution licensing

Software contributions are submitted under the
[Apache License 2.0](LICENSE). Original documentation, specifications,
research, books and visual material are submitted under
[CC BY 4.0](LICENSE-DOCS.md) where applicable. Contributors must preserve
third-party licenses and provenance. See [Licensing Scope](LICENSES.md).

## Definition of done

A change is done when ownership is clear, documentation and compatibility records agree, checks pass, and no stronger claim is made than the evidence supports.
