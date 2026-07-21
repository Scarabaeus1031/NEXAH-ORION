"""Declarative, provider-independent operator inventory for Phase 5A."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re

from .transformation_contracts import DEFAULT_TRANSITION_CONTRACTS


OPERATOR_REGISTRY_SCHEMA = "orion.operator-registry/0.1-draft"

_EVIDENCE_PATTERN = re.compile(r"^E[0-4](?:–E[0-4])?$")
_TRANSITION_PATTERN = re.compile(r"^T[0-9]{2}$")
_CONTRACT_COMPATIBILITY_PATTERN = re.compile(r"^(T[0-9]{2})@(.+)$")


class OperatorStatus(str, Enum):
    """Explicit architectural lifecycle; values are never inferred."""

    UNKNOWN = "unknown"
    CANDIDATE = "candidate"
    DOCUMENTED = "documented"
    VERIFIED = "verified"
    EXPERIMENTAL = "experimental"
    RETIRED = "retired"


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be non-empty text")


def _freeze_unique_text(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    frozen = tuple(values)
    if any(not isinstance(value, str) or not value.strip() for value in frozen):
        raise ValueError(f"{field_name} entries must be non-empty text")
    if len(set(frozen)) != len(frozen):
        raise ValueError(f"{field_name} entries must be unique")
    return frozen


@dataclass(frozen=True, slots=True)
class OperatorReference:
    """Stable reference to a versioned registry entry."""

    operator_id: str
    operator_version: str

    def __post_init__(self) -> None:
        _require_text(self.operator_id, "operator_id")
        _require_text(self.operator_version, "operator_version")


@dataclass(frozen=True, slots=True)
class OperatorSpecification:
    """Immutable operator metadata; it contains no callable implementation."""

    operator_id: str
    operator_name: str
    operator_version: str
    status: OperatorStatus
    evidence_level: str
    implemented_transition_ids: tuple[str, ...]
    supported_contract_versions: tuple[str, ...]
    supported_representation_versions: tuple[str, ...]
    owner: str
    provider_dependencies: tuple[str, ...]
    renderer_dependencies: tuple[str, ...]
    required_parameters: tuple[str, ...]
    optional_parameters: tuple[str, ...]
    declared_invariants: tuple[str, ...]
    declared_lossiness: str
    executable: bool
    notes: str

    def __post_init__(self) -> None:
        for field_name in (
            "operator_id",
            "operator_name",
            "operator_version",
            "evidence_level",
            "owner",
            "declared_lossiness",
            "notes",
        ):
            _require_text(getattr(self, field_name), field_name)
        if not isinstance(self.status, OperatorStatus):
            raise TypeError("status must be an OperatorStatus")
        if not _EVIDENCE_PATTERN.fullmatch(self.evidence_level):
            raise ValueError("evidence_level must be E0–E4 or a bounded range")
        for field_name in (
            "implemented_transition_ids",
            "supported_contract_versions",
            "supported_representation_versions",
            "provider_dependencies",
            "renderer_dependencies",
            "required_parameters",
            "optional_parameters",
            "declared_invariants",
        ):
            object.__setattr__(
                self,
                field_name,
                _freeze_unique_text(getattr(self, field_name), field_name),
            )
        if not self.implemented_transition_ids:
            raise ValueError("implemented_transition_ids must not be empty")
        if any(
            not _TRANSITION_PATTERN.fullmatch(transition_id)
            for transition_id in self.implemented_transition_ids
        ):
            raise ValueError("implemented_transition_ids entries must match Txx")
        compatible_transition_ids: set[str] = set()
        for compatibility in self.supported_contract_versions:
            match = _CONTRACT_COMPATIBILITY_PATTERN.fullmatch(compatibility)
            if match is None:
                raise ValueError(
                    "supported_contract_versions entries must use Txx@version"
                )
            compatible_transition_ids.add(match.group(1))
        if compatible_transition_ids != set(self.implemented_transition_ids):
            raise ValueError(
                "each implemented transition requires explicit contract compatibility"
            )
        if set(self.required_parameters) & set(self.optional_parameters):
            raise ValueError("required and optional parameters must be disjoint")
        if not isinstance(self.executable, bool):
            raise TypeError("executable must be a boolean")
        if self.executable:
            raise ValueError("Phase 5A operator specifications are never executable")

    @property
    def reference(self) -> OperatorReference:
        return OperatorReference(self.operator_id, self.operator_version)

    def supports_contract(self, transition_id: str, contract_version: str) -> bool:
        """Report declared compatibility without selecting or executing an operator."""

        return (
            transition_id in self.implemented_transition_ids
            and f"{transition_id}@{contract_version}"
            in self.supported_contract_versions
        )

    def supports_representation(self, representation_version: str) -> bool:
        """Report explicitly declared representation-version compatibility."""

        return representation_version in self.supported_representation_versions


@dataclass(frozen=True, slots=True)
class OperatorRegistry:
    """Deterministic lookup catalog; it never selects, ranks, loads, or executes."""

    operators: tuple[OperatorSpecification, ...]
    registry_version: str = OPERATOR_REGISTRY_SCHEMA

    def __post_init__(self) -> None:
        frozen = tuple(self.operators)
        _require_text(self.registry_version, "registry_version")
        if any(not isinstance(item, OperatorSpecification) for item in frozen):
            raise TypeError("operators must contain OperatorSpecification records")
        operator_ids = tuple(item.operator_id for item in frozen)
        if len(set(operator_ids)) != len(operator_ids):
            raise ValueError("operator IDs must be unique")
        object.__setattr__(self, "operators", frozen)

    def get(self, operator_id: str) -> OperatorSpecification | None:
        """Return an exact ID match, if it is registered."""

        return next(
            (item for item in self.operators if item.operator_id == operator_id),
            None,
        )

    def for_transition(
        self,
        transition_id: str,
    ) -> tuple[OperatorSpecification, ...]:
        """Return all declarations in registry order; make no choice between them."""

        return tuple(
            item
            for item in self.operators
            if transition_id in item.implemented_transition_ids
        )


def _placeholder(transition_id: str) -> OperatorSpecification:
    contract = DEFAULT_TRANSITION_CONTRACTS.get(transition_id)
    if contract is None:  # guarded by construction and repository checks
        raise ValueError(f"missing Transition Contract for {transition_id}")
    return OperatorSpecification(
        operator_id=f"orion.operator.placeholder/{transition_id}",
        operator_name=f"{transition_id} operator placeholder",
        operator_version="0.1-draft",
        status=OperatorStatus(contract.operator_status),
        evidence_level=contract.evidence_level,
        implemented_transition_ids=(transition_id,),
        supported_contract_versions=(
            f"{transition_id}@{contract.contract_version}",
        ),
        supported_representation_versions=(),
        owner="NEXAH ORION capability inventory; implementation owner unassigned",
        provider_dependencies=(),
        renderer_dependencies=(),
        required_parameters=contract.required_parameters,
        optional_parameters=contract.optional_parameters,
        declared_invariants=contract.preserved_invariants,
        declared_lossiness=(
            f"Declared by {contract.documentation_ref} under Lossiness"
        ),
        executable=False,
        notes="Declarative placeholder only; no operator implementation exists.",
    )


DEFAULT_OPERATOR_REGISTRY = OperatorRegistry(
    operators=tuple(
        _placeholder(f"T{number:02d}")
        for number in range(1, 16)
    )
)
