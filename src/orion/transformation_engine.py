"""Deterministic Transformation Graph orchestration without operator execution."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any

from .operator_registry import DEFAULT_OPERATOR_REGISTRY, OperatorRegistry
from .transformation_contracts import (
    DEFAULT_REPRESENTATION_GRAPH,
    DEFAULT_TRANSITION_CONTRACTS,
    HARD_INVARIANTS,
    GraphEdge,
    RepresentationGraph,
    TransitionContract,
    TransitionContractRegistry,
)


TRANSFORMATION_PLAN_SCHEMA = "orion.transformation-plan/0.1"
TRANSFORMATION_REPORT_SCHEMA = "orion.transformation-report/0.1"


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


def _digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class RepresentationRef:
    """Identity and compatibility metadata for an existing representation."""

    representation_id: str
    representation_type: str
    representation_version: str
    coordinate_profile: str

    def __post_init__(self) -> None:
        for field_name in (
            "representation_id",
            "representation_type",
            "representation_version",
            "coordinate_profile",
        ):
            _require_text(getattr(self, field_name), field_name)


@dataclass(frozen=True, slots=True)
class OrientationObject:
    """Immutable planning input; the engine never mutates it."""

    orientation_object_id: str
    orientation_object_version: str
    representation: RepresentationRef
    source_references: tuple[str, ...]
    provenance: tuple[str, ...]
    epoch: str | None = None
    known_constants: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_text(self.orientation_object_id, "orientation_object_id")
        _require_text(self.orientation_object_version, "orientation_object_version")
        if not isinstance(self.representation, RepresentationRef):
            raise TypeError("representation must be a RepresentationRef")
        source_references = _freeze_unique_text(
            self.source_references,
            "source_references",
        )
        provenance = tuple(self.provenance)
        if not provenance or any(
            not isinstance(item, str) or not item.strip() for item in provenance
        ):
            raise ValueError("provenance must contain non-empty text")
        known_constants = _freeze_unique_text(self.known_constants, "known_constants")
        if self.epoch is not None:
            _require_text(self.epoch, "epoch")
        object.__setattr__(self, "source_references", source_references)
        object.__setattr__(self, "provenance", provenance)
        object.__setattr__(self, "known_constants", known_constants)

    @property
    def active_invariants(self) -> tuple[str, ...]:
        conditional = (
            *(("epoch",) if self.epoch is not None else ()),
            *(("known_constants",) if self.known_constants else ()),
        )
        return HARD_INVARIANTS + conditional


@dataclass(frozen=True, slots=True)
class RepresentationTarget:
    """Requested target type; no target representation is fabricated."""

    representation_type: str
    representation_version: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.representation_type, "representation_type")
        if self.representation_version is not None:
            _require_text(self.representation_version, "representation_version")


@dataclass(frozen=True, slots=True)
class PlannedTransition:
    sequence: int
    transition_id: str
    source_representation: str
    target_representation: str
    contract_version: str | None
    evidence_level: str
    operator_id: str | None
    operator_version: str | None
    operator_status: str
    operator_owner: str | None
    renderer_family: str | None
    required_parameters: tuple[str, ...]
    documentation_ref: str | None


@dataclass(frozen=True, slots=True)
class TransformationProvenanceStep:
    sequence: int
    transition_id: str
    contract_version: str | None
    source_representation: str
    target_representation: str
    evidence_level: str


@dataclass(frozen=True, slots=True)
class TransformationIssue:
    kind: str
    reason: str
    transition_id: str | None = None
    evidence_level: str = "unknown"

    def __post_init__(self) -> None:
        _require_text(self.kind, "kind")
        _require_text(self.reason, "reason")
        _require_text(self.evidence_level, "evidence_level")
        if self.transition_id is not None:
            _require_text(self.transition_id, "transition_id")


@dataclass(frozen=True, slots=True)
class TransformationValidation:
    valid: bool
    checks: tuple[str, ...]
    errors: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "checks", tuple(self.checks))
        object.__setattr__(self, "errors", tuple(self.errors))
        if self.valid == bool(self.errors):
            raise ValueError("validation status and errors disagree")


@dataclass(frozen=True, slots=True)
class TransformationPlan:
    """Deterministic plan; it is not a transformed representation."""

    plan_id: str
    orientation_object_id: str
    orientation_object_version: str
    source_representation_id: str
    source_representation: str
    source_representation_version: str
    target_representation: str
    target_representation_version: str | None
    graph_version: str
    contract_registry_version: str
    operator_registry_version: str
    path: tuple[PlannedTransition, ...]
    alternative_paths: tuple[tuple[str, ...], ...]
    required_invariants: tuple[str, ...]
    preserved_invariants: tuple[str, ...]
    source_references: tuple[str, ...]
    source_provenance: tuple[str, ...]
    provenance_chain: tuple[TransformationProvenanceStep, ...]
    evidence_chain: tuple[str, ...]
    schema_version: str = TRANSFORMATION_PLAN_SCHEMA

    @property
    def transition_ids(self) -> tuple[str, ...]:
        return tuple(step.transition_id for step in self.path)


@dataclass(frozen=True, slots=True)
class TransformationReport:
    """Planning outcome and explicit blockers; no operator has been executed."""

    report_id: str
    status: str
    plan: TransformationPlan
    validation: TransformationValidation
    issues: tuple[TransformationIssue, ...]
    produced_representation: None = None
    schema_version: str = TRANSFORMATION_REPORT_SCHEMA

    def __post_init__(self) -> None:
        if self.status not in ("planned", "blocked"):
            raise ValueError("status must be planned or blocked")
        if self.status == "planned" and self.issues:
            raise ValueError("a planned report cannot contain blockers")
        if self.status == "blocked" and not self.issues:
            raise ValueError("a blocked report requires at least one issue")
        if self.produced_representation is not None:
            raise ValueError("Phase 4A never produces a representation")


@dataclass(frozen=True, slots=True)
class TransformationEngine:
    """Navigate registered edges and report, but never run, transformations."""

    graph: RepresentationGraph = DEFAULT_REPRESENTATION_GRAPH
    contracts: TransitionContractRegistry = DEFAULT_TRANSITION_CONTRACTS
    operators: OperatorRegistry = DEFAULT_OPERATOR_REGISTRY

    def __post_init__(self) -> None:
        if not isinstance(self.graph, RepresentationGraph):
            raise TypeError("graph must be a RepresentationGraph")
        if not isinstance(self.contracts, TransitionContractRegistry):
            raise TypeError("contracts must be a TransitionContractRegistry")
        if not isinstance(self.operators, OperatorRegistry):
            raise TypeError("operators must be an OperatorRegistry")

    def execute(
        self,
        orientation_object: OrientationObject,
        target: RepresentationTarget,
    ) -> TransformationReport:
        if not isinstance(orientation_object, OrientationObject):
            raise TypeError("orientation_object must be an OrientationObject")
        if not isinstance(target, RepresentationTarget):
            raise TypeError("target must be a RepresentationTarget")

        source_type = orientation_object.representation.representation_type
        graph_paths = self._find_paths(source_type, target.representation_type)
        issues: list[TransformationIssue] = []
        checks: list[str] = [
            f"orientation-object:{orientation_object.orientation_object_id}:immutable",
            f"graph:{self.graph.graph_version}:explicit-edges-only",
        ]

        if not graph_paths:
            issues.append(
                TransformationIssue(
                    kind="UnsupportedPath",
                    reason=(
                        "no registered directed path from "
                        f"{source_type} to {target.representation_type}"
                    ),
                )
            )
            selected_path: tuple[GraphEdge, ...] = ()
            alternatives: tuple[tuple[str, ...], ...] = ()
        else:
            selected_path = graph_paths[0]
            alternatives = tuple(
                tuple(edge.transition_id for edge in path)
                for path in graph_paths[1:]
            )
            checks.append(
                "path:selected:"
                + ">".join(edge.transition_id for edge in selected_path)
            )

        planned_steps: list[PlannedTransition] = []
        provenance_steps: list[TransformationProvenanceStep] = []
        evidence_chain: list[str] = []
        contracts_on_path: list[TransitionContract | None] = []
        current_version: str | None = (
            orientation_object.representation.representation_version
        )

        for sequence, edge in enumerate(selected_path, start=1):
            contract = self.contracts.get(edge.transition_id)
            contracts_on_path.append(contract)
            if contract is None:
                issues.append(
                    TransformationIssue(
                        kind="MissingContract",
                        transition_id=edge.transition_id,
                        reason=(
                            f"{edge.transition_id} is registered in the graph but has "
                            "no Transition Contract"
                        ),
                    )
                )
                planned_steps.append(
                    PlannedTransition(
                        sequence=sequence,
                        transition_id=edge.transition_id,
                        source_representation=edge.source_representation,
                        target_representation=edge.target_representation,
                        contract_version=None,
                        evidence_level="unknown",
                        operator_id=None,
                        operator_version=None,
                        operator_status="unknown",
                        operator_owner=None,
                        renderer_family=None,
                        required_parameters=(),
                        documentation_ref=None,
                    )
                )
                provenance_steps.append(
                    TransformationProvenanceStep(
                        sequence=sequence,
                        transition_id=edge.transition_id,
                        contract_version=None,
                        source_representation=edge.source_representation,
                        target_representation=edge.target_representation,
                        evidence_level="unknown",
                    )
                )
                evidence_chain.append("unknown")
                current_version = None
                continue

            evidence_chain.append(contract.evidence_level)
            registered_operators = self.operators.for_transition(edge.transition_id)
            registered_operator = (
                registered_operators[0]
                if len(registered_operators) == 1
                else None
            )
            planned_steps.append(
                PlannedTransition(
                    sequence=sequence,
                    transition_id=edge.transition_id,
                    source_representation=edge.source_representation,
                    target_representation=edge.target_representation,
                    contract_version=contract.contract_version,
                    evidence_level=contract.evidence_level,
                    operator_id=(
                        registered_operator.operator_id
                        if registered_operator is not None
                        else None
                    ),
                    operator_version=(
                        registered_operator.operator_version
                        if registered_operator is not None
                        else None
                    ),
                    operator_status=(
                        registered_operator.status.value
                        if registered_operator is not None
                        else contract.operator_status
                    ),
                    operator_owner=(
                        registered_operator.owner
                        if registered_operator is not None
                        else None
                    ),
                    renderer_family=contract.renderer_family,
                    required_parameters=contract.required_parameters,
                    documentation_ref=contract.documentation_ref,
                )
            )
            provenance_steps.append(
                TransformationProvenanceStep(
                    sequence=sequence,
                    transition_id=edge.transition_id,
                    contract_version=contract.contract_version,
                    source_representation=edge.source_representation,
                    target_representation=edge.target_representation,
                    evidence_level=contract.evidence_level,
                )
            )

            if (
                contract.source_representation != edge.source_representation
                or contract.target_representation != edge.target_representation
            ):
                issues.append(
                    TransformationIssue(
                        kind="ContractIncompatible",
                        transition_id=edge.transition_id,
                        evidence_level=contract.evidence_level,
                        reason=(
                            f"{edge.transition_id} contract endpoints do not match "
                            "the registered graph edge"
                        ),
                    )
                )
            else:
                checks.append(f"contract:{edge.transition_id}:edge-compatible")

            if (
                contract.supported_source_versions
                and current_version not in contract.supported_source_versions
            ):
                issues.append(
                    TransformationIssue(
                        kind="ContractIncompatible",
                        transition_id=edge.transition_id,
                        evidence_level=contract.evidence_level,
                        reason=(
                            f"{edge.transition_id} does not support source version "
                            f"{current_version or 'unknown'}"
                        ),
                    )
                )

            missing_invariants = tuple(
                invariant
                for invariant in orientation_object.active_invariants
                if invariant not in contract.preserved_invariants
            )
            if missing_invariants:
                issues.append(
                    TransformationIssue(
                        kind="InvariantViolation",
                        transition_id=edge.transition_id,
                        evidence_level=contract.evidence_level,
                        reason=(
                            f"{edge.transition_id} does not preserve required "
                            f"invariant(s): {', '.join(missing_invariants)}"
                        ),
                    )
                )
            else:
                checks.append(f"contract:{edge.transition_id}:invariants-preserved")

            if not registered_operators:
                operator_reason = (
                    f"{edge.transition_id} has no Operator Registry entry"
                )
            elif len(registered_operators) > 1:
                operator_reason = (
                    f"{edge.transition_id} has multiple Operator Registry entries; "
                    "the registry and engine do not select between operators"
                )
            elif not registered_operator.supports_contract(
                edge.transition_id,
                contract.contract_version,
            ):
                operator_reason = (
                    f"{registered_operator.operator_id} does not declare support for "
                    f"{edge.transition_id}@{contract.contract_version}"
                )
            elif not registered_operator.executable:
                operator_reason = (
                    f"{registered_operator.operator_id} is "
                    f"{registered_operator.status.value} and executable=false; "
                    "no executable operator is registered"
                )
            else:  # Phase 5A records reject executable=true during construction.
                operator_reason = ""

            if operator_reason:
                issues.append(
                    TransformationIssue(
                        kind="MissingOperator",
                        transition_id=edge.transition_id,
                        evidence_level=(
                            registered_operator.evidence_level
                            if registered_operator is not None
                            else contract.evidence_level
                        ),
                        reason=operator_reason,
                    )
                )
            if not contract.has_renderer:
                issues.append(
                    TransformationIssue(
                        kind="MissingRenderer",
                        transition_id=edge.transition_id,
                        evidence_level=contract.evidence_level,
                        reason=(
                            f"{edge.transition_id} requires {contract.renderer_family}; "
                            "no renderer is registered"
                        ),
                    )
                )

            is_last = sequence == len(selected_path)
            next_version = contract.target_representation_version
            if is_last and target.representation_version is not None:
                if (
                    next_version is not None
                    and next_version != target.representation_version
                ):
                    issues.append(
                        TransformationIssue(
                            kind="ContractIncompatible",
                            transition_id=edge.transition_id,
                            evidence_level=contract.evidence_level,
                            reason=(
                                f"{edge.transition_id} produces version {next_version}, "
                                f"not requested version {target.representation_version}"
                            ),
                        )
                    )
                next_version = target.representation_version
            current_version = next_version

        preserved_invariants = tuple(
            invariant
            for invariant in orientation_object.active_invariants
            if all(
                contract is not None
                and invariant in contract.preserved_invariants
                for contract in contracts_on_path
            )
        )
        if selected_path and len(provenance_steps) == len(selected_path):
            checks.append("provenance-chain:complete")
        if selected_path and len(evidence_chain) == len(selected_path):
            checks.append("evidence-chain:complete")

        plan_payload = {
            "schema_version": TRANSFORMATION_PLAN_SCHEMA,
            "orientation_object_id": orientation_object.orientation_object_id,
            "orientation_object_version": orientation_object.orientation_object_version,
            "source_representation_id": orientation_object.representation.representation_id,
            "source_representation": source_type,
            "source_representation_version": orientation_object.representation.representation_version,
            "target_representation": target.representation_type,
            "target_representation_version": target.representation_version,
            "graph_version": self.graph.graph_version,
            "contract_registry_version": self.contracts.registry_version,
            "operator_registry_version": self.operators.registry_version,
            "path": [step.transition_id for step in planned_steps],
            "alternative_paths": alternatives,
            "required_invariants": orientation_object.active_invariants,
            "preserved_invariants": preserved_invariants,
            "source_references": orientation_object.source_references,
            "source_provenance": orientation_object.provenance,
            "evidence_chain": evidence_chain,
        }
        plan_digest = _digest(plan_payload)
        plan = TransformationPlan(
            plan_id=f"transform-plan-{plan_digest[:16]}",
            orientation_object_id=orientation_object.orientation_object_id,
            orientation_object_version=orientation_object.orientation_object_version,
            source_representation_id=orientation_object.representation.representation_id,
            source_representation=source_type,
            source_representation_version=(
                orientation_object.representation.representation_version
            ),
            target_representation=target.representation_type,
            target_representation_version=target.representation_version,
            graph_version=self.graph.graph_version,
            contract_registry_version=self.contracts.registry_version,
            operator_registry_version=self.operators.registry_version,
            path=tuple(planned_steps),
            alternative_paths=alternatives,
            required_invariants=orientation_object.active_invariants,
            preserved_invariants=preserved_invariants,
            source_references=orientation_object.source_references,
            source_provenance=orientation_object.provenance,
            provenance_chain=tuple(provenance_steps),
            evidence_chain=tuple(evidence_chain),
        )

        frozen_issues = tuple(issues)
        validation = TransformationValidation(
            valid=not frozen_issues,
            checks=tuple(checks),
            errors=tuple(issue.reason for issue in frozen_issues),
        )
        report_payload = {
            "schema_version": TRANSFORMATION_REPORT_SCHEMA,
            "plan_id": plan.plan_id,
            "status": "blocked" if frozen_issues else "planned",
            "issues": [
                {
                    "kind": issue.kind,
                    "transition_id": issue.transition_id,
                    "evidence_level": issue.evidence_level,
                    "reason": issue.reason,
                }
                for issue in frozen_issues
            ],
        }
        report_digest = _digest(report_payload)
        return TransformationReport(
            report_id=f"transform-report-{report_digest[:16]}",
            status="blocked" if frozen_issues else "planned",
            plan=plan,
            validation=validation,
            issues=frozen_issues,
        )

    def _find_paths(
        self,
        source_representation: str,
        target_representation: str,
    ) -> tuple[tuple[GraphEdge, ...], ...]:
        if source_representation == target_representation:
            return ((),)
        if (
            source_representation not in self.graph.representations
            or target_representation not in self.graph.representations
        ):
            return ()

        adjacency: dict[str, list[GraphEdge]] = {}
        for edge in self.graph.edges:
            adjacency.setdefault(edge.source_representation, []).append(edge)
        for edges in adjacency.values():
            edges.sort(key=lambda edge: edge.transition_id)

        paths: list[tuple[GraphEdge, ...]] = []

        def visit(
            current: str,
            visited: frozenset[str],
            path: tuple[GraphEdge, ...],
        ) -> None:
            for edge in adjacency.get(current, ()):
                if edge.target_representation in visited:
                    continue
                next_path = path + (edge,)
                if edge.target_representation == target_representation:
                    paths.append(next_path)
                    continue
                visit(
                    edge.target_representation,
                    visited | frozenset((edge.target_representation,)),
                    next_path,
                )

        visit(source_representation, frozenset((source_representation,)), ())
        return tuple(
            sorted(
                paths,
                key=lambda path: (
                    len(path),
                    tuple(edge.transition_id for edge in path),
                ),
            )
        )
