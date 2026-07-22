#!/usr/bin/env python3
"""Run and print the first instrumented live Understand orientation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from orion.gateway import GatewayResponse, OrientationGateway  # noqa: E402
from orion.public_contracts import (  # noqa: E402
    EVIDENCE_REFERENCE_SCHEMA,
    AuthorityDeclaration,
    ContinuationOption,
    ContractSet,
    EvidenceReference,
    EvidenceValidation,
    OrientationReport,
    ProvenanceStep,
    SourceReference,
    TraceabilityTarget,
    validate_contract_set,
    validate_public_contract,
)


SOURCE_REVISION = "facb20f3439d183f8494ba27d94975509ddec415"
SOURCE_REF = "docs/architecture/operators/ORION_ORIENTATION_POLICIES.md"
HUMAN_REQUEST = (
    "I need to understand how ORION keeps evidence, interpretation, and Human "
    "authority separate before I trust an Orientation Report."
)


@dataclass(frozen=True, slots=True)
class LiveOrientationSession:
    session_id: str
    human_request: str
    external_request: dict[str, object]
    evidence: tuple[EvidenceReference, ...]
    response: GatewayResponse


def request_payload() -> dict[str, object]:
    """NEXAHEDRON-owned mapping of the Human's explicit session choices."""

    return {
        "request_id": "phase-vi-understand-policies-01",
        "request_version": "1",
        "mode": "understand",
        "requested_by": {
            "requester_id": "nexahedron-live-review",
            "requester_kind": "human",
            "authority_domain": "nexahedron.orientation-laboratory",
        },
        "human_authority": {
            "human_ref": "human-phase-vi",
            "authority_scope": ["intention", "scope", "continuation"],
        },
        "orientation_objects": [
            {
                "object_id": "orion-orientation-policies",
                "object_version": "1.0",
                "object_kind": "Canonical Policy Document",
                "source_owner": "NEXAH Project",
                "source_ref": SOURCE_REF,
                "source_revision": SOURCE_REVISION,
                "identity_scope": "canonical",
                "access_status": "available",
            }
        ],
        "intention": {
            "direction": HUMAN_REQUEST,
            "focus": "separation of evidence, interpretation, and Human authority",
            "success_boundary": (
                "I can identify the governing policies and inspect their source locations."
            ),
        },
        "scope": {
            "include": [
                "Human authority",
                "separation of authority",
                "evidence before interpretation",
            ],
            "exclude": ["execution technology", "provider behavior"],
            "unresolved": [],
            "depth": "focused",
        },
        "effects": "none",
    }


def evidence_references() -> tuple[EvidenceReference, ...]:
    fragments = (
        ("p01", "2.1 P01 — The Human Owns Intention"),
        ("p04", "2.1 P04 — Separation of Authority"),
        ("p12", "2.3 P12 — Evidence Before Interpretation"),
    )
    report_id = "report-phase-vi-understand-policies-01-1"
    return tuple(
        EvidenceReference(
            schema_version=EVIDENCE_REFERENCE_SCHEMA,
            evidence_id=f"evidence-policy-{key}",
            evidence_version="1",
            source=SourceReference(
                source_id="orion-orientation-policies",
                source_version=SOURCE_REVISION,
                identity_domain="orion.canonical-policy",
                source_owner="NEXAH Project",
                source_ref=SOURCE_REF,
                fragment_ref=fragment,
            ),
            authority=AuthorityDeclaration(
                authority_owner="NEXAH Project",
                authority_domain="orion.canonical-policy",
                editorial_status="published",
                authority_version="1.0",
            ),
            evidence_class="observed",
            relationship="supports",
            provenance=(
                ProvenanceStep(
                    step_id=f"source-policy-{key}",
                    step_kind="source",
                    input_refs=(),
                    output_ref=f"{SOURCE_REF}#{key}@{SOURCE_REVISION}",
                    owner="NEXAH Project",
                    lossiness="none",
                ),
            ),
            validation=EvidenceValidation(
                status="valid",
                checks=("source_resolved", "version_resolved", "fragment_resolved"),
                issues=(),
                validated_against=(EVIDENCE_REFERENCE_SCHEMA,),
            ),
            traceability=(
                TraceabilityTarget(
                    report_id=report_id,
                    report_version="1",
                    target_path=f"mode_payload.content.claims_and_support[{index}]",
                    finding_id=f"finding-policy-{key}",
                ),
            ),
            access_status="available",
        )
        for index, (key, fragment) in enumerate(fragments)
    )


def run_session() -> LiveOrientationSession:
    payload = request_payload()
    evidence = evidence_references()
    response = OrientationGateway().handle(payload, evidence)
    session = LiveOrientationSession(
        session_id="phase-vi-first-live-understand",
        human_request=HUMAN_REQUEST,
        external_request=payload,
        evidence=evidence,
        response=response,
    )
    validate_session(session)
    return session


def validate_session(session: LiveOrientationSession) -> None:
    if session.response.request is None:
        raise AssertionError("Gateway did not construct an Orientation Request")
    if not all(validate_public_contract(item).valid for item in session.response.contracts):
        raise AssertionError("live session contains an invalid public outcome")
    reports = tuple(
        item for item in session.response.contracts if isinstance(item, OrientationReport)
    )
    graph = ContractSet(
        requests=(session.response.request,),
        reports=reports,
        continuations=tuple(
            item
            for item in session.response.contracts
            if isinstance(item, ContinuationOption)
        ),
        evidence=session.evidence,
    )
    validation = validate_contract_set(graph)
    if not validation.valid:
        raise AssertionError(f"live session lineage failed: {validation.errors}")


def trace(session: LiveOrientationSession) -> dict[str, object]:
    report = next(
        item for item in session.response.contracts if isinstance(item, OrientationReport)
    )
    continuation = next(
        item
        for item in session.response.contracts
        if isinstance(item, ContinuationOption)
    )
    return {
        "session_id": session.session_id,
        "request": {
            "human_intention": session.human_request,
            "external_payload": session.external_request,
        },
        "validated_request": asdict(session.response.request),
        "runtime_outcome": [asdict(item) for item in session.response.contracts],
        "evidence": [asdict(item) for item in session.evidence],
        "orientation_report": asdict(report),
        "continuation": asdict(continuation),
        "presentation": [asdict(item) for item in session.response.presentation],
    }


def main() -> int:
    print(json.dumps(trace(run_session()), indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
