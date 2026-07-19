# Phase 1A: kleinste vollständige ORION-Ausführung

## Zweck

Phase 1A beweist, dass die stabile Architektur genau eine Anfrage vollständig
ausführen kann, ohne Modell, Netzwerk, Provider-SDK, Persistenz oder Kernel-Aufruf.
Das Ergebnis ist ein validierter Kandidat und ausdrücklich keine kanonische
Entscheidung.

```text
OrientationRequest
  -> ContextManifest
  -> ReasoningBackend
  -> FakeBackend
  -> ReasoningResult
  -> Validation
  -> OrientationResponse
```

## Eigentumsgrenzen

| Bestandteil | Eigentümer | Aussage |
|---|---|---|
| `OrientationRequest` | Aufrufer an der ORION-Grenze | Absicht, Typ und Scope der Anfrage |
| `ContextManifest` | ORION | eingefrorener Kontext mit Quelle, Eigentümer, Revision und Digest |
| `ReasoningBackend` | ORION | einziger austauschbarer Reasoning-Port |
| `FakeBackend` | ORION-Test-/Entwicklungsadapter | deterministischer Vorschlag ohne externe Effekte |
| `ReasoningResult` | Backend-Ausgabe, untrusted | Kandidat und evidenzgebundene Claims |
| `ValidationReport` | ORION | unabhängige Prüfung der Bindungen und Evidenzreferenzen |
| `OrientationResponse` | ORION | validierte Grenzantwort; niemals Kernel-Wahrheit |

Der Executor orchestriert nur. Er übernimmt weder Kernel- noch Library- oder
Builder-Autorität. Ein abgelehntes Backend-Ergebnis wird protokollierbar
zurückgegeben, aber Kandidat und Claims werden nicht als gültige Ausgabe exponiert.

## Provenienz

Jeder Kontexteintrag trägt `owner`, `source_ref`, `revision` und einen SHA-256-Digest
des Inhalts. Das Manifest bindet diese Angaben an die Anfrage. Claims referenzieren
Kontexteinträge ausschließlich über deren IDs. Die finale Antwort enthält die
inhaltsfreie Provenienzkette und das separate Validierungsergebnis.

Die Digests dienen in Phase 1A der Integritäts- und Reproduzierbarkeitsprüfung. Sie
sind weder Signaturen noch ein dauerhaft freigegebenes Austauschformat.

## Ausführen

Voraussetzung ist Python 3.10 oder neuer. Es werden ausschließlich Module der
Python-Standardbibliothek geladen.

```bash
make demo
make test
```

Falls `python3` nicht die gewünschte Version bezeichnet:

```bash
ORION_PYTHON=/absolute/path/to/python3.12 make test
```

## Bewusst nicht enthalten

- echtes LLM oder intelligente Heuristik
- Netzwerkzugriff und Provider-SDK
- öffentliche Schemas oder Cross-Repository-API
- Context Retrieval, Ranking oder Prompt Rendering
- Persistenz, Replay Store oder Telemetrie
- Kernel-Aufruf, Kernel-Mutation oder kanonische Effekte
- Library- und Builder-Hub-Integration

Diese Punkte bleiben verschoben, bis ihre jeweilige Architektur- und
Vertragseigentümerschaft den bestehenden Governance-Prozess durchlaufen hat.
