#!/usr/bin/env python3
"""Independent POA-002 implementation of the frozen COMPARE capability."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Any


PROCESSOR_ID = "poa-002-compare-b"
RESULT_ID = "result-002-b"
FROZEN_REQUEST_ID = "request-001"
FROZEN_REQUEST_SHA256 = (
    "d847553992b746790bc7f55dd8b58f06631c5f1e31fd0e8d60b6425f9fd7d52a"
)
FROZEN_PRESERVE = ["evidence", "uncertainty"]
FROZEN_PROHIBITED = ["preference", "recommendation", "domain-validity"]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: Path) -> tuple[bytes, Any]:
    raw = path.read_bytes()
    return raw, json.loads(raw)


def exact_keys(value: Any, keys: set[str]) -> bool:
    return isinstance(value, dict) and set(value) == keys


def is_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and (not isinstance(value, float) or math.isfinite(value))
    )


def observation_is_valid(value: Any) -> bool:
    if not exact_keys(
        value, {"id", "subject", "field", "records", "limitation"}
    ):
        return False
    if not all(
        isinstance(value[name], str)
        for name in ("id", "subject", "field", "limitation")
    ):
        return False
    records = value["records"]
    if not isinstance(records, list) or len(records) != 2:
        return False
    for record in records:
        if not exact_keys(
            record, {"id", "declared_value", "evidence", "uncertainty"}
        ):
            return False
        if not all(
            isinstance(record[name], str)
            for name in ("id", "evidence", "uncertainty")
        ):
            return False
        if not is_number(record["declared_value"]):
            return False
    return records[0]["id"] != records[1]["id"]


def expression_is_valid(value: Any) -> bool:
    if not exact_keys(
        value,
        {
            "id",
            "request_ref",
            "request_sha256",
            "observation_ref",
            "observation_sha256",
            "operator",
            "inputs",
            "field",
            "preserve",
            "prohibited_implications",
        },
    ):
        return False
    if not all(
        isinstance(value[name], str)
        for name in (
            "id",
            "request_ref",
            "request_sha256",
            "observation_ref",
            "observation_sha256",
            "operator",
            "field",
        )
    ):
        return False
    if (
        not isinstance(value["inputs"], list)
        or len(value["inputs"]) != 2
        or not all(isinstance(item, str) for item in value["inputs"])
    ):
        return False
    if value["preserve"] != FROZEN_PRESERVE:
        return False
    return value["prohibited_implications"] == FROZEN_PROHIBITED


def preserved_fields(
    observation: dict[str, Any], expression: dict[str, Any]
) -> dict[str, Any]:
    records = observation["records"]
    return {
        "evidence": [
            {"record_ref": record["id"], "value": record["evidence"]}
            for record in records
        ],
        "uncertainty": {
            "records": [
                {"record_ref": record["id"], "value": record["uncertainty"]}
                for record in records
            ],
            "limitation": observation["limitation"],
        },
        "prohibited_implications": expression["prohibited_implications"],
    }


def make_result(
    expression: dict[str, Any],
    expression_raw: bytes,
    processor_digest: str,
    preserved: dict[str, Any],
    *,
    reason: str | None = None,
    comparison: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "id": RESULT_ID if reason is None else f"{RESULT_ID}-blocked",
        "status": "complete" if reason is None else "blocked",
    }
    if reason is not None:
        result["reason"] = reason
    result.update(
        {
            "expression_ref": expression["id"],
            "expression_sha256": sha256_bytes(expression_raw),
            "processor": PROCESSOR_ID,
            "processor_sha256": processor_digest,
            "evidence": preserved["evidence"],
            "uncertainty": preserved["uncertainty"],
            "prohibited_implications": preserved["prohibited_implications"],
        }
    )
    if comparison is not None:
        result["comparison"] = comparison
    return result


def emit(value: dict[str, Any], exit_status: int) -> None:
    sys.stdout.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    raise SystemExit(exit_status)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: processor-b.py OBSERVATION EXPRESSION")

    observation_path = Path(sys.argv[1])
    expression_path = Path(sys.argv[2])

    try:
        observation_raw, observation = load_json(observation_path)
        expression_raw, expression = load_json(expression_path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SystemExit(f"input unreadable: {error}") from error

    if not observation_is_valid(observation):
        raise SystemExit("observation cannot preserve the frozen Result shape")

    if not isinstance(expression, dict):
        raise SystemExit("expression cannot preserve the frozen Result shape")

    fallback_prohibited = expression.get("prohibited_implications")
    if fallback_prohibited != FROZEN_PROHIBITED:
        raise SystemExit("expression cannot preserve prohibited implications")

    preserved = preserved_fields(observation, expression)
    processor_digest = sha256_bytes(Path(__file__).read_bytes())

    if not expression_is_valid(expression):
        emit(
            make_result(
                expression,
                expression_raw,
                processor_digest,
                preserved,
                reason="required_expression_shape_invalid",
            ),
            2,
        )

    if expression["operator"] != "COMPARE":
        emit(
            make_result(
                expression,
                expression_raw,
                processor_digest,
                preserved,
                reason="operator_not_implemented",
            ),
            2,
        )

    if (
        expression["request_ref"] != FROZEN_REQUEST_ID
        or expression["request_sha256"] != FROZEN_REQUEST_SHA256
    ):
        emit(
            make_result(
                expression,
                expression_raw,
                processor_digest,
                preserved,
                reason="request_lineage_conflict",
            ),
            2,
        )

    if (
        expression["observation_ref"] != observation["id"]
        or expression["observation_sha256"] != sha256_bytes(observation_raw)
    ):
        emit(
            make_result(
                expression,
                expression_raw,
                processor_digest,
                preserved,
                reason="input_digest_conflict",
            ),
            2,
        )

    if expression["field"] != observation["field"]:
        emit(
            make_result(
                expression,
                expression_raw,
                processor_digest,
                preserved,
                reason="comparison_field_conflict",
            ),
            2,
        )

    records_by_id = {record["id"]: record for record in observation["records"]}
    if (
        len(records_by_id) != 2
        or any(record_id not in records_by_id for record_id in expression["inputs"])
    ):
        emit(
            make_result(
                expression,
                expression_raw,
                processor_digest,
                preserved,
                reason="ordered_sources_unavailable",
            ),
            2,
        )

    ordered_records = tuple(
        records_by_id[record_id] for record_id in expression["inputs"]
    )
    ordered_values = tuple(
        record[expression["field"]] for record in ordered_records
    )
    signed_difference = sum((ordered_values[1], -ordered_values[0]))

    comparison = {
        "field": expression["field"],
        "sources": [
            {"record_ref": record["id"], "value": value}
            for record, value in zip(ordered_records, ordered_values)
        ],
        "signed_difference": signed_difference,
    }
    emit(
        make_result(
            expression,
            expression_raw,
            processor_digest,
            preserved,
            comparison=comparison,
        ),
        0,
    )


if __name__ == "__main__":
    main()
