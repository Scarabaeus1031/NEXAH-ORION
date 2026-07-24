#!/usr/bin/env python3
"""Execute the first deterministic ORION Representation proof."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from orion.representation_alpha import (  # noqa: E402
    ExactTextRenderer,
    confirmed_source_from_mapping,
    representation_as_dict,
    validate_representation,
)


FIXTURE = ROOT / "examples" / "representation_alpha" / "confirmed_local_source.json"


def main() -> int:
    source = confirmed_source_from_mapping(
        json.loads(FIXTURE.read_text(encoding="utf-8"))
    )
    representation = ExactTextRenderer().render(source)
    conformance = validate_representation(source, representation)
    print(
        json.dumps(
            {
                "profile": "ORION Representation Alpha · exact text",
                "source": {
                    "entry_id": source.entry.entry_id,
                    "source_ref": source.entry.source_ref,
                    "source_version": source.entry.revision,
                    "fragment_ref": source.fragment_ref,
                    "confirmation_id": source.confirmation_id,
                },
                "representation": representation_as_dict(representation),
                "conformance": asdict(conformance),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if conformance.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
