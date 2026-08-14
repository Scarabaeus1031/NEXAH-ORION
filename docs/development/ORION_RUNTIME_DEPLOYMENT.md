# ORION Version 1.1 — Runtime Deployment

Status: Stage 1 implementation guidance

## Service boundary

The ORION Runtime is a versioned deterministic Orientation Runtime. It is not
an AI service, assistant, reasoning engine, or semantic layer.

The service exposes exactly:

- `GET /health`
- `POST /orientation/v1/requests`

It binds to loopback by default. HTTPS terminates at a separately managed
reverse proxy. The Runtime must not be exposed directly to the public network.

## Required platform

- Linux
- Python 3.10 or newer
- one non-root service identity
- read-only release files
- bounded temporary storage
- HTTPS reverse proxy
- external secret storage or a root-readable environment file

The production target is Linux. macOS is supported for local verification but
does not enforce the Linux worker address-space limit.

## Configuration

| Variable | Required | Default | Purpose |
|---|---:|---|---|
| `ORION_SERVICE_CREDENTIALS_JSON` | yes | none | JSON map of consumer IDs to rotatable bearer secrets |
| `ORION_BIND_HOST` | no | `127.0.0.1` | HTTP listen address |
| `ORION_PORT` | no | `8080` | HTTP listen port |
| `ORION_STARTUP_CANARY` | no | `true` | Require two byte-identical isolated startup executions |
| `ORION_CORE_COMMIT` | container | frozen commit | Immutable release binding used in the image |

Secrets must never enter the repository, container image, command line, URL,
request body, log, or Core input.

## Docker image

Build from the frozen release checkout:

```text
docker build \
  --build-arg ORION_CORE_COMMIT=d34fbb2f99334534f4db89465a29f8bdb16d14d3 \
  -t orion-runtime:1.1.0 .
```

Create an internal Docker network shared only with the HTTPS reverse proxy:

```text
docker network create --internal orion-runtime
```

Run with a read-only filesystem and the frozen resource profile:

```text
docker run -d \
  --name orion-runtime \
  --network orion-runtime \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --memory 1536m \
  --pids-limit 32 \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --env-file /etc/orion/runtime.env \
  --restart unless-stopped \
  orion-runtime:1.1.0
```

The reverse proxy must join the same internal network, publish HTTPS, enforce
the header/body timeouts in the Operational Boundary Contract, and forward no
other path.

## Linux service

Install the immutable release at `/opt/orion/releases/1.1.0`, make it
root-owned and read-only, and atomically point `/opt/orion/current` to it.

Install:

- `deploy/orion-runtime.service` as
  `/etc/systemd/system/orion-runtime.service`;
- `deploy/runtime.env.example` as `/etc/orion/runtime.env`;
- replace the example credential;
- set `/etc/orion/runtime.env` to owner `root`, mode `0600`.

Then:

```text
systemctl daemon-reload
systemctl enable --now orion-runtime
systemctl status orion-runtime
```

The reverse proxy forwards only the two defined endpoints to
`127.0.0.1:8080`.

## Readiness

The process becomes ready only after:

1. the frozen Core commit binding is verified;
2. the canonical V1 fingerprint is reproduced;
3. service credentials are present;
4. the full canary chain executes twice in separate workers;
5. both canonical success responses are byte-identical.

`GET /health` returns `503` while any condition is false or shutdown has
begun.

## Logging

Logs are canonical operational metadata written to standard output or the
system journal. They contain no request bodies, source text, artifact bodies,
authorization values, Human annotations, or clarification content.

Operational retention is limited to 30 days.

## Upgrade

1. Build a new immutable image or release directory.
2. Verify its image digest or file manifest.
3. Start it without public traffic.
4. require `/health` to return `200`;
5. run the authenticated Stage 1 proof;
6. switch the reverse proxy;
7. retain the prior release until acceptance.

No in-place source edit is permitted.

## Rollback

Restore the previous verified image digest or `/opt/orion/current` symlink,
restart the service, and require readiness before restoring traffic.

Runtime is stateless. There is no session recovery, artifact database, or
Human payload backup.

## Current deployment boundary

The implementation enforces process separation, CPU and file limits, Linux
address-space limits, kill-on-timeout, response limits, and an application
network-denial guard in every worker.

For public deployment, the container or host must additionally deny external
egress at the network boundary. The recommended internal Docker network
provides that deployment control. This requirement must be verified on the
target Linux host before public exposure.
