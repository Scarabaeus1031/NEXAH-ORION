# ORION Version 1 RC1 Checklist

- Candidate: ORION Version 1 RC1
- Contract Suite: 1.0
- Implemented Operator: Understand 1.0
- Release status: candidate verification complete; external Core synchronization pending

## Clean checkout and prerequisites

- [x] Clean candidate snapshot can be constructed from the reviewed repository content.
- [x] Git is available.
- [x] Python 3.10 or newer is available.
- [x] POSIX shell and standard Unix tools are available.
- [x] `rsvg-convert` is available for Architecture Plate verification.
- [ ] Exact pinned NEXAH Core is connected in the current workspace.
- [x] Exact pinned NEXAH Core was verified in an isolated clean candidate.

The current connected Core is `64d1c817f7661e518dcc217bd56f34d272807372`;
the required revision is
`9f79bb06210402c40c9ef7d9937ca00d86c092b1`.

## Install

- [x] No third-party Python runtime dependencies are declared.
- [x] Tests and evaluation run directly from a checkout through `PYTHONPATH=src`.
- [x] Optional editable package installation is documented and reproducible
  when the declared `setuptools>=61` build backend is installed:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install "setuptools>=61"
python3 -m pip install --no-build-isolation -e .
```

Installing the build backend may require package-index access. Package
installation is not required to run the canonical verification scripts.

## Verification commands

- [x] Test suite

  ```sh
  ./scripts/test
  ```

  Expected: `Ran 128 tests`, `OK (skipped=1)`, then
  `ORION isolated test suite passed.` The skip is the opt-in Ollama integration.

- [x] Phase VI live journey

  ```sh
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
    python3 scripts/phase_vi_live_orientation.py > phase-vi.json
  ```

  Expected: one JSON trace containing request, validated request, runtime
  outcome, evidence, Orientation Report, Continuation Option and presentation;
  report status `complete`.

- [x] Phase VII evaluation

  ```sh
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
    python3 scripts/phase_vii_real_world_evaluation.py > phase-vii.json
  ```

  Expected: corpus `1.0.1`, 12 sessions, completion rate `1.0`, evidence
  coverage rate `1.0`, continuation usefulness rate `1.0`.

- [x] Architecture consistency and boundary checks

  ```sh
  ./scripts/check-boundaries
  ./scripts/check-architecture-plates
  ```

  Expected: 15 graph edges verified; frozen responsibility boundaries pass;
  10 SVG/PNG Architecture Plate pairs pass.

- [ ] Complete workspace check in the current connected workspace

  ```sh
  ./scripts/check-workspace
  ./scripts/release-check --development
  ```

  Expected after Core synchronization: both commands pass. Current expected
  result: all local checks pass, followed by exactly one Core revision mismatch.

## Known limitations

- [x] Understand is the only implemented Orientation Operator.
- [x] No provider, transport, persistence, authentication, streaming or sessions.
- [x] No Runtime implementation for the other six specified modes.
- [x] No LUCY Runtime, reflection authority, transition mathematics or renderers.
- [x] Evaluation demonstrates the versioned repository corpus, not universal
  document understanding or a Human user study.

## Publication controls

- [x] Version 1 release notes, audit, classification and certification exist.
- [x] Internal Markdown references resolve.
- [x] Historical release and architecture records are marked historical.
- [ ] External Core dependency is synchronized or explicitly approved.
- [ ] Reviewed RC1 content is committed as an immutable release revision.
- [ ] Release metadata/tag is applied through the release process.

## Checklist decision

The RC1 candidate passes every repository-owned reproducibility item. The only
verification failure is the already-known external Core checkout mismatch.
Commit and tag operations are publication actions after RC1 acceptance, not
changes to the candidate behavior.
