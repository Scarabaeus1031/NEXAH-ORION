"""Stage 1 verification for the ORION Version 1.1 Runtime."""

from __future__ import annotations

from http.client import HTTPConnection
import os
from pathlib import Path
import copy
from hashlib import sha256
import signal
import socket
import subprocess
import sys
import threading
import time
import unittest
from unittest.mock import patch

from orion_runtime.canonical import CanonicalJSONError, canonical_bytes, parse_json_bytes
from orion_runtime.constants import API_VERSION, MAX_REQUEST_BYTES, MEDIA_TYPE
from orion_runtime.contracts import validate_envelope
from orion_runtime.errors import RuntimeBoundaryError
from orion_runtime.fixtures import canary_envelope
from orion_runtime.gateway import Gateway
from orion_runtime.manifest import verify_manifest
from orion_runtime.process import WorkerProcess
from orion_runtime.release import verify_release, verify_runtime_release_manifest
from orion_runtime.server import OrionHTTPServer, RuntimeConfig, RuntimeState


class CanonicalBoundaryTests(unittest.TestCase):
    def test_duplicate_keys_and_floats_are_rejected(self) -> None:
        with self.assertRaises(CanonicalJSONError):
            parse_json_bytes(b'{"a":1,"a":2}')
        with self.assertRaises(CanonicalJSONError):
            parse_json_bytes(b'{"a":1.5}')

    def test_valid_envelope_is_canonical_and_replayable(self) -> None:
        first, request, first_digest = validate_envelope(canary_envelope())
        second, _, second_digest = validate_envelope(
            parse_json_bytes(canonical_bytes(first))
        )
        self.assertEqual(request.request_id, "runtime-canary-request")
        self.assertEqual(first, second)
        self.assertEqual(first_digest, second_digest)

    def test_invalid_and_oversized_material_are_rejected_before_worker(self) -> None:
        envelope = canary_envelope()
        envelope["confirmed_material"]["source"]["content"] = "x" * 262_145
        with self.assertRaises(RuntimeBoundaryError) as caught:
            validate_envelope(envelope)
        self.assertEqual(caught.exception.status, 422)


class RuntimeExecutionTests(unittest.TestCase):
    def test_independent_workers_replay_byte_identically(self) -> None:
        gateway = Gateway()
        first = gateway.execute(canary_envelope())
        second = gateway.execute(canary_envelope())
        self.assertEqual(canonical_bytes(first.body), canonical_bytes(second.body))
        self.assertEqual(first.result_digest, second.result_digest)
        self.assertEqual(first.body["artifact_manifest"]["artifact_count"], 22)
        self.assertEqual(first.body["terminal_stop"], "at_slice_iv_certified")

    def test_timeout_terminates_worker(self) -> None:
        worker = WorkerProcess(timeout=0.001)
        with self.assertRaises(RuntimeBoundaryError) as caught:
            worker.execute(canary_envelope())
        self.assertEqual(caught.exception.status, 504)
        self.assertEqual(caught.exception.code, "core_timeout")

    def test_startup_readiness_replays_isolated_canary(self) -> None:
        state = RuntimeState(
            RuntimeConfig(
                host="127.0.0.1",
                port=0,
                credentials={"integration": "test-secret"},
            )
        )
        state.verify_startup()
        self.assertTrue(state.ready)
        self.assertEqual(state.readiness_errors, ())

    def test_startup_canary_cannot_be_disabled_by_environment(self) -> None:
        with patch.dict(
            os.environ,
            {
                "ORION_SERVICE_CREDENTIALS_JSON": '{"integration":"test-secret"}',
                "ORION_STARTUP_CANARY": "false",
            },
            clear=False,
        ):
            config = RuntimeConfig.from_environment()
        self.assertFalse(hasattr(config, "startup_canary"))
        state = RuntimeState(config)
        state.verify_startup()
        self.assertTrue(state.ready)

    def test_release_identity_ignores_environment_assertion(self) -> None:
        with patch.dict(os.environ, {"ORION_CORE_COMMIT": "attacker-controlled"}):
            self.assertTrue(verify_release()[0])
            self.assertTrue(verify_runtime_release_manifest()[0])

    def test_worker_isolation_denies_tcp_udp_and_unix_sockets(self) -> None:
        script = """
from orion_runtime.isolation import install_worker_network_isolation, assert_network_isolated
install_worker_network_isolation()
assert_network_isolated()
print("isolated")
"""
        root = Path(__file__).resolve().parent.parent
        env = {
            "PATH": os.environ.get("PATH", ""),
            "PYTHONPATH": str(root / "src"),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
        }
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=root,
            env=env,
            capture_output=True,
            check=False,
            timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(result.stdout.strip(), b"isolated")

    def test_manifest_rejects_cross_artifact_reference_mismatch(self) -> None:
        raw = WorkerProcess().execute(canary_envelope())["artifact_manifest"]
        altered = copy.deepcopy(raw)
        entry = altered["artifacts"][18]
        entry["body"]["expression_contract_ref"] = "sha256:" + ("0" * 64)
        body_bytes = canonical_bytes(entry["body"])
        entry["canonical_byte_length"] = len(body_bytes)
        entry["artifact_ref"] = "sha256:" + sha256(body_bytes).hexdigest()
        with patch("orion_runtime.manifest._verify_native_artifact"):
            with self.assertRaises(RuntimeBoundaryError) as caught:
                verify_manifest(altered)
        self.assertIn("reference_mismatch", caught.exception.detail_refs[0])

    def test_worker_refuses_new_work_after_shutdown(self) -> None:
        worker = WorkerProcess()
        worker.shutdown()
        with self.assertRaises(RuntimeBoundaryError) as caught:
            worker.execute(canary_envelope())
        self.assertEqual(caught.exception.status, 503)


class HTTPRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        config = RuntimeConfig(
            host="127.0.0.1",
            port=0,
            credentials={"integration": "test-secret"},
        )
        self.state = RuntimeState(config)
        self.state.ready = True
        self.server = OrionHTTPServer(("127.0.0.1", 0), self.state)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]

    def tearDown(self) -> None:
        self.state.shutting_down = True
        self.state.ready = False
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def test_health_and_authenticated_execution(self) -> None:
        connection = HTTPConnection("127.0.0.1", self.port, timeout=10)
        connection.request("GET", "/health")
        health = connection.getresponse()
        health_body = parse_json_bytes(health.read())
        self.assertEqual(health.status, 200)
        self.assertEqual(health_body["status"], "ready")

        body = canonical_bytes(canary_envelope())
        connection.request(
            "POST",
            "/orientation/v1/requests",
            body=body,
            headers=self._headers(len(body)),
        )
        response = connection.getresponse()
        result = parse_json_bytes(response.read())
        self.assertEqual(response.status, 200)
        self.assertEqual(result["terminal_stop"], "at_slice_iv_certified")
        self.assertEqual(result["artifact_manifest"]["artifact_count"], 22)
        self.assertNotIn("execution_id", result)
        self.assertTrue(response.getheader("ORION-Execution-ID"))
        connection.close()

    def test_invalid_auth_and_oversized_body_are_rejected(self) -> None:
        connection = HTTPConnection("127.0.0.1", self.port, timeout=10)
        body = canonical_bytes(canary_envelope())
        headers = self._headers(len(body))
        headers["Authorization"] = "Bearer wrong"
        connection.request("POST", "/orientation/v1/requests", body=body, headers=headers)
        response = connection.getresponse()
        self.assertEqual(response.status, 401)
        response.read()
        connection.close()

        connection = HTTPConnection("127.0.0.1", self.port, timeout=10)
        connection.putrequest("POST", "/orientation/v1/requests")
        for name, value in self._headers(MAX_REQUEST_BYTES + 1).items():
            connection.putheader(name, value)
        connection.endheaders()
        response = connection.getresponse()
        self.assertEqual(response.status, 413)
        response.read()
        connection.close()

    def test_restart_has_no_recovery_state(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        replacement = OrionHTTPServer(("127.0.0.1", 0), self.state)
        thread = threading.Thread(target=replacement.serve_forever, daemon=True)
        thread.start()
        connection = HTTPConnection("127.0.0.1", replacement.server_address[1], timeout=5)
        connection.request("GET", "/health")
        response = connection.getresponse()
        self.assertEqual(response.status, 200)
        response.read()
        connection.close()
        replacement.shutdown()
        replacement.server_close()
        thread.join(timeout=2)
        self.server = OrionHTTPServer(("127.0.0.1", 0), self.state)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def test_sigterm_performs_clean_shutdown(self) -> None:
        probe = socket.socket()
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
        probe.close()
        root = Path(__file__).resolve().parent.parent
        env = dict(os.environ)
        env.update(
            {
                "PYTHONPATH": str(root / "src"),
                "ORION_BIND_HOST": "127.0.0.1",
                "ORION_PORT": str(port),
                "ORION_SERVICE_CREDENTIALS_JSON": '{"integration":"test-secret"}',
            }
        )
        process = subprocess.Popen(
            [sys.executable, "-m", "orion_runtime"],
            cwd=root,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            for _ in range(50):
                try:
                    connection = HTTPConnection("127.0.0.1", port, timeout=0.2)
                    connection.request("GET", "/health")
                    response = connection.getresponse()
                    response.read()
                    connection.close()
                    if response.status == 200:
                        break
                except OSError:
                    time.sleep(0.05)
            else:
                self.fail("Runtime did not become ready")
            process.send_signal(signal.SIGTERM)
            self.assertEqual(process.wait(timeout=5), 0)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=2)
            process.communicate()

    @staticmethod
    def _headers(length: int) -> dict[str, str]:
        return {
            "Authorization": "Bearer test-secret",
            "Content-Type": MEDIA_TYPE,
            "Accept": MEDIA_TYPE,
            "ORION-API-Version": API_VERSION,
            "Content-Length": str(length),
        }


if __name__ == "__main__":
    unittest.main()
