"""Non-sensitive deterministic startup canary for Runtime readiness."""

from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256

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

from .canonical import canonical_bytes, parse_json_bytes
from .constants import API_VERSION, LINEAGE_SCHEMA, MATERIAL_SCHEMA


def canary_envelope() -> dict[str, object]:
    content = "# Runtime canary\n\nDeterministic readiness verification.\n"
    content_digest = sha256(content.encode("utf-8")).hexdigest()
    source_version = f"sha256:{content_digest}"
    confirmation_basis = {
        "orientation_object_id": "runtime-canary-object",
        "orientation_object_version": "1",
        "source_id": "runtime-canary-source",
        "source_revision": source_version,
        "confirmed_by": "runtime-canary-authority",
        "confirmed_revision": 1,
        "boundary_ref": "whole",
    }
    confirmation_id = (
        f"confirmation-{sha256(canonical_bytes(confirmation_basis)).hexdigest()[:16]}"
    )
    request = OrientationRequest(
        schema_version=ORIENTATION_REQUEST_SCHEMA,
        request_id="runtime-canary-request",
        request_version="1",
        mode="understand",
        requested_by=RequesterReference(
            "runtime-readiness",
            "authorized_consumer",
            "orion.runtime.readiness",
        ),
        human_authority=HumanAuthorityReference(
            "runtime-canary-authority",
            ("intention", "scope", "continuation"),
        ),
        orientation_objects=(
            OrientationObjectReference(
                object_id="runtime-canary-object",
                object_version="1",
                object_kind="Document",
                source_owner="runtime-canary-authority",
                source_ref="orion://runtime/canary",
                source_revision=source_version,
                identity_scope="canonical",
                integrity_ref=IntegrityReference(
                    "sha256",
                    content_digest,
                    "whole",
                    True,
                ),
                access_status="available",
            ),
        ),
        intention=Intention("Verify deterministic Runtime readiness."),
        scope=Scope(("declared structure",), (), ()),
        effects=NO_EFFECTS,
    )
    material = {
        "schema_version": MATERIAL_SCHEMA,
        "orientation_object_id": "runtime-canary-object",
        "orientation_object_version": "1",
        "source": {
            "entry_id": "runtime-canary-source",
            "source_owner": "runtime-canary-authority",
            "source_ref": "orion://runtime/canary",
            "source_version": source_version,
            "fragment_ref": "whole",
            "media_type": "text/markdown;charset=utf-8",
            "grammar": "CommonMark",
            "grammar_version": "0.31.2",
            "content": content,
            "integrity_sha256": content_digest,
        },
        "confirmation": {
            "confirmed_by": "runtime-canary-authority",
            "confirmed_revision": 1,
            "confirmation_id": confirmation_id,
        },
    }
    envelope = {
        "api_version": API_VERSION,
        "request": asdict(request),
        "confirmed_material": material,
        "lineage": {
            "schema_version": LINEAGE_SCHEMA,
            "requests": [],
            "clarifications": [],
        },
        "evidence": [],
    }
    return parse_json_bytes(canonical_bytes(envelope))
