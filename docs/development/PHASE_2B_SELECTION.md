# Phase 2B: deterministische Dokumentauswahl

## Zweck

Phase 2B entscheidet vor dem Context Building, welche Repository-Dokumente zu
einer Anfrage gehören. Der Aufrufer gibt keine Dokumentpfade mehr an. ORION
leitet sie ausschließlich aus versionierten, expliziten Scope-Regeln ab.

```text
OrientationRequest
  -> DocumentSelector
  -> SelectionResult
  -> RepositoryContextProvider
  -> ContextBuilder
  -> ContextManifest
  -> ReasoningBackend
  -> ReasoningResult
  -> Validation
  -> OrientationResponse
```

Der Phase-2A-`ContextBuilder` bleibt unverändert und ist in der Phase-2-Pipeline
weiterhin die einzige Komponente, die `ContextManifest`-Objekte erzeugt. Der
eingefrorene Phase-1A-Executor bleibt als historische Baseline unangetastet.

## Verantwortlichkeiten

| Komponente | Verantwortung | Nicht erlaubt |
|---|---|---|
| `DocumentSelector` | Request-Metadaten lesen und explizite Scope-Regeln anwenden | Dateien lesen, Repository crawlen, Inhalte bewerten, Manifest oder Backend aufrufen |
| `DocumentSelectionRule` | eine versionierte Scope-zu-Pfad-Zuordnung beschreiben | versteckte Discovery- oder Rankinglogik |
| `SelectionResult` | geordnete Pfade, Ruleset-ID und Auswahlprovenienz immutable festhalten | Dokumentinhalte oder Dokument-Hashes enthalten |
| `RepositoryContextProvider` | die ausgewählten Pfade anschließend read-only laden | Auswahlentscheidungen treffen |
| `ContextBuilder` | geladene Dokumente hashen und an ein Manifest binden | Auswahlregeln interpretieren |
| `SelectingOrientationExecutor` | Selector, Provider, unveränderten Builder und bestehende Ausführung komponieren | Pfade ergänzen oder Regeln überschreiben |

## Warum Auswahl und Context Building getrennt sind

Eine Auswahl beantwortet: „Welche Quellen sollen geprüft werden?“ Context
Building beantwortet: „Welche exakten Inhalte und Digests wurden verwendet?“
Diese Entscheidungen haben unterschiedliche Provenienz und dürfen nicht
verschmelzen.

Der Selector kann deshalb deterministisch getestet werden, ohne dass die Dateien
existieren. Erst der Provider prüft Existenz, Repository-Grenze und UTF-8-Inhalt.
Erst der Builder erzeugt Dokument-Hashes und den Manifest-Hash. Ein
`SelectionResult` enthält ausdrücklich keinen Content-Digest.

## Erste explizite Regeln

Das Ruleset `explicit-scope-selection/1` enthält drei Scope-Regeln:

| Scope | Regel | Explizit ausgewählte Bereiche |
|---|---|---|
| `architecture` | `scope-architecture/1` | Root-README, Architektur-Baseline und die bestehenden ADR-Dokumente |
| `backend` | `scope-backend/1` | Phase-1A/1B-Backend-Dokumentation, Backend-Port, Contracts, Executor, Adapter und Tests |
| `validation` | `scope-validation/1` | Phase-1A-Dokumentation, Contracts, Validation und relevante Ausführungstests |

Die vollständigen Dateilisten stehen als Konstanten in
`src/orion/document_selector.py`. Es gibt keine Verzeichnisexpansion und kein
automatisches Auffinden neuer Dateien. Neue Dokumente werden erst durch eine
reviewte Regeländerung Teil einer Auswahl.

Bei mehreren bekannten Scopes bildet der Selector die Vereinigungsmenge aller
expliziten Pfade, entfernt Duplikate und sortiert lexikalisch. Diese Reihenfolge
entspricht der deterministischen Ordnung des unveränderten Context Builders.

Ein unbekannter Scope führt zu `UnknownDocumentScopeError`. Ein leerer Scope oder
eine explizite Regel ohne Pfade führt zu `EmptyDocumentSelectionError`. ORION
rät weder einen Scope noch ein Ersatzdokument.

## SelectionResult und Provenienz

`SelectionResult` enthält:

- `request_id` als Bindung an die Anfrage;
- `selected_paths` als eindeutiges, lexikalisch geordnetes Tupel;
- `rule_id` als Version des gesamten Rulesets;
- `selection_provenance` mit Request-ID, Request-Typ, Auftraggeber,
  Request-Schemaversion, Objective und allen angewendeten Scope-Regel-IDs.

Objective und Request-Metadaten werden damit explizit inspiziert und auditierbar
festgehalten. In Phase 2B lösen sie keine Wortsuche oder Heuristik aus; die
Pfadauswahl wird ausschließlich durch exakte Scope-Bezeichner bestimmt.

Dokument-Hashes, Inhalte und Manifest-IDs fehlen absichtlich. Sie gehören allein
dem nachfolgenden Provider und Context Builder.

## Ausführung

```python
from pathlib import Path

from orion import (
    DocumentSelector,
    FakeBackend,
    OrientationRequest,
    RepositoryContextProvider,
    SelectingOrientationExecutor,
)

request = OrientationRequest(
    request_id="review-003",
    objective="Review the ORION validation boundary.",
    requested_by="local-operator",
    scope=("validation",),
)
executor = SelectingOrientationExecutor(
    backend=FakeBackend(),
    selector=DocumentSelector(),
    context_provider=RepositoryContextProvider(
        repository_root=Path("."),
        source_id="orion",
        owner="NEXAH ORION",
        revision="0.3.0-dev.0",
    ),
)

selection = executor.select(request)
response = executor.execute(request)
```

`select()` exponiert das reproduzierbare Auswahlprotokoll zur Prüfung. `execute()`
leitet dieselbe deterministische Auswahl an einen neu konfigurierten, aber
unveränderten `ContextBuilder` weiter. Der Aufrufer reicht keine Pfade ein.

## Tests

```bash
make test
```

Die Phase-2B-Tests decken ab:

- wiederholbar identische Auswahl;
- kontrollierte Ablehnung unbekannter Scopes;
- kontrollierte Ablehnung leerer Auswahlen;
- lexikalische Ordnung;
- Duplikatvermeidung innerhalb und zwischen Regeln;
- Ruleset- und Regelprovenienz;
- Inhalts- und Hashfreiheit des `SelectionResult`;
- Auswahl ohne Dateizugriff;
- vollständige Übergabe an den unveränderten Context Builder.

## Grenzen

- keine semantische Suche oder Heuristik
- keine Embeddings oder Vector Database
- kein automatisches Repository-Crawling
- kein Prompt Engineering
- kein Token-Budget oder Größenranking
- keine Library- oder Builder-Hub-Integration
- keine Runtime-, Backend- oder Kernel-Änderung
- keine persistierte Selection-Historie

## Zukünftige Erweiterungsstrategie

Weitere deterministische Scopes können als neue versionierte Regeln ergänzt
werden. Änderungen an bestehenden Pfadmengen benötigen Review, weil sie die
Evidenzbasis zukünftiger Runs verändern. Regeln für Request-Typen oder andere
explizite Metadaten benötigen ebenfalls eine eigene Rule-ID und Tests.

Semantisches Retrieval, Ranking, Repository-Discovery und Budgetierung bleiben
separate spätere Architekturentscheidungen. Sie dürfen weder stillschweigend in
`DocumentSelector` noch in `ContextBuilder` einziehen.
