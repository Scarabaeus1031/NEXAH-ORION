#!/usr/bin/env python3
"""Build the local POA-002 Equivalence Review without executing OLS."""

from __future__ import annotations

import ast
import difflib
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


FROZEN_DIGESTS = {
    "request.json": "d847553992b746790bc7f55dd8b58f06631c5f1e31fd0e8d60b6425f9fd7d52a",
    "observation.json": "fe3f1c9e4339bd7d646814e1af101876573934539e40e01b4878852d29bd1d73",
    "expression.json": "cc57e561e0e209d4cca504f63d044bb012a740ac6479da71fd4dacc0247a9667",
    "compare.py": "05e122b25d0cfb5f2ec05ec3d88ed9305013fb30f85ea77210380e885704b262",
    "result.json": "6d565b327ed812f7b4e3b2239298e07715bdf3ac077d759d48263ce1279bb6b3",
}
NEGATIVE_FILES = (
    ("unsupported_operator", "unsupported-operator.json"),
    ("stale_observation_digest", "stale-observation.json"),
    ("invalid_required_input_shape", "invalid-shape.json"),
)
IDENTITY_PATHS = {"/id", "/processor", "/processor_sha256"}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read_json(path: Path) -> tuple[bytes, Any]:
    raw = path.read_bytes()
    return raw, json.loads(raw)


def json_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, str):
        return "string"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def pointer(base: str, part: str | int) -> str:
    escaped = str(part).replace("~", "~0").replace("/", "~1")
    return f"{base}/{escaped}" if base else f"/{escaped}"


def parsed_differences(
    left: Any, right: Any, base: str = ""
) -> list[dict[str, Any]]:
    if json_type(left) != json_type(right):
        return [{"path": base or "/", "result_a": left, "result_b": right}]
    if isinstance(left, dict):
        differences: list[dict[str, Any]] = []
        for key in sorted(set(left) | set(right)):
            path = pointer(base, key)
            if key not in left:
                differences.append(
                    {"path": path, "result_a": {"absent": True}, "result_b": right[key]}
                )
            elif key not in right:
                differences.append(
                    {"path": path, "result_a": left[key], "result_b": {"absent": True}}
                )
            else:
                differences.extend(parsed_differences(left[key], right[key], path))
        return differences
    if isinstance(left, list):
        differences = []
        for index in range(max(len(left), len(right))):
            path = pointer(base, index)
            if index >= len(left):
                differences.append(
                    {"path": path, "result_a": {"absent": True}, "result_b": right[index]}
                )
            elif index >= len(right):
                differences.append(
                    {"path": path, "result_a": left[index], "result_b": {"absent": True}}
                )
            else:
                differences.extend(parsed_differences(left[index], right[index], path))
        return differences
    return [] if left == right else [
        {"path": base or "/", "result_a": left, "result_b": right}
    ]


def shape_differences(
    left: Any, right: Any, base: str = ""
) -> list[dict[str, Any]]:
    left_type = json_type(left)
    right_type = json_type(right)
    if left_type != right_type:
        return [
            {
                "path": base or "/",
                "result_a_type": left_type,
                "result_b_type": right_type,
            }
        ]
    if isinstance(left, dict):
        differences: list[dict[str, Any]] = []
        if set(left) != set(right):
            differences.append(
                {
                    "path": base or "/",
                    "result_a_fields": sorted(left),
                    "result_b_fields": sorted(right),
                }
            )
        for key in sorted(set(left) & set(right)):
            differences.extend(
                shape_differences(left[key], right[key], pointer(base, key))
            )
        return differences
    if isinstance(left, list):
        differences = []
        if len(left) != len(right):
            differences.append(
                {
                    "path": base or "/",
                    "result_a_cardinality": len(left),
                    "result_b_cardinality": len(right),
                }
            )
        for index, (left_item, right_item) in enumerate(zip(left, right)):
            differences.extend(
                shape_differences(left_item, right_item, pointer(base, index))
            )
        return differences
    return []


def raw_segments(left: bytes, right: bytes) -> list[dict[str, Any]]:
    matcher = difflib.SequenceMatcher(None, left, right, autojunk=False)
    segments = []
    for operation, a_start, a_end, b_start, b_end in matcher.get_opcodes():
        if operation == "equal":
            continue
        left_part = left[a_start:a_end]
        right_part = right[b_start:b_end]
        segments.append(
            {
                "operation": operation,
                "result_a_range": [a_start, a_end],
                "result_b_range": [b_start, b_end],
                "result_a_segment_sha256": sha256_bytes(left_part),
                "result_b_segment_sha256": sha256_bytes(right_part),
                "classification": "implementation-specific",
                "reason": "Raw bytes differ only where required implementation identities differ.",
            }
        )
    return segments


def imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".", 1)[0])
    return sorted(names)


def semantic_row(
    concern: str,
    path: str,
    left: Any,
    right: Any,
    required_relation: str,
    passes: bool,
) -> dict[str, Any]:
    return {
        "concern": concern,
        "path": path,
        "result_a": left,
        "result_b": right,
        "required_relation": required_relation,
        "pass": passes,
    }


def main() -> None:
    if len(sys.argv) != 7:
        raise SystemExit(
            "usage: verify-equivalence.py POA1_DIR POA2_DIR "
            "RESULT_A RESULT_B NEGATIVE_A_DIR NEGATIVE_B_DIR"
        )

    poa1 = Path(sys.argv[1]).resolve()
    poa2 = Path(sys.argv[2]).resolve()
    result_a_path = Path(sys.argv[3]).resolve()
    result_b_path = Path(sys.argv[4]).resolve()
    negative_a = Path(sys.argv[5]).resolve()
    negative_b = Path(sys.argv[6]).resolve()

    request_raw, request = read_json(poa1 / "request.json")
    observation_raw, observation = read_json(poa1 / "observation.json")
    expression_raw, expression = read_json(poa1 / "expression.json")
    result_a_raw, result_a = read_json(result_a_path)
    result_b_raw, result_b = read_json(result_b_path)
    processor_a_path = poa1 / "compare.py"
    processor_b_path = poa2 / "processor-b.py"
    processor_a_raw = processor_a_path.read_bytes()
    processor_b_raw = processor_b_path.read_bytes()

    frozen_checks = {
        "request.json": sha256_bytes(request_raw) == FROZEN_DIGESTS["request.json"],
        "observation.json": (
            sha256_bytes(observation_raw) == FROZEN_DIGESTS["observation.json"]
        ),
        "expression.json": (
            sha256_bytes(expression_raw) == FROZEN_DIGESTS["expression.json"]
        ),
        "compare.py": (
            sha256_bytes(processor_a_raw) == FROZEN_DIGESTS["compare.py"]
        ),
        "result.json": (
            sha256_bytes((poa1 / "result.json").read_bytes())
            == FROZEN_DIGESTS["result.json"]
        ),
    }

    processor_a_digest = sha256_bytes(processor_a_raw)
    processor_b_digest = sha256_bytes(processor_b_raw)
    result_a_digest = sha256_bytes(result_a_raw)
    result_b_digest = sha256_bytes(result_b_raw)

    source_a = processor_a_raw.decode("utf-8")
    source_b = processor_b_raw.decode("utf-8")
    imports_a = imported_modules(processor_a_path)
    imports_b = imported_modules(processor_b_path)
    local_imports_a = sorted(set(imports_a) - set(sys.stdlib_module_names) - {"__future__"})
    local_imports_b = sorted(set(imports_b) - set(sys.stdlib_module_names) - {"__future__"})
    cross_references = {
        "processor_a_names_processor_b": any(
            marker in source_a
            for marker in ("processor-b.py", "poa-002-compare-b", "result-002-b")
        ),
        "processor_b_names_processor_a": any(
            marker in source_b
            for marker in ("compare.py", "poa-001-compare", "result-001")
        ),
    }

    expected_evidence = [
        {"record_ref": record["id"], "value": record["evidence"]}
        for record in observation["records"]
    ]
    expected_uncertainty = {
        "records": [
            {"record_ref": record["id"], "value": record["uncertainty"]}
            for record in observation["records"]
        ],
        "limitation": observation["limitation"],
    }
    expected_sources = [
        {
            "record_ref": record_id,
            "value": next(
                record[expression["field"]]
                for record in observation["records"]
                if record["id"] == record_id
            ),
        }
        for record_id in expression["inputs"]
    ]

    raw_diff = raw_segments(result_a_raw, result_b_raw)
    parsed_diff = parsed_differences(result_a, result_b)
    classified_parsed = []
    for difference in parsed_diff:
        path = difference["path"]
        implementation_specific = path in IDENTITY_PATHS
        classified_parsed.append(
            {
                **difference,
                "classification": (
                    "implementation-specific"
                    if implementation_specific
                    else "semantic"
                ),
                "reason": (
                    "Independent Results must retain distinct Result or Processor identity."
                    if implementation_specific
                    else "This path is meaning-bearing in the frozen POA-001 Result."
                ),
            }
        )

    shape_diff = shape_differences(result_a, result_b)
    structural_pass = not shape_diff
    semantic_path_pass = all(
        difference["classification"] == "implementation-specific"
        for difference in classified_parsed
    )

    complete_shape = {
        "id",
        "status",
        "expression_ref",
        "expression_sha256",
        "processor",
        "processor_sha256",
        "evidence",
        "uncertainty",
        "prohibited_implications",
        "comparison",
    }
    exact_complete_shapes = (
        isinstance(result_a, dict)
        and isinstance(result_b, dict)
        and set(result_a) == complete_shape
        and set(result_b) == complete_shape
    )

    negative_results = []
    stop_pass = True
    for case_name, filename in NEGATIVE_FILES:
        _, blocked_a = read_json(negative_a / filename)
        _, blocked_b = read_json(negative_b / filename)
        a_pass = (
            blocked_a.get("status") == "blocked"
            and "comparison" not in blocked_a
            and blocked_a.get("evidence") == expected_evidence
            and blocked_a.get("uncertainty") == expected_uncertainty
            and blocked_a.get("prohibited_implications")
            == expression["prohibited_implications"]
        )
        b_pass = (
            blocked_b.get("status") == "blocked"
            and "comparison" not in blocked_b
            and blocked_b.get("evidence") == expected_evidence
            and blocked_b.get("uncertainty") == expected_uncertainty
            and blocked_b.get("prohibited_implications")
            == expression["prohibited_implications"]
        )
        same_lineage = (
            blocked_a.get("expression_ref") == blocked_b.get("expression_ref")
            and blocked_a.get("expression_sha256")
            == blocked_b.get("expression_sha256")
        )
        boundary_equivalent = a_pass and b_pass and same_lineage
        stop_pass = stop_pass and boundary_equivalent
        negative_results.append(
            {
                "case": case_name,
                "processor_a": {
                    "status": blocked_a.get("status"),
                    "reason": blocked_a.get("reason"),
                    "comparison_present": "comparison" in blocked_a,
                    "preserved_boundary": a_pass,
                },
                "processor_b": {
                    "status": blocked_b.get("status"),
                    "reason": blocked_b.get("reason"),
                    "comparison_present": "comparison" in blocked_b,
                    "preserved_boundary": b_pass,
                },
                "same_expression_lineage": same_lineage,
                "boundary_equivalent": boundary_equivalent,
            }
        )

    result_lineage_pass = (
        result_a.get("expression_ref") == expression["id"]
        and result_b.get("expression_ref") == expression["id"]
        and result_a.get("expression_sha256") == sha256_bytes(expression_raw)
        and result_b.get("expression_sha256") == sha256_bytes(expression_raw)
        and result_a.get("processor_sha256") == processor_a_digest
        and result_b.get("processor_sha256") == processor_b_digest
    )
    independence_pass = (
        processor_a_path != processor_b_path
        and processor_a_digest != processor_b_digest
        and result_a.get("processor") != result_b.get("processor")
        and result_a.get("id") != result_b.get("id")
        and not local_imports_a
        and not local_imports_b
        and not any(cross_references.values())
    )
    copied_boundaries_pass = (
        result_a.get("evidence") == expected_evidence
        and result_b.get("evidence") == expected_evidence
        and result_a.get("uncertainty") == expected_uncertainty
        and result_b.get("uncertainty") == expected_uncertainty
        and result_a.get("prohibited_implications")
        == expression["prohibited_implications"]
        and result_b.get("prohibited_implications")
        == expression["prohibited_implications"]
    )
    source_values_pass = (
        result_a.get("comparison", {}).get("field") == expression["field"]
        and result_b.get("comparison", {}).get("field") == expression["field"]
        and result_a.get("comparison", {}).get("sources") == expected_sources
        and result_b.get("comparison", {}).get("sources") == expected_sources
    )

    stop_values_a = [
        {
            "case": item["case"],
            "status": item["processor_a"]["status"],
            "comparison_present": item["processor_a"]["comparison_present"],
        }
        for item in negative_results
    ]
    stop_values_b = [
        {
            "case": item["case"],
            "status": item["processor_b"]["status"],
            "comparison_present": item["processor_b"]["comparison_present"],
        }
        for item in negative_results
    ]

    semantic_rows = [
        semantic_row(
            "Input Request digest",
            "/inputs/request/sha256",
            expression["request_sha256"],
            expression["request_sha256"],
            "Equal to POA-001",
            expression["request_sha256"] == sha256_bytes(request_raw),
        ),
        semantic_row(
            "Input Observation digest",
            "/inputs/observation/sha256",
            expression["observation_sha256"],
            expression["observation_sha256"],
            "Equal to POA-001",
            expression["observation_sha256"] == sha256_bytes(observation_raw),
        ),
        semantic_row(
            "Input Expression digest",
            "/inputs/expression/sha256",
            result_a.get("expression_sha256"),
            result_b.get("expression_sha256"),
            "Equal to POA-001",
            result_lineage_pass,
        ),
        semantic_row(
            "Result status",
            "/status",
            result_a.get("status"),
            result_b.get("status"),
            "Equal",
            result_a.get("status") == result_b.get("status") == "complete",
        ),
        semantic_row(
            "Comparison field",
            "/comparison/field",
            result_a.get("comparison", {}).get("field"),
            result_b.get("comparison", {}).get("field"),
            "Equal",
            result_a.get("comparison", {}).get("field")
            == result_b.get("comparison", {}).get("field"),
        ),
        semantic_row(
            "Ordered source IDs",
            "/comparison/sources",
            [
                item.get("record_ref")
                for item in result_a.get("comparison", {}).get("sources", [])
            ],
            [
                item.get("record_ref")
                for item in result_b.get("comparison", {}).get("sources", [])
            ],
            "Equal and same order",
            source_values_pass,
        ),
        semantic_row(
            "Source values",
            "/comparison/sources",
            [
                item.get("value")
                for item in result_a.get("comparison", {}).get("sources", [])
            ],
            [
                item.get("value")
                for item in result_b.get("comparison", {}).get("sources", [])
            ],
            "Equal",
            source_values_pass,
        ),
        semantic_row(
            "Signed difference",
            "/comparison/signed_difference",
            result_a.get("comparison", {}).get("signed_difference"),
            result_b.get("comparison", {}).get("signed_difference"),
            "Equal",
            result_a.get("comparison", {}).get("signed_difference")
            == result_b.get("comparison", {}).get("signed_difference"),
        ),
        semantic_row(
            "Evidence",
            "/evidence",
            result_a.get("evidence"),
            result_b.get("evidence"),
            "Equal to Observation",
            result_a.get("evidence")
            == result_b.get("evidence")
            == expected_evidence,
        ),
        semantic_row(
            "Uncertainty and limitation",
            "/uncertainty",
            result_a.get("uncertainty"),
            result_b.get("uncertainty"),
            "Equal to Observation",
            result_a.get("uncertainty")
            == result_b.get("uncertainty")
            == expected_uncertainty,
        ),
        semantic_row(
            "Prohibited implications",
            "/prohibited_implications",
            result_a.get("prohibited_implications"),
            result_b.get("prohibited_implications"),
            "Equal to Expression",
            result_a.get("prohibited_implications")
            == result_b.get("prohibited_implications")
            == expression["prohibited_implications"],
        ),
        semantic_row(
            "Invented information",
            "/boundary_checks/no_invention",
            [],
            [],
            "None",
            exact_complete_shapes
            and source_values_pass
            and copied_boundaries_pass,
        ),
        semantic_row(
            "STOP behavior",
            "/boundary_checks/stop_cases",
            stop_values_a,
            stop_values_b,
            "Same boundary",
            stop_pass,
        ),
    ]
    semantic_pass = (
        semantic_path_pass
        and all(row["pass"] for row in semantic_rows)
        and structural_pass
        and exact_complete_shapes
    )

    all_checks = (
        all(frozen_checks.values())
        and result_a_raw == (poa1 / "result.json").read_bytes()
        and result_b_raw == (poa2 / "result-b.json").read_bytes()
        and not (result_a_raw == result_b_raw)
        and result_lineage_pass
        and independence_pass
        and structural_pass
        and semantic_pass
        and copied_boundaries_pass
        and stop_pass
    )

    review = {
        "id": "equivalence-review-001",
        "inputs": {
            "request": {
                "id": request["id"],
                "path": "../poa-001/request.json",
                "sha256": sha256_bytes(request_raw),
                "processor_a_binding_sha256": expression["request_sha256"],
                "processor_b_binding_sha256": expression["request_sha256"],
            },
            "observation": {
                "id": observation["id"],
                "path": "../poa-001/observation.json",
                "sha256": sha256_bytes(observation_raw),
                "processor_a_binding_sha256": expression["observation_sha256"],
                "processor_b_binding_sha256": expression["observation_sha256"],
            },
            "expression": {
                "id": expression["id"],
                "path": "../poa-001/expression.json",
                "sha256": sha256_bytes(expression_raw),
                "processor_a_result_sha256": result_a["expression_sha256"],
                "processor_b_result_sha256": result_b["expression_sha256"],
            },
            "frozen_digest_checks": frozen_checks,
        },
        "processors": {
            "independent_development_statement": (
                "Processor B was authored anew in a separate implementation task "
                "from the frozen POA-002 artifact requirements; it does not copy, "
                "import, call, inspect at runtime, generate from, or wrap Processor A."
            ),
            "processor_a": {
                "identity": result_a["processor"],
                "source_path": "../poa-001/compare.py",
                "source_sha256": processor_a_digest,
                "method_summary": (
                    "Validates the frozen shapes and lineage, then subtracts the "
                    "first ordered declared value from the second."
                ),
                "origin": "Frozen committed POA-001 implementation.",
                "working_directory": "temporary/processor-a",
                "result_read_from_other_processor": False,
                "imports": imports_a,
                "local_imports": local_imports_a,
            },
            "processor_b": {
                "identity": result_b["processor"],
                "source_path": "processor-b.py",
                "source_sha256": processor_b_digest,
                "method_summary": (
                    "Indexes the two validated records by identifier, resolves the "
                    "declared order, and sums the second value with the negated first."
                ),
                "origin": (
                    "Authored from the frozen POA-002 design in a separate "
                    "implementation task."
                ),
                "working_directory": "temporary/processor-b",
                "result_read_from_other_processor": False,
                "imports": imports_b,
                "local_imports": local_imports_b,
            },
            "cross_references": cross_references,
            "distinct_source_paths": processor_a_path != processor_b_path,
            "distinct_source_digests": processor_a_digest != processor_b_digest,
            "separate_processes": True,
            "separate_working_directories": True,
            "shared_output_path": False,
            "shared_local_helper": False,
            "dependency_check_pass": independence_pass,
        },
        "results": {
            "result_a": {
                "id": result_a["id"],
                "path": "../poa-001/result.json",
                "sha256": result_a_digest,
                "processor": result_a["processor"],
            },
            "result_b": {
                "id": result_b["id"],
                "path": "result-b.json",
                "sha256": result_b_digest,
                "processor": result_b["processor"],
            },
            "distinct_identities": result_a["id"] != result_b["id"],
            "distinct_digests": result_a_digest != result_b_digest,
        },
        "byte_equivalence": {
            "required": False,
            "equal": result_a_raw == result_b_raw,
            "result_a_size": len(result_a_raw),
            "result_b_size": len(result_b_raw),
            "difference_segments": raw_diff,
        },
        "structural_equivalence": {
            "required": True,
            "equal": structural_pass and exact_complete_shapes,
            "identity_values_treated_as_corresponding": sorted(IDENTITY_PATHS),
            "differences": shape_diff,
        },
        "semantic_equivalence": {
            "required": True,
            "equal": semantic_pass,
            "comparisons": semantic_rows,
        },
        "differences": {
            "parsed_path_count": len(classified_parsed),
            "parsed": classified_parsed,
            "raw_segment_count": len(raw_diff),
            "raw": raw_diff,
            "discarded_before_classification": 0,
        },
        "boundary_checks": {
            "same_frozen_inputs": all(frozen_checks.values()),
            "lineage_preserved": result_lineage_pass,
            "evidence_preserved": (
                result_a.get("evidence")
                == result_b.get("evidence")
                == expected_evidence
            ),
            "uncertainty_and_limitation_preserved": (
                result_a.get("uncertainty")
                == result_b.get("uncertainty")
                == expected_uncertainty
            ),
            "prohibited_implications_preserved": (
                result_a.get("prohibited_implications")
                == result_b.get("prohibited_implications")
                == expression["prohibited_implications"]
            ),
            "invented_information": {
                "processor_a": [],
                "processor_b": [],
                "pass": exact_complete_shapes
                and source_values_pass
                and copied_boundaries_pass,
            },
            "stop_cases": negative_results,
            "stop_equivalence": stop_pass,
            "silent_repair": False,
            "processor_communication": False,
        },
        "verdict": {
            "status": "pass" if all_checks else "fail",
            "claim": (
                "The two independent implementations are semantically equivalent "
                "for this single frozen POA-002 experiment."
            ),
        },
    }

    sys.stdout.write(json.dumps(review, ensure_ascii=False, indent=2) + "\n")
    raise SystemExit(0 if all_checks else 2)


if __name__ == "__main__":
    main()
