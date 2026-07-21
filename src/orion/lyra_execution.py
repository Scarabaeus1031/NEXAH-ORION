"""ORION-owned composition around the non-authoritative LYRA boundary."""

from __future__ import annotations

from dataclasses import dataclass, field

from .lyra import (
    HumanLanguageRequest,
    LyraExplainer,
    LyraInteraction,
    LyraTranslator,
)
from .transformation_engine import TransformationEngine


@dataclass(frozen=True, slots=True)
class LyraOrientationExecutor:
    """Translate, delegate planning unchanged, then explain the exact report."""

    engine: TransformationEngine = field(default_factory=TransformationEngine)
    translator: LyraTranslator = field(default_factory=LyraTranslator)
    explainer: LyraExplainer = field(default_factory=LyraExplainer)

    def __post_init__(self) -> None:
        if not isinstance(self.engine, TransformationEngine):
            raise TypeError("engine must be a TransformationEngine")
        if not isinstance(self.translator, LyraTranslator):
            raise TypeError("translator must be a LyraTranslator")
        if not isinstance(self.explainer, LyraExplainer):
            raise TypeError("explainer must be a LyraExplainer")
        if self.translator.graph != self.engine.graph:
            raise ValueError("translator and engine must use the same Representation Graph")

    def execute(self, request: HumanLanguageRequest) -> LyraInteraction:
        translation = self.translator.translate(request)
        report = self.engine.execute(
            request.orientation_object,
            translation.target,
        )
        explanation = self.explainer.explain(report)
        return LyraInteraction(
            translation=translation,
            report=report,
            explanation=explanation,
        )
