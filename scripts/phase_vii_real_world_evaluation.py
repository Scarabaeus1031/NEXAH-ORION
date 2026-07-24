#!/usr/bin/env python3
"""Execute the versioned Phase VII real-world UNDERSTAND corpus."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from orion.gateway import GatewayResponse, OrientationGateway  # noqa: E402
from orion.public_contracts import (  # noqa: E402
    EVIDENCE_REFERENCE_SCHEMA,
    AuthorityDeclaration,
    ClarificationResult,
    ContinuationOption,
    ContractSet,
    EvidenceReference,
    EvidenceValidation,
    OrientationReport,
    ProvenanceStep,
    RuntimeError,
    SourceReference,
    TraceabilityTarget,
    validate_contract_set,
    validate_public_contract,
)


CORPUS_PATH = ROOT / "evaluation" / "phase_vii" / "corpus.json"


@dataclass(frozen=True, slots=True)
class EvaluationSession:
    document: dict[str, Any]
    external_request: dict[str, object]
    evidence: tuple[EvidenceReference, ...]
    response: GatewayResponse
    review: dict[str, str]


def load_corpus() -> dict[str, Any]:
    corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    if corpus.get("corpus_version") != "1.0.1":
        raise AssertionError("unsupported Phase VII corpus version")
    documents = corpus.get("documents")
    if not isinstance(documents, list) or not 10 <= len(documents) <= 20:
        raise AssertionError("Phase VII corpus must contain 10–20 documents")
    if len({item["document_id"] for item in documents}) != len(documents):
        raise AssertionError("corpus document identities must be unique")
    return corpus


def verify_document(document: dict[str, Any]) -> str:
    path = ROOT / document["path"]
    content = path.read_bytes()
    digest = hashlib.sha256(content).hexdigest()
    if digest != document["sha256"]:
        raise AssertionError(f"corpus revision mismatch: {document['path']}")
    normalized = " ".join(content.decode("utf-8").split())
    for quote in document["evidence_fragments"]:
        if " ".join(quote.split()) not in normalized:
            raise AssertionError(
                f"evidence selector not found in {document['path']}: {quote}"
            )
    return digest


def request_payload(document: dict[str, Any], corpus_version: str) -> dict[str, object]:
    scope = document["scope"]
    return {
        "request_id": f"phase-vii-{document['document_id']}",
        "request_version": "1",
        "mode": "understand",
        "requested_by": {
            "requester_id": "nexahedron-phase-vii-evaluation",
            "requester_kind": "human",
            "authority_domain": "nexahedron.orientation-laboratory",
        },
        "human_authority": {
            "human_ref": f"human-{document['document_id']}",
            "authority_scope": ["intention", "scope", "continuation"],
        },
        "orientation_objects": [
            {
                "object_id": f"corpus-{document['document_id']}",
                "object_version": corpus_version,
                "object_kind": document["document_type"],
                "source_owner": "NEXAH Project",
                "source_ref": document["path"],
                "source_revision": document["sha256"],
                "identity_scope": "external",
                "access_status": "available",
            }
        ],
        "intention": {
            "direction": document["human_intention"],
            "focus": document["focus"],
            "success_boundary": document["success_boundary"],
        },
        "scope": {
            "include": scope["include"],
            "exclude": scope["exclude"],
            "unresolved": [],
            "depth": scope["depth"],
        },
        "evidence_policy": "phase-vii/exact-text-quote",
        "effects": "none",
    }


def evidence_references(document: dict[str, Any]) -> tuple[EvidenceReference, ...]:
    request_id = f"phase-vii-{document['document_id']}"
    report_id = f"report-{request_id}-1"
    return tuple(
        EvidenceReference(
            schema_version=EVIDENCE_REFERENCE_SCHEMA,
            evidence_id=f"evidence-{document['document_id']}-{index + 1}",
            evidence_version="1",
            source=SourceReference(
                source_id=document["document_id"],
                source_version=document["sha256"],
                identity_domain="orion.phase-vii-corpus",
                source_owner="NEXAH Project",
                source_ref=document["path"],
                fragment_ref=f"text_quote:{quote}",
            ),
            authority=AuthorityDeclaration(
                authority_owner="NEXAH Project",
                authority_domain="orion.phase-vii-corpus",
                editorial_status=document["editorial_status"],
                authority_version="1.0.0",
            ),
            evidence_class="observed",
            relationship="supports",
            provenance=(
                ProvenanceStep(
                    step_id=f"source-{document['document_id']}-{index + 1}",
                    step_kind="source",
                    input_refs=(),
                    output_ref=(
                        f"{document['path']}#text-quote-"
                        f"{hashlib.sha256(quote.encode('utf-8')).hexdigest()}"
                    ),
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
                    finding_id=f"finding-{document['document_id']}-{index + 1}",
                ),
            ),
            access_status="available",
        )
        for index, quote in enumerate(document["evidence_fragments"])
    )


def classify_session(document: dict[str, Any], response: GatewayResponse) -> dict[str, str]:
    report = next(
        (item for item in response.contracts if isinstance(item, OrientationReport)),
        None,
    )
    evidence_count = len(report.evidence) if report else 0
    return {
        "Runtime": (
            "The unchanged UNDERSTAND Runtime returned a source-aware public report "
            f"with {evidence_count} bound evidence references."
        ),
        "Presentation": (
            "The presentation exposes report status, confirmed Scope, continuation, "
            "and each evidence text-quote selector with source and authority."
        ),
        "Evidence": (
            f"{len(document['evidence_fragments'])} exact text-quote selectors were "
            "verified against the pinned document revision before execution."
        ),
        "UX": (
            "The natural Human intention is preserved verbatim; object, focus and "
            "Scope remain explicit NEXAHEDRON choices."
        ),
        "Missing Representation": (
            "No content-bearing semantic Representation participated; orientation "
            "uses source text-quote selectors and structured report fields."
        ),
        "Missing Capability": (
            "No semantic extraction or language interpretation was executed; direct "
            "Human understanding is represented by an inspection proxy, not a user study."
        ),
    }


def validate_session(session: EvaluationSession) -> None:
    request = session.response.request
    if request is None:
        raise AssertionError("Gateway did not construct an Orientation Request")
    if not all(
        validate_public_contract(item).valid
        for item in (*session.evidence, *session.response.contracts)
    ):
        raise AssertionError("session contains an invalid public contract")
    graph = ContractSet(
        requests=(request,),
        clarifications=tuple(
            item for item in session.response.contracts if isinstance(item, ClarificationResult)
        ),
        reports=tuple(
            item for item in session.response.contracts if isinstance(item, OrientationReport)
        ),
        continuations=tuple(
            item for item in session.response.contracts if isinstance(item, ContinuationOption)
        ),
        evidence=session.evidence,
        runtime_errors=tuple(
            item for item in session.response.contracts if isinstance(item, RuntimeError)
        ),
    )
    result = validate_contract_set(graph)
    if not result.valid:
        raise AssertionError(f"session lineage failed: {result.errors}")


def run_corpus() -> tuple[dict[str, Any], tuple[EvaluationSession, ...]]:
    corpus = load_corpus()
    sessions = []
    for document in corpus["documents"]:
        verify_document(document)
        payload = request_payload(document, corpus["corpus_version"])
        evidence = evidence_references(document)
        response = OrientationGateway().handle(payload, evidence)
        session = EvaluationSession(
            document=document,
            external_request=payload,
            evidence=evidence,
            response=response,
            review=classify_session(document, response),
        )
        validate_session(session)
        sessions.append(session)
    return corpus, tuple(sessions)


def metrics(sessions: tuple[EvaluationSession, ...]) -> dict[str, object]:
    reports = [
        next(
            (item for item in session.response.contracts if isinstance(item, OrientationReport)),
            None,
        )
        for session in sessions
    ]
    errors = [
        item
        for session in sessions
        for item in session.response.contracts
        if isinstance(item, RuntimeError)
    ]
    continuations = [
        item
        for session in sessions
        for item in session.response.contracts
        if isinstance(item, ContinuationOption)
    ]
    total = len(sessions)
    completed = sum(report is not None and report.status == "complete" for report in reports)
    partial = sum(report is not None and report.status == "partial" for report in reports)
    blocked_reports = sum(report is not None and report.status == "blocked" for report in reports)
    clarifications = sum(error.kind == "clarification_required" for error in errors)
    unsupported = sum(error.kind == "unsupported" for error in errors)
    blocked_before = sum(error.kind == "blocked" for error in errors)
    evidence_complete = sum(
        report is not None and report.confidence.evidence_coverage == "complete"
        for report in reports
    )
    useful_continuations = sum(
        option.availability == "available" and option.action_type == "inspect_evidence"
        for option in continuations
    )
    understanding_proxy = sum(
        report is not None
        and bool(report.mode_payload.content.get("key_concepts"))
        and bool(session.response.presentation[0].evidence_details)
        for session, report in zip(sessions, reports)
    )
    return {
        "session_count": total,
        "completion": {"count": completed, "rate": completed / total},
        "partial": {"count": partial, "rate": partial / total},
        "clarification": {"count": clarifications, "rate": clarifications / total},
        "blocked": {
            "count": blocked_reports + blocked_before,
            "rate": (blocked_reports + blocked_before) / total,
        },
        "unsupported": {"count": unsupported, "rate": unsupported / total},
        "evidence_coverage_complete": {
            "count": evidence_complete,
            "rate": evidence_complete / total,
        },
        "continuation_useful": {
            "count": useful_continuations,
            "rate": useful_continuations / total,
            "criterion": "available inspect_evidence option with preserved lineage",
        },
        "user_understanding_proxy": {
            "count": understanding_proxy,
            "rate": understanding_proxy / total,
            "criterion": "confirmed key concepts plus inspectable evidence details",
            "limitation": "inspection proxy; no Human user study was performed",
        },
    }


def session_summary(session: EvaluationSession) -> dict[str, object]:
    report = next(
        item for item in session.response.contracts if isinstance(item, OrientationReport)
    )
    continuation = next(
        item for item in session.response.contracts if isinstance(item, ContinuationOption)
    )
    return {
        "document_id": session.document["document_id"],
        "document_type": session.document["document_type"],
        "path": session.document["path"],
        "sha256": session.document["sha256"],
        "human_intention": session.document["human_intention"],
        "request_ref": f"{report.identity.request_id}@{report.identity.request_version}",
        "report_ref": f"{report.identity.report_id}@{report.identity.report_version}",
        "status": report.status,
        "evidence_coverage": report.confidence.evidence_coverage,
        "evidence_refs": report.evidence,
        "continuation": {
            "ref": f"{continuation.option_id}@{continuation.option_version}",
            "action_type": continuation.action_type,
            "availability": continuation.availability,
        },
        "review": session.review,
    }


def full_trace(session: EvaluationSession) -> dict[str, object]:
    return {
        "document": session.document,
        "request": session.external_request,
        "validated_request": asdict(session.response.request),
        "runtime_outcome": [asdict(item) for item in session.response.contracts],
        "evidence": [asdict(item) for item in session.evidence],
        "orientation_report": next(
            asdict(item)
            for item in session.response.contracts
            if isinstance(item, OrientationReport)
        ),
        "continuation": next(
            asdict(item)
            for item in session.response.contracts
            if isinstance(item, ContinuationOption)
        ),
        "presentation": [asdict(item) for item in session.response.presentation],
        "review": session.review,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--full-trace",
        action="store_true",
        help="emit every validated request, public outcome, evidence object, and presentation",
    )
    args = parser.parse_args()
    corpus, sessions = run_corpus()
    output = {
        "corpus_id": corpus["corpus_id"],
        "corpus_version": corpus["corpus_version"],
        "metrics": metrics(sessions),
        "sessions": [
            full_trace(session) if args.full_trace else session_summary(session)
            for session in sessions
        ],
    }
    print(json.dumps(output, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
