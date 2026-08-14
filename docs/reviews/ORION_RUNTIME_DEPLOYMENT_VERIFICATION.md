# ORION Version 1.1 — Runtime Deployment Verification

Date: 2026-07-24

## Environment

Verification host:

```text
Operating system: Darwin
Docker executable: unavailable
Supported production target: Linux
```

## Static preparation

| Requirement | Prepared |
|---|---|
| Python base image pinned by OCI index digest | Yes |
| Non-root image user | Yes |
| Runtime release manifest copied into image | Yes |
| Image health check | Yes |
| systemd non-root service | Yes |
| systemd read-only system protection | Yes |
| systemd memory and task limits | Yes |
| reverse-proxy admission configuration | Yes |
| external credential example without canary bypass | Yes |
| automated Linux verification script | Yes |

## Executed locally

- focused Runtime tests: `15 passed`;
- complete regression: `561` tests, `1` existing skip, no failures;
- mandatory startup canary: passed;
- byte-identical Runtime replay: passed;
- artifact manifest and reference graph: passed;
- Runtime timeout and shutdown behavior: passed;
- Slice II, Slice III, and Slice IV proofs: passed;
- frozen Core diff: empty;
- `git diff --check`: passed.

## Required target-Linux command

```text
make runtime-v1-1-linux-verification
```

The command is fail-closed and requires Linux and Docker. It performs:

- two clean builds from the immutable base;
- root-filesystem layer comparison;
- seccomp TCP/UDP/Unix-socket denial inside the image;
- non-root and read-only container inspection;
- bounded memory, process, file, and temporary-storage configuration;
- mandatory readiness;
- authenticated full Slice II–IV request;
- restart and post-restart readiness.

## Not yet verified

The following required production evidence does not exist yet:

- Docker build success on Linux;
- non-root and read-only behavior on the actual target;
- Linux seccomp behavior on the target architecture;
- memory and CPU exhaustion enforcement;
- no surviving process after forced container shutdown;
- reverse-proxy syntax, HTTPS, headers, and timeouts;
- credential injection, rotation, and revocation;
- restart under the selected service manager;
- rollback to the previous immutable image;
- independent image digest capture and release-record binding.

## Deployment verdict

**FAILED — EVIDENCE INCOMPLETE**

No production deployment is authorized until every item above is executed and
recorded on the supported Linux target.
