"""Deterministic Expression Artifact construction for Slice IV WP27.

WP27 consumes one immutable WP26 Expression Contract and materializes only the
authority and certified references already declared by that contract. It does
not reopen upstream artifacts, generate language, interpret, validate external
conformance, certify, present, or execute downstream behavior.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import re
from typing import Mapping

from orion.expression_contract_alpha import (
    EXPRESSION_CONTRACT_SCHEMA_VERSION,
    EXPRESSION_CONTRACT_VERSION,
    STATUS as CONTRACT_STATUS,
    STOP_AT_EXPRESSION_CONTRACT,
    ExpressionContract,
    canonical_expression_contract_bytes,
)


EXPRESSION_ARTIFACT_SCHEMA_VERSION = "orion.expression-artifact/0.1-alpha"
SERIALIZATION_VERSION = "canonical-json/1"
CONSTRUCTION_STATE = "constructed_unvalidated"
RESPONSIBILITY = "expression_construction"
STOP_AFTER_EXPRESSION_CONSTRUCTION = "after_expression_construction"

_EXPRESSION_ID = re.compile(r"^expression-[0-9a-f]{24}$")
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


def _require_sha256_ref(value: str, field_name: str) -> None:
    if not isinstance(value, str) or _SHA256_REF.fullmatch(value) is None:
        raise ValueError(f"{field_name} must be a SHA-256 reference")


def _construction_basis(
    *,
    expression_contract_id: str,
    expression_contract_integrity: str,
    expression_contract_ref: str,
    expression_contract_schema_version: str,
    expression_contract_version: str,
    expression_contract_status: str,
    slice_iii_certification_ref: str,
    orientation_map_conformance_ref: str,
    orientation_map_id: str,
    orientation_map_ref: str,
    orientation_map_construction_id: str,
    orientation_map_construction_ref: str,
    provenance_ref: str,
    communicative_scope: tuple[str, ...],
    declared_lossiness: tuple[str, ...],
    declared_exclusions: tuple[str, ...],
    canonical_order: int,
) -> dict[str, object]:
    return {
        "schema_version": EXPRESSION_ARTIFACT_SCHEMA_VERSION,
        "expression_contract_id": expression_contract_id,
        "expression_contract_integrity": expression_contract_integrity,
        "expression_contract_ref": expression_contract_ref,
        "expression_contract_schema_version": (
            expression_contract_schema_version
        ),
        "expression_contract_version": expression_contract_version,
        "expression_contract_status": expression_contract_status,
        "slice_iii_certification_ref": slice_iii_certification_ref,
        "orientation_map_conformance_ref": (
            orientation_map_conformance_ref
        ),
        "orientation_map_id": orientation_map_id,
        "orientation_map_ref": orientation_map_ref,
        "orientation_map_construction_id": (
            orientation_map_construction_id
        ),
        "orientation_map_construction_ref": (
            orientation_map_construction_ref
        ),
        "provenance_ref": provenance_ref,
        "communicative_scope": communicative_scope,
        "declared_lossiness": declared_lossiness,
        "declared_exclusions": declared_exclusions,
        "canonical_order": canonical_order,
        "serialization_version": SERIALIZATION_VERSION,
        "construction_state": CONSTRUCTION_STATE,
        "responsibility": RESPONSIBILITY,
        "externally_conformant": False,
        "stop": STOP_AFTER_EXPRESSION_CONSTRUCTION,
    }


@dataclass(frozen=True, slots=True)
class ExpressionArtifact:
    """One immutable, unvalidated materialization of a WP26 contract."""

    expression_id: str
    expression_integrity: str
    schema_version: str
    expression_contract_id: str
    expression_contract_integrity: str
    expression_contract_ref: str
    expression_contract_schema_version: str
    expression_contract_version: str
    expression_contract_status: str
    slice_iii_certification_ref: str
    orientation_map_conformance_ref: str
    orientation_map_id: str
    orientation_map_ref: str
    orientation_map_construction_id: str
    orientation_map_construction_ref: str
    provenance_ref: str
    communicative_scope: tuple[str, ...]
    declared_lossiness: tuple[str, ...]
    declared_exclusions: tuple[str, ...]
    canonical_order: int
    serialization_version: str
    construction_state: str
    responsibility: str
    externally_conformant: bool
    stop: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "communicative_scope",
            tuple(self.communicative_scope),
        )
        object.__setattr__(
            self,
            "declared_lossiness",
            tuple(self.declared_lossiness),
        )
        object.__setattr__(
            self,
            "declared_exclusions",
            tuple(self.declared_exclusions),
        )
        if _EXPRESSION_ID.fullmatch(self.expression_id) is None:
            raise ValueError("expression_id is not canonical")
        for field_name in (
            "expression_integrity",
            "expression_contract_integrity",
        ):
            if _SHA256_HEX.fullmatch(getattr(self, field_name)) is None:
                raise ValueError(f"{field_name} must be SHA-256 hexadecimal")
        if self.schema_version != EXPRESSION_ARTIFACT_SCHEMA_VERSION:
            raise ValueError("Expression Artifact schema version changed")
        if (
            not isinstance(self.expression_contract_id, str)
            or not self.expression_contract_id
        ):
            raise ValueError(
                "expression_contract_id must be exact non-empty text"
            )
        for field_name in (
            "expression_contract_ref",
            "slice_iii_certification_ref",
            "orientation_map_conformance_ref",
            "orientation_map_ref",
            "orientation_map_construction_ref",
            "provenance_ref",
        ):
            _require_sha256_ref(getattr(self, field_name), field_name)
        for field_name in (
            "orientation_map_id",
            "orientation_map_construction_id",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{field_name} must be exact non-empty text")
        if (
            self.expression_contract_schema_version
            != EXPRESSION_CONTRACT_SCHEMA_VERSION
        ):
            raise ValueError("bound Expression Contract schema changed")
        if self.expression_contract_version != EXPRESSION_CONTRACT_VERSION:
            raise ValueError("bound Expression Contract version changed")
        if self.expression_contract_status != CONTRACT_STATUS:
            raise ValueError("bound Expression Contract status changed")
        if self.provenance_ref != self.slice_iii_certification_ref:
            raise ValueError(
                "Expression provenance must preserve Slice III Certification"
            )
        if (
            not self.communicative_scope
            or not self.declared_lossiness
            or not self.declared_exclusions
        ):
            raise ValueError("Expression declarations must remain explicit")
        for field_name in (
            "communicative_scope",
            "declared_lossiness",
            "declared_exclusions",
        ):
            values = getattr(self, field_name)
            if values != tuple(sorted(set(values))):
                raise ValueError(
                    f"{field_name} must preserve canonical declaration order"
                )
        if type(self.canonical_order) is not int or self.canonical_order != 0:
            raise ValueError("the atomic Expression Artifact order is zero")
        if self.serialization_version != SERIALIZATION_VERSION:
            raise ValueError("Expression Artifact serialization changed")
        if self.construction_state != CONSTRUCTION_STATE:
            raise ValueError("WP27 artifact must remain unvalidated")
        if self.responsibility != RESPONSIBILITY:
            raise ValueError("Expression construction responsibility changed")
        if (
            type(self.externally_conformant) is not bool
            or self.externally_conformant
        ):
            raise ValueError("WP27 cannot claim External Conformance")
        if self.stop != STOP_AFTER_EXPRESSION_CONSTRUCTION:
            raise ValueError("WP27 STOP boundary changed")
        basis = _construction_basis(
            expression_contract_id=self.expression_contract_id,
            expression_contract_integrity=self.expression_contract_integrity,
            expression_contract_ref=self.expression_contract_ref,
            expression_contract_schema_version=(
                self.expression_contract_schema_version
            ),
            expression_contract_version=self.expression_contract_version,
            expression_contract_status=self.expression_contract_status,
            slice_iii_certification_ref=self.slice_iii_certification_ref,
            orientation_map_conformance_ref=(
                self.orientation_map_conformance_ref
            ),
            orientation_map_id=self.orientation_map_id,
            orientation_map_ref=self.orientation_map_ref,
            orientation_map_construction_id=(
                self.orientation_map_construction_id
            ),
            orientation_map_construction_ref=(
                self.orientation_map_construction_ref
            ),
            provenance_ref=self.provenance_ref,
            communicative_scope=self.communicative_scope,
            declared_lossiness=self.declared_lossiness,
            declared_exclusions=self.declared_exclusions,
            canonical_order=self.canonical_order,
        )
        digest = _digest(basis)
        if self.expression_id != f"expression-{digest[:24]}":
            raise ValueError("expression_id differs from construction basis")
        if self.expression_integrity != digest:
            raise ValueError(
                "expression_integrity differs from construction basis"
            )


def construct_expression(contract: ExpressionContract) -> ExpressionArtifact:
    """Materialize only the immutable authority already bound by WP26."""

    if not isinstance(contract, ExpressionContract):
        raise TypeError("WP27 accepts only an immutable Expression Contract")
    contract.__post_init__()
    if contract.stop != STOP_AT_EXPRESSION_CONTRACT:
        raise ValueError("WP26 contract did not stop at its frozen boundary")
    contract_ref = _artifact_ref(canonical_expression_contract_bytes(contract))
    basis = _construction_basis(
        expression_contract_id=contract.contract_id,
        expression_contract_integrity=contract.contract_integrity,
        expression_contract_ref=contract_ref,
        expression_contract_schema_version=contract.schema_version,
        expression_contract_version=contract.contract_version,
        expression_contract_status=contract.status,
        slice_iii_certification_ref=contract.slice_iii_certification_ref,
        orientation_map_conformance_ref=(
            contract.orientation_map_conformance_ref
        ),
        orientation_map_id=contract.orientation_map_id,
        orientation_map_ref=contract.orientation_map_ref,
        orientation_map_construction_id=(
            contract.orientation_map_construction_id
        ),
        orientation_map_construction_ref=(
            contract.orientation_map_construction_ref
        ),
        provenance_ref=contract.provenance_ref,
        communicative_scope=contract.communicative_scope,
        declared_lossiness=contract.declared_lossiness,
        declared_exclusions=contract.declared_exclusions,
        canonical_order=0,
    )
    digest = _digest(basis)
    return ExpressionArtifact(
        expression_id=f"expression-{digest[:24]}",
        expression_integrity=digest,
        **basis,
    )


def expression_artifact_as_dict(
    artifact: ExpressionArtifact,
) -> dict[str, object]:
    artifact.__post_init__()
    return asdict(artifact)


def canonical_expression_artifact_bytes(
    artifact: ExpressionArtifact,
) -> bytes:
    return _canonical_bytes(expression_artifact_as_dict(artifact))


def expression_artifact_from_dict(
    value: Mapping[str, object],
) -> ExpressionArtifact:
    if not isinstance(value, Mapping):
        raise TypeError("Expression Artifact must be a mapping")
    expected_fields = {
        "expression_id",
        "expression_integrity",
        "schema_version",
        "expression_contract_id",
        "expression_contract_integrity",
        "expression_contract_ref",
        "expression_contract_schema_version",
        "expression_contract_version",
        "expression_contract_status",
        "slice_iii_certification_ref",
        "orientation_map_conformance_ref",
        "orientation_map_id",
        "orientation_map_ref",
        "orientation_map_construction_id",
        "orientation_map_construction_ref",
        "provenance_ref",
        "communicative_scope",
        "declared_lossiness",
        "declared_exclusions",
        "canonical_order",
        "serialization_version",
        "construction_state",
        "responsibility",
        "externally_conformant",
        "stop",
    }
    if set(value) != expected_fields:
        raise ValueError("Expression Artifact fields do not match WP27")
    converted = dict(value)
    for field_name in (
        "communicative_scope",
        "declared_lossiness",
        "declared_exclusions",
    ):
        field_value = converted[field_name]
        if not isinstance(field_value, (tuple, list)):
            raise TypeError(f"{field_name} must be ordered")
        converted[field_name] = tuple(field_value)
    return ExpressionArtifact(**converted)


__all__: tuple[str, ...] = ()
