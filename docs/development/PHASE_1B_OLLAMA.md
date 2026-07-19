# Phase 1B: lokales Ollama-Referenzbackend

## Zweck

`OllamaBackend` ist die erste reale Implementierung des bestehenden
`ReasoningBackend`-Ports. Der Adapter ersetzt keine Phase-1A-Komponente. Er wird
dem unveränderten `OrientationExecutor` per Dependency Injection übergeben.

```text
OrientationRequest
  -> ContextManifest
  -> OllamaBackend
  -> lokale Ollama HTTP API
  -> llama3.1:8b
  -> ReasoningResult
  -> unabhängige Validation
  -> OrientationResponse
```

Providerdetails enden im Adapter. ORION erhält ausschließlich bestehende
`ReasoningResult`-, `ReasoningClaim`- und Fehlerobjekte ohne Ollama-Antworttypen.
Der Adapter erzeugt weder Kernel-Kommandos noch Library-Schreibvorgänge und kann
den eingefrorenen Kontext nicht verändern.

## Runtime-Lifecycle

Ollama ist eine externe lokale Runtime. ORION und `OllamaBackend` dürfen den
Dienst weder installieren noch starten, stoppen, neu starten oder überwachen.
Der Adapter führt ausschließlich einen bereits erreichbaren HTTP-Aufruf aus.

Ist die Runtime nicht erreichbar, endet der Aufruf kontrolliert mit dem
provider-neutralen `ReasoningBackendUnavailableError`, einer Unterklasse von
`ReasoningBackendError`. Es gibt keinen automatischen Startversuch und keinen
Fallback auf einen anderen Endpoint oder Provider.

## Laufzeitanforderungen

- Python 3.10 oder neuer
- Ollama 0.32.1 oder eine separat verifizierte kompatible Version
- laufender lokaler Ollama-Dienst
- installiertes Modell `llama3.1:8b`
- verifizierter lokaler Modell-Digest:
  `46e0c10c039e019119339687c3c1757cc81b9da49709a3b3924863ba87ca666e`

Der Python-Adapter verwendet ausschließlich die Standardbibliothek. Es gibt kein
Ollama-SDK und keine zusätzliche Runtime-Abhängigkeit im ORION-Paket.

## Konfiguration

| Parameter | Standard | Bedeutung |
|---|---|---|
| `model` | kein impliziter Standard | expliziter Ollama-Modellname |
| `endpoint` | `http://127.0.0.1:11434` | lokaler API-Origin |
| `timeout` | `120.0` | gesamter HTTP-Timeout in Sekunden |

Nur explizite Loopback-Adressen und `localhost` werden akzeptiert. Pfade,
Query-Parameter, eingebettete Zugangsdaten und entfernte Hosts werden abgelehnt.
HTTP-Proxies sind deaktiviert und Redirects werden nicht verfolgt. Dadurch kann
diese Phase nicht versehentlich einen Cloud-Endpunkt verwenden.

## Ausführungsbeispiel

```python
from orion import (
    ContextEntry,
    OllamaBackend,
    OrientationExecutor,
    OrientationRequest,
)

request = OrientationRequest(
    request_id="review-001",
    objective="Prüfe die angegebene Autoritätsgrenze.",
    requested_by="local-operator",
    scope=("architecture",),
)
context = ContextEntry.create(
    entry_id="architecture-principle",
    owner="ORION",
    source_ref="docs/architecture/ORION_ARCHITECTURE.md",
    revision="phase-1b",
    content="The model proposes. The Orchestrator validates. The Kernel decides.",
)
backend = OllamaBackend(
    model="llama3.1:8b",
    endpoint="http://127.0.0.1:11434",
    timeout=180,
)
response = OrientationExecutor(backend).execute(request, (context,))
```

Der Adapter fordert eine strukturierte JSON-Antwort an, beschränkt
`evidence_refs` auf die IDs des Manifests und übersetzt die Antwort anschließend
streng in `ReasoningResult`. Das ersetzt nicht die unabhängige Validation. Eine
formal übersetzbare, aber unbelegte Behauptung wird weiterhin dort abgelehnt.

## Tests

Alle isolierten Tests, einschließlich Phase 1A:

```bash
make test
```

Echter lokaler Modelllauf:

```bash
make integration
```

Optionale Konfiguration:

```bash
ORION_OLLAMA_MODEL=llama3.1:8b \
ORION_OLLAMA_ENDPOINT=http://127.0.0.1:11434 \
ORION_OLLAMA_TIMEOUT=180 \
make integration
```

Der Integrationstest ist bewusst opt-in. CI und dokumentarische Checks benötigen
weder einen laufenden Dienst noch Modellgewichte.

## Fehlerverhalten

| Fehler | ORION-Ausnahme |
|---|---|
| Timeout | `ReasoningBackendTimeoutError` |
| externe lokale Runtime nicht erreichbar | `ReasoningBackendUnavailableError` |
| HTTP-Fehler oder zu große Antwort | `ReasoningBackendResponseError` |
| ungültiges Ollama- oder Kandidaten-JSON | `ReasoningBackendResponseError` |

Provider-Response-Bodies werden nicht als Fehlerobjekte nach außen gereicht.

## Troubleshooting

### Verbindung abgelehnt

Prüfen, ob Ollama läuft:

```bash
ollama --version
curl http://127.0.0.1:11434/api/version
```

Falls kein Dienst läuft, muss der lokale Runtime-Operator ihn außerhalb von ORION
starten. Der Adapter übernimmt diese Aufgabe niemals.

### Modell fehlt

```bash
ollama list
```

Der Integrationstest lädt kein Modell automatisch herunter. Modellinstallation
und Lizenzprüfung bleiben explizite lokale Betriebsaufgaben.

### Timeout beim ersten Lauf

Der erste Lauf kann das Modell erst in den Speicher laden. `timeout` beziehungsweise
`ORION_OLLAMA_TIMEOUT` erhöhen und erneut testen. Ein Timeout wird nicht als
ReasoningResult behandelt.

### Antwort wird als malformed abgelehnt

Der Adapter akzeptiert nur die eingefrorene provider-neutrale Ergebnisform. Rohtext,
Markdown, leere Claims, unvollständige Streaming-Antworten und unerwartete
Modellantworten werden verworfen. Die Strenge ist Teil der Autoritätsgrenze.

## Grenzen dieser Phase

- ausschließlich Ollama; keine weiteren Provider
- ausschließlich lokale Loopback-Kommunikation
- kein Streaming, Tool Calling, Embedding oder Vision
- kein automatisches Routing oder Capability Negotiation
- keine Persistenz oder Replay-Datenbank
- keine Kernel- oder Library-Schreiboperation
- kein Installieren, Starten, Stoppen oder Überwachen der Ollama-Runtime
- keine Garantie bitidentischer Modellantworten
- `backend_id` enthält den Modelltag, aber der eingefrorene `ReasoningResult`
  besitzt noch kein separates Feld für den Ollama-Modell-Digest

`llama.cpp` bleibt das geplante zweite Conformance-Backend. Es wird in Phase 1B
nicht implementiert.
