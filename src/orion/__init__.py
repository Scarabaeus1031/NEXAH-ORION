"""Provider-independent ORION execution and transformation boundaries."""

from .backend import ReasoningBackend
from .brief_backend import ContextBriefReasoningBackend
from .brief_execution import ContextBriefOrientationExecutor
from .context_brief import (
    CONTEXT_BRIEF_SCHEMA,
    ContextBrief,
    ContextBriefBuilder,
    ContextBriefEntry,
)
from .context_builder import (
    ContextBuilder,
    ContextDocumentError,
    ContextDocumentNotFoundError,
    InvalidContextDocumentPathError,
    RepositoryContextProvider,
)
from .context_execution import ContextualOrientationExecutor
from .contracts import (
    ContextEntry,
    ContextManifest,
    OrientationRequest,
    OrientationResponse,
    ProvenanceRef,
    ReasoningClaim,
    ReasoningResult,
    ValidationReport,
)
from .document_selector import (
    DEFAULT_SELECTION_RULES,
    DocumentSelectionError,
    DocumentSelectionRule,
    DocumentSelector,
    EmptyDocumentSelectionError,
    SelectionResult,
    UnknownDocumentScopeError,
)
from .executor import OrientationExecutor
from .fake_backend import FakeBackend
from .ollama_backend import (
    OllamaBackend,
    ReasoningBackendError,
    ReasoningBackendResponseError,
    ReasoningBackendTimeoutError,
    ReasoningBackendUnavailableError,
)
from .selection_execution import SelectingOrientationExecutor
from .transformation_contracts import (
    DEFAULT_REPRESENTATION_GRAPH,
    DEFAULT_TRANSITION_CONTRACTS,
    HARD_INVARIANTS,
    TRANSITION_CONTRACT_SCHEMA,
    GraphEdge,
    RepresentationGraph,
    TransitionContract,
    TransitionContractRegistry,
)
from .transformation_engine import (
    TRANSFORMATION_PLAN_SCHEMA,
    TRANSFORMATION_REPORT_SCHEMA,
    OrientationObject,
    PlannedTransition,
    RepresentationRef,
    RepresentationTarget,
    TransformationEngine,
    TransformationIssue,
    TransformationPlan,
    TransformationProvenanceStep,
    TransformationReport,
    TransformationValidation,
)
from .validation import validate_execution

__all__ = [
    "CONTEXT_BRIEF_SCHEMA",
    "ContextBrief",
    "ContextBriefBuilder",
    "ContextBriefEntry",
    "ContextBriefOrientationExecutor",
    "ContextBriefReasoningBackend",
    "ContextEntry",
    "ContextBuilder",
    "ContextDocumentError",
    "ContextDocumentNotFoundError",
    "ContextManifest",
    "ContextualOrientationExecutor",
    "DEFAULT_SELECTION_RULES",
    "DocumentSelectionError",
    "DocumentSelectionRule",
    "DocumentSelector",
    "EmptyDocumentSelectionError",
    "FakeBackend",
    "GraphEdge",
    "HARD_INVARIANTS",
    "InvalidContextDocumentPathError",
    "OrientationObject",
    "OrientationExecutor",
    "OrientationRequest",
    "OrientationResponse",
    "OllamaBackend",
    "PlannedTransition",
    "ProvenanceRef",
    "ReasoningBackend",
    "ReasoningBackendError",
    "ReasoningBackendResponseError",
    "ReasoningBackendTimeoutError",
    "ReasoningBackendUnavailableError",
    "ReasoningClaim",
    "ReasoningResult",
    "RepositoryContextProvider",
    "RepresentationGraph",
    "RepresentationRef",
    "RepresentationTarget",
    "SelectionResult",
    "SelectingOrientationExecutor",
    "TRANSFORMATION_PLAN_SCHEMA",
    "TRANSFORMATION_REPORT_SCHEMA",
    "TRANSITION_CONTRACT_SCHEMA",
    "TransitionContract",
    "TransitionContractRegistry",
    "TransformationEngine",
    "TransformationIssue",
    "TransformationPlan",
    "TransformationProvenanceStep",
    "TransformationReport",
    "TransformationValidation",
    "UnknownDocumentScopeError",
    "ValidationReport",
    "validate_execution",
    "DEFAULT_REPRESENTATION_GRAPH",
    "DEFAULT_TRANSITION_CONTRACTS",
]

__version__ = "0.3.0.dev0"
