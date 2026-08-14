# ORION Version 1.1 — Runtime Implementation Report

Status: **READY FOR TARGET-LINUX VERIFICATION**

## Scope

The Runtime remains an operational boundary around the unchanged ORION
Version 1 Core. It owns HTTP admission, authentication, rate limits, worker
lifecycle, contract validation, manifest observation, readiness, logging, and
shutdown. It does not own ORION semantics, artifacts, provenance,
certification, Expression, or Slice logic.

## Audit-closure implementation

The release candidate now includes:

- Linux seccomp filtering that denies TCP, UDP, and Unix-socket syscalls,
  including x86-64 x32 syscall variants, before Core invocation;
- fail-closed architecture checking and a non-production socket guard;
- mandatory release, fingerprint, and two-run byte-identical startup canary
  verification with no disable configuration;
- a content-derived Runtime release manifest independent of environment
  assertions;
- coverage of the complete `src/orion` and `src/orion_runtime` execution set,
  normative Runtime contracts, build inputs, and deployment definitions;
- explicit verification of every top-level frozen cross-artifact reference;
- a 30-second total request deadline and 15-second worker wall/CPU boundaries;
- CPU timeout mapping, aggregate temporary-storage observation, early
  element/relation limits, and stable operational-profile errors;
- active-worker tracking, process-group termination, cleanup, and prevention
  of success publication after shutdown;
- duplicate critical-header and unsupported-method rejection;
- an immutable Python base-image digest;
- a target-Linux verification script covering independent image builds,
  worker isolation, non-root/read-only execution, resource settings,
  authenticated execution, health, and restart.

## Release identity

The frozen Core identity remains:

```text
commit: d34fbb2f99334534f4db89465a29f8bdb16d14d3
fingerprint: 6201362c094530a0a31fa3d80b46c9131011bb8c8d400183271b0da0eb423f8d
```

Runtime readiness additionally verifies
`release/orion-runtime-1.1.0.json`. The release ID is derived from canonical
manifest bytes. Every listed file is checked by byte length and SHA-256.
`ORION_CORE_COMMIT` is ignored and cannot define release identity.

## Verification

Focused Runtime suite:

```text
15 passed
```

Complete repository regression:

```text
Ran 561 tests
OK (skipped=1)
```

Runtime Gate 0 replay and the Slice II, Slice III, and Slice IV certification
proofs all passed. The Runtime replay retained the established 22 artifacts,
digests, terminal certification, and `at_slice_iv_certified` STOP.

No file under `src/orion` changed.

## Remaining limitation

The development host is macOS and has no Docker executable. Consequently the
new Linux seccomp boundary, container controls, reverse proxy, image
reproducibility, restart, and rollback have not been executed on the supported
Linux deployment target. Static definitions and an executable verification
procedure exist, but they are not equivalent to target evidence.

Public deployment remains prohibited until
`make runtime-v1-1-linux-verification` and the reverse-proxy/rollback checks
pass on the release host.
