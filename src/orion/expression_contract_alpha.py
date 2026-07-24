"""Immutable Expression Contract for Vertical Slice IV WP26.

WP26 binds the exact certified Slice III Orientation Map lineage and explicit
communicative declarations into one deterministic contract. It performs no
Expression construction, formatting, communication, conformance,
certification, interpretation, Runtime work, or downstream execution.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import re
from typing import Mapping

from orion.orientation_map_conformance_alpha import (
    ACCEPTED,
    STOP_AFTER_ORIENTATION_MAP_CONFORMANCE,
    OrientationMapConformanceReport,
    canonical_orientation_map_conformance_report_bytes,
)
from orion.orientation_map_construction_alpha import (
    ConstructedOrientationMap,
    canonical_constructed_orientation_map_bytes,
)
from orion.orientation_map_object_alpha import (
    OrientationMapObject,
    canonical_orientation_map_object_bytes,
)
from orion.slice_iii_certification_alpha import (
    PASSED,
    STOP_AT_SLICE_III_CERTIFIED,
    SliceIIICertificationReport,
    canonical_slice_iii_certification_report_bytes,
)


EXPRESSION_CONTRACT_SCHEMA_VERSION = "orion.expression-contract/0.1-alpha"
EXPRESSION_CONTRACT_VERSION = "0.1-alpha"
SERIALIZATION_VERSION = "canonical-json/1"
STATUS = "contract_defined"
RESPONSIBILITY = "expression_contract"
STOP_AT_EXPRESSION_CONTRACT = "at_expression_contract"

PERMITTED_COMMUNICATIVE_SCOPE = (
    "canonical_order",
    "certified_boundaries",
    "declared_absence",
    "orientation_map_entries",
    "orientation_map_identity",
    "provenance",
    "structural_adjacency",
)

_CONTRACT_ID = re.compile(r"^expression-contract-[0-9a-f]{24}$")
_DECLARATION = re.compile(r"^[a-z][a-z0-9_]*$")
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


def _require_declarations(
    values: tuple[str, ...],
    field_name: str,
    *,
    permitted: tuple[str, ...] | None = None,
) -> None:
    if not isinstance(values, tuple) or not values:
        raise ValueError(f"{field_name} must be a non-empty tuple")
    if any(
        not isinstance(value, str)
        or _DECLARATION.fullmatch(value) is None
        for value in values
    ):
        raise ValueError(
            f"{field_name} must contain canonical declaration identifiers"
        )
    if values != tuple(sorted(set(values))):
        raise ValueError(
            f"{field_name} must be unique and canonically ordered"
        )
    if permitted is not None and any(value not in permitted for value in values):
        raise ValueError(f"{field_name} contains an undeclared scope")


def _contract_basis(
    *,
    slice_iii_certification_id: str,
    slice_iii_certification_ref: str,
    orientation_map_conformance_id: str,
    orientation_map_conformance_ref: str,
    orientation_map_id: str,
    orientation_map_ref: str,
    orientation_map_construction_id: str,
    orientation_map_construction_ref: str,
    provenance_ref: str,
    communicative_scope: tuple[str, ...],
    declared_lossiness: tuple[str, ...],
    declared_exclusions: tuple[str, ...],
) -> dict[str, object]:
    return {
        "schema_version": EXPRESSION_CONTRACT_SCHEMA_VERSION,
        "contract_version": EXPRESSION_CONTRACT_VERSION,
        "slice_iii_certification_id": slice_iii_certification_id,
        "slice_iii_certification_ref": slice_iii_certification_ref,
        "orientation_map_conformance_id": orientation_map_conformance_id,
        "orientation_map_conformance_ref": orientation_map_conformance_ref,
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
        "serialization_version": SERIALIZATION_VERSION,
        "status": STATUS,
        "responsibility": RESPONSIBILITY,
        "stop": STOP_AT_EXPRESSION_CONTRACT,
    }


@dataclass(frozen=True, slots=True)
class ExpressionContract:
    """One immutable Expression authority definition with no Expression."""

    contract_id: str
    contract_integrity: str
    schema_version: str
    contract_version: str
    slice_iii_certification_id: str
    slice_iii_certification_ref: str
    orientation_map_conformance_id: str
    orientation_map_conformance_ref: str
    orientation_map_id: str
    orientation_map_ref: str
    orientation_map_construction_id: str
    orientation_map_construction_ref: str
    provenance_ref: str
    communicative_scope: tuple[str, ...]
    declared_lossiness: tuple[str, ...]
    declared_exclusions: tuple[str, ...]
    serialization_version: str
    status: str
    responsibility: str
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
        if _CONTRACT_ID.fullmatch(self.contract_id) is None:
            raise ValueError("contract_id is not canonical")
        if _SHA256_HEX.fullmatch(self.contract_integrity) is None:
            raise ValueError("contract_integrity must be SHA-256 hexadecimal")
        if self.schema_version != EXPRESSION_CONTRACT_SCHEMA_VERSION:
            raise ValueError("Expression Contract schema version changed")
        if self.contract_version != EXPRESSION_CONTRACT_VERSION:
            raise ValueError("Expression Contract version changed")
        for field_name in (
            "slice_iii_certification_id",
            "orientation_map_conformance_id",
            "orientation_map_id",
            "orientation_map_construction_id",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"{field_name} must be exact non-empty text")
        for field_name in (
            "slice_iii_certification_ref",
            "orientation_map_conformance_ref",
            "orientation_map_ref",
            "orientation_map_construction_ref",
            "provenance_ref",
        ):
            _require_sha256_ref(getattr(self, field_name), field_name)
        if self.provenance_ref != self.slice_iii_certification_ref:
            raise ValueError(
                "Expression provenance must name Slice III Certification"
            )
        _require_declarations(
            self.communicative_scope,
            "communicative_scope",
            permitted=PERMITTED_COMMUNICATIVE_SCOPE,
        )
        _require_declarations(
            self.declared_lossiness,
            "declared_lossiness",
        )
        _require_declarations(
            self.declared_exclusions,
            "declared_exclusions",
        )
        if self.serialization_version != SERIALIZATION_VERSION:
            raise ValueError("Expression Contract serialization changed")
        if self.status != STATUS:
            raise ValueError("Expression Contract status changed")
        if self.responsibility != RESPONSIBILITY:
            raise ValueError("Expression Contract responsibility changed")
        if self.stop != STOP_AT_EXPRESSION_CONTRACT:
            raise ValueError("WP26 STOP boundary changed")
        basis = _contract_basis(
            slice_iii_certification_id=self.slice_iii_certification_id,
            slice_iii_certification_ref=self.slice_iii_certification_ref,
            orientation_map_conformance_id=(
                self.orientation_map_conformance_id
            ),
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
        )
        digest = _digest(basis)
        if self.contract_id != f"expression-contract-{digest[:24]}":
            raise ValueError("contract_id differs from canonical identity basis")
        if self.contract_integrity != digest:
            raise ValueError(
                "contract_integrity differs from canonical identity basis"
            )


@dataclass(frozen=True, slots=True)
class ExpressionContractValidation:
    """Deterministic validation of one supplied Expression Contract."""

    valid: bool
    checks: tuple[str, ...]
    errors: tuple[str, ...]
    stop: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "checks", tuple(self.checks))
        object.__setattr__(self, "errors", tuple(self.errors))
        if type(self.valid) is not bool:
            raise TypeError("valid must be boolean")
        if any(not isinstance(item, str) or not item for item in self.checks):
            raise ValueError("checks must contain deterministic labels")
        if any(not isinstance(item, str) or not item for item in self.errors):
            raise ValueError("errors must contain deterministic text")
        if self.valid != (not self.errors):
            raise ValueError("validation state must match errors")
        if self.stop != STOP_AT_EXPRESSION_CONTRACT:
            raise ValueError("Contract validation crossed the WP26 STOP")


def _validated_lineage_refs(
    slice_iii_certification: SliceIIICertificationReport,
    orientation_map_conformance: OrientationMapConformanceReport,
    orientation_map: OrientationMapObject,
    constructed_map: ConstructedOrientationMap,
) -> tuple[str, str, str, str]:
    inputs = (
        (
            slice_iii_certification,
            SliceIIICertificationReport,
            "Slice III Certification",
        ),
        (
            orientation_map_conformance,
            OrientationMapConformanceReport,
            "Orientation Map Conformance",
        ),
        (orientation_map, OrientationMapObject, "Orientation Map Object"),
        (
            constructed_map,
            ConstructedOrientationMap,
            "Constructed Orientation Map",
        ),
    )
    for value, expected, name in inputs:
        if not isinstance(value, expected):
            raise TypeError(f"WP26 requires immutable {name}")
        value.__post_init__()

    certification_ref = _artifact_ref(
        canonical_slice_iii_certification_report_bytes(
            slice_iii_certification
        )
    )
    conformance_ref = _artifact_ref(
        canonical_orientation_map_conformance_report_bytes(
            orientation_map_conformance
        )
    )
    orientation_map_ref = _artifact_ref(
        canonical_orientation_map_object_bytes(orientation_map)
    )
    construction_ref = _artifact_ref(
        canonical_constructed_orientation_map_bytes(constructed_map)
    )
    if (
        not slice_iii_certification.certified
        or slice_iii_certification.status != PASSED
        or slice_iii_certification.errors
        or slice_iii_certification.stop != STOP_AT_SLICE_III_CERTIFIED
    ):
        raise ValueError("Slice III Certification Gate has not passed")
    if (
        not orientation_map_conformance.valid
        or orientation_map_conformance.decision != ACCEPTED
        or orientation_map_conformance.errors
        or orientation_map_conformance.stop
        != STOP_AFTER_ORIENTATION_MAP_CONFORMANCE
    ):
        raise ValueError("Orientation Map Conformance has not accepted inputs")
    if (
        slice_iii_certification.orientation_map_id
        != orientation_map.orientation_map_id
        or slice_iii_certification.orientation_map_ref
        != orientation_map_ref
        or slice_iii_certification.orientation_map_construction_id
        != constructed_map.construction_id
        or slice_iii_certification.orientation_map_construction_ref
        != construction_ref
        or slice_iii_certification.orientation_map_conformance_id
        != orientation_map_conformance.report_id
        or slice_iii_certification.orientation_map_conformance_ref
        != conformance_ref
        or orientation_map_conformance.orientation_map_id
        != orientation_map.orientation_map_id
        or orientation_map_conformance.orientation_map_ref
        != orientation_map_ref
        or orientation_map_conformance.construction_id
        != constructed_map.construction_id
        or orientation_map_conformance.construction_ref
        != construction_ref
        or orientation_map_conformance.accepted_orientation_map_ref
        != orientation_map_ref
        or orientation_map_conformance.accepted_construction_ref
        != construction_ref
        or constructed_map.orientation_map_id
        != orientation_map.orientation_map_id
        or constructed_map.orientation_map_contract_ref
        != orientation_map_ref
    ):
        raise ValueError("WP26 inputs do not share exact certified lineage")
    return (
        certification_ref,
        conformance_ref,
        orientation_map_ref,
        construction_ref,
    )


def create_expression_contract(
    slice_iii_certification: SliceIIICertificationReport,
    orientation_map_conformance: OrientationMapConformanceReport,
    orientation_map: OrientationMapObject,
    constructed_map: ConstructedOrientationMap,
    *,
    communicative_scope: tuple[str, ...],
    declared_lossiness: tuple[str, ...],
    declared_exclusions: tuple[str, ...],
) -> ExpressionContract:
    """Bind exact certified inputs and declarations without expressing them."""

    _require_declarations(
        communicative_scope,
        "communicative_scope",
        permitted=PERMITTED_COMMUNICATIVE_SCOPE,
    )
    _require_declarations(declared_lossiness, "declared_lossiness")
    _require_declarations(declared_exclusions, "declared_exclusions")
    (
        certification_ref,
        conformance_ref,
        orientation_map_ref,
        construction_ref,
    ) = _validated_lineage_refs(
        slice_iii_certification,
        orientation_map_conformance,
        orientation_map,
        constructed_map,
    )
    basis = _contract_basis(
        slice_iii_certification_id=(
            slice_iii_certification.certification_id
        ),
        slice_iii_certification_ref=certification_ref,
        orientation_map_conformance_id=(
            orientation_map_conformance.report_id
        ),
        orientation_map_conformance_ref=conformance_ref,
        orientation_map_id=orientation_map.orientation_map_id,
        orientation_map_ref=orientation_map_ref,
        orientation_map_construction_id=constructed_map.construction_id,
        orientation_map_construction_ref=construction_ref,
        provenance_ref=certification_ref,
        communicative_scope=communicative_scope,
        declared_lossiness=declared_lossiness,
        declared_exclusions=declared_exclusions,
    )
    digest = _digest(basis)
    return ExpressionContract(
        contract_id=f"expression-contract-{digest[:24]}",
        contract_integrity=digest,
        **basis,
    )


def validate_expression_contract(
    slice_iii_certification: SliceIIICertificationReport,
    orientation_map_conformance: OrientationMapConformanceReport,
    orientation_map: OrientationMapObject,
    constructed_map: ConstructedOrientationMap,
    contract: ExpressionContract,
) -> ExpressionContractValidation:
    """Validate contract shape and exact lineage without constructing Expression."""

    checks: list[str] = []
    errors: list[str] = []

    def check(name: str, condition: bool, error: str) -> None:
        checks.append(name)
        if not condition:
            errors.append(error)

    try:
        contract.__post_init__()
        checks.append("contract_shape_valid")
    except (AttributeError, TypeError, ValueError) as exc:
        checks.append("contract_shape_valid")
        errors.append(str(exc))

    expected = None
    try:
        expected = create_expression_contract(
            slice_iii_certification,
            orientation_map_conformance,
            orientation_map,
            constructed_map,
            communicative_scope=contract.communicative_scope,
            declared_lossiness=contract.declared_lossiness,
            declared_exclusions=contract.declared_exclusions,
        )
        checks.append("certified_lineage_valid")
    except (AttributeError, TypeError, ValueError) as exc:
        checks.append("certified_lineage_valid")
        errors.append(str(exc))

    check(
        "contract_identity_exact",
        expected is not None
        and contract.contract_id == expected.contract_id
        and contract.contract_integrity == expected.contract_integrity,
        "Expression Contract identity or integrity differs",
    )
    check(
        "contract_references_exact",
        expected is not None and contract == expected,
        "Expression Contract differs from exact certified inputs",
    )
    check(
        "wp26_stop_preserved",
        contract.stop == STOP_AT_EXPRESSION_CONTRACT,
        "Expression Contract crossed the WP26 STOP",
    )
    return ExpressionContractValidation(
        valid=not errors,
        checks=tuple(checks),
        errors=tuple(errors),
        stop=STOP_AT_EXPRESSION_CONTRACT,
    )


def expression_contract_as_dict(
    contract: ExpressionContract,
) -> dict[str, object]:
    contract.__post_init__()
    return asdict(contract)


def canonical_expression_contract_bytes(contract: ExpressionContract) -> bytes:
    return _canonical_bytes(expression_contract_as_dict(contract))


def expression_contract_from_dict(
    value: Mapping[str, object],
) -> ExpressionContract:
    if not isinstance(value, Mapping):
        raise TypeError("Expression Contract must be a mapping")
    expected_fields = {
        "contract_id",
        "contract_integrity",
        "schema_version",
        "contract_version",
        "slice_iii_certification_id",
        "slice_iii_certification_ref",
        "orientation_map_conformance_id",
        "orientation_map_conformance_ref",
        "orientation_map_id",
        "orientation_map_ref",
        "orientation_map_construction_id",
        "orientation_map_construction_ref",
        "provenance_ref",
        "communicative_scope",
        "declared_lossiness",
        "declared_exclusions",
        "serialization_version",
        "status",
        "responsibility",
        "stop",
    }
    if set(value) != expected_fields:
        raise ValueError("Expression Contract fields do not match WP26")
    ordered_fields = (
        "communicative_scope",
        "declared_lossiness",
        "declared_exclusions",
    )
    converted = dict(value)
    for field_name in ordered_fields:
        field_value = converted[field_name]
        if not isinstance(field_value, (tuple, list)):
            raise TypeError(f"{field_name} must be ordered")
        converted[field_name] = tuple(field_value)
    return ExpressionContract(**converted)


__all__: tuple[str, ...] = ()
