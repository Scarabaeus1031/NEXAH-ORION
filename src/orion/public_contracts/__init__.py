"""Executable definitions of the frozen ORION Public Contract Suite 1.0."""

from .fixtures import CANONICAL_CONTRACT_SET
from .models import *  # noqa: F403 - this package is the public contract boundary
from .models import __all__ as _model_exports
from .validation import (
    ContractSet,
    ContractValidationResult,
    ValidationIssue,
    validate_clarification_result,
    validate_continuation_option,
    validate_contract_set,
    validate_evidence_reference,
    validate_orientation_report,
    validate_orientation_request,
    validate_public_contract,
    validate_runtime_error,
)

__all__ = [
    *_model_exports,
    "CANONICAL_CONTRACT_SET",
    "ContractSet",
    "ContractValidationResult",
    "ValidationIssue",
    "validate_clarification_result",
    "validate_continuation_option",
    "validate_contract_set",
    "validate_evidence_reference",
    "validate_orientation_report",
    "validate_orientation_request",
    "validate_public_contract",
    "validate_runtime_error",
]
