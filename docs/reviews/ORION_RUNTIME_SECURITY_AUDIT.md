# ORION Version 1.1 — Runtime Security Audit

Audit date: 2026-07-24

## Security decision

**ACCEPT WITH CONDITIONS**

The authenticated happy path does not disclose Human source content through
normal logs or error bodies. However, worker isolation and release identity
are not trustworthy enough for integration.

## Threat boundary

The audit assumes:

- NEXAHEDRON is the only intended service consumer;
- the Runtime is not exposed directly to browsers;
- the Runtime still has to reject malformed or hostile authenticated input;
- the frozen Core is trusted only after its exact release identity has been
  proven;
- worker isolation must remain effective even if a Core failure takes an
  unexpected path.

## Critical findings

### S-01 — Application-level network denial is bypassable

The worker's socket substitution blocks common TCP connection paths but leaves
UDP `sendto` operational. A local adversarial test transmitted 13 bytes from a
worker child after network denial was activated.

The same mechanism also does not establish an operating-system security
boundary against inherited descriptors, subprocesses, native extensions, or
alternate syscalls.

Security effect:

- the worker can communicate outside its declared authority;
- the worker can potentially reach the parent Runtime or internal proxy;
- an internal Docker network is not equivalent to zero network access.

This violates a mandatory Operational Boundary requirement.

### S-02 — Deployed source identity can be spoofed

The container supplies the expected Core commit through an environment
variable. Runtime startup treats that value as the observed commit. The image
does not contain Git metadata, and the fingerprint excludes the invoked
Slice II–IV source files and Runtime files.

Security effect:

A modified image can claim the certified release identity without containing
the certified implementation. This is a supply-chain integrity failure, not a
cosmetic metadata issue.

### S-03 — Mandatory canary is operator-bypassable

The canary is part of the frozen readiness contract, but a normal environment
variable disables it while leaving the service ready.

Security effect:

Misconfiguration or unauthorized configuration change can remove the only
startup execution proof without creating a readiness failure.

## High findings

### S-04 — Cross-artifact references lack independent Gateway verification

The Gateway verifies each artifact in isolation. It cannot prove that
cross-artifact references resolve to the exact earlier entries in the supplied
manifest.

Security effect:

The process boundary is trusted for a property that the frozen contract
assigns to the Gateway. A compromised or defective worker can return a
self-consistent set of individually serializable artifacts without the
required independently verified graph.

### S-05 — HTTP concurrency exists before authenticated admission

`ThreadingHTTPServer` creates unbounded handler threads before authentication
and rate/concurrency admission. The five-second socket timeout reduces but
does not eliminate connection-exhaustion exposure.

The Runtime is documented as reverse-proxy-only, but no source restriction is
enforced by the Runtime itself.

### S-06 — Ambiguous critical HTTP headers are not rejected

Duplicate `Authorization`, `Content-Length`, `Content-Type`, `Accept`,
`Content-Encoding`, and version headers are not explicitly rejected.
Interpretation may differ between reverse proxy and Python's header parser.

Security effect:

This creates avoidable request-confusion risk at a security boundary.

## Medium findings

### S-07 — Authentication configuration permits ambiguous consumer identity

The credential map permits:

- duplicate secret values for different consumers;
- unbounded consumer identifiers;
- arbitrarily short secrets.

Because the first matching secret determines the logged consumer and
rate-limit bucket, duplicate values make operational identity depend on map
order.

### S-08 — Unsupported-method responses disclose implementation metadata

Inherited `http.server` behavior returns HTML and the Runtime server banner for
unsupported methods. This does not expose source content, but it violates the
otherwise narrow and canonical response surface.

### S-09 — Aggregate resource exhaustion is not fully bounded

- temporary storage is not bounded per invocation;
- handler threads are not bounded;
- profile limits are checked after expensive Core stages;
- unauthenticated failures are not source-rate-limited.

Together these leave denial-of-service paths outside the two-worker Core
concurrency limit.

## Controls that passed

- Bearer values are compared with `hmac.compare_digest`.
- Authorization values are not logged.
- Request and response bodies are not logged.
- Operational Execution IDs are syntax-bounded before entering headers or
  logs.
- Error bodies contain stable codes rather than exception messages or stack
  traces.
- Worker stderr is not published.
- Strict JSON rejects duplicate object keys, floats, invalid constants, BOM,
  and invalid UTF-8.
- Confirmed source integrity is recomputed from exact UTF-8 bytes.
- No CORS allowance is emitted.
- Runtime results use `Cache-Control: no-store`.
- Runtime JSON responses use `X-Content-Type-Options: nosniff`.
- No artifact retrieval or anonymous manifest endpoint exists.

## Credential and privacy assessment

The repository contains only a placeholder credential. Runtime logging is
content-free on inspected paths.

Production compliance still depends on external controls that are not
verifiable here:

- secret injection and file permissions;
- credential revocation and overlap rotation;
- log retention no longer than 30 days;
- deletion procedures;
- reverse-proxy access restrictions;
- TLS configuration;
- source-IP admission controls.

## Required security conditions before integration

1. Worker network isolation must be enforced by a boundary that passes
   adversarial TCP, UDP, DNS, subprocess, and inherited-descriptor tests.
2. Runtime startup must prove the actual deployed Runtime and Core release,
   not a caller-supplied assertion.
3. Mandatory startup verification must not be bypassable in a releasable
   configuration.
4. Gateway manifest verification must prove the complete cross-artifact
   reference graph.
5. Critical duplicate headers and unsupported methods must have one
   deterministic rejection behavior.
6. Pre-authentication connection and thread exhaustion must be bounded at the
   deployed boundary.

## Conclusion

No evidence of semantic authority migration, credential logging, path
traversal, or artifact-body disclosure was found. The current isolation and
release-attestation failures are nevertheless sufficient to block
integration.
