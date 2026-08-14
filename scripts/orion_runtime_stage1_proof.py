#!/usr/bin/env python3
"""Replay the Gate 0 input through the Version 1.1 Runtime boundary."""

from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
import json

from orion.public_contracts import (
    HumanAuthorityReference,
    IntegrityReference,
    Intention,
    NO_EFFECTS,
    ORIENTATION_REQUEST_SCHEMA,
    OrientationObjectReference,
    OrientationRequest,
    RequesterReference,
    Scope,
)
from orion_runtime.canonical import canonical_bytes, parse_json_bytes
from orion_runtime.constants import API_VERSION, LINEAGE_SCHEMA, MATERIAL_SCHEMA
from orion_runtime.gateway import Gateway


EXPECTED_MANIFEST_REF = (
    "sha256:e1a879bf9869be43e50519d25e066977fbcec6e612327afa3a103fb806f13a3c"
)
EXPECTED_REQUEST_DIGEST = (
    "sha256:4aa3941b6378280a265327ce2c42af7bd2f0526913480eda78b2f9c9c914c354"
)
EXPECTED_RESULT_DIGEST = (
    "sha256:430008906972034e65989614e11318bb2dd487a9d1d74884bf03189a598b8030"
)
EXPECTED_TERMINAL_REF = (
    "sha256:6114accd7a4f662dcee593414b8253eeb7e3b2cc947b11392978a3f13b1eb82a"
)


def gate0_envelope() -> dict[str, object]:
    content = (
        "# Gate 0\n"
        "\n"
        "The frozen ORION Core is invoked through its certified boundaries.\n"
        "\n"
        "## Verification\n"
        "\n"
        "Every produced artifact remains deterministic and inspectable.\n"
    )
    content_digest = sha256(content.encode("utf-8")).hexdigest()
    source_version = f"sha256:{content_digest}"
    confirmation_basis = {
        "orientation_object_id": "gate0-orientation-object",
        "orientation_object_version": "1",
        "source_id": "gate0-confirmed-source",
        "source_revision": source_version,
        "confirmed_by": "gate0-human-authority",
        "confirmed_revision": 1,
        "boundary_ref": "whole",
    }
    confirmation_id = (
        f"confirmation-{sha256(canonical_bytes(confirmation_basis)).hexdigest()[:16]}"
    )
    request = OrientationRequest(
        schema_version=ORIENTATION_REQUEST_SCHEMA,
        request_id="gate0-request",
        request_version="1",
        mode="understand",
        requested_by=RequesterReference(
            "nexahedron-gate0",
            "authorized_consumer",
            "nexahedron.gate0",
        ),
        human_authority=HumanAuthorityReference(
            "gate0-human-authority",
            ("intention", "scope", "continuation"),
        ),
        orientation_objects=(
            OrientationObjectReference(
                object_id="gate0-orientation-object",
                object_version="1",
                object_kind="Document",
                source_owner="gate0-human-authority",
                source_ref="gate0://confirmed-source/markdown",
                source_revision=source_version,
                identity_scope="session_local",
                integrity_ref=IntegrityReference(
                    "sha256",
                    content_digest,
                    "whole",
                    True,
                ),
                access_status="available",
            ),
        ),
        intention=Intention(
            "Inspect the deterministic structural orientation of this material."
        ),
        scope=Scope(("declared structure",), (), ()),
        effects=NO_EFFECTS,
    )
    envelope = {
        "api_version": API_VERSION,
        "request": asdict(request),
        "confirmed_material": {
            "schema_version": MATERIAL_SCHEMA,
            "orientation_object_id": "gate0-orientation-object",
            "orientation_object_version": "1",
            "source": {
                "entry_id": "gate0-confirmed-source",
                "source_owner": "gate0-human-authority",
                "source_ref": "gate0://confirmed-source/markdown",
                "source_version": source_version,
                "fragment_ref": "whole",
                "media_type": "text/markdown;charset=utf-8",
                "grammar": "CommonMark",
                "grammar_version": "0.31.2",
                "content": content,
                "integrity_sha256": content_digest,
            },
            "confirmation": {
                "confirmed_by": "gate0-human-authority",
                "confirmed_revision": 1,
                "confirmation_id": confirmation_id,
            },
        },
        "lineage": {
            "schema_version": LINEAGE_SCHEMA,
            "requests": [],
            "clarifications": [],
        },
        "evidence": [],
    }
    return parse_json_bytes(canonical_bytes(envelope))


def main() -> int:
    gateway = Gateway()
    first = gateway.execute(gate0_envelope())
    second = gateway.execute(gate0_envelope())
    manifest_ref = (
        "sha256:"
        + sha256(canonical_bytes(first.body["artifact_manifest"])).hexdigest()
    )
    checks = {
        "runtime_replay_byte_identical": (
            canonical_bytes(first.body) == canonical_bytes(second.body)
        ),
        "artifact_count": first.body["artifact_manifest"]["artifact_count"] == 22,
        "manifest_matches_gate0": manifest_ref == EXPECTED_MANIFEST_REF,
        "request_digest_matches_gate0": first.request_digest == EXPECTED_REQUEST_DIGEST,
        "result_digest_matches_gate0": first.result_digest == EXPECTED_RESULT_DIGEST,
        "terminal_ref_matches_gate0": (
            first.body["terminal_certification_ref"] == EXPECTED_TERMINAL_REF
        ),
        "terminal_stop": first.body["terminal_stop"] == "at_slice_iv_certified",
    }
    output = {
        "proof_schema": "orion.runtime-stage1-proof/1.0",
        "checks": checks,
        "passed": all(checks.values()),
        "manifest_ref": manifest_ref,
        "request_digest": first.request_digest,
        "result_digest": first.result_digest,
        "terminal_certification_ref": first.body["terminal_certification_ref"],
    }
    print(json.dumps(output, separators=(",", ":"), sort_keys=True))
    return 0 if output["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
