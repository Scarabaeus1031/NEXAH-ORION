"""Observational Vertical Slice IV Certification for WP30.

WP30 consumes exactly one immutable WP29 Expression Certification Report. It
records Slice IV certification only. It never reopens, reconstructs, validates,
repairs, interprets, presents, or executes an earlier artifact.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import re
from typing import Mapping

from orion.expression_certification_alpha import (
    CERTIFIED as EXPRESSION_CERTIFIED,
    EXPRESSION_CERTIFICATION_SCHEMA_VERSION,
    RESPONSIBILITY as EXPRESSION_CERTIFICATION_RESPONSIBILITY,
    STOP_AT_EXPRESSION_CERTIFIED,
    ExpressionCertificationReport,
    canonical_expression_certification_report_bytes,
)


SLICE_IV_CERTIFICATION_SCHEMA_VERSION = (
    "orion.slice-iv-certification/0.1-alpha"
)
SLICE_IV_CERTIFICATION_VERSION = "0.1-alpha"
CERTIFIED = "certified"
RESPONSIBILITY = "vertical_slice_iv_certification"
STOP_AT_SLICE_IV_CERTIFIED = "at_slice_iv_certified"

_CERTIFICATION_ID = re.compile(r"^slice-iv-certification-[0-9a-f]{24}$")
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
    expression_certification_id: str,
    expression_certification_integrity: str,
    decision: str,
    provenance_ref: str,
) -> dict[str, object]:
    return {
        "schema_version": SLICE_IV_CERTIFICATION_SCHEMA_VERSION,
        "certification_version": SLICE_IV_CERTIFICATION_VERSION,
        "expression_certification_id": expression_certification_id,
        "expression_certification_integrity": (
            expression_certification_integrity
        ),
        "decision": decision,
        "provenance_ref": provenance_ref,
        "responsibility": RESPONSIBILITY,
        "stop": STOP_AT_SLICE_IV_CERTIFIED,
    }


@dataclass(frozen=True, slots=True)
class SliceIVCertificationReport:
    """Immutable certification of one accepted WP29 report."""

    certification_id: str
    certification_integrity: str
    schema_version: str
    certification_version: str
    expression_certification_id: str
    expression_certification_integrity: str
    decision: str
    provenance_ref: str
    responsibility: str
    stop: str

    def __post_init__(self) -> None:
        if _CERTIFICATION_ID.fullmatch(self.certification_id) is None:
            raise ValueError("certification_id is not canonical")
        for field_name in (
            "certification_integrity",
            "expression_certification_integrity",
        ):
            if _SHA256_HEX.fullmatch(getattr(self, field_name)) is None:
                raise ValueError(f"{field_name} must be SHA-256 hexadecimal")
        if self.schema_version != SLICE_IV_CERTIFICATION_SCHEMA_VERSION:
            raise ValueError("Slice IV Certification schema changed")
        if self.certification_version != SLICE_IV_CERTIFICATION_VERSION:
            raise ValueError("Slice IV Certification version changed")
        if (
            not isinstance(self.expression_certification_id, str)
            or not self.expression_certification_id
        ):
            raise ValueError(
                "expression_certification_id must be exact text"
            )
        if _SHA256_REF.fullmatch(self.provenance_ref) is None:
            raise ValueError("provenance_ref must be a SHA-256 reference")
        if self.decision != CERTIFIED:
            raise ValueError("Slice IV Certification decision changed")
        if self.responsibility != RESPONSIBILITY:
            raise ValueError("Slice IV Certification responsibility changed")
        if self.stop != STOP_AT_SLICE_IV_CERTIFIED:
            raise ValueError("WP30 STOP boundary changed")
        basis = _certification_basis(
            expression_certification_id=self.expression_certification_id,
            expression_certification_integrity=(
                self.expression_certification_integrity
            ),
            decision=self.decision,
            provenance_ref=self.provenance_ref,
        )
        digest = _digest(basis)
        if self.certification_id != (
            f"slice-iv-certification-{digest[:24]}"
        ):
            raise ValueError("certification_id differs from observations")
        if self.certification_integrity != digest:
            raise ValueError(
                "certification_integrity differs from observations"
            )


def certify_slice_iv(
    report: ExpressionCertificationReport,
) -> SliceIVCertificationReport:
    """Certify one accepted WP29 report without reopening earlier stages."""

    if not isinstance(report, ExpressionCertificationReport):
        raise TypeError(
            "WP30 accepts only immutable Expression Certification Report"
        )
    report.__post_init__()
    if (
        report.schema_version != EXPRESSION_CERTIFICATION_SCHEMA_VERSION
        or report.responsibility
        != EXPRESSION_CERTIFICATION_RESPONSIBILITY
        or report.stop != STOP_AT_EXPRESSION_CERTIFIED
        or report.decision != EXPRESSION_CERTIFIED
    ):
        raise ValueError("WP29 report is not a certified Expression boundary")
    report_bytes = canonical_expression_certification_report_bytes(report)
    report_ref = _artifact_ref(report_bytes)
    basis = _certification_basis(
        expression_certification_id=report.certification_id,
        expression_certification_integrity=report.certification_integrity,
        decision=CERTIFIED,
        provenance_ref=report_ref,
    )
    digest = _digest(basis)
    return SliceIVCertificationReport(
        certification_id=f"slice-iv-certification-{digest[:24]}",
        certification_integrity=digest,
        **basis,
    )


def slice_iv_certification_report_as_dict(
    report: SliceIVCertificationReport,
) -> dict[str, object]:
    report.__post_init__()
    return asdict(report)


def canonical_slice_iv_certification_report_bytes(
    report: SliceIVCertificationReport,
) -> bytes:
    return _canonical_bytes(slice_iv_certification_report_as_dict(report))


def slice_iv_certification_report_from_dict(
    value: Mapping[str, object],
) -> SliceIVCertificationReport:
    if not isinstance(value, Mapping):
        raise TypeError("Slice IV Certification Report must be a mapping")
    expected_fields = {
        "certification_id",
        "certification_integrity",
        "schema_version",
        "certification_version",
        "expression_certification_id",
        "expression_certification_integrity",
        "decision",
        "provenance_ref",
        "responsibility",
        "stop",
    }
    if set(value) != expected_fields:
        raise ValueError("Slice IV Certification fields do not match WP30")
    return SliceIVCertificationReport(**dict(value))


__all__: tuple[str, ...] = ()
