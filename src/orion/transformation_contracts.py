"""Provider-independent graph and contract records for Phase 4A planning."""

from __future__ import annotations

from dataclasses import dataclass
import re


TRANSITION_CONTRACT_SCHEMA = "orion.transition-contract/0.1-draft"

HARD_INVARIANTS = (
    "identity",
    "provenance",
    "orientation_object_id",
    "source_references",
)

CONDITIONAL_INVARIANTS = (
    "epoch",
    "known_constants",
)

_EVIDENCE_PATTERN = re.compile(r"^E[0-4](?:–E[0-4])?$")
_TRANSITION_PATTERN = re.compile(r"^T[0-9]{2}$")
_OPERATOR_STATUSES = frozenset(("unknown", "candidate", "documented", "verified"))


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
class GraphEdge:
    """One explicitly registered directed edge in the Representation Graph."""

    transition_id: str
    source_representation: str
    target_representation: str

    def __post_init__(self) -> None:
        for field_name in (
            "transition_id",
            "source_representation",
            "target_representation",
        ):
            _require_text(getattr(self, field_name), field_name)
        if not _TRANSITION_PATTERN.fullmatch(self.transition_id):
            raise ValueError("transition_id must match Txx")


@dataclass(frozen=True, slots=True)
class RepresentationGraph:
    """Immutable graph registry; it never infers edges."""

    edges: tuple[GraphEdge, ...]
    graph_version: str = "orientation-representation-graph/0.1-draft"

    def __post_init__(self) -> None:
        frozen_edges = tuple(self.edges)
        _require_text(self.graph_version, "graph_version")
        if not frozen_edges:
            raise ValueError("a representation graph requires at least one edge")
        transition_ids = tuple(edge.transition_id for edge in frozen_edges)
        if len(set(transition_ids)) != len(transition_ids):
            raise ValueError("graph transition IDs must be unique")
        object.__setattr__(self, "edges", frozen_edges)

    @property
    def representations(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                {
                    representation
                    for edge in self.edges
                    for representation in (
                        edge.source_representation,
                        edge.target_representation,
                    )
                }
            )
        )


@dataclass(frozen=True, slots=True)
class TransitionContract:
    """Executable-planning projection of one Phase 3C documentation contract."""

    transition_id: str
    name: str
    source_representation: str
    target_representation: str
    evidence_level: str
    operator_status: str
    renderer_family: str
    required_parameters: tuple[str, ...]
    preserved_invariants: tuple[str, ...] = HARD_INVARIANTS + CONDITIONAL_INVARIANTS
    optional_parameters: tuple[str, ...] = ()
    operator_id: str | None = None
    renderer_ids: tuple[str, ...] = ()
    supported_source_versions: tuple[str, ...] = ()
    target_representation_version: str | None = None
    contract_version: str = "0.1-draft"
    schema_version: str = TRANSITION_CONTRACT_SCHEMA
    documentation_ref: str = ""

    def __post_init__(self) -> None:
        for field_name in (
            "transition_id",
            "name",
            "source_representation",
            "target_representation",
            "evidence_level",
            "operator_status",
            "renderer_family",
            "contract_version",
            "schema_version",
            "documentation_ref",
        ):
            _require_text(getattr(self, field_name), field_name)
        if not _TRANSITION_PATTERN.fullmatch(self.transition_id):
            raise ValueError("transition_id must match Txx")
        if not _EVIDENCE_PATTERN.fullmatch(self.evidence_level):
            raise ValueError("evidence_level must be E0–E4 or a bounded E0–E4 range")
        if self.operator_status not in _OPERATOR_STATUSES:
            raise ValueError(f"unsupported operator status: {self.operator_status}")
        if self.schema_version != TRANSITION_CONTRACT_SCHEMA:
            raise ValueError(f"unsupported transition contract schema: {self.schema_version}")
        for field_name in (
            "required_parameters",
            "preserved_invariants",
            "optional_parameters",
            "renderer_ids",
            "supported_source_versions",
        ):
            object.__setattr__(
                self,
                field_name,
                _freeze_unique_text(getattr(self, field_name), field_name),
            )
        if self.operator_id is not None:
            _require_text(self.operator_id, "operator_id")
        if self.target_representation_version is not None:
            _require_text(
                self.target_representation_version,
                "target_representation_version",
            )

    @property
    def has_executable_operator(self) -> bool:
        return self.operator_status == "verified" and self.operator_id is not None

    @property
    def has_renderer(self) -> bool:
        return bool(self.renderer_ids)


