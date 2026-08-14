"""Gateway-owned Artifact Manifest verification."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import fields, is_dataclass
import types
from typing import Any
from typing import get_args, get_origin, get_type_hints

from .canonical import canonical_bytes, digest_ref
from .constants import (
    EXPECTED_ARTIFACT_KINDS,
    MANIFEST_SCHEMA,
    MAX_MANIFEST_BYTES,
)
from .errors import RuntimeBoundaryError


MANIFEST_FIELDS = {
    "schema_version",
    "artifact_count",
    "artifacts",
    "terminal_artifact_ref",
}
ENTRY_FIELDS = {
    "ordinal",
    "artifact_kind",
    "artifact_version",
    "artifact_ref",
    "canonical_byte_length",
    "body",
}

# Every named cross-artifact reference required by the frozen Manifest Contract.
# Nested occurrences of the same field name are verified as well.
REFERENCE_GRAPH: dict[int, dict[str, int]] = {
    2: {"input_inventory_ref": 1},
    3: {"input_inventory_ref": 1},
    4: {
        "input_inventory_ref": 1,
        "structural_summary_ref": 2,
        "structural_statistics_ref": 3,
    },
    5: {
        "input_inventory_ref": 1,
        "structural_summary_ref": 2,
        "structural_statistics_ref": 3,
        "sequential_relation_set_ref": 4,
    },
    6: {
        "input_inventory_ref": 1,
        "structural_summary_ref": 2,
        "structural_statistics_ref": 3,
        "structural_equality_relation_set_ref": 5,
    },
    7: {
        "relation_set_ref": 6,
        "accepted_relation_set_ref": 6,
        "structural_summary_ref": 2,
        "structural_statistics_ref": 3,
    },
    8: {
        "relation_set_ref": 6,
        "conformance_report_ref": 7,
        "structural_summary_ref": 2,
        "structural_statistics_ref": 3,
    },
    9: {
        "relation_set_ref": 6,
        "relations_certification_ref": 8,
        "summary_ref": 2,
        "statistics_ref": 3,
        "provenance_ref": 8,
    },
    10: {
        "navigation_contract_ref": 9,
        "relation_set_ref": 6,
        "relations_certification_ref": 8,
        "summary_ref": 2,
        "statistics_ref": 3,
        "provenance_ref": 8,
    },
    11: {
        "construction_ref": 10,
        "accepted_construction_ref": 10,
        "navigation_ref": 9,
        "relation_set_ref": 6,
        "relations_certification_ref": 8,
        "structural_summary_ref": 2,
        "structural_statistics_ref": 3,
    },
    12: {
        "conformance_report_ref": 11,
        "construction_ref": 10,
        "navigation_ref": 9,
        "relation_set_ref": 6,
        "relations_certification_ref": 8,
        "structural_summary_ref": 2,
        "structural_statistics_ref": 3,
    },
    13: {
        "navigation_certification_ref": 12,
        "navigation_conformance_ref": 11,
        "navigation_construction_ref": 10,
        "navigation_object_ref": 9,
        "relation_set_ref": 6,
        "relations_certification_ref": 8,
        "summary_ref": 2,
        "statistics_ref": 3,
        "provenance_ref": 12,
    },
    14: {
        "orientation_map_contract_ref": 13,
        "navigation_certification_ref": 12,
        "navigation_construction_ref": 10,
        "provenance_ref": 12,
    },
    15: {
        "orientation_map_ref": 13,
        "accepted_orientation_map_ref": 13,
        "construction_ref": 14,
        "accepted_construction_ref": 14,
        "navigation_certification_ref": 12,
        "relation_set_ref": 6,
        "structural_summary_ref": 2,
        "structural_statistics_ref": 3,
    },
    16: {
        "orientation_map_conformance_ref": 15,
        "orientation_map_construction_ref": 14,
        "orientation_map_ref": 13,
        "navigation_certification_ref": 12,
        "navigation_ref": 9,
        "relation_set_ref": 6,
        "relations_certification_ref": 8,
        "structural_summary_ref": 2,
        "structural_statistics_ref": 3,
    },
    17: {
        "slice_iii_certification_ref": 16,
        "orientation_map_conformance_ref": 15,
        "orientation_map_construction_ref": 14,
        "orientation_map_ref": 13,
        "provenance_ref": 16,
    },
    18: {
        "expression_contract_ref": 17,
        "slice_iii_certification_ref": 16,
        "orientation_map_conformance_ref": 15,
        "orientation_map_construction_ref": 14,
        "orientation_map_ref": 13,
        "provenance_ref": 16,
    },
    19: {
        "expression_ref": 18,
        "accepted_expression_ref": 18,
        "expression_contract_ref": 17,
    },
    20: {
        "expression_conformance_report_ref": 19,
        "expression_ref": 18,
        "provenance_ref": 19,
    },
    21: {"provenance_ref": 20},
}


def verify_manifest(value: object) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != MANIFEST_FIELDS:
        _invalid("manifest_shape")
    if value["schema_version"] != MANIFEST_SCHEMA:
        _invalid("manifest_schema")
    artifacts = value["artifacts"]
    if (
        value["artifact_count"] != 22
        or not isinstance(artifacts, list)
        or len(artifacts) != 22
    ):
        _invalid("artifact_count")
    refs: list[str] = []
    for ordinal, (expected_kind, entry) in enumerate(
        zip(EXPECTED_ARTIFACT_KINDS, artifacts)
    ):
        if not isinstance(entry, dict) or set(entry) != ENTRY_FIELDS:
            _invalid(f"entry_shape:{ordinal}")
        if entry["ordinal"] != ordinal or entry["artifact_kind"] != expected_kind:
            _invalid(f"entry_order:{ordinal}")
        if not isinstance(entry["artifact_version"], str) or not entry["artifact_version"]:
            _invalid(f"artifact_version:{ordinal}")
        body_bytes = canonical_bytes(entry["body"])
        if entry["canonical_byte_length"] != len(body_bytes):
            _invalid(f"artifact_length:{ordinal}")
        if entry["artifact_ref"] != digest_ref(body_bytes):
            _invalid(f"artifact_integrity:{ordinal}")
        _verify_native_artifact(expected_kind, entry["body"], body_bytes, ordinal)
        refs.append(entry["artifact_ref"])
    if len(set(refs)) != len(refs):
        _invalid("duplicate_artifact_ref")
    if value["terminal_artifact_ref"] != refs[-1]:
        _invalid("terminal_artifact_ref")
    _verify_reference_graph(artifacts, refs)
    if len(canonical_bytes(value)) > MAX_MANIFEST_BYTES:
        raise RuntimeBoundaryError(
            status=422,
            category="output_validation",
            code="operational_profile_exceeded",
            detail_refs=("manifest_size",),
        )
    terminal = artifacts[-1]["body"]
    if (
        not isinstance(terminal, dict)
        or terminal.get("decision") != "certified"
        or terminal.get("stop") != "at_slice_iv_certified"
    ):
        _invalid("terminal_certification")
    return value


def _verify_reference_graph(
    artifacts: list[dict[str, Any]],
    refs: list[str],
) -> None:
    for ordinal, requirements in REFERENCE_GRAPH.items():
        body = artifacts[ordinal]["body"]
        for field_name, target_ordinal in requirements.items():
            if not isinstance(body, dict) or field_name not in body:
                _invalid(f"reference_missing:{ordinal}:{field_name}")
            if body[field_name] != refs[target_ordinal]:
                _invalid(f"reference_mismatch:{ordinal}:{field_name}")


def _verify_native_artifact(
    kind: str,
    body: object,
    expected_bytes: bytes,
    ordinal: int,
) -> None:
    try:
        parser, serializer = _native_codec(kind)
        artifact = parser(body)
        if serializer(artifact) != expected_bytes:
            _invalid(f"native_serialization:{ordinal}")
    except RuntimeBoundaryError:
        raise
    except Exception:
        _invalid(f"native_validation:{ordinal}")


def _native_codec(kind: str) -> tuple[Any, Any]:
    from orion.declared_cross_references_alpha import (
        canonical_declared_reference_relation_set_bytes,
        declared_reference_relation_set_from_dict,
    )
    from orion.expression_certification_alpha import (
        canonical_expression_certification_report_bytes,
        expression_certification_report_from_dict,
    )
    from orion.expression_conformance_alpha import (
        canonical_expression_conformance_report_bytes,
        expression_conformance_report_from_dict,
    )
    from orion.expression_construction_alpha import (
        canonical_expression_artifact_bytes,
        expression_artifact_from_dict,
    )
    from orion.expression_contract_alpha import (
        canonical_expression_contract_bytes,
        expression_contract_from_dict,
    )
    from orion.markdown_structural_renderer_alpha import (
        ImmutableMarkdownStructuralRepresentation,
        canonical_representation_bytes,
    )
    from orion.navigation_certification_alpha import (
        canonical_navigation_certification_report_bytes,
        navigation_certification_report_from_dict,
    )
    from orion.navigation_conformance_alpha import (
        canonical_navigation_conformance_report_bytes,
        navigation_conformance_report_from_dict,
    )
    from orion.navigation_construction_alpha import (
        canonical_constructed_navigation_bytes,
        constructed_navigation_from_dict,
    )
    from orion.navigation_object_alpha import (
        canonical_navigation_object_bytes,
        navigation_object_from_dict,
    )
    from orion.orientation_map_conformance_alpha import (
        canonical_orientation_map_conformance_report_bytes,
        orientation_map_conformance_report_from_dict,
    )
    from orion.orientation_map_construction_alpha import (
        canonical_constructed_orientation_map_bytes,
        constructed_orientation_map_from_dict,
    )
    from orion.orientation_map_object_alpha import (
        canonical_orientation_map_object_bytes,
        orientation_map_object_from_dict,
    )
    from orion.relation_conformance_alpha import (
        canonical_relation_conformance_report_bytes,
        relation_conformance_report_from_dict,
    )
    from orion.relations_certification_alpha import (
        canonical_relations_certification_report_bytes,
        relations_certification_report_from_dict,
    )
    from orion.sequential_relations_alpha import (
        canonical_sequential_relation_set_bytes,
        sequential_relation_set_from_dict,
    )
    from orion.slice_iii_certification_alpha import (
        canonical_slice_iii_certification_report_bytes,
        slice_iii_certification_report_from_dict,
    )
    from orion.slice_iv_certification_alpha import (
        canonical_slice_iv_certification_report_bytes,
        slice_iv_certification_report_from_dict,
    )
    from orion.structural_equality_relations_alpha import (
        canonical_structural_equality_relation_set_bytes,
        structural_equality_relation_set_from_dict,
    )
    from orion.understand_source_element_inventory_alpha import (
        DeclaredSourceElementInventoryDiagnostic,
        canonical_inventory_bytes,
    )
    from orion.understand_structural_statistics_alpha import (
        StructuralStatisticsDiagnostic,
        canonical_structural_statistics_bytes,
    )
    from orion.understand_structural_summary_alpha import (
        StructuralSummaryDiagnostic,
        canonical_structural_summary_bytes,
    )

    generic = lambda cls: lambda value: _decode_dataclass(cls, value)
    codecs = {
        "structural_representation": (
            generic(ImmutableMarkdownStructuralRepresentation),
            canonical_representation_bytes,
        ),
        "source_element_inventory": (
            generic(DeclaredSourceElementInventoryDiagnostic),
            canonical_inventory_bytes,
        ),
        "structural_summary": (
            generic(StructuralSummaryDiagnostic),
            canonical_structural_summary_bytes,
        ),
        "structural_statistics": (
            generic(StructuralStatisticsDiagnostic),
            canonical_structural_statistics_bytes,
        ),
        "sequential_relation_set": (
            sequential_relation_set_from_dict,
            canonical_sequential_relation_set_bytes,
        ),
        "structural_equality_relation_set": (
            structural_equality_relation_set_from_dict,
            canonical_structural_equality_relation_set_bytes,
        ),
        "declared_reference_relation_set": (
            declared_reference_relation_set_from_dict,
            canonical_declared_reference_relation_set_bytes,
        ),
        "relation_conformance": (
            relation_conformance_report_from_dict,
            canonical_relation_conformance_report_bytes,
        ),
        "relations_certification": (
            relations_certification_report_from_dict,
            canonical_relations_certification_report_bytes,
        ),
        "navigation_object": (
            navigation_object_from_dict,
            canonical_navigation_object_bytes,
        ),
        "constructed_navigation": (
            constructed_navigation_from_dict,
            canonical_constructed_navigation_bytes,
        ),
        "navigation_conformance": (
            navigation_conformance_report_from_dict,
            canonical_navigation_conformance_report_bytes,
        ),
        "navigation_certification": (
            navigation_certification_report_from_dict,
            canonical_navigation_certification_report_bytes,
        ),
        "orientation_map_object": (
            orientation_map_object_from_dict,
            canonical_orientation_map_object_bytes,
        ),
        "constructed_orientation_map": (
            constructed_orientation_map_from_dict,
            canonical_constructed_orientation_map_bytes,
        ),
        "orientation_map_conformance": (
            orientation_map_conformance_report_from_dict,
            canonical_orientation_map_conformance_report_bytes,
        ),
        "slice_iii_certification": (
            slice_iii_certification_report_from_dict,
            canonical_slice_iii_certification_report_bytes,
        ),
        "expression_contract": (
            expression_contract_from_dict,
            canonical_expression_contract_bytes,
        ),
        "expression_artifact": (
            expression_artifact_from_dict,
            canonical_expression_artifact_bytes,
        ),
        "expression_conformance": (
            expression_conformance_report_from_dict,
            canonical_expression_conformance_report_bytes,
        ),
        "expression_certification": (
            expression_certification_report_from_dict,
            canonical_expression_certification_report_bytes,
        ),
        "slice_iv_certification": (
            slice_iv_certification_report_from_dict,
            canonical_slice_iv_certification_report_bytes,
        ),
    }
    return codecs[kind]


def _decode_dataclass(cls: type[Any], value: object) -> Any:
    if not is_dataclass(cls) or not isinstance(value, dict):
        raise TypeError("dataclass object required")
    hints = get_type_hints(cls)
    expected = {field.name for field in fields(cls)}
    if set(value) != expected:
        raise ValueError("dataclass fields differ")
    return cls(
        **{
            field.name: _decode_value(hints[field.name], value[field.name])
            for field in fields(cls)
        }
    )


def _decode_value(annotation: Any, value: object) -> Any:
    origin = get_origin(annotation)
    args = get_args(annotation)
    if is_dataclass(annotation):
        return _decode_dataclass(annotation, value)
    if origin is tuple:
        if not isinstance(value, list):
            raise TypeError("array required")
        subtype = args[0] if args else Any
        return tuple(_decode_value(subtype, item) for item in value)
    if origin in {dict, Mapping}:
        if not isinstance(value, dict):
            raise TypeError("object required")
        value_type = args[1] if len(args) == 2 else Any
        return {
            key: _decode_value(value_type, item)
            for key, item in value.items()
        }
    if origin in {types.UnionType, getattr(__import__("typing"), "Union")}:
        if value is None and type(None) in args:
            return None
        for subtype in args:
            if subtype is type(None):
                continue
            try:
                return _decode_value(subtype, value)
            except (TypeError, ValueError):
                continue
        raise TypeError("union value invalid")
    return value


def _invalid(rule: str) -> None:
    raise RuntimeBoundaryError(
        status=500,
        category="output_validation",
        code="artifact_manifest_invalid",
        retry="manual_review",
        detail_refs=(rule,),
    )
