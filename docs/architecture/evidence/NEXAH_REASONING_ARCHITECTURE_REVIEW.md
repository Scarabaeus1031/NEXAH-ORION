# NEXAH × LLAMA – Architekturreview und Zielbild

Stand: 19. Juli 2026
Status: Architekturentscheidung, kein Implementierungsentwurf

## 1. Entscheidungsfassung

NEXAH sollte Reasoning **nicht** als weitere Engine im bestehenden Kernel modellieren. Der Kernel bleibt die autoritative, deterministische Orientierungsschicht. Darüber liegt ein eigener **Orientation Orchestrator**, der strukturierte Aufträge plant, Kontext zusammenstellt, Reasoning-Backends aufruft, Ergebnisse prüft und ausschließlich über Kernel-Kommandos in NEXAH zurückschreibt.

Das Kernprinzip lautet:

> Das Modell schlägt vor. Der Orchestrator prüft. Der Kernel entscheidet und protokolliert.

Damit wird nicht nur der Modellanbieter austauschbar. Auch Retrieval, Prompt-Rendering, Werkzeugnutzung, Validierung und Evaluierung bleiben jeweils separat ersetzbar und beobachtbar.

## 2. Quellenlage und Grenzen

Ausgewertet wurden 22 PNG-Visualisierungen aus dem Builder-Hub-ZIP. Sie zeigen eine Construction-Documents-Serie (überwiegend Version 0.1, Mai 2025) mit Mission, Master Plan, Orientation Kernel, Project Scope, Reference Implementation, Application Landscape, Question Lifecycle, Data Flow, Architecture, Ecosystem, Roadmap, Design Principles und Build Philosophy.

Der bereitgestellte Workspace enthält aktuell nur ein leeres Git-Repository ohne Commit. Der behauptete Freeze-Stand, die sechs Subsysteme, Tests, Release Checks, Repository Map, Editorial OS und Review Toolbox konnten deshalb lokal nicht verifiziert werden. Der Google-Drive-Connector war bei der Analyse noch nicht verfügbar. Aussagen zum heutigen Core werden daher als vom Auftraggeber gesetzte Baseline, nicht als geprüfter Repository-Befund behandelt.

## 3. Was aus den Construction Documents erhalten bleiben sollte

### Weiterhin tragfähig

- **One Kernel, many applications**: Domänen und Oberflächen dürfen den Kern nicht verändern.
- **Structure first / protocol first**: Schnittstellen und Invarianten gehen Implementierungsdetails voraus.
- **Provenance, Boundaries, Evidence** als Kernkonzepte, nicht als spätere Zusatzfunktionen.
- Der Lifecycle **Wonder → Orient → Explore → Synthesize → Answer → Apply → Reflect → Share** als fachliche Orientierung, nicht als fest verdrahtete LLM-Chain.
- Der Datenfluss **Sources → Ingest → Structure → Orient → Reason → Output → Feedback** als konzeptionelle Pipeline.
- **Open, composable, observable, testable, replaceable** als Architekturqualitäten.
- Die Trennung zwischen Framework/Protokoll, Referenzimplementierung, Anwendungen, Builder-Netzwerk und gesellschaftlicher Wirkung.

### Erkennbar weiterentwickelt

- Die frühere „NEXAHEDRON Engine“-Referenzimplementierung ist laut aktueller Projektbeschreibung inzwischen der eingefrorene NEXAH Core mit sechs Subsystemen.
- „Question Engine“ und „Comparison Engine“ sind nicht mehr sinnvoll als monolithische Kern-Engines. Ihre deterministischen Operationen gehören in den Kernel; heuristische Planung und Synthese gehören in den Orchestrator.
- Der frühere REST-/API-zentrierte Datenfluss muss um typisierte Requests, Artefakte, Capability Negotiation, Policy und Evaluierung ergänzt werden.
- „AI Assistant“ darf nicht nur Anwendungskanal sein. Reasoning wird eine kontrollierte Infrastrukturleistung hinter dem Orchestrator.

### Neu zu entwerfen