@dataclass(frozen=True, slots=True)
class TransitionContractRegistry:
    """Immutable lookup collection for injected Transition Contracts."""

    contracts: tuple[TransitionContract, ...]
    registry_version: str = "orientation-transition-contracts/0.1-draft"

    def __post_init__(self) -> None:
        frozen_contracts = tuple(self.contracts)
        _require_text(self.registry_version, "registry_version")
        transition_ids = tuple(contract.transition_id for contract in frozen_contracts)
        if len(set(transition_ids)) != len(transition_ids):
            raise ValueError("contract transition IDs must be unique")
        object.__setattr__(self, "contracts", frozen_contracts)

    def get(self, transition_id: str) -> TransitionContract | None:
        return next(
            (
                contract
                for contract in self.contracts
                if contract.transition_id == transition_id
            ),
            None,
        )


DEFAULT_REPRESENTATION_GRAPH = RepresentationGraph(
    edges=(
        GraphEdge("T01", "Reality", "Observation"),
        GraphEdge("T02", "Observation", "Planetary Chemistry"),
        GraphEdge("T03", "Observation", "Lunar/Solar Dynamics"),
        GraphEdge("T04", "Planetary Chemistry", "Scarabaeus Engine"),
        GraphEdge("T05", "Lunar/Solar Dynamics", "Scarabaeus Engine"),
        GraphEdge("T06", "Scarabaeus Engine", "Möbius Topology"),
        GraphEdge("T07", "Scarabaeus Engine", "Frequency Space"),
        GraphEdge("T08", "Möbius Topology", "Lissajous Geometry"),
        GraphEdge("T09", "Frequency Space", "Lissajous Geometry"),
        GraphEdge("T10", "Lissajous Geometry", "Frequency Space"),
        GraphEdge("T11", "Lissajous Geometry", "Stellar Projection"),
        GraphEdge("T12", "Stellar Projection", "Dodecahedral Sky Map"),
        GraphEdge("T13", "Stellar Projection", "Calendar Projection"),
        GraphEdge("T14", "Dodecahedral Sky Map", "Calendar Projection"),
        GraphEdge("T15", "Calendar Projection", "Orientation Layer"),
    )
)


def _contract(
    transition_id: str,
    name: str,
    source: str,
    target: str,
    evidence: str,
    operator_status: str,
    renderer_family: str,
    required_parameters: tuple[str, ...],
    optional_parameters: tuple[str, ...] = (),
) -> TransitionContract:
    return TransitionContract(
        transition_id=transition_id,
        name=name,
        source_representation=source,
        target_representation=target,
        evidence_level=evidence,
        operator_status=operator_status,
        renderer_family=renderer_family,
        required_parameters=required_parameters,
        optional_parameters=optional_parameters,
        documentation_ref=(
            "docs/architecture/transformations/contracts/"
            f"{transition_id}.md"
        ),
    )


