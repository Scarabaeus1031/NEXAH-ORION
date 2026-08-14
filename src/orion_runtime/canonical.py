"""ORION Canonical JSON 1.0 utilities."""

from __future__ import annotations

from hashlib import sha256
import json
from typing import Any


class CanonicalJSONError(ValueError):
    """Raised when input cannot enter ORION Canonical JSON."""


def canonical_bytes(value: object) -> bytes:
    _reject_floats(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def digest_ref(data: bytes) -> str:
    return f"sha256:{sha256(data).hexdigest()}"


def parse_json_bytes(data: bytes) -> Any:
    if data.startswith(b"\xef\xbb\xbf"):
        raise CanonicalJSONError("UTF-8 BOM is forbidden")
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise CanonicalJSONError("body is not strict UTF-8") from exc

    def object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise CanonicalJSONError(f"duplicate object key: {key}")
            result[key] = value
        return result

    def reject_float(value: str) -> None:
        raise CanonicalJSONError(f"floating-point number is forbidden: {value}")

    try:
        value = json.loads(
            text,
            object_pairs_hook=object_pairs,
            parse_float=reject_float,
            parse_constant=reject_float,
        )
    except (json.JSONDecodeError, TypeError) as exc:
        raise CanonicalJSONError("malformed JSON") from exc
    _reject_floats(value)
    return value


def _reject_floats(value: object) -> None:
    if isinstance(value, float):
        raise CanonicalJSONError("floating-point numbers are forbidden")
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise CanonicalJSONError("object keys must be strings")
        for item in value.values():
            _reject_floats(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _reject_floats(item)
    elif value is not None and not isinstance(value, (str, int, bool)):
        raise CanonicalJSONError(f"unsupported canonical value: {type(value).__name__}")
