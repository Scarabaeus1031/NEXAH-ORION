# Phase 4A Closeout — Context, Representation and Navigation Baseline

- Date: 2026-07-19
- Repository version: `0.3.0-dev.0`
- Branch before commit: `main`
- Previous baseline: `801e3a6c923ff27cf7d15c0008f06a8349af8c69`
- Status: development baseline candidate; no release, tag, or push

## Executive summary

This closeout freezes the complete ORION development baseline from Phase 2A
through Phase 4A. ORION can select and load explicit repository context, build an
immutable `ContextManifest`, derive a content-free `ContextBrief`, run the
provider-neutral reasoning pipeline, navigate the registered Representation
Graph, verify planning contracts, and return deterministic plans and blocker
reports.

No transformation operator or renderer exists in this baseline. The
Transformation Engine plans only. It never creates a Target Representation;
`TransformationReport.produced_representation` remains `None`.

All authority boundaries remain intact. The frozen Phase 1A contracts, backend
port, executor, validation, and `FakeBackend` are byte-identical to their first
baseline. The Phase 1B `OllamaBackend` is also byte-identical. Ollama remains an
externally managed runtime and was not started, stopped, or required by this
closeout.

## Phase history

| Phase | Result | Authority boundary retained |
|---|---|---|
| 2A | `RepositoryContextProvider`, `ContextBuilder`, and `ContextualOrientationExecutor` provide deterministic read-only repository context | only `ContextBuilder` creates Phase 2 manifests; backend and Validation remain separate |
| 2B | `DocumentSelector`, `SelectionResult`, and `SelectingOrientationExecutor` derive explicit paths from versioned scope rules | selector performs no file I/O, hashing, manifest creation, or reasoning |
| 2C | immutable `ContextBrief`, builder, brief-capable backend port, and executor project manifest metadata without content | no prompt, document text, selection, or changed Phase 1 backend contract |
| 3A | Representation and Rendering Architecture formalizes immutable projections and renderer boundaries | architecture documentation only; no renderer implementation |
| 3B | Transform Stack, Graph, Matrix, Cards, Invariants, and open questions map existing representation states | candidate cartography only; no new geometry or executable operators |
| 3C | provider-independent TransitionContract specification and normalized `T01–T15` contracts | documentation contracts remain draft; unknown/candidate operators remain non-executable |
| 4A | immutable runtime graph and planning-contract registries plus `TransformationEngine`, plans, provenance, evidence, validation, and blocker reports | orchestration only; no operator, renderer, persistence, LLM call, target production, or Kernel mutation |

## Executable architecture

The following capabilities execute in the current development baseline:

- deterministic scope-based repository document selection;
- explicit read-only document loading and deterministic context building;
- immutable `ContextManifest` creation by `ContextBuilder`;
- deterministic, content-free `ContextBrief` projection;
- backend-independent reasoning contracts and execution composition;
- `FakeBackend` offline reasoning and the externally managed local Ollama
  reference adapter;
- independent Validation against the original `ContextManifest`;
- deterministic navigation of registered Representation Graph edges;
- Transition Contract presence, endpoint, version, and invariant verification;
- deterministic `TransformationPlan`, alternative routes, provenance chain,
  evidence chain, Validation, and blocker reports.

Phase 4A navigation is executable; representation transformation is not.

## Documentation-only architecture

The following remain specifications or architectural evidence only:

- Representation and Rendering Architecture;
- domain-specific renderer families;
- Orientation Transform Stack semantics;
- mathematical candidates named in Transition Cards and Contracts;
- coordinate operations between representation states;
- all `T01–T15` transformation execution;
- scientific interpretation or validation of NEXAH representations.

Documentation never upgrades an operator beyond the evidence available in Phase
3. A formula named as a candidate is not an implementation.

## Explicit executable/non-executable distinction

### Executable

- context selection and building;
- Context Brief projection;
- backend-independent reasoning pipeline;
- deterministic graph navigation;
- contract verification;
- `TransformationPlan` and blocker reports.

### Not executable

- mathematical transformation operators;
- renderers;
- Target Representation production;
- semantic retrieval;
- persistence;
- Kernel mutation;
- scientific validation of NEXAH representations.

## Responsibility map

