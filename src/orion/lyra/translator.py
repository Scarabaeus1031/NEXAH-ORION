"""Deterministic translation from canonical human language to planning inputs."""

from __future__ import annotations

from dataclasses import dataclass
import re

from ..transformation_contracts import DEFAULT_REPRESENTATION_GRAPH, RepresentationGraph
from ..transformation_engine import RepresentationTarget
from .exceptions import (
    ClarificationRequired,
    UnknownRepresentation,
    UnknownTarget,
    UnsupportedIntent,
)
from .models import HumanLanguageRequest, PlanningTranslation
from .vocabulary import OrientationIntent, PLANNING_INTENTS, resolve_intent


_NATURAL_NAVIGATION = re.compile(
    r"^i want to understand how (?:this |the )?(.+?) reaches (?:the )?(.+?)[.]?$",
    re.IGNORECASE,
)


@dataclass(frozen=True, slots=True)
class LyraTranslator:
    """Map explicit language to existing models without planning or guessing."""

    graph: RepresentationGraph = DEFAULT_REPRESENTATION_GRAPH

    def __post_init__(self) -> None:
        if not isinstance(self.graph, RepresentationGraph):
            raise TypeError("graph must be a RepresentationGraph")

    def translate(self, request: HumanLanguageRequest) -> PlanningTranslation:
        if not isinstance(request, HumanLanguageRequest):
            raise TypeError("request must be a HumanLanguageRequest")

        utterance = " ".join(request.utterance.strip().split())
        natural = _NATURAL_NAVIGATION.fullmatch(utterance)
        if natural is not None:
            intents = (OrientationIntent.NAVIGATE, OrientationIntent.EXPLAIN)
            source_text, target_text = natural.groups()
        else:
            separator_count = utterance.count("→") + utterance.count("->")
            if separator_count > 1:
                raise ClarificationRequired(
                    "a planning request must identify exactly one source and target"
                )
            match = re.fullmatch(
                r"([A-Za-z ?]+?)\s+(.*?)\s*(?:→|->)\s*(.+?)[.]?",
                utterance,
            )
            if match is None:
                first_words = self._command_prefix(utterance)
                intent = resolve_intent(first_words)
                if intent is None:
                    raise UnsupportedIntent(
                        "the request does not use the canonical Orientation Vocabulary"
                    )
                raise ClarificationRequired(
                    f"{intent.value} does not identify one source-to-target planning request"
                )
            command, source_text, target_text = match.groups()
            intent = resolve_intent(command)
            if intent is None:
                raise UnsupportedIntent(
                    "the request does not use the canonical Orientation Vocabulary"
                )
            if intent not in PLANNING_INTENTS:
                raise ClarificationRequired(
                    f"{intent.value} is not a source-to-target planning intent"
                )
            intents = (intent,)

        source = self._resolve_source(source_text)
        target = self._resolve_target(target_text)
        actual_source = request.orientation_object.representation.representation_type
        if source != actual_source:
            raise ClarificationRequired(
                f"request source {source} does not match supplied Orientation Object "
                f"representation {actual_source}"
            )
        return PlanningTranslation(
            request=request,
            intents=intents,
            source_representation=source,
            target=RepresentationTarget(target),
        )

    def _command_prefix(self, utterance: str) -> str:
        normalized = utterance.casefold()
        for intent in sorted(OrientationIntent, key=lambda item: len(item.value), reverse=True):
            phrase = intent.value.rstrip("?")
            if normalized.startswith(phrase.casefold()):
                return phrase
        return utterance.split(maxsplit=1)[0]

    def _resolve_source(self, value: str) -> str:
        resolved = self._resolve_representation(value)
        if resolved is None:
            raise UnknownRepresentation(
                f"unknown source representation: {value.strip()}"
            )
        return resolved

    def _resolve_target(self, value: str) -> str:
        resolved = self._resolve_representation(value)
        if resolved is None:
            raise UnknownTarget(f"unknown target representation: {value.strip()}")
        return resolved

    def _resolve_representation(self, value: str) -> str | None:
        normalized = " ".join(value.strip().rstrip(".").casefold().split())
        for prefix in ("this ", "the "):
            if normalized.startswith(prefix):
                normalized = normalized[len(prefix):]
        aliases = {
            "calendar": "Calendar Projection",
            "observation": "Observation",
        }
        if normalized in aliases:
            candidate = aliases[normalized]
            return candidate if candidate in self.graph.representations else None
        return next(
            (
                representation
                for representation in self.graph.representations
                if representation.casefold() == normalized
            ),
            None,
        )