- Die Visuals setzen „Reasoning Engine“ als einzelnen Pipeline-Kasten voraus. Für Modellunabhängigkeit ist das zu grob.
- Ein direkter Pfeil `Context → Model → Answer` reicht nicht. Es fehlen Budgetierung, Retrieval-Plan, Kontextmanifest, strukturierte Ausgabe, Validierung, Reparatur, Audit und Replay.
- „OpenAI-compatible“ ist ein Transportvorteil, aber kein fachlicher NEXAH-Vertrag.
- Open WebUI ist eine optionale Oberfläche, kein Reasoning-Backend und keine Core-Abhängigkeit.
- Das Modell darf NEXAH-Objekte nicht unmittelbar mutieren.

## 4. Zielarchitektur

```text
Applications / Builder Hub / Editorial OS / Review Toolbox
                         │
                 Orientation Requests
                         │
              ┌──────────▼──────────┐
              │ Orientation         │
              │ Orchestrator        │
              ├─────────────────────┤
              │ Request validation  │
              │ Task planning       │
              │ Context planning    │
              │ Policy & budgets    │
              │ Backend routing     │
              │ Result validation   │
              │ Evaluation & audit  │
              └───────┬───────┬─────┘
                      │       │
          read/query  │       │ propose commands
                      │       │
              ┌───────▼───────▼─────┐
              │ NEXAH Core / Kernel │
              │                     │
              │ Posets & Lattices   │
              │ Orientation Graphs  │
              │ Neighborhoods       │
              │ Reader Paths        │
              │ Review Corpora      │
              │ Atlas Objects       │
              │ Evidence/Provenance │
              │ Boundaries/Policy   │
              └──────────┬──────────┘
                         │ typed snapshots / views
              ┌──────────▼──────────┐
              │ Context Pipeline    │
              │ discovery           │
              │ retrieval/ranking   │
              │ graph expansion     │
              │ compression         │
              │ manifest/citations  │
              └──────────┬──────────┘
                         │ BackendRequest
              ┌──────────▼──────────┐
              │ Reasoning Port      │
              └──┬────┬────┬────┬──┘
                 │    │    │    │
              GPT Claude Ollama llama.cpp / vLLM / future
```

## 5. Autoritätsgrenzen

### NEXAH Core ist autoritativ für

- Identitäten, Typen und Relationen von NEXAH-Objekten
- Invarianten von Posets, Lattices und Graphen
- Provenance, Versionen, Status und Grenzen
- kanonische Schreiboperationen
- Berechtigungen, Publikationsstatus und Historie

### Orientation Orchestrator ist autoritativ für

- Ausführung eines Orientation Request
- Auswahl von Kontextstrategie und Reasoning-Profil
- Budgets, Abbruchbedingungen, Retry- und Fallback-Politik
- Validierung, Reparaturversuche und Evaluierung
- vollständiges Run-Protokoll und Reproduzierbarkeit

### Reasoning Backend ist autoritativ für nichts im Domänenmodell

Es erzeugt Kandidaten: Hypothesen, Vergleiche, Klassifikationen, Zusammenfassungen, Pfadvorschläge oder vorgeschlagene Kernel-Kommandos. Jede Ausgabe ist untrusted input, bis Schema-, Evidenz-, Policy- und Domänenprüfung erfolgreich waren.

## 6. Verträge statt Anbieter-Abstraktionen

### OrientationRequest

Ein Request sollte mindestens enthalten:

- `request_id`, `request_type`, `schema_version`
- Ziel und erwartete Ergebnisart
- Referenzen auf NEXAH-Objekte statt eingebettetem Volltext
- Scope und explizite Ausschlüsse
- Evidence Policy und Citation Requirements
- Qualitäts-, Kosten-, Latenz- und Datenschutzbudget
- gewünschte Determinismus-/Reproduzierbarkeitsstufe
- erlaubte Werkzeuge und erlaubte Schreibwirkungen
- Output-Schema

Spezialisierungen: `ReviewRequest`, `NavigationRequest`, `ComparisonRequest`, `AtlasRequest`, `BuilderRequest`. Dies sind versionierte fachliche Verträge, keine unterschiedlichen Backend-APIs.

### ContextPackage

- unveränderliches `ContextManifest`
- Objekt-Snapshots mit IDs und Versionen
- ausgewählte Evidenzsegmente mit Provenance
- relevante Nachbarschaften/Graphausschnitte
- explizite Auslassungen und Retrieval-Begründungen
- Token-/Größenbudget und Digest jedes Bestandteils

### BackendRequest

