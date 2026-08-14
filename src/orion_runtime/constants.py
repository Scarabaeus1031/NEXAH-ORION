"""Frozen Runtime 1.1 constants and operational limits."""

API_VERSION = "1.0"
RUNTIME_VERSION = "1.1.0"
CORE_VERSION = "1.0.0"
CORE_COMMIT = "d34fbb2f99334534f4db89465a29f8bdb16d14d3"
CORE_FINGERPRINT = (
    "6201362c094530a0a31fa3d80b46c9131011bb8c8d400183271b0da0eb423f8d"
)

MEDIA_TYPE = "application/vnd.orion.runtime+json;version=1.0"
MATERIAL_SCHEMA = "orion.confirmed-material/1.0"
LINEAGE_SCHEMA = "orion.clarification-lineage/1.0"
MANIFEST_SCHEMA = "orion.runtime-artifact-manifest/1.0"
TERMINAL_STOP = "at_slice_iv_certified"

MAX_REQUEST_BYTES = 2_000_000
MAX_HEADER_BYTES = 32_768
MAX_HEADERS = 50
MAX_CONTENT_BYTES = 262_144
MAX_SOURCE_LINES = 8_192
MAX_LINEAGE_DEPTH = 8
MAX_LINEAGE_BYTES = 1_000_000
MAX_ELEMENTS = 128
MAX_RELATIONS = 16_384
MAX_MANIFEST_BYTES = 16_000_000
MAX_RESPONSE_BYTES = 16_777_216
CORE_TIMEOUT_SECONDS = 15
CORE_CPU_SECONDS = 15
TOTAL_REQUEST_SECONDS = 30
WORKER_MEMORY_BYTES = 512 * 1024 * 1024
WORKER_TEMP_BYTES = 64 * 1024 * 1024
WORKER_OPEN_FILES = 64
RELEASE_MANIFEST_SCHEMA = "orion.runtime-release-manifest/1.0"
RELEASE_MANIFEST_PATH = "release/orion-runtime-1.1.0.json"

COMMUNICATIVE_SCOPE = (
    "canonical_order",
    "orientation_map_entries",
    "orientation_map_identity",
    "provenance",
    "structural_adjacency",
)
DECLARED_LOSSINESS = (
    "human_interpretation",
    "semantic_meaning",
    "visual_layout",
)
DECLARED_EXCLUSIONS = (
    "actions",
    "generated_language",
    "recommendations",
    "semantic_reasoning",
)

EXPECTED_ARTIFACT_KINDS = (
    "structural_representation",
    "source_element_inventory",
    "structural_summary",
    "structural_statistics",
    "sequential_relation_set",
    "structural_equality_relation_set",
    "declared_reference_relation_set",
    "relation_conformance",
    "relations_certification",
    "navigation_object",
    "constructed_navigation",
    "navigation_conformance",
    "navigation_certification",
    "orientation_map_object",
    "constructed_orientation_map",
    "orientation_map_conformance",
    "slice_iii_certification",
    "expression_contract",
    "expression_artifact",
    "expression_conformance",
    "expression_certification",
    "slice_iv_certification",
)
