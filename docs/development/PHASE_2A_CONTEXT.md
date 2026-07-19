# Phase 2A: deterministischer Repository-Kontext

## Zweck

Phase 2A ergänzt die erste Context-Building-Schicht vor dem austauschbaren
Reasoning-Backend. Eine Anfrage kann damit explizit ausgewählte Dokumente aus
einem lokalen Repository erhalten, bevor das Backend aufgerufen wird.

```text
OrientationRequest
  -> ContextBuilder
  -> RepositoryContextProvider
  -> ContextManifest
  -> ReasoningBackend
  -> ReasoningResult
  -> Validation
  -> OrientationResponse
```

Der Builder bewertet, rankt oder interpretiert keine Inhalte. Er führt keine
Netzwerkaufrufe aus und kennt kein Reasoning-Backend.

## Komponenten und Verantwortlichkeiten

| Komponente | Verantwortung | Darf ausdrücklich nicht |
|---|---|---|
| `RepositoryContextProvider` | explizite repository-relative UTF-8-Dateien read-only laden | suchen, ranken, schreiben oder einem Symlink-Ziel außerhalb des Repository folgen |
| `ContextBuilder` | geladene Einträge an eine Anfrage binden und ein `ContextManifest` erzeugen | ein Backend aufrufen oder Kontext mutieren |
| `ContextualOrientationExecutor` | Builder, injiziertes Backend und bestehende Validation in dieser Reihenfolge koordinieren | Kontext auswählen, Providerdetails übernehmen oder Validation umgehen |
| `ReasoningBackend` | aus Request und Manifest einen untrusted Kandidaten erzeugen | Kontext, Kernel oder Library verändern |
| Validation | Request-, Manifest-, Backend- und Evidenzbindungen prüfen | einen Kernel-Entscheid erzeugen |

Der bisherige `OrientationExecutor` bleibt als eingefrorene Phase-1A-Baseline
unverändert. Phase 2A ergänzt mit `ContextualOrientationExecutor` eine neue
Komposition, anstatt die bestehende Ausführungsgrenze umzudeuten.

## Explizite Dokumentauswahl

Die Auswahl wird beim Erzeugen des Builders vollständig angegeben. Der Provider
normalisiert die Pfade, entfernt doppelte Angaben und lädt die eindeutigen Pfade
in lexikalischer Reihenfolge. Fehlende Dokumente führen zu
`ContextDocumentNotFoundError`; es gibt kein stilles Überspringen und keinen
Fallback.

Absolute Pfade, `..`, Backslash-Trenner und Symlinks mit einem Ziel außerhalb des
Repository-Roots werden abgelehnt. Gelesen werden ausschließlich reguläre
UTF-8-Dateien.

Beispiel:

```python
from pathlib import Path

from orion import (
    ContextBuilder,
    ContextualOrientationExecutor,
    FakeBackend,
    OrientationRequest,
    RepositoryContextProvider,
)

provider = RepositoryContextProvider(
    repository_root=Path("."),
    source_id="orion",
    owner="NEXAH ORION",
    revision="0.3.0-dev.0",
)
builder = ContextBuilder(
    provider=provider,
    document_paths=(
        "README.md",
        "docs/architecture/ORION_ARCHITECTURE.md",
        "docs/adr/0004-immutable-context-manifest.md",
    ),
)
request = OrientationRequest(
    request_id="review-002",
    objective="Review the selected ORION architecture documents.",
    requested_by="local-operator",
    scope=("architecture",),
)
response = ContextualOrientationExecutor(
    backend=FakeBackend(),
    context_builder=builder,
).execute(request)
```

`revision` wird explizit injiziert. Der Provider ermittelt weder selbstständig
einen Git-Stand noch verändert er das Repository. Aufrufer können einen
vollständigen Commit-Hash, einen dokumentierten Baseline-Identifier oder eine
andere verfügbare Dokumentversion angeben. Ist keine Version verfügbar, muss dies
mit einem stabilen Wert wie `unversioned` ausdrücklich kenntlich gemacht werden;
ein leeres Revisionsfeld ist im eingefrorenen Contract nicht zulässig.

## Manifest und Provenienz

Phase 2A verwendet die eingefrorenen Phase-1A-Verträge unverändert:

| Geforderte Angabe | Bestehendes Contract-Feld |
|---|---|
| Source-Identifier und Dokumentpfad | `ContextEntry.source_ref`, kanonisch als `<source_id>:<repository-relative-path>` |
| stabile Eintrags-ID | `ContextEntry.entry_id`, identisch zur kanonischen Source Reference |
| Dokument-Hash | `ContextEntry.content_sha256` |
| Dokumentversion, sofern verfügbar | `ContextEntry.revision` |
| Eigentümer | `ContextEntry.owner` |
| Provenienzmetadaten | `ContextManifest.provenance` mit ID, Owner, Source Reference, Revision und Hash |

Der SHA-256-Wert wird aus den exakten UTF-8-Inhalten gebildet. Der Manifest-Hash
bindet Request-ID, Reihenfolge und inhaltsfreie Provenienz aller Einträge. Gleiche
Anfrage, Auswahl, Revision und Dateiinhalte erzeugen daher dasselbe Manifest.
Ändert sich ein Dokument, ändert sich sein Digest und damit das Manifest.

Manifest, Einträge, Provenienz und Builder-Konfiguration sind immutable
Dataclasses beziehungsweise Tupel. Das ist eine Integritäts- und
Auditierbarkeitsgarantie innerhalb dieser Phase, keine kryptografische Signatur.

## Tests

```bash
make test
```

Die Unit-Tests decken ab:

- deterministische Manifest-Erzeugung;
- reproduzierbare lexikalische Ordnung;
- Verhinderung doppelter Einträge;
- explizites Verhalten bei fehlenden Dokumenten;
- Ablehnung von Repository-Escapes;
- Immutabilität von Builder, Manifest und Einträgen;
- vollständige Ausführung über Builder, Backend, Validation und Response.

## Grenzen

- ein Repository-Provider und explizite Dateiauswahl
- kein inhaltliches Ranking oder automatisches Discovery
- keine token- oder größenbasierte Kontextbudgetierung
- keine Teilabschnitte, Chunking oder inkrementelle Nachladung
- keine Library-, Builder-Hub- oder Kernel-Integration
- keine Runtime- oder Backend-Änderung
- keine Persistenz oder Run-Aufzeichnung

## Zukünftige Retrieval-Strategie

Eine spätere Retrieval-Phase kann zusätzliche Provider und Auswahlstrategien vor
dem bestehenden Builder-Port ergänzen. Dafür müssen Ownership, Auswahlbegründung,
Budgetierung, Ranking-Provenienz und Reproduzierbarkeit zuerst separat entschieden
werden. Embeddings, Vector Stores, semantische Suche, RAG und Prompt-Optimierung
sind keine implizite Fortsetzung dieses Providers und bleiben ausdrücklich
verschoben.

Phase 2A schafft nur die auditierbare Grenze: Auswahl hinein, immutable Manifest
heraus.