| Component | Owner | Responsibility | Must not do |
|---|---|---|---|
| `DocumentSelector` | ORION selection layer | apply explicit scope-to-path rules | file I/O, crawling, ranking, manifest creation |
| `RepositoryContextProvider` | ORION context-source boundary | load selected repository files read-only | select, rank, write, or call a backend |
| `ContextBuilder` | ORION context-integrity layer | create the Phase 2 `ContextManifest` | select documents, call a backend, validate results |
| `ContextBriefBuilder` | ORION presentation-metadata layer | project manifest order and provenance without content | read files, prompt, summarize, rank, infer |
| reasoning backend ports/adapters | ORION reasoning boundary | return provider-neutral untrusted results | validate or mutate Kernel, Library, or context |
| Validation | ORION validation boundary | validate results against request, manifest, backend, and evidence | decide canonical Kernel truth |
| Representation Graph registry | ORION planning boundary | enumerate only registered directed edges | infer missing transitions |
| Transition Contract registry | ORION planning boundary | expose normalized planning metadata | implement operators or upgrade evidence |
| `TransformationEngine` | ORION navigation layer | plan routes and report compatibility, invariants, evidence, provenance, and blockers | calculate, approximate, render, persist, reason, call a provider, or mutate Kernel |
| transformation operators | unassigned | none in this baseline | not executable |
| renderers | future Lyra/Representation boundary | none in this baseline | not executable |

The normative repository ownership map is
[`docs/governance/OWNERSHIP.md`](../governance/OWNERSHIP.md).

## Frozen boundaries

### Phase 1A and 1B byte identity

| File | SHA-256 |
|---|---|
| `src/orion/contracts.py` | `82e4dbc3c915cf6545bc410ce7aa00749ef86a52241e92ecf8f24de900c9ab13` |
| `src/orion/backend.py` | `6e8057112a116172136b02311a314dff76bd90818f1c9992d481ee68977ed6f1` |
| `src/orion/executor.py` | `12ed38214c12ba637d63f1f6fb81619f43e886ac5c6ff91cdfc8a1f2e4fb9fd4` |
| `src/orion/validation.py` | `47bfcce22f804c109f8b4a7428aa551c962ea6a2f78bf792daf30ff320860c66` |
| `src/orion/fake_backend.py` | `114fff63a1a8345c73028503b8086f149e8f2494c18aae604448e610fc46f736` |
| `src/orion/ollama_backend.py` | `6a242195e5ea50ffdb3149277aae939fd15560591b6c397ffd7aecb88e1b474d` |

`ReasoningBackend`, `FakeBackend`, `OllamaBackend`, the Phase 1 executor, and
Validation are unchanged. Validation still accepts a `ContextManifest` and
checks claims against its entries.

### Phase 2 responsibility verification

- `ContextBuilder` is the only `ContextManifest.create` caller in the Phase 2
  flow. The frozen historical Phase 1 executor remains separate.
- `DocumentSelector` contains no file-read or file-write operation.
- `RepositoryContextProvider` owns the only repository read in Phase 2.
- `ContextBrief` and `ContextBriefEntry` contain neither a `content` nor a
  `prompt` field.
- `ContextBriefBuilder` receives only a valid manifest and performs no file I/O,
  selection, backend call, summarization, or ranking.

### Phase 4A responsibility verification

- the Transformation Engine imports no backend, provider, networking, database,
  Kernel, operator, or renderer implementation;
- all runtime catalog operator statuses remain `unknown` or `candidate`;
- no default contract has an executable operator or registered renderer;
- `produced_representation` has the immutable default `None`;
- navigation uses only explicit graph edges and simple paths.

The automated checks live in [`scripts/check-boundaries`](../../scripts/check-boundaries)
and [`scripts/check-architecture-consistency`](../../scripts/check-architecture-consistency).

## Graph and contract inventory

The following table is identical across the Representation Graph, Transition
Cards, normalized Contract documents, runtime graph registry, and runtime
contract registry:

