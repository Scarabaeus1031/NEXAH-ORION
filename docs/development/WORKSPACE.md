# Local Workspace

The repository is the ORION source repository and the entry point for a local
multi-repository workshop. Independent repositories are never copied into
ORION; local working copies live under `.workspace/`, which is ignored by Git.

## Bootstrap

Create the local zones:

```bash
./scripts/bootstrap-workspace
```

Connect an existing Core clone:

```bash
./scripts/bootstrap-workspace --core-path /absolute/path/to/NEXAH
```

Or clone and detach the pinned Core revision:

```bash
./scripts/bootstrap-workspace --clone-core
```

The Core checkout is verified against the revision in `workspace.yaml`. The script does not initialize Library or Builder Hub while their remotes remain `pending`.

## Resulting local layout

```text
nexah-orion/
├── docs/                         tracked ORION records
├── schemas/                      reserved transport encodings
├── src/orion/                    Version 1 binding and retained internal slices
├── tests/                        ORION-owned verification
├── tools/                        future maintained repository tools
├── scripts/                      workshop automation
├── workspace.yaml               repository and local-zone manifest
└── .workspace/                   ignored local workshop
    ├── architecture/
    ├── repositories/
    │   ├── NEXAH                 pinned Core clone or symlink
    │   ├── nexah-library         only after remote confirmation
    │   └── nexah-builder-hub     only after repository confirmation
    ├── research/
    ├── experiments/
    ├── runs/
    ├── reviews/
    ├── releases/
    └── archive/
```

## Zone rules

| Zone | Purpose | May become authoritative by placement? | Commit to ORION? |
|---|---|---:|---:|
| `docs/` | reviewed ORION records | yes, according to document status | yes |
| `schemas/` | optional future transport encodings | only after separate approval | later |
| `src/orion/` | executable public binding, Runtime, Gateway and retained internal slices | according to the public boundary | yes |
| `tests/` | ORION-owned execution verification | yes | yes |
| `.workspace/research/` | sources, notes, hypotheses | no | no |
| `.workspace/experiments/` | disposable trials and benchmarks | no | no |
| `.workspace/runs/` | manifests, outputs, model traces | no | no |
| `.workspace/reviews/` | local review bundles | no | no |
| `.workspace/releases/` | local release candidates | no | no |
| `.workspace/archive/` | inactive clones and evidence | no | no |

Promotion is a reviewed change, not a file move. A local artifact enters the repository only after ownership, provenance, licensing, redaction, and target status are explicit.

## Repository safety

- Never run formatting or bulk edits across `.workspace/repositories/NEXAH`.
- Never make ORION depend on an uncommitted sibling working tree.
- Record external repository revisions in compatibility and release records.
- Keep tokens, model weights, private sources, and raw runs outside Git.
- Do not replace a pinned Core clone with a newer branch without updating governance records first.

## Daily check

```bash
./scripts/check-workspace
./scripts/test
```

The default checks verify repository structure, ADR metadata, the F1 Architecture
Freeze, version syntax, forbidden tracked paths, the Core revision when a local
Core checkout is connected, all offline unit and documentation-conformance tests,
architecture consistency, frozen boundaries, and Architecture Plate
reproducibility. `make integration` additionally requires the explicitly
configured local Ollama runtime and model.