- gerenderte Messages/Promptfragmente
- Response-Schema
- Tool-Spezifikationen
- Sampling- und Stop-Konfiguration
- Modell-/Runtime-Anforderungen über Capabilities
- Deadline, Tokenlimit, Seed soweit unterstützt

### ReasoningResult

- typisierte Payload
- Claims mit Evidence-Referenzen
- Unsicherheiten und offene Konflikte
- vorgeschlagene Kernel-Kommandos, nie direkte Mutationen
- Backend-, Modell-, Adapter- und Prompt-Template-Version
- Usage, Timing, Finish Reason und rohe Antwort als geschütztes Audit-Artefakt

## 7. Backend-Adapter

Ein `ReasoningBackend` sollte nur die minimale Inferenzgrenze abbilden:

- `describeCapabilities()`
- `health()`
- `invoke(BackendRequest)`
- `stream(BackendRequest)` optional
- `cancel(run_id)` optional

Capabilities müssen zur Laufzeit verhandelt werden, z. B. strukturierte Ausgabe, Tool Calling, Vision, Embeddings, Kontextfenster, Seeds, Logprobs, Streaming und Parallel Tool Calls. Keine Anwendung darf über `instanceof GPTBackend` oder Anbieter-Namen verzweigen. Routing erfolgt gegen Anforderungen und Policies.

Adapter normalisieren Transport und Metadaten. Sie dürfen keine NEXAH-Fachlogik, Retrieval-Logik oder Prompt-Inhalte besitzen. Anbieterbesonderheiten bleiben in kleinen Codec-/Mapper-Komponenten innerhalb des Adapters.

## 8. Laufzeitentscheidung

### Empfehlung

1. **Ollama als erstes lokales Referenz-Backend** für den vertikalen Architekturbeweis.
2. **llama.cpp als zweites Conformance-Backend**, um zu beweisen, dass der Vertrag nicht versehentlich Ollama-spezifisch ist.
3. **vLLM als skalierendes Serving-Backend**, sobald GPU-Server, Parallelität und belastbare Betriebsmetriken relevant werden.
4. **LM Studio als optionale Entwickleroberfläche**, nicht als Architekturvoraussetzung.
5. **Open WebUI ausschließlich als optionale Anwendung/Operations-UI**, nicht als Backend.

Begründung: Ollama minimiert Installations- und Modellmanagementaufwand und bietet OpenAI-kompatible Endpunkte, Tools, strukturierte Ausgabe und Embeddings. llama.cpp bietet die direkteste, leichtgewichtige Kontrolle über GGUF, Grammars und CPU/GPU-Ausführung, verlangt aber mehr Betriebs- und Templatepflege. vLLM ist auf hohen Durchsatz sowie verteiltes GPU-Serving ausgelegt und wäre für den ersten lokalen Architekturbeweis unnötig schwer. LM Studio ist stark für interaktive lokale Entwicklung, erhöht als kanonische Runtime aber die Produktkopplung. Open WebUI aggregiert Backends und Benutzerfunktionen; es ist eine Oberfläche, keine stabile Inferenzgrenze.

Wichtig: Der erste Meilenstein gilt erst als bestanden, wenn derselbe Acceptance Corpus gegen mindestens zwei Backends läuft. Sonst ist „Modellunabhängigkeit“ nur eine Behauptung.

## 9. Context Pipeline ohne massive Prompts

1. **Request normalisieren**: Ziele, Scope, Objekt-IDs, Policies und Output-Schema validieren.
2. **Deterministische Discovery**: Repository Map, Symbolindex, Objektregister, Metadaten und Provenance zuerst nutzen.
3. **Hybrides Retrieval**: strukturierte Filter + Graphtraversal + lexikalische Suche + Embedding-Suche.
4. **Neighborhood Expansion**: nur relevante Vorgänger, Nachfolger, Grenzen, Gegenbeispiele und Evidenzkanten nachladen.
5. **Reranking nach Zweck**: Relevanz allein reicht nicht; Autorität, Aktualität, Diversität und Widerspruch zählen.
6. **Strukturtreue Kompression**: keine freie Zusammenfassung ohne Rückverweise; Objekt- und Claim-IDs erhalten.
7. **Context Assembly**: Budget pro Segmentklasse, feste Reihenfolge, Deduplizierung, Konfliktmarkierung.
8. **Manifest versiegeln**: Hashes, Versionen, Retrieval-Query, Ranking-Scores und Auslassungen speichern.
9. **Iterative Nachladung**: Backend darf gezielte Context Queries vorschlagen; Orchestrator entscheidet und protokolliert.

