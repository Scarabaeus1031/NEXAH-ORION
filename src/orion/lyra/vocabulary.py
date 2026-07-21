"""Canonical Phase 6A Orientation Vocabulary used by the Phase 6B boundary."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


LYRA_VOCABULARY_VERSION = "orion.lyra-vocabulary/0.1"


class OrientationIntent(str, Enum):
    OBSERVE = "Observe"
    REPRESENT = "Represent"
    PROJECT = "Project"
    NAVIGATE = "Navigate"
    COMPARE = "Compare"
    EXPLAIN = "Explain"
    INSPECT = "Inspect"
    PLAN = "Plan"
    VALIDATE = "Validate"
    WHY = "Why"
    SHOW_ALTERNATIVES = "Show Alternatives"
    WHAT_IS_MISSING = "What is missing?"


@dataclass(frozen=True, slots=True)
class VocabularyEntry:
    intent: OrientationIntent
    existing_concepts: tuple[str, ...]
    planning_input: bool = False
    report_view: bool = False


CANONICAL_ORIENTATION_VOCABULARY = (
    VocabularyEntry(OrientationIntent.OBSERVE, ("Observation", "Provenance")),
    VocabularyEntry(OrientationIntent.REPRESENT, ("OrientationObject", "RepresentationRef")),
    VocabularyEntry(
        OrientationIntent.PROJECT,
        ("RepresentationTarget", "TransitionContract"),
        planning_input=True,
    ),
    VocabularyEntry(
        OrientationIntent.NAVIGATE,
        ("TransformationEngine", "TransformationPlan"),
        planning_input=True,
    ),
    VocabularyEntry(OrientationIntent.COMPARE, ("TransformationReport",), report_view=True),
    VocabularyEntry(OrientationIntent.EXPLAIN, ("TransformationReport",), report_view=True),
    VocabularyEntry(OrientationIntent.INSPECT, ("TransformationReport", "Provenance"), report_view=True),
    VocabularyEntry(
        OrientationIntent.PLAN,
        ("TransformationPlan", "RepresentationTarget"),
        planning_input=True,
    ),
    VocabularyEntry(OrientationIntent.VALIDATE, ("TransformationValidation",), report_view=True),
    VocabularyEntry(OrientationIntent.WHY, ("TransformationIssue", "checks"), report_view=True),
    VocabularyEntry(
        OrientationIntent.SHOW_ALTERNATIVES,
        ("TransformationPlan.alternative_paths",),
        report_view=True,
    ),
    VocabularyEntry(
        OrientationIntent.WHAT_IS_MISSING,
        ("TransformationIssue",),
        report_view=True,
    ),
)

PLANNING_INTENTS = frozenset(
    entry.intent for entry in CANONICAL_ORIENTATION_VOCABULARY if entry.planning_input
)
REPORT_VIEW_INTENTS = frozenset(
    entry.intent for entry in CANONICAL_ORIENTATION_VOCABULARY if entry.report_view
)


def resolve_intent(command: str) -> OrientationIntent | None:
    """Resolve one exact vocabulary phrase without inference or fuzzy matching."""

    normalized = " ".join(command.strip().casefold().rstrip(".").split())
    for intent in OrientationIntent:
        candidate = " ".join(intent.value.casefold().rstrip("?").split())
        if normalized.rstrip("?") == candidate:
            return intent
    return None