| ID | Source | Target | Evidence | Operator |
|---|---|---|---|---|
| T01 | Reality | Observation | E1 | unknown |
| T02 | Observation | Planetary Chemistry | E0 | unknown |
| T03 | Observation | Lunar/Solar Dynamics | E0–E1 | candidate |
| T04 | Planetary Chemistry | Scarabaeus Engine | E0 | unknown |
| T05 | Lunar/Solar Dynamics | Scarabaeus Engine | E0 | unknown |
| T06 | Scarabaeus Engine | Möbius Topology | E0–E1 | candidate |
| T07 | Scarabaeus Engine | Frequency Space | E1 | candidate |
| T08 | Möbius Topology | Lissajous Geometry | E0 | unknown |
| T09 | Frequency Space | Lissajous Geometry | E1 | candidate |
| T10 | Lissajous Geometry | Frequency Space | E1 | candidate |
| T11 | Lissajous Geometry | Stellar Projection | E0 | unknown |
| T12 | Stellar Projection | Dodecahedral Sky Map | E0–E1 | candidate |
| T13 | Stellar Projection | Calendar Projection | E0–E1 | candidate |
| T14 | Dodecahedral Sky Map | Calendar Projection | E0 | unknown |
| T15 | Calendar Projection | Orientation Layer | E1 | candidate |

No edge is inferred. Unknown and candidate operators are non-executable.

### Consistency corrections during closeout

The audit found six demonstrable terminology-only mismatches. Alias text or
spacing was normalized to canonical Graph endpoints in T01, T03, T05, T07, T09,
and T10. No edge, representation, contract, evidence level, operator status, or
meaning changed. The automated consistency check passes after these corrections.

## Runtime inventory

| Capability | Runtime files | Status |
|---|---|---|
| Phase 1 request/reasoning/validation | `contracts.py`, `backend.py`, `executor.py`, `validation.py`, `fake_backend.py` | frozen and executable |
| Local Ollama adapter | `ollama_backend.py` | frozen; external runtime only |
| Phase 2A context | `context_builder.py`, `context_execution.py` | executable |
| Phase 2B selection | `document_selector.py`, `selection_execution.py` | executable |
| Phase 2C brief | `context_brief.py`, `brief_backend.py`, `brief_execution.py` | executable with a brief-capable injected backend |
| Phase 4A planning contracts | `transformation_contracts.py` | executable metadata validation; no operator or renderer |
| Phase 4A navigation | `transformation_engine.py` | executable planning and blocker reporting only |

There are no provider SDK dependencies. Network imports remain confined to the
frozen local Ollama adapter.

## Verification results

| Check | Result before commit |
|---|---|
| all isolated tests | PASS: 45 discovered, 44 passed, 1 opt-in integration test skipped |
| Ollama integration | NOT EXECUTED: optional external runtime; no lifecycle action |
| `./scripts/check-architecture-consistency` | PASS for T01–T15 across all five representations of the registry |
| `./scripts/check-boundaries` | PASS |
| `./scripts/check-workspace` | PASS |
| `./scripts/release-check --development` | PASS for `0.3.0-dev.0` |
| Python syntax and imports | PASS for 25 Python files without bytecode output |
| TOML validation | PASS for `pyproject.toml` |
| Markdown links | PASS; rerun after final closeout artifact creation |
| `git diff --check` | PASS |
| secret and credential scan | PASS; no values or private keys detected |
| machine-specific absolute path scan | PASS |
| large-file scan | PASS; no candidate file exceeds 1 MiB |
| binary/generated/model/cache scan | PASS; no candidate artifact detected |
| vendor and submodule scan | PASS; no submodule or embedded repository candidate |

The complete candidate is measured again after this record and its checksum
sidecar are finalized.

## Critical checksums

| File | SHA-256 |
|---|---|
| `src/orion/transformation_contracts.py` | `1a14bf652111f67a18b331e2b52e0e268eb0f85a57b03b9da2f721cae07e267b` |
| `src/orion/transformation_engine.py` | `057a3915a6e9e14a11e1004f8a388f6bd857cf97e499c865e0b3db610205b2b0` |
| `scripts/check-architecture-consistency` | `e2b34b56796dc5ba0001bca6a2b586530b8e80ebc15e5c57295a976b63d5f4ba` |
| `scripts/check-boundaries` | `fb9637405ad540d5f0d831bbee7c1828e66df5dd05aefd095d7cb1d03eefc6f7` |