Prompt Caching ist eine Optimierung. Ein Context Manifest ist die Reproduzierbarkeitsgrundlage.

## 10. Interaktion mit strukturierten NEXAH-Objekten

- **Posets/Lattices**: Kernel berechnet Ordnung, Meets/Joins und Invarianten; Modell interpretiert, vergleicht oder schlägt Kandidaten vor.
- **Orientation Graphs**: Modell erhält begrenzte Subgraphen und darf neue Kanten als evidenzgebundene Vorschläge liefern.
- **Neighborhoods**: Retrieval-Primitiv mit Richtung, Radius, Kantentypen, Zeit- und Autoritätsfiltern.
- **Reader Paths**: Modell kann Pfade entwerfen; Kernel prüft Knotenexistenz, Übergänge, Grenzen und Versionen.
- **Review Corpora**: zugleich Kontextquelle und versionsgebundener Acceptance-/Regression-Corpus.
- **Atlas Objects**: stabile Referenzen auf Karten, Sichten und Navigationsartefakte; Rendering bleibt außerhalb des Modells.

Kein Domänenobjekt sollte ausschließlich als Prompttext serialisiert werden. Jedes benötigt eine kanonische, versionierte Projektion für Maschinen und eine separate menschenlesbare Darstellung.

## 11. Prompts werden Renderer, nicht Produktverträge

Prompts bleiben intern notwendig, sind aber kompiliertes Laufzeitmaterial. Der stabile Vertrag ist der `OrientationRequest`.

```text
OrientationRequest
  → Request Validator
  → Task/Context Plan
  → ContextPackage
  → Prompt Renderer (backend/model family/version)
  → BackendRequest
  → ReasoningResult
  → Validators
  → Proposed Kernel Commands
```

Prompt-Templates werden versioniert und zusammen mit Modell, Adapter, Kontextmanifest und Evaluierung gespeichert. Ein Anbieterwechsel erfordert idealerweise einen neuen Renderer und neue Conformance-Ergebnisse, nicht Änderungen an Anwendungen oder Core.

## 12. Reproduzierbarkeit richtig definieren

Bit-identische Modellantworten sind backendübergreifend nicht realistisch. NEXAH sollte drei Ebenen unterscheiden:

- **Replayable**: kompletter Input, Manifest, Versionen, Parameter und Rohantwort sind rekonstruierbar.
- **Repeatable**: gleicher Backend-/Modell-Build und Seed erzeugen innerhalb definierter Toleranzen dasselbe Resultat.
- **Equivalent**: verschiedene Backends erfüllen dieselben fachlichen Invarianten und Qualitätsgrenzen.

Für Modellunabhängigkeit ist semantische Äquivalenz wichtiger als Textgleichheit.

## 13. Roadmap mit Gates

### Phase A – Architecture

- Architecture Decision Records für Autoritätsgrenzen, Request-Modell, Context Manifest und Reproduzierbarkeit
- Ist-Abgleich mit den realen sechs Subsystemen
- Threat Model und Data Classification

**Gate:** Kein Reasoning-Backend kennt oder mutiert Core-Interna.

### Phase B – Interfaces

- versionierte Schemas für Requests, ContextPackage, BackendRequest, Result und vorgeschlagene Kernel-Kommandos
- Capability-Matrix und Fehler-/Cancellation-Modell
- Contract-Test-Suite mit Fake Backend

**Gate:** Anwendungen und Core kompilieren konzeptionell gegen eigene Ports, nicht gegen Anbieter-SDKs.

### Phase C – Prototype

- ein einziger vertikaler Use Case, vorzugsweise `ReviewRequest`
- deterministisches Retrieval aus einem kleinen Review Corpus
- Dry-run: keine Schreibwirkung, nur Vorschläge und Audit

**Gate:** Jeder Claim ist auf Context-IDs zurückführbar; fehlende Evidenz wird als solche ausgewiesen.

### Phase D – Backends

- Ollama-Adapter
- llama.cpp-Adapter gegen denselben Corpus
- optional ein Cloud-Adapter als dritter Heterogenitätstest

