#!/usr/bin/env python3
"""POA-001: one isolated implementation of the frozen minimal COMPARE slice."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Any


PROCESSOR_ID = "poa-001-compare"
EXPECTED_EXPRESSION_KEYS = {
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
}
EXPECTED_OBSERVATION_KEYS = {
    "id",
    "subject",
    "field",
    "records",
    "limitation",
}
EXPECTED_RECORD_KEYS = {
    "id",
    "declared_value",
    "evidence",
    "uncertainty",
}
EXPECTED_PROHIBITED_IMPLICATIONS = [
    "preference",
    "recommendation",
    "domain-validity",
]


class Blocked(Exception):
    """A visible POA-001 STOP with a stable reason."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> tuple[bytes, Any]:
    raw = path.read_bytes()
    try:
        return raw, json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Blocked("invalid_required_input_shape") from exc


def is_sha256(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    return all(character in "0123456789abcdef" for character in value)


def require_base_shapes(observation: Any, expression: Any) -> None:
    if not isinstance(observation, dict) or not isinstance(expression, dict):
        raise Blocked("invalid_required_input_shape")
    if set(observation) != EXPECTED_OBSERVATION_KEYS:
        raise Blocked("invalid_required_input_shape")
    if not isinstance(observation.get("records"), list):
        raise Blocked("invalid_required_input_shape")
    if len(observation["records"]) != 2:
        raise Blocked("invalid_required_input_shape")
    if any(
        not isinstance(record, dict) or set(record) != EXPECTED_RECORD_KEYS
        for record in observation["records"]
    ):
        raise Blocked("invalid_required_input_shape")
    if not isinstance(expression.get("prohibited_implications"), list):
        raise Blocked("invalid_required_input_shape")


def copied_evidence(observation: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {"record_ref": record["id"], "value": record["evidence"]}
        for record in observation["records"]
    ]


def copied_uncertainty(observation: dict[str, Any]) -> dict[str, Any]:
    return {
        "records": [
            {"record_ref": record["id"], "value": record["uncertainty"]}
            for record in observation["records"]
        ],
        "limitation": observation["limitation"],
    }


def common_result(
    *,
    observation: dict[str, Any],
    expression: dict[str, Any],
    expression_raw: bytes,
) -> dict[str, Any]:
    return {
        "expression_ref": expression["id"],
        "expression_sha256": sha256_bytes(expression_raw),
        "processor": PROCESSOR_ID,
        "processor_sha256": sha256_bytes(Path(__file__).read_bytes()),
        "evidence": copied_evidence(observation),
        "uncertainty": copied_uncertainty(observation),
        "prohibited_implications": list(expression["prohibited_implications"]),
    }


def validate(
    *,
    observation: dict[str, Any],
    observation_raw: bytes,
    expression: dict[str, Any],
) -> None:
    if expression.get("operator") != "COMPARE":
        raise Blocked("unsupported_operator")
    if set(expression) != EXPECTED_EXPRESSION_KEYS:
        raise Blocked("invalid_required_input_shape")
    if expression["observation_sha256"] != sha256_bytes(observation_raw):
        raise Blocked("observation_digest_mismatch")

    records = observation["records"]
    record_ids = [record["id"] for record in records]
    values = [record["declared_value"] for record in records]

    valid = (
        observation["id"] == "observation-001"
        and observation["subject"] == "Two supplied orientation records"
        and observation["field"] == "declared_value"
        and isinstance(observation["limitation"], str)
        and bool(observation["limitation"])
        and record_ids == ["record-a", "record-b"]
        and all(
            isinstance(record["evidence"], str)
            and bool(record["evidence"])
            and isinstance(record["uncertainty"], str)
            and bool(record["uncertainty"])
            for record in records
        )
        and all(
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(value)
            for value in values
        )
        and expression["id"] == "expression-001"
        and expression["request_ref"] == "request-001"
        and is_sha256(expression["request_sha256"])
        and expression["observation_ref"] == observation["id"]
        and expression["inputs"] == record_ids
        and expression["field"] == observation["field"]
        and expression["preserve"] == ["evidence", "uncertainty"]
        and expression["prohibited_implications"]
        == EXPECTED_PROHIBITED_IMPLICATIONS
    )
    if not valid:
        raise Blocked("invalid_required_input_shape")


def complete_result(
    *,
    observation: dict[str, Any],
    expression: dict[str, Any],
    expression_raw: bytes,
) -> dict[str, Any]:
    records = observation["records"]
    field = expression["field"]
    common = common_result(
        observation=observation,
        expression=expression,
        expression_raw=expression_raw,
    )
    return {
        "id": "result-001",
        "status": "complete",
        **common,
        "comparison": {
            "field": field,
            "sources": [
                {"record_ref": record["id"], "value": record[field]}
                for record in records
            ],
            "signed_difference": records[1][field] - records[0][field],
        },
    }


def blocked_result(
    *,
    reason: str,
    observation: dict[str, Any],
    expression: dict[str, Any],
    expression_raw: bytes,
) -> dict[str, Any]:
    common = common_result(
        observation=observation,
        expression=expression,
        expression_raw=expression_raw,
    )
    return {
        "id": f"result-001-{reason}",
        "status": "blocked",
        **common,
        "reason": reason,
    }


def write_result(result: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(result, ensure_ascii=False, indent=2))
    sys.stdout.write("\n")


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        sys.stderr.write("usage: compare.py OBSERVATION EXPRESSION\n")
        return 64

    try:
        observation_raw, observation = load_json(Path(argv[1]))
        expression_raw, expression = load_json(Path(argv[2]))
        require_base_shapes(observation, expression)
        try:
            validate(
                observation=observation,
                observation_raw=observation_raw,
                expression=expression,
            )
        except Blocked as exc:
            write_result(
                blocked_result(
                    reason=exc.reason,
                    observation=observation,
                    expression=expression,
                    expression_raw=expression_raw,
                )
            )
            return 2
        write_result(
            complete_result(
                observation=observation,
                expression=expression,
                expression_raw=expression_raw,
            )
        )
        return 0
    except (Blocked, KeyError, OSError, TypeError, ValueError) as exc:
        reason = exc.reason if isinstance(exc, Blocked) else "invalid_required_input_shape"
        sys.stderr.write(f"blocked: {reason}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
