"""Immutable input and output records for the LYRA language boundary."""

from __future__ import annotations

from dataclasses import dataclass

from ..transformation_engine import (
    OrientationObject,
    RepresentationTarget,
    TransformationReport,
)
from .vocabulary import LYRA_VOCABULARY_VERSION, OrientationIntent


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be non-empty text")


@dataclass(frozen=True, slots=True)
class HumanLanguageRequest:
    """A human utterance bound to an existing Orientation Object."""

    utterance: str
    orientation_object: OrientationObject

    def __post_init__(self) -> None:
        _require_text(self.utterance, "utterance")
        if not isinstance(self.orientation_object, OrientationObject):
            raise TypeError("orientation_object must be an OrientationObject")


@dataclass(frozen=True, slots=True)
class PlanningTranslation:
    """LYRA output composed exclusively from existing planning models."""

    request: HumanLanguageRequest
    intents: tuple[OrientationIntent, ...]
    source_representation: str
    target: RepresentationTarget
    vocabulary_version: str = LYRA_VOCABULARY_VERSION

    def __post_init__(self) -> None:
        if not isinstance(self.request, HumanLanguageRequest):
            raise TypeError("request must be a HumanLanguageRequest")
        intents = tuple(self.intents)
        if not intents or any(not isinstance(intent, OrientationIntent) for intent in intents):
            raise ValueError("intents must contain OrientationIntent values")
        _require_text(self.source_representation, "source_representation")
        if not isinstance(self.target, RepresentationTarget):
            raise TypeError("target must be a RepresentationTarget")
        if self.vocabulary_version != LYRA_VOCABULARY_VERSION:
            raise ValueError("unsupported LYRA vocabulary version")
        object.__setattr__(self, "intents", intents)


@dataclass(frozen=True, slots=True)
class LyraExplanation:
    """Human-readable projection that retains the exact source report."""

    source_report: TransformationReport
    sentences: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.source_report, TransformationReport):
            raise TypeError("source_report must be a TransformationReport")
        sentences = tuple(self.sentences)
        if not sentences or any(
            not isinstance(sentence, str) or not sentence.strip()
            for sentence in sentences
        ):
            raise ValueError("sentences must contain non-empty text")
        object.__setattr__(self, "sentences", sentences)

    @property
    def text(self) -> str:
        return "\n".join(self.sentences)

    @property
    def status(self) -> str:
        return self.source_report.status

    @property
    def evidence(self) -> tuple[str, ...]:
        return self.source_report.plan.evidence_chain

    @property
    def provenance(self):
        return self.source_report.plan.provenance_chain

    @property
    def blockers(self):
        return self.source_report.issues

    @property
    def alternatives(self) -> tuple[tuple[str, ...], ...]:
        return self.source_report.plan.alternative_paths


@dataclass(frozen=True, slots=True)
class LyraInteraction:
    """End-to-end composition result; every authoritative object remains intact."""

    translation: PlanningTranslation
    report: TransformationReport
    explanation: LyraExplanation

    def __post_init__(self) -> None:
        if not isinstance(self.translation, PlanningTranslation):
            raise TypeError("translation must be a PlanningTranslation")
        if not isinstance(self.report, TransformationReport):
            raise TypeError("report must be a TransformationReport")
        if not isinstance(self.explanation, LyraExplanation):
            raise TypeError("explanation must be a LyraExplanation")
        if self.explanation.source_report is not self.report:
            raise ValueError("explanation must retain the exact TransformationReport")
