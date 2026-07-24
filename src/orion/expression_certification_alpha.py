"""Observational Expression Certification for Vertical Slice IV WP29.

WP29 consumes exactly one accepted immutable WP28 Expression Conformance
Report. It records certification only. It never reopens, reconstructs,
validates, repairs, interprets, presents, or executes an earlier artifact.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import re
from typing import Mapping

from orion.expression_conformance_alpha import (
    ACCEPTED,
    EXPRESSION_CONFORMANCE_SCHEMA_VERSION,
    RESPONSIBILITY as CONFORMANCE_RESPONSIBILITY,
    STOP_AFTER_EXPRESSION_CONFORMANCE,
    ExpressionConformanceReport,
    canonical_expression_conformance_report_bytes,
)


EXPRESSION_CERTIFICATION_SCHEMA_VERSION = (
    "orion.expression-certification/0.1-alpha"
)
EXPRESSION_CERTIFICATION_VERSION = "0.1-alpha"
CERTIFIED = "certified"
RESPONSIBILITY = "expression_certification"
STOP_AT_EXPRESSION_CERTIFIED = "at_expression_certified"

_CERTIFICATION_ID = re.compile(r"^expression-certification-[0-9a-f]{24}$")
_SHA256_REF = re.compile(r"^sha256:[0-9a-f]{64}$")
_SHA256_HEX = re.compile(r"^[0-9a-f]{64}$")


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(value: object) -> str:
    return sha256(_canonical_bytes(value)).hexdigest()


def _artifact_ref(value: bytes) -> str:
    return f"sha256:{sha256(value).hexdigest()}"


def _certification_basis(
    *,
    expression_conformance_report_id: str,
    expression_conformance_report_integrity: str,
    expression_conformance_report_ref: str,
    expression_ref: str,
    decision: str,
    provenance_ref: str,
) -> dict[str, object]:
    return {
        "schema_version": EXPRESSION_CERTIFICATION_SCHEMA_VERSION,
        "certification_version": EXPRESSION_CERTIFICATION_VERSION,
        "expression_conformance_report_id": (
            expression_conformance_report_id
        ),
        "expression_conformance_report_integrity": (
            expression_conformance_report_integrity
        ),
        "expression_conformance_report_ref": (
            expression_conformance_report_ref
        ),
        "expression_ref": expression_ref,
        "decision": decision,
        "provenance_ref": provenance_ref,
        "responsibility": RESPONSIBILITY,
        "stop": STOP_AT_EXPRESSION_CERTIFIED,
    }


@dataclass(frozen=True, slots=True)
class ExpressionCertificationReport:
    """Immutable certification of one accepted WP28 report."""

    certification_id: str
    certification_integrity: str
    schema_version: str
    certification_version: str
    expression_conformance_report_id: str
    expression_conformance_report_integrity: str
    expression_conformance_report_ref: str
    expression_ref: str
    decision: str
    provenance_ref: str
    responsibility: str
    stop: str

    def __post_init__(self) -> None:
        if _CERTIFICATION_ID.fullmatch(self.certification_id) is None:
            raise ValueError("certification_id is not canonical")
        for field_name in (
            "certification_integrity",
            "expression_conformance_report_integrity",
        ):
            if _SHA256_HEX.fullmatch(getattr(self, field_name)) is None:
                raise ValueError(f"{field_name} must be SHA-256 hexadecimal")
        if self.schema_version != EXPRESSION_CERTIFICATION_SCHEMA_VERSION:
            raise ValueError("Expression Certification schema changed")
        if self.certification_version != EXPRESSION_CERTIFICATION_VERSION:
            raise ValueError("Expression Certification version changed")
        if (
            not isinstance(self.expression_conformance_report_id, str)
            or not self.expression_conformance_report_id
        ):
            raise ValueError(
                "expression_conformance_report_id must be exact text"
            )
        for field_name in (
            "expression_conformance_report_ref",
            "expression_ref",
            "provenance_ref",
        ):
            value = getattr(self, field_name)
            if _SHA256_REF.fullmatch(value) is None:
                raise ValueError(f"{field_name} must be a SHA-256 reference")
        if self.provenance_ref != self.expression_conformance_report_ref:
            raise ValueError(
                "Expression Certification provenance must name WP28"
            )
        if self.decision != CERTIFIED:
            raise ValueError("Expression Certification decision changed")
        if self.responsibility != RESPONSIBILITY:
            raise ValueError("Expression Certification responsibility changed")
        if self.stop != STOP_AT_EXPRESSION_CERTIFIED:
            raise ValueError("WP29 STOP boundary changed")
        basis = _certification_basis(
            expression_conformance_report_id=(
                self.expression_conformance_report_id
            ),
            expression_conformance_report_integrity=(
                self.expression_conformance_report_integrity
            ),
            expression_conformance_report_ref=(
                self.expression_conformance_report_ref
            ),
            expression_ref=self.expression_ref,
            decision=self.decision,
            provenance_ref=self.provenance_ref,
        )
        digest = _digest(basis)
        if self.certification_id != (
            f"expression-certification-{digest[:24]}"
        ):
            raise ValueError("certification_id differs from observations")
        if self.certification_integrity != digest:
            raise ValueError(
                "certification_integrity differs from observations"
            )


def certify_expression(
    report: ExpressionConformanceReport,
) -> ExpressionCertificationReport:
    """Certify one accepted WP28 report without rerunning conformance."""

    if not isinstance(report, ExpressionConformanceReport):
        raise TypeError(
            "WP29 accepts only immutable Expression Conformance Report"
        )
    report.__post_init__()
    if (
        report.schema_version != EXPRESSION_CONFORMANCE_SCHEMA_VERSION
        or report.responsibility != CONFORMANCE_RESPONSIBILITY
        or report.stop != STOP_AFTER_EXPRESSION_CONFORMANCE
    ):
        raise ValueError("WP28 report boundary is invalid")
    if (
        not report.valid
        or report.decision != ACCEPTED
        or report.errors
        or report.accepted_expression_ref is None
        or report.accepted_expression_ref != report.expression_ref
        or not report.inputs_unchanged
    ):
        raise ValueError("WP28 did not accept the exact Expression Artifact")
    report_bytes = canonical_expression_conformance_report_bytes(report)
    report_integrity = sha256(report_bytes).hexdigest()
    report_ref = _artifact_ref(report_bytes)
    basis = _certification_basis(
        expression_conformance_report_id=report.report_id,
        expression_conformance_report_integrity=report_integrity,
        expression_conformance_report_ref=report_ref,
        expression_ref=report.accepted_expression_ref,
        decision=CERTIFIED,
        provenance_ref=report_ref,
    )
    digest = _digest(basis)
    return ExpressionCertificationReport(
        certification_id=f"expression-certification-{digest[:24]}",
        certification_integrity=digest,
        **basis,
    )


def expression_certification_report_as_dict(
    report: ExpressionCertificationReport,
) -> dict[str, object]:
    report.__post_init__()
    return asdict(report)


def canonical_expression_certification_report_bytes(
    report: ExpressionCertificationReport,
) -> bytes:
    return _canonical_bytes(expression_certification_report_as_dict(report))


def expression_certification_report_from_dict(
    value: Mapping[str, object],
) -> ExpressionCertificationReport:
    if not isinstance(value, Mapping):
        raise TypeError("Expression Certification Report must be a mapping")
    expected_fields = {
        "certification_id",
        "certification_integrity",
        "schema_version",
        "certification_version",
        "expression_conformance_report_id",
        "expression_conformance_report_integrity",
        "expression_conformance_report_ref",
        "expression_ref",
        "decision",
        "provenance_ref",
        "responsibility",
        "stop",
    }
    if set(value) != expected_fields:
        raise ValueError("Expression Certification fields do not match WP29")
    return ExpressionCertificationReport(**dict(value))


__all__: tuple[str, ...] = ()
