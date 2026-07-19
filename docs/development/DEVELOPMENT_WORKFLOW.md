# Development Workflow

## 1. Route the work

Before opening a branch, identify:

- the responsible repository;
- the owning module or document;
- whether the change is local, architectural, cross-repository, canonical, or externally effective;
- the strongest authority touched by the change.

If ownership is unclear, stop and resolve ownership. Do not prototype inside a production module to discover where the work belongs.

## 2. Choose the work lane

```text
question or source
  ├── research lane      .workspace/research
  ├── experiment lane    .workspace/experiments
  ├── decision lane      docs/adr
  ├── documentation lane docs
  ├── contract lane      schemas (after approval)
  ├── implementation     src (after approval)
  └── release lane       docs/releases + tag
```

Research and experiments do not gain product status automatically. Promotion requires a pull request into the owning tracked location.

## 3. Branch

Create a short-lived branch from an up-to-date `main`. Use the prefixes in `CONTRIBUTING.md`. One branch should address one ownership concern.

## 4. Decide before implementing

An ADR is required when a change affects:

- authority or repository ownership;
- a stable public contract;
- cross-repository dependency direction;
- persistence, provenance, security, or effect policy;
- release compatibility;
- a previously accepted ADR.

Use:

```bash
./scripts/new-adr "Decision title"
```

Implementation waits while the ADR is `Proposed`.

## 5. Develop and verify

At Phase 1B, default verification covers the workshop, bounded offline execution,
and isolated Ollama adapter behavior:

```bash
./scripts/check-workspace
./scripts/test
```

The default check remains independent of external model runtimes, provider SDKs,
networking, and sibling repository availability. The explicit local integration
gate is:

```bash
make integration
```

## 6. Review

Reviewers assess in this order:

1. ownership;
2. authority and effects;
3. contract and compatibility impact;
4. evidence;
5. implementation detail;
6. documentation and release impact.

Cross-repository changes require acknowledgment from every affected owner. A PR in ORION cannot silently approve a Core or Library contract change.

## 7. Merge

- Use a reviewed pull request.
- Preserve ADR history.
- Update `CHANGELOG.md` for user-, contributor-, contract-, or governance-visible changes.
- Update compatibility records when an external revision or contract changes.
- Keep `main` releasable according to its current development status.

## 8. Release

Follow [`docs/releases/RELEASE_STRATEGY.md`](../releases/RELEASE_STRATEGY.md). A repository release does not imply Core, Library, Builder Hub, or model-runtime release.
