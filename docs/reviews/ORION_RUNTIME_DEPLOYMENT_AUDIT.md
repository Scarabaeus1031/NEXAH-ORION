# ORION Version 1.1 — Runtime Deployment Audit

Audit date: 2026-07-24

## Deployment decision

The supplied Docker and systemd artifacts are useful deployment drafts. They
are not yet a reproducible or contract-complete production package.

Public deployment status: **Not approved**

NEXAHEDRON integration status: **Blocked by release and isolation conditions**

## Docker audit

### Passed

- non-root service user;
- no application package dependencies;
- explicit Runtime command;
- health check;
- no secrets copied into the image;
- documented read-only container execution;
- documented memory, process, capability, and privilege restrictions;
- bounded shared tmpfs in the documented run command;
- reverse-proxy-only publication model.

### Failed or unproven

#### D-01 — Mutable base image

`python:3.12-slim` is not pinned by immutable image digest. Equal source
checkouts are therefore not guaranteed to produce equal deployment inputs.

#### D-02 — Core commit is supplied, not observed

The build argument is copied into `ORION_CORE_COMMIT`; Runtime then accepts it
as the current commit. Git metadata is excluded. This does not prove which
source was copied into the image.

#### D-03 — No Runtime release manifest

The image does not bind:

- Runtime file identities;
- complete frozen Core file identities;
- image digest;
- supported NEXAHEDRON Gateway version;
- verification evidence.

Operational Boundary Sections 7 and 12 remain unsatisfied.

#### D-04 — Worker network isolation is incomplete

The internal Docker network blocks external routing but still permits
communication among attached containers. It does not give the child worker a
network boundary distinct from the parent Runtime.

#### D-05 — Temporary-storage semantics differ from the contract

One 64 MiB tmpfs is shared by the Runtime and both permitted workers. The
contract defines 64 MiB per invocation. `RLIMIT_FSIZE` does not impose an
aggregate directory quota.

#### D-06 — Target image was not built

Docker is unavailable in the audited environment. Consequently, the
Dockerfile, health check, file ownership, read-only execution, memory
termination, process limit, and actual image contents remain unverified.

## systemd audit

### Passed

- dedicated non-root user and group;
- loopback binding;
- root-owned external environment-file model;
- `NoNewPrivileges`;
- strict filesystem and home protection;
- kernel and control-group protection;
- memory and task limits;
- control-group kill mode;
- restart-on-failure policy;
- finite stop timeout.

### Failed or unproven

#### D-07 — No worker-specific network isolation

The service requires network access for the parent HTTP server and applies no
separate network boundary to worker subprocesses. The Python socket guard is
not sufficient.

#### D-08 — Temporary storage is not quota-bounded

`PrivateTmp=true` isolates the namespace but does not enforce the specified
64 MiB per invocation.

#### D-09 — Python runtime is outside the immutable release

`/usr/bin/python3` is supplied by the host and is not bound by the Runtime
release manifest. An operating-system update can change execution without
changing the ORION release directory.

#### D-10 — Active-worker shutdown is not demonstrated

`KillMode=control-group` is a useful final safety net, but application shutdown
does not track active workers or implement the contract's explicit deadline
and kill sequence. The existing SIGTERM test is idle.

## Reverse proxy and TLS

The deployment guide delegates TLS, path restriction, header/body timeouts,
and public admission to a reverse proxy but provides no verified
configuration.

Before deployment, Operations must demonstrate:

- HTTPS-only publication;
- no direct Runtime exposure;
- only `/health` and `/orientation/v1/requests` forwarded;
- request-header, body, and total deadline enforcement;
- no request buffering or retry behavior that changes the frozen API;
- critical duplicate-header rejection;
- body-size enforcement;
- source-level abuse controls;
- correct propagation of the service credential;
- no credential or body logging.

## Readiness and restart

The `/health` endpoint correctly reflects the in-memory ready and shutdown
flags. Readiness is still noncompliant because:

- mandatory canary execution is optional;
- actual source identity is not proven;
- Runtime release-manifest verification is absent;
- commit/fingerprint are not continuously revalidated.

Restart is stateless on the tested happy path. No recovery store or session
state was found.

## Logging and monitoring

Application logs use bounded structural fields and omit bodies. The deployment
artifacts do not enforce:

- the 30-day maximum retention;
- deletion capability;
- required monitoring for memory termination, response-size distribution,
  saturation, restart count, or fingerprint mismatch.

These remain Operations-owned controls but must be proven before public
deployment.

## Upgrade and rollback

The documented blue/green direction is sound. It cannot yet be executed
normatively because no immutable Runtime release manifest or tested image
digest exists. Compatibility with a NEXAHEDRON Gateway version is also not
bound.

## Deployment conditions

Before any public deployment:

1. create and verify an immutable release binding for Runtime and the complete
   invoked Core;
2. build the container from an immutable base and record its digest;
3. prove mandatory readiness in that exact image;
4. prove operating-system worker network isolation;
5. prove memory, CPU, process, temporary-storage, timeout, and active-shutdown
   behavior on target Linux;
6. verify the reverse-proxy configuration;
7. verify secret rotation and log retention;
8. execute authenticated smoke, deterministic replay, upgrade, and rollback
   tests against the exact deployment artifact.

## Conclusion

The deployment design is directionally minimal and appropriate. Its current
artifacts do not yet satisfy the frozen operational contract or provide a
reproducible production release.