The checksum of this closeout record is stored after finalization in
[`PHASE_4A_CLOSEOUT.sha256`](PHASE_4A_CLOSEOUT.sha256). A file cannot contain its
own ordinary SHA-256 without changing that checksum; the adjacent sidecar avoids
that self-reference.

## Repository status before commit

- Branch: `main`
- Base commit: `801e3a6c923ff27cf7d15c0008f06a8349af8c69`
- Tracked modifications: 8 files
- New baseline files: 44 files, including this record and its checksum sidecar
- Commit candidate: 112 files, approximately 540.7 KiB
- Candidate files over 1 MiB: 0
- Candidate binary files: 0
- Staged files at initial audit: 0

Ignored local material remains outside the candidate:

- `.workspace/` local multi-repository links and workspace state;
- `source_material/` visual evidence, approximately 36 MiB;
- Python `__pycache__/` directories generated by local test runs.

No model weights, model stores, runs, outputs, caches, external repositories, or
machine-specific absolute paths are part of the baseline commit.

## Exact baseline commit scope

The single baseline commit contains only:

1. Phase 2A–2C ORION source, tests, and development documentation;
2. Phase 3A Representation Architecture;
3. Phase 3B Transform Stack, Graph, Matrix, Cards, Invariants, and open questions;
4. Phase 3C specification and normalized T01–T15 Contract documents;
5. Phase 4A graph/contract registries, Transformation Engine, tests, and
   development documentation;
6. this closeout record and checksum sidecar;
7. additive ownership, README, source/test navigation, changelog, workspace, and
   automated consistency/boundary checks required to describe and protect the
   baseline.

It contains no Phase 1 frozen-source change, external repository, production
release artifact, model/runtime content, operator, renderer, or Target
Representation.

Proposed commit message:

```text
feat: establish ORION context and transformation planning baseline
```

## Known limitations

- The Context Brief contains metadata but deliberately no document content or
  prompt; existing Phase 1 backends do not automatically consume it.
- Scope selection has only explicit deterministic rules; there is no semantic
  retrieval or automatic discovery.
- Only one real reasoning adapter exists, so cross-provider conformance is not
  demonstrated.
- Phase 3 evidence remains E0–E1. Architecture documentation is not scientific
  validation.
- The Transformation Engine selects deterministic structural paths. It does not
  rank them semantically or by evidence.
- Every default transformation route is blocked because operators and renderers
  are intentionally absent.
- Plans and reports are not persisted.

## Intentionally blocked capabilities

- all mathematical, geometric, astronomical, temporal, musical, and other
  transformation operators;
- all renderers, visual output, and Target Representation production;
- operator approximation, inferred edges, or invented transitions;
- prompt rendering, semantic retrieval, embeddings, vector databases, and RAG;
- additional model providers and runtime lifecycle management;
- persistence, replay database, and production audit store;
- NEXAH Core or Library mutation;
- Builder Hub integration;
- scientific proof or validation of representation claims;
- production release, stable tag, and remote push.

## Reproduction commands

Core verification:

```bash
make test
./scripts/check-architecture-consistency
./scripts/check-boundaries
./scripts/check-workspace
./scripts/release-check --development
git diff --check
```

Syntax, imports, and TOML without bytecode output:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -c \
  'import ast, tomllib; from pathlib import Path; files=sorted([*Path("src").rglob("*.py"), *Path("tests").rglob("*.py")]); [ast.parse(path.read_text(encoding="utf-8"), filename=str(path)) for path in files]; tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8")); import orion; import orion.transformation_engine; print(len(files))'
```

Frozen and critical checksums:

```bash
shasum -a 256 \
  src/orion/contracts.py \
  src/orion/backend.py \
  src/orion/executor.py \
  src/orion/validation.py \
  src/orion/fake_backend.py \
  src/orion/ollama_backend.py \
  src/orion/transformation_contracts.py \
  src/orion/transformation_engine.py \
  docs/development/PHASE_4A_CLOSEOUT.md
```

Repository candidate inventory and staged review:

```bash
git ls-files --cached --others --exclude-standard
git status --short --ignored
git diff --cached --check
git diff --cached --stat
git diff --cached --name-status
git diff --cached
```

The opt-in integration remains separate:

```bash
make integration
```

It must be run only when the externally managed Ollama runtime is intentionally
available. This closeout does not require or invoke it.
