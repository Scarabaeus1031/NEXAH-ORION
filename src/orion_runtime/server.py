"""Minimal stateless HTTP Runtime for ORION Version 1.1."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
import hmac
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import logging
import os
import re
import signal
import socket
import threading
import time
from typing import Any
from uuid import uuid4

from .canonical import CanonicalJSONError, canonical_bytes, parse_json_bytes
from .constants import (
    API_VERSION,
    CORE_FINGERPRINT,
    CORE_VERSION,
    MAX_HEADER_BYTES,
    MAX_HEADERS,
    MAX_REQUEST_BYTES,
    MEDIA_TYPE,
    RUNTIME_VERSION,
    TOTAL_REQUEST_SECONDS,
)
from .errors import RuntimeBoundaryError
from .fixtures import canary_envelope
from .gateway import Gateway
from .release import verify_release


LOG = logging.getLogger("orion.runtime")
EXECUTION_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,63}$")


@dataclass(frozen=True, slots=True)
class RuntimeConfig:
    host: str
    port: int
    credentials: dict[str, str]

    @classmethod
    def from_environment(cls) -> "RuntimeConfig":
        raw = os.environ.get("ORION_SERVICE_CREDENTIALS_JSON", "")
        try:
            parsed = json.loads(raw) if raw else {}
        except json.JSONDecodeError as exc:
            raise ValueError("ORION_SERVICE_CREDENTIALS_JSON is invalid") from exc
        if not isinstance(parsed, dict) or any(
            not isinstance(name, str)
            or not name
            or not isinstance(secret, str)
            or not secret
            for name, secret in parsed.items()
        ):
            raise ValueError("service credentials must map consumer IDs to secrets")
        return cls(
            host=os.environ.get("ORION_BIND_HOST", "127.0.0.1"),
            port=int(os.environ.get("ORION_PORT", "8080")),
            credentials=dict(parsed),
        )


class TokenBucket:
    def __init__(self, capacity: float, refill_per_second: float) -> None:
        self.capacity = capacity
        self.refill = refill_per_second
        self.tokens = capacity
        self.updated = time.monotonic()

    def take(self) -> bool:
        now = time.monotonic()
        self.tokens = min(
            self.capacity,
            self.tokens + (now - self.updated) * self.refill,
        )
        self.updated = now
        if self.tokens < 1:
            return False
        self.tokens -= 1
        return True


class RuntimeState:
    def __init__(self, config: RuntimeConfig, gateway: Gateway | None = None) -> None:
        self.config = config
        self.gateway = gateway or Gateway()
        self.ready = False
        self.shutting_down = False
        self.readiness_errors: tuple[str, ...] = ()
        self._lock = threading.Lock()
        self._buckets: dict[str, TokenBucket] = {}
        self._attempts: dict[str, deque[float]] = defaultdict(deque)
        self._active: dict[str, int] = defaultdict(int)
        self._health: dict[str, deque[float]] = defaultdict(deque)

    def verify_startup(self) -> None:
        errors = list(verify_release()[1])
        if not self.config.credentials:
            errors.append("service_credentials_missing")
        if not errors:
            try:
                first = self.gateway.execute(canary_envelope())
                second = self.gateway.execute(canary_envelope())
                if canonical_bytes(first.body) != canonical_bytes(second.body):
                    errors.append("startup_canary_replay_mismatch")
            except Exception:
                errors.append("startup_canary_failed")
        self.readiness_errors = tuple(errors)
        self.ready = not errors

    def shutdown_workers(self) -> None:
        self.gateway.shutdown()

    def authenticate(self, authorization: str | None) -> str | None:
        if not authorization or not authorization.startswith("Bearer "):
            return None
        supplied = authorization[7:]
        for consumer, secret in self.config.credentials.items():
            if hmac.compare_digest(supplied, secret):
                return consumer
        return None

    def admit(self, consumer: str) -> None:
        with self._lock:
            now = time.monotonic()
            attempts = self._attempts[consumer]
            while attempts and attempts[0] <= now - 60:
                attempts.popleft()
            if len(attempts) >= 30:
                raise RuntimeBoundaryError(
                    status=429,
                    category="rate_limit",
                    code="capacity_limited",
                    retry="safe",
                    retry_after=2,
                )
            attempts.append(now)
            bucket = self._buckets.setdefault(
                consumer,
                TokenBucket(capacity=5, refill_per_second=0.5),
            )
            if not bucket.take() or self._active[consumer] >= 2:
                raise RuntimeBoundaryError(
                    status=429,
                    category="rate_limit",
                    code="capacity_limited",
                    retry="safe",
                    retry_after=2,
                )
            self._active[consumer] += 1

    def release(self, consumer: str) -> None:
        with self._lock:
            self._active[consumer] = max(0, self._active[consumer] - 1)

    def admit_health(self, address: str) -> bool:
        now = time.monotonic()
        with self._lock:
            values = self._health[address]
            while values and values[0] <= now - 60:
                values.popleft()
            if len(values) >= 60:
                return False
            values.append(now)
            return True


class OrionHTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, address: tuple[str, int], state: RuntimeState) -> None:
        self.state = state
        super().__init__(address, OrionRequestHandler)


class OrionRequestHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "ORION-Runtime/1.1"
    sys_version = ""

    @property
    def state(self) -> RuntimeState:
        return self.server.state  # type: ignore[attr-defined,no-any-return]

    def setup(self) -> None:
        super().setup()
        self.request_started = time.monotonic()
        self.connection.settimeout(5)

    def log_message(self, format: str, *args: object) -> None:
        return

    def do_GET(self) -> None:
        if self.path != "/health":
            self._plain_error(404)
            return
        if not self.state.admit_health(self.client_address[0]):
            self._runtime_error(
                RuntimeBoundaryError(
                    status=429,
                    category="rate_limit",
                    code="capacity_limited",
                    retry="safe",
                    retry_after=1,
                ),
                str(uuid4()),
            )
            return
        status = 200 if self.state.ready and not self.state.shutting_down else 503
        body = {
            "status": "ready" if status == 200 else "not_ready",
            "runtime_version": RUNTIME_VERSION,
            "api_version": API_VERSION,
            "core_version": CORE_VERSION,
            "core_fingerprint": CORE_FINGERPRINT,
        }
        self._send_json(status, body, execution_id=None)

    def do_POST(self) -> None:
        execution_id = self.headers.get("ORION-Execution-ID") or str(uuid4())
        if not EXECUTION_ID.fullmatch(execution_id):
            self._runtime_error(
                RuntimeBoundaryError(
                    status=400,
                    category="transport",
                    code="execution_id_invalid",
                ),
                str(uuid4()),
            )
            return
        started = self.request_started
        consumer = ""
        try:
            self._validate_transport()
            consumer = self.state.authenticate(self.headers.get("Authorization")) or ""
            if not consumer:
                raise RuntimeBoundaryError(
                    status=401,
                    category="authentication",
                    code="service_credential_invalid",
                )
            if not self.state.ready or self.state.shutting_down:
                raise RuntimeBoundaryError(
                    status=503,
                    category="runtime_unavailable",
                    code="core_worker_unavailable",
                    retry="safe",
                    retry_after=1,
                )
            self.state.admit(consumer)
            try:
                remaining = self._remaining()
                self.connection.settimeout(min(10, remaining))
                body = self._read_body()
                parsed = parse_json_bytes(body)
                result = self.state.gateway.execute(
                    parsed,
                    worker_timeout=min(15, self._remaining()),
                )
            finally:
                self.state.release(consumer)
            if self.state.shutting_down:
                raise RuntimeBoundaryError(
                    status=503,
                    category="runtime_unavailable",
                    code="core_worker_unavailable",
                    retry="safe",
                    retry_after=1,
                )
            self.connection.settimeout(self._remaining())
            self._send_json(200, result.body, execution_id=execution_id)
            self._log(
                execution_id,
                consumer,
                200,
                "complete",
                len(body),
                started,
            )
        except CanonicalJSONError:
            error = RuntimeBoundaryError(
                status=400,
                category="transport",
                code="malformed_json",
            )
            self._runtime_error(error, execution_id)
            self._log(execution_id, consumer, error.status, error.code, 0, started)
        except RuntimeBoundaryError as error:
            self._runtime_error(error, execution_id)
            self._log(execution_id, consumer, error.status, error.code, 0, started)
        except (BrokenPipeError, ConnectionResetError, socket.timeout):
            self._log(execution_id, consumer, 500, "client_disconnected", 0, started)
        except Exception:
            error = RuntimeBoundaryError(
                status=500,
                category="runtime_unavailable",
                code="runtime_internal_failure",
                retry="manual_review",
            )
            self._runtime_error(error, execution_id)
            self._log(execution_id, consumer, error.status, error.code, 0, started)

    def do_PUT(self) -> None:
        self._method_not_allowed()

    def do_PATCH(self) -> None:
        self._method_not_allowed()

    def do_DELETE(self) -> None:
        self._method_not_allowed()

    def do_OPTIONS(self) -> None:
        self._method_not_allowed()

    def _method_not_allowed(self) -> None:
        self._runtime_error(
            RuntimeBoundaryError(
                status=405,
                category="transport",
                code="method_not_allowed",
            ),
            str(uuid4()),
        )

    def _validate_transport(self) -> None:
        if self.path != "/orientation/v1/requests":
            raise RuntimeBoundaryError(
                status=404,
                category="transport",
                code="endpoint_not_found",
            )
        if len(self.headers) > MAX_HEADERS:
            raise RuntimeBoundaryError(
                status=431,
                category="transport",
                code="request_headers_too_large",
            )
        header_bytes = sum(
            len(name.encode("utf-8")) + len(value.encode("utf-8")) + 4
            for name, value in self.headers.items()
        )
        if header_bytes > MAX_HEADER_BYTES:
            raise RuntimeBoundaryError(
                status=431,
                category="transport",
                code="request_headers_too_large",
            )
        if self.headers.get("Content-Encoding", "identity").lower() != "identity":
            raise RuntimeBoundaryError(
                status=415,
                category="transport",
                code="content_encoding_unsupported",
            )
        if self.headers.get("Transfer-Encoding"):
            raise RuntimeBoundaryError(
                status=415,
                category="transport",
                code="transfer_encoding_unsupported",
            )
        if self.headers.get("Content-Type") != MEDIA_TYPE:
            raise RuntimeBoundaryError(
                status=415,
                category="transport",
                code="content_type_unsupported",
            )
        if self.headers.get("Accept") != MEDIA_TYPE:
            raise RuntimeBoundaryError(
                status=406,
                category="transport",
                code="accept_unsupported",
            )
        if self.headers.get("ORION-API-Version") != API_VERSION:
            raise RuntimeBoundaryError(
                status=400,
                category="version",
                code="api_version_unsupported",
            )
        for name in (
            "Authorization",
            "Content-Length",
            "Content-Type",
            "Accept",
            "ORION-API-Version",
            "ORION-Execution-ID",
        ):
            if len(self.headers.get_all(name, [])) > 1:
                raise RuntimeBoundaryError(
                    status=400,
                    category="transport",
                    code="duplicate_header",
                    detail_refs=(name.lower(),),
                )

    def _remaining(self) -> float:
        remaining = TOTAL_REQUEST_SECONDS - (time.monotonic() - self.request_started)
        if remaining <= 0:
            raise RuntimeBoundaryError(
                status=504,
                category="timeout",
                code="core_timeout",
                retry="safe",
                retry_after=1,
            )
        return remaining

    def _read_body(self) -> bytes:
        raw_length = self.headers.get("Content-Length")
        try:
            length = int(raw_length or "")
        except ValueError as exc:
            raise RuntimeBoundaryError(
                status=400,
                category="transport",
                code="content_length_invalid",
            ) from exc
        if length < 0:
            raise RuntimeBoundaryError(
                status=400,
                category="transport",
                code="content_length_invalid",
            )
        if length > MAX_REQUEST_BYTES:
            raise RuntimeBoundaryError(
                status=413,
                category="transport",
                code="request_body_too_large",
            )
        body = self.rfile.read(length)
        if len(body) != length:
            raise RuntimeBoundaryError(
                status=400,
                category="transport",
                code="request_body_incomplete",
            )
        return body

    def _runtime_error(self, error: RuntimeBoundaryError, execution_id: str) -> None:
        self.close_connection = True
        body = {
            "api_version": API_VERSION,
            "runtime_version": RUNTIME_VERSION,
            "execution_id": execution_id,
            "error": {
                "category": error.category,
                "code": error.code,
                "retry": error.retry,
                "detail_refs": list(error.detail_refs),
            },
        }
        headers = {}
        headers["Connection"] = "close"
        if error.retry_after is not None:
            headers["Retry-After"] = str(error.retry_after)
        self._send_json(
            error.status,
            body,
            execution_id=execution_id,
            extra_headers=headers,
        )

    def _send_json(
        self,
        status: int,
        body: object,
        *,
        execution_id: str | None,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        encoded = canonical_bytes(body)
        self.send_response(status)
        self.send_header("Content-Type", MEDIA_TYPE)
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("ORION-API-Version", API_VERSION)
        self.send_header("ORION-Runtime-Version", RUNTIME_VERSION)
        self.send_header("ORION-Core-Version", CORE_VERSION)
        self.send_header("ORION-Core-Fingerprint", CORE_FINGERPRINT)
        if execution_id:
            self.send_header("ORION-Execution-ID", execution_id)
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        for name, value in (extra_headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(encoded)

    def _plain_error(self, status: int) -> None:
        body = canonical_bytes({"status": HTTPStatus(status).phrase.lower()})
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    @staticmethod
    def _log(
        execution_id: str,
        consumer: str,
        status: int,
        code: str,
        request_bytes: int,
        started: float,
    ) -> None:
        LOG.info(
            json.dumps(
                {
                    "execution_id": execution_id,
                    "consumer": consumer or "unavailable",
                    "api_version": API_VERSION,
                    "runtime_version": RUNTIME_VERSION,
                    "core_fingerprint": CORE_FINGERPRINT,
                    "request_bytes": request_bytes,
                    "status": status,
                    "code": code,
                    "duration_ms": int((time.monotonic() - started) * 1000),
                },
                separators=(",", ":"),
                sort_keys=True,
            )
        )


def serve(config: RuntimeConfig | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    resolved = config or RuntimeConfig.from_environment()
    state = RuntimeState(resolved)
    state.verify_startup()
    server = OrionHTTPServer((resolved.host, resolved.port), state)

    def stop(_signum: int, _frame: object) -> None:
        state.shutting_down = True
        state.ready = False
        state.shutdown_workers()
        threading.Thread(target=server.shutdown, daemon=True).start()

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    LOG.info(
        json.dumps(
            {
                "event": "runtime_started",
                "ready": state.ready,
                "host": resolved.host,
                "port": server.server_address[1],
                "runtime_version": RUNTIME_VERSION,
                "api_version": API_VERSION,
                "core_fingerprint": CORE_FINGERPRINT,
            },
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    try:
        server.serve_forever(poll_interval=0.25)
    finally:
        state.shutting_down = True
        state.ready = False
        state.shutdown_workers()
        server.server_close()
    return 0
