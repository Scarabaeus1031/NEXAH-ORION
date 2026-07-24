# Security Policy

## Current support status

ORION Version `1.0.0` certifies the bounded responsibilities named by the
canonical Version 1 baseline. It does not certify Runtime, Gateway, deployment,
network service operation, or a production-support SLA.

## Reporting a vulnerability

Report suspected security issues privately to
[`contact@nexah.de`](mailto:contact@nexah.de). Do not publish credentials,
private source material, model outputs containing sensitive data or exploit
details in an issue.

Include the affected revision, reproduction steps, expected boundary and
potential impact. State whether the issue concerns:

- deterministic ORION behavior;
- the Ollama loopback adapter;
- generated or local workspace material; or
- an external runtime.

Ollama is externally managed. ORION never starts, stops or updates that
runtime. Issues owned by NEXAH Framework, Library, Builder Hub or an external
provider are routed to their canonical owner.

No bounty, response-time guarantee or stable production support commitment is
implied by this development policy.