**Gate:** Capability-basierte Auswahl und fachliche Conformance auf mindestens zwei Laufzeiten.

### Phase E – Structured Objects

- kanonische Projektionen für Graphen, Posets/Lattices, Neighborhoods, Reader Paths und Atlas Objects
- Invariantenprüfung vor jeder Übernahme

**Gate:** Keine Modellantwort kann ungültige Core-Zustände erzeugen.

### Phase F – Builder Integration

- Review/Diff/Approve-Workflow
- Run Inspector mit Context Manifest, Claims, Kosten, Latenz und Validation Results
- Rollback über neue Versionen/Ereignisse, nicht durch History-Rewrite

**Gate:** Menschen können jede vorgeschlagene Wirkung vor Ausführung nachvollziehen.

### Phase G – Production & Scale

- vLLM oder verwaltete Backends, Queueing, SLOs, Rate Limits, Isolation
- Shadow Runs, Canary Routing und Qualitäts-/Kostenrouting
- Golden Corpus plus adversariale und boundary-spezifische Tests

**Gate:** Backendwechsel ist eine Konfigurations-/Deploymententscheidung mit messbarer Qualitätsfreigabe.

## 14. Chancen und Risiken

### Größte Chancen

- Das vorhandene Review Corpus kann zum dauerhaften, modellübergreifenden Acceptance Benchmark werden.
- Provenance und Boundaries sind bereits kulturell und architektonisch verankert; das ist ein Wettbewerbsvorteil gegenüber nachträglich abgesicherten RAG-Systemen.
- Atlas, Reader Paths und Neighborhoods erlauben kontextsparendes, graphbasiertes Retrieval statt Prompt-Aufblähung.
- Der Builder Hub kann vom Inhaltswerkzeug zum inspectable Reasoning Control Plane werden.
- Capability- und Qualitätsrouting ermöglicht lokale Vertraulichkeit, Cloud-Spitzenqualität und später Kostenoptimierung ohne Fachumbau.

### Kritische Risiken

- Ein universeller `generate(prompt)`-Adapter würde die Komplexität nur verstecken und Anbietersemantik in Anwendungen leaken lassen.
- Die Gleichsetzung von OpenAI-Kompatibilität mit Backend-Unabhängigkeit ist falsch; Semantik, Tool Calls, JSON-Schema, Seeds und Fehler unterscheiden sich.
- Modellgenerierte Graphoperationen ohne Kernelprüfung gefährden Invarianten und Autorität.
- Automatische Kontextzusammenfassungen ohne Manifest zerstören Provenance und Replay.
- Zu frühes Multi-Agent-Design vervielfacht Zustände, Kosten und Debuggingflächen. Erst einen einzelnen orchestrierten Run beherrschen.
- Das derzeit fehlende eingefrorene Repository verhindert einen belastbaren Integrationsschnitt. Architektur-Mapping muss vor Interface-Freeze nachgeholt werden.

## 15. Unmittelbar nächste Entscheidungen

1. Den eingefrorenen NEXAH-Core in diesem Workspace verfügbar machen oder seine Repository Map bereitstellen.
2. Einen `ReviewRequest` als ersten fachlichen Vertical Slice wählen und den bestehenden Review Corpus als Golden Set bestimmen.
3. Vier ADRs beschließen: Autorität, Request/Result-Verträge, Context Manifest, Backend Capabilities.
4. Erst danach Interface-Schemas entwerfen.
5. Ollama und llama.cpp früh gegeneinander testen; die zweite Implementierung ist der eigentliche Beweis der Abstraktion.

## 16. Externe Primärquellen zur Runtime-Entscheidung

- Ollama OpenAI compatibility: https://docs.ollama.com/api/openai-compatibility
- Ollama embeddings: https://docs.ollama.com/capabilities/embeddings
- llama.cpp HTTP server: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
- LM Studio local server/headless: https://lmstudio.ai/docs/developer/core/server und https://lmstudio.ai/docs/developer/core/headless
- vLLM OpenAI-compatible serving: https://docs.vllm.ai/en/stable/serving/openai_compatible_server/
- vLLM parallelism/scaling: https://docs.vllm.ai/en/stable/serving/parallelism_scaling/
- Open WebUI: https://docs.openwebui.com/
