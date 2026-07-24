# ORION Version 1 RC1 Reproducibility Report

## Audit result

A clean source snapshot can reproduce the isolated test suite, Phase VI live
journey, Phase VII corpus evaluation, architecture consistency checks,
responsibility-boundary checks and Architecture Plate verification without a
provider, network service, database or model runtime.

The complete workspace/release check additionally requires the exact external
NEXAH Core revision declared in `workspace.yaml`.

## Prerequisites

| Requirement | Minimum or purpose | Audited environment |
|---|---|---|
| Git | checkout, revision and clean-tree verification | system Git |
| Python | 3.10 or newer | CPython 3.12.7 |
| Build backend | `setuptools>=61`, only for package installation | system build backend used in isolated audit |
| POSIX shell | repository scripts | Bash on macOS |
| Unix tools | `awk`, `grep`, `find`, `od`, `tr`, `wc`, `shasum`, `mktemp` | macOS system tools |
| librsvg | `rsvg-convert` for SVG renderability | available via Homebrew path |
| NEXAH Core | only for complete workspace/release gate | exact pin currently not connected |

No third-party Python runtime dependency, model weight, provider credential or
running service is required. A fresh virtual environment may need package-index
access to install the declared build backend before editable installation. The
Ollama integration is optional and skipped by the isolated suite.

## Platform support

- macOS on ARM64: verified directly;
- Linux on x86_64 or ARM64: intended POSIX target when Python 3.10+, the named
  Unix tools, `shasum` and librsvg are installed; not independently exercised
  during RC1;
- Windows: use WSL or another POSIX-compatible environment; native PowerShell
  execution is not certified by RC1.

## Reproduction sequence

```sh
git clone https://github.com/Scarabaeus1031/NEXAH-ORION.git
cd NEXAH-ORION
./scripts/bootstrap-workspace
./scripts/test
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 scripts/phase_vi_live_orientation.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 scripts/phase_vii_real_world_evaluation.py
./scripts/check-boundaries
./scripts/check-architecture-plates
```

To verify the complete external compatibility gate:

```sh
./scripts/bootstrap-workspace --clone-core
./scripts/check-workspace
./scripts/release-check --development
```

`--clone-core` requires network access to the configured Core remote. An
existing clean checkout at the exact revision may instead be connected with
`--core-path`.

## Observed results

| Verification | Result |
|---|---|
| isolated tests | 128 passed, 1 optional integration skipped |
| Phase VI | complete report and available continuation |
| Phase VII | 12/12 complete; evidence and continuation metrics 1.0 |
| architecture consistency | 15 edges/contracts/registries verified |
| responsibility boundaries | passed |
| Architecture Plates | 10 source/artifact pairs passed |
| isolated clean candidate with exact Core pin | complete development release gate passed |
| current connected workspace | stopped only at external Core revision comparison |

## Reproducibility identifiers

| Identifier | Value |
|---|---|
| Audited repository base revision | `ff9a94ac9f5a566b99c33f19ce3208055b4923c1` |
| RC1 canonical-content fingerprint | `b94c47adfda9d33a3d367718a56c63aca6b7250b78fa5ad57bb2b64c903f9c0b` |
| Architecture | `orion-architecture-v1` |
| Orientation Policies/Operators | `orion.orientation-operators/1.0` |
| Public Contract Suite | `1.0` |
| Understand operator/payload | `1.0` |
| Evaluation corpus | `orion-real-world-understand-corpus@1.0.1` |
| Repository package metadata | `0.3.0-dev.0` (unchanged for RC preparation) |
| Required Core pin | `9f79bb06210402c40c9ef7d9937ca00d86c092b1` |
| Audited Python | `CPython 3.12.7` |
| Audited platform | `macOS 26.5.2, Darwin arm64` |

The canonical-content fingerprint is the SHA-256 of the sorted SHA-256 manifest
for: the six contract specifications; Orientation Policies and Operators;
`public_contracts`, `orientation_runtime` and `gateway` Python sources; the
Phase VII corpus manifest; `workspace.yaml`; and `VERSION`. It identifies the
reviewed behavior-bearing candidate independently of uncommitted release prose.

The isolated proof applied the complete reviewed candidate to a temporary clone,
committed it only inside that disposable clone to obtain a clean tree, installed
it into a fresh virtual environment, cloned the locally available Core history,
checked out the exact declared pin and ran the complete development Release
Gate. The temporary audit commit is not a publication revision and is therefore
not used as a canonical identifier.

## External dependency finding

The connected Core is
`64d1c817f7661e518dcc217bd56f34d272807372`, not the required pin. The exact-pin
guard correctly rejects it. No check was weakened and no compatibility claim
was inferred from the newer checkout.