DEFAULT_TRANSITION_CONTRACTS = TransitionContractRegistry(
    contracts=(
        _contract(
            "T01", "Reality to Observation", "Reality", "Observation", "E1",
            "unknown", "Observation Renderer",
            ("observer", "instrument_profile", "units", "timestamp", "sampling_rule"),
            ("uncertainty_profile", "calibration_reference", "annotation"),
        ),
        _contract(
            "T02", "Observation to Planetary Chemistry", "Observation",
            "Planetary Chemistry", "E0", "unknown", "Atlas/Correspondence Renderer",
            ("taxonomy_version", "crosswalk", "entity_identity", "unit_normalization", "ambiguity_policy"),
            ("relation_weight", "curator_note", "category_aliases"),
        ),
        _contract(
            "T03", "Observation to Lunar/Solar Dynamics", "Observation",
            "Lunar/Solar Dynamics", "E0–E1", "candidate", "Tide/Phase Renderer",
            ("amplitudes", "periods", "phase_origins", "epoch", "sampling_profile", "output_unit"),
            ("additional_harmonics", "uncertainty", "filter_profile"),
        ),
        _contract(
            "T04", "Planetary Chemistry to Scarabaeus Engine",
            "Planetary Chemistry", "Scarabaeus Engine", "E0", "unknown",
            "Engine Renderer",
            ("category_state_crosswalk", "state_field_ids", "encoding", "scale_units", "normalization", "merge_role"),
            ("weights", "uncertainty", "layout_hints"),
        ),
        _contract(
            "T05", "Lunar/Solar Dynamics to Scarabaeus Engine",
            "Lunar/Solar Dynamics", "Scarabaeus Engine", "E0", "unknown",
            "Engine Renderer",
            ("input_role", "state_field_ids", "coupling", "timestep", "epoch", "merge_role"),
            ("beat_field", "phase_lock_threshold", "component_filters"),
        ),
        _contract(
            "T06", "Scarabaeus Engine to Möbius Topology", "Scarabaeus Engine",
            "Möbius Topology", "E0–E1", "candidate", "Topology Renderer",
            ("state_strip_mapping", "boundary_pair", "seam", "direction", "landmark_crosswalk"),
            ("embedding", "visual_scale", "sampling_density"),
        ),
        _contract(
            "T07", "Scarabaeus Engine to Frequency Space", "Scarabaeus Engine",
            "Frequency Space", "E1", "candidate", "Spectral/Frequency Renderer",
            ("selected_signal", "sampling_profile", "interval", "window", "normalization"),
            ("detrending", "zero_padding", "spectral_truncation"),
        ),
        _contract(
            "T08", "Möbius Topology to Lissajous Geometry", "Möbius Topology",
            "Lissajous Geometry", "E0", "unknown", "Parametric Curve Renderer",
            ("selected_path", "chart", "seam_handling", "observation_map", "axes", "phase_origin"),
            ("embedding", "sampling_density", "labels"),
        ),
        _contract(
            "T09", "Frequency Space to Lissajous Geometry", "Frequency Space",
            "Lissajous Geometry", "E1", "candidate", "Parametric Curve Renderer",
            ("component_ids", "amplitudes", "frequencies", "relative_phase", "parameter_interval", "sampling_density"),
            ("labels", "display_scale", "closure_tolerance"),
        ),
        _contract(
            "T10", "Lissajous Geometry to Frequency Space", "Lissajous Geometry",
            "Frequency Space", "E1", "candidate", "Spectral/Frequency Renderer",
            ("ordered_samples", "fit_model", "normalization", "aliasing_policy", "residual_tolerance"),
            ("window", "initial_estimates", "sample_weighting"),
        ),
        _contract(
            "T11", "Lissajous Geometry to Stellar Projection", "Lissajous Geometry",
            "Stellar Projection", "E0", "unknown", "Stellar/Spherical Renderer",
            ("projection_operator", "source_frame", "target_frame", "center_pole", "orientation", "point_crosswalk"),
            ("clipping", "landmark_labels", "camera"),
        ),
        _contract(
            "T12", "Stellar Projection to Dodecahedral Sky Map", "Stellar Projection",
            "Dodecahedral Sky Map", "E0–E1", "candidate", "Polyhedral Sky Renderer",
            ("polyhedron_orientation", "face_normals", "assignment_rule", "boundary_rule", "local_coordinates", "adjacency"),
            ("unfolding", "labels", "visual_padding"),
        ),
        _contract(
            "T13", "Stellar Projection to Calendar Projection", "Stellar Projection",
            "Calendar Projection", "E0–E1", "candidate", "Calendar/Temporal Renderer",
            ("phase_rule", "epoch", "period", "direction", "calendar_profile", "timezone"),
            ("granularity", "intercalation", "labels"),
        ),
        _contract(
            "T14", "Dodecahedral Sky Map to Calendar Projection",
            "Dodecahedral Sky Map", "Calendar Projection", "E0", "unknown",
            "Calendar/Temporal Renderer",
            ("address_calendar_mapping", "polyhedron_profile", "ordering", "epoch", "calendar_profile", "within_face_policy"),
            ("labels", "granularity", "grouping"),
        ),
        _contract(
            "T15", "Calendar Projection to Orientation Layer", "Calendar Projection",
            "Orientation Layer", "E1", "candidate", "Orientation Renderer",
            ("epoch", "period", "direction", "calendar_profile", "normalization_profile", "orientation_fields", "lossiness_profile"),
            ("labels", "granularity", "orientation_markers"),
        ),
    )
)
