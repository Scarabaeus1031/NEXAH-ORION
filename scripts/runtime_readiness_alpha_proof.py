#!/usr/bin/env python3
"""Run the cross-repository Runtime Readiness Validation Alpha proof."""

from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

from orion.gateway.translation import construct_orientation_request
from orion.public_contracts import OrientationRequest, validate_orientation_request
from orion.readiness_alpha import prove_runtime_readiness


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_NEXAHEDRON_ROOT = ROOT.parent / "NEXAHEDRON"


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _run_nexahedron_proof(root: Path, script: str) -> dict[str, Any]:
    environment = os.environ.copy()
    environment["ORION_SOURCE_PATH"] = str(ROOT / "src")
    result = subprocess.run(
        [
            "node",
            "--no-warnings",
            "--experimental-strip-types",
            script,
        ],
        cwd=root,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip() or f"NEXAHEDRON proof failed: {script}"
        )
    return json.loads(result.stdout)


def _lineage_checks(
    request: OrientationRequest,
    representation: dict[str, Any],
) -> dict[str, bool]:
    if len(request.orientation_objects) != 1:
        return {"exactly_one_orientation_object": False}

    orientation_object = request.orientation_objects[0]
    representation_ref = (
        f"{representation['representation_id']}"
        f"@{representation['representation_version']}"
    )
    integrity = orientation_object.integrity_ref
    return {
        "exactly_one_orientation_object": True,
        "exactly_one_representation_referenced":
            orientation_object.representation_refs == (representation_ref,),
        "representation_identity_unchanged":
            orientation_object.object_id
            == representation["orientation_object_id"]
            and orientation_object.object_version
            == representation["orientation_object_version"],
        "source_identity_traceable":
            orientation_object.source_owner
            == representation["source"]["owner"]
            and orientation_object.source_ref
            == representation["source"]["source_ref"],
        "source_revision_traceable":
            orientation_object.source_revision
            == representation["source"]["revision"],
        "integrity_traceable":
            integrity is not None
            and integrity.method == "sha256"
            and integrity.value
            == representation["payload"]["content_sha256"]
            and integrity.coverage == "whole"
            and integrity.verified is True,
        "request_identity_unchanged":
            request.request_id == "request-representation-ref-alpha-001"
            and request.request_version == "1",
    }


def main() -> int:
    nexahedron_root = Path(
        os.environ.get("NEXAHEDRON_ROOT", DEFAULT_NEXAHEDRON_ROOT)
    ).resolve()
    try:
        handoff = _run_nexahedron_proof(
            nexahedron_root,
            "scripts/representation-alpha-handoff.mjs",
        )
        request_proof = _run_nexahedron_proof(
            nexahedron_root,
            "scripts/representation-referenced-request.mjs",
        )
        representation = handoff["representation"]
        request = construct_orientation_request(request_proof["request"])
        validation = validate_orientation_request(request)
        if not validation.valid:
            raise ValueError("accepted OrientationRequest 1.0 is no longer valid")

        lineage_checks = _lineage_checks(request, representation)
        failed = tuple(
            name for name, passed in lineage_checks.items() if not passed
        )
        if failed:
            raise ValueError(
                "readiness lineage checks failed: " + ", ".join(failed)
            )

        diagnostic = prove_runtime_readiness(request)
    except (
        KeyError,
        OSError,
        TypeError,
        ValueError,
        RuntimeError,
        json.JSONDecodeError,
    ) as error:
        print(f"[Runtime Readiness Alpha] {error}", file=sys.stderr)
        return 1

    representation_ref = (
        f"{representation['representation_id']}"
        f"@{representation['representation_version']}"
    )
    proof = {
        "diagnostic_kind": "internal_runtime_readiness_proof",
        "lineage": {
            "checks": lineage_checks,
            "representation_ref": representation_ref,
            "representation_sha256": representation["representation_sha256"],
            "request_ref": f"{request.request_id}@{request.request_version}",
            "request_sha256": sha256(_canonical_bytes(asdict(request))).hexdigest(),
            "source_owner": representation["source"]["owner"],
            "source_ref": representation["source"]["source_ref"],
            "source_revision": representation["source"]["revision"],
            "integrity_sha256": representation["payload"]["content_sha256"],
        },
        "public_contract_validation": {
            "errors": [asdict(error) for error in validation.errors],
            "valid": validation.valid,
        },
        "readiness": asdict(diagnostic),
        "stop": "before_processing",
    }
    print(
        json.dumps(
            proof,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
