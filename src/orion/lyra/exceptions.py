"""Provider-neutral LYRA language-boundary failures."""


class LyraLanguageError(ValueError):
    """Base class for deterministic language translation failures."""


class UnsupportedIntent(LyraLanguageError):
    """The utterance does not use the canonical Orientation Vocabulary."""


class ClarificationRequired(LyraLanguageError):
    """The utterance is known but does not identify one unambiguous request."""


class UnknownRepresentation(LyraLanguageError):
    """The requested source is absent from the registered Representation Graph."""


class UnknownTarget(LyraLanguageError):
    """The requested target is absent from the registered Representation Graph."""
