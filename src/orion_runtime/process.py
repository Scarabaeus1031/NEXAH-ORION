"""Operational lifecycle for one isolated Core worker."""

from __future__ import annotations

import json
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import tempfile
import threading
import time
from typing import Any

from .canonical import canonical_bytes, parse_json_bytes
from .constants import (
    CORE_CPU_SECONDS,
    CORE_TIMEOUT_SECONDS,
    MAX_RESPONSE_BYTES,
    WORKER_MEMORY_BYTES,
    WORKER_OPEN_FILES,
    WORKER_TEMP_BYTES,
)
from .errors import RuntimeBoundaryError


ROOT = Path(__file__).resolve().parents[2]


def _resource_limits() -> None:
    import resource

    limits = [
        (resource.RLIMIT_CPU, (CORE_CPU_SECONDS, CORE_CPU_SECONDS + 1)),
        (resource.RLIMIT_FSIZE, WORKER_TEMP_BYTES),
        (resource.RLIMIT_NOFILE, WORKER_OPEN_FILES),
    ]
    if platform.system() == "Linux":
        limits.append((resource.RLIMIT_AS, WORKER_MEMORY_BYTES))
    for kind, requested in limits:
        _soft_hard_limit(resource, kind, requested)


def _soft_hard_limit(
    resource: Any,
    kind: int,
    requested: int | tuple[int, int],
) -> None:
    _soft, hard = resource.getrlimit(kind)
    soft_requested, hard_requested = (
        requested if isinstance(requested, tuple) else (requested, requested)
    )
    effective_hard = (
        hard_requested if hard == resource.RLIM_INFINITY else min(hard_requested, hard)
    )
    resource.setrlimit(kind, (min(soft_requested, effective_hard), effective_hard))


class WorkerProcess:
    def __init__(self, timeout: float = CORE_TIMEOUT_SECONDS) -> None:
        self.timeout = timeout
        self._lock = threading.Lock()
        self._active: set[subprocess.Popen[bytes]] = set()
        self._closing = False

    def execute(
        self,
        envelope: dict[str, Any],
        *,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        effective_timeout = self.timeout if timeout is None else min(self.timeout, timeout)
        if effective_timeout <= 0:
            raise RuntimeBoundaryError(
                status=504,
                category="timeout",
                code="core_timeout",
                retry="safe",
                retry_after=1,
            )
        input_bytes = canonical_bytes(envelope)
        with tempfile.TemporaryDirectory(prefix="orion-runtime-") as temp_dir:
            env = {
                "PATH": os.environ.get("PATH", ""),
                "PYTHONPATH": str(ROOT / "src"),
                "PYTHONHASHSEED": "0",
                "LANG": "C.UTF-8",
                "LC_ALL": "C.UTF-8",
                "TMPDIR": temp_dir,
            }
            process = subprocess.Popen(
                [sys.executable, "-m", "orion_runtime.worker"],
                cwd=ROOT,
                env=env,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True,
                preexec_fn=_resource_limits if os.name == "posix" else None,
            )
            with self._lock:
                if self._closing:
                    self._terminate(process)
                    process.communicate()
                    raise RuntimeBoundaryError(
                        status=503,
                        category="runtime_unavailable",
                        code="core_worker_unavailable",
                        retry="safe",
                        retry_after=1,
                    )
                self._active.add(process)
            temp_exceeded = threading.Event()
            monitor_stop = threading.Event()
            monitor = threading.Thread(
                target=self._monitor_temp,
                args=(Path(temp_dir), process, temp_exceeded, monitor_stop),
                daemon=True,
            )
            monitor.start()
            try:
                stdout, _stderr = process.communicate(
                    input=input_bytes,
                    timeout=effective_timeout,
                )
            except subprocess.TimeoutExpired:
                self._terminate(process)
                process.communicate()
                raise RuntimeBoundaryError(
                    status=504,
                    category="timeout",
                    code="core_timeout",
                    retry="safe",
                    retry_after=1,
                )
            finally:
                monitor_stop.set()
                monitor.join(timeout=1)
                with self._lock:
                    self._active.discard(process)
            if temp_exceeded.is_set():
                raise RuntimeBoundaryError(
                    status=422,
                    category="output_validation",
                    code="operational_profile_exceeded",
                    detail_refs=("worker_temporary_storage",),
                )
            if process.returncode == -getattr(signal, "SIGXCPU", signal.SIGKILL):
                raise RuntimeBoundaryError(
                    status=504,
                    category="timeout",
                    code="core_timeout",
                    retry="safe",
                    retry_after=1,
                )
        if len(stdout) > MAX_RESPONSE_BYTES:
            raise RuntimeBoundaryError(
                status=422,
                category="output_validation",
                code="operational_profile_exceeded",
                detail_refs=("worker_output_size",),
            )
        try:
            output = parse_json_bytes(stdout)
        except Exception as exc:
            raise RuntimeBoundaryError(
                status=500,
                category="core_invocation",
                code="core_worker_failed",
                retry="manual_review",
            ) from exc
        if not isinstance(output, dict) or output.get("ok") is not True:
            error = output.get("error", {}) if isinstance(output, dict) else {}
            raise RuntimeBoundaryError(
                status=int(error.get("status", 500)),
                category=str(error.get("category", "core_invocation")),
                code=str(error.get("code", "core_worker_failed")),
                retry=str(error.get("retry", "manual_review")),
                detail_refs=tuple(error.get("detail_refs", ())),
            )
        result = output.get("result")
        if not isinstance(result, dict):
            raise RuntimeBoundaryError(
                status=500,
                category="core_invocation",
                code="core_worker_failed",
                retry="manual_review",
            )
        return result

    def shutdown(self) -> None:
        with self._lock:
            self._closing = True
            active = tuple(self._active)
        for process in active:
            self._terminate(process)

    @staticmethod
    def _monitor_temp(
        directory: Path,
        process: subprocess.Popen[bytes],
        exceeded: threading.Event,
        stop: threading.Event,
    ) -> None:
        while not stop.wait(0.02):
            try:
                total = sum(
                    path.stat().st_size
                    for path in directory.rglob("*")
                    if path.is_file()
                )
            except (FileNotFoundError, OSError):
                return
            if total > WORKER_TEMP_BYTES:
                exceeded.set()
                WorkerProcess._terminate(process)
                return

    @staticmethod
    def _terminate(process: subprocess.Popen[bytes]) -> None:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            return
        try:
            process.wait(timeout=1)
            return
        except subprocess.TimeoutExpired:
            pass
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            return
        process.wait(timeout=1)
