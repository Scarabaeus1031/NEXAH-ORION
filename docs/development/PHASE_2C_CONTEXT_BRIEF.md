# Phase 2C: deterministischer Context Brief

## Zweck

Phase 2C leitet aus jedem gültigen `ContextManifest` eine immutable,
inhaltsfreie Präsentationsbeschreibung ab. Der `ContextBrief` hält fest, in
welcher Reihenfolge und mit welcher Provenienz der Kontext einem Backend
präsentiert wird, ohne selbst Dokumenttext, Prompt oder Interpretation zu
enthalten.

```text
OrientationRequest
  -> DocumentSelector
  -> RepositoryContextProvider
  -> ContextBuilder
  -> ContextManifest
  -> ContextBriefBuilder
  -> ContextBrief
  -> ContextBriefReasoningBackend
  -> ReasoningResult
  -> Validation gegen ContextManifest
  -> OrientationResponse
```

`DocumentSelector`, `RepositoryContextProvider` und `ContextBuilder` bleiben
unverändert. Der Context Builder ist in der Phase-2-Pipeline weiterhin die einzige
Komponente, die Manifeste erzeugt.

## Verantwortlichkeiten

| Komponente | Beantwortet | Verantwortung |
|---|---|---|
| `ContextBuilder` | „Was wurde exakt geladen?“ | Inhalte, Quellrevisionen, Content-Digests und Manifest-Integrität binden |
| `ContextBriefBuilder` | „Wie wird dieser Kontext präsentiert?“ | Manifest-Reihenfolge und inhaltsfreie Metadaten deterministisch projizieren |
| `ContextBriefReasoningBackend` | „Was schlage ich daraus vor?“ | Request und Brief als untrusted Reasoning-Eingabe behandeln |
| Validation | „Ist der Vorschlag korrekt gebunden?“ | Ergebnis weiterhin gegen Request, ursprüngliches Manifest, Backend-ID und Evidenzreferenzen prüfen |

Der Brief Builder wählt keine Dokumente aus, liest keine Repository-Datei, ruft
kein Backend auf und führt weder Zusammenfassung noch Ranking durch. Seine einzige
Eingabe ist ein bereits gültiges `ContextManifest`.

## Warum Manifest und Brief getrennt sind

Das Manifest ist die Integritätsaufzeichnung des tatsächlich geladenen Kontexts.
Es enthält die exakten Dokumenttexte und beweist über Digests, welche Inhalte
verwendet wurden. Der Brief ist eine inhaltsfreie Projektion dieser Aufzeichnung.
Er macht Präsentationsreihenfolge, Länge, Revision und Provenienz explizit, ohne
die geladenen Inhalte zu duplizieren.

Die Trennung verhindert drei Ownership-Verschiebungen:

- Auswahlregeln gelangen nicht in die Inhalts- oder Präsentationsschicht.
- Präsentationsmetadaten verändern weder Dokumente noch Manifest.
- Backends übernehmen weder Dateizugriff noch Manifest-Erzeugung.

Ein Brief kann jederzeit reproduziert werden. Gleicher Manifest-Stand erzeugt
denselben Brief, dieselbe Brief-ID und denselben Brief-Digest.

## ContextBrief-Contract

`ContextBrief` ist ein neuer interner Phase-2C-Contract mit dem Schema
`orion.context-brief/0.1`. Er enthält:

- `brief_id`, `brief_sha256` und `schema_version`;
- die Bindung an `request_id`, `manifest_id` und `manifest_sha256`;
- ein immutable Tupel geordneter `ContextBriefEntry`-Objekte.

Jeder Eintrag enthält:

| Feld | Bedeutung |
|---|---|
| `source_ref` | unveränderte Source Reference des Manifest-Eintrags |
| `repository_path` | deterministisch aus der kanonischen Source Reference abgeleiteter Repository-Pfad |
| `revision` | Dokument- beziehungsweise Repository-Revision |
| `content_sha256` | unveränderter Content-Digest aus dem Manifest |
| `provenance` | vollständige bestehende `ProvenanceRef` |
| `document_length` | Länge des ursprünglichen Dokumenttexts in UTF-8-Bytes |
| `document_order` | nullbasierte Position im ursprünglichen Manifest |

Der Contract besitzt kein `content`- und kein `prompt`-Feld. Der Brief-Digest
bindet alle Felder und deren Reihenfolge. Dokumentpositionen müssen eindeutig,
lückenlos und mit `0` beginnend sein.

Vor der Ableitung ruft `ContextBriefBuilder` die bestehende Manifest- und
Entry-Integritätsprüfung erneut auf. Ein nachträglich manipulierter Manifest- oder
Content-Digest wird deshalb abgelehnt.

## Backend-Port ohne Änderung eingefrorener Contracts

Der Phase-1A-`ReasoningBackend`-Port ist eingefroren und typisiert seine zweite
Eingabe als `ContextManifest`. Phase 2C ändert diesen Port nicht. Stattdessen
ergänzt `ContextBriefReasoningBackend` additiv dieselbe provider-neutrale Grenze
mit `ContextBrief` als Eingabe.

Dadurch bleiben `FakeBackend`, `OllamaBackend` und sämtliche Phase-1A/1B-Tests
unverändert. Neue brief-fähige Backends implementieren den additiven Port und
geben weiterhin ausschließlich den bestehenden provider-neutralen
`ReasoningResult` zurück. Validation behält das ursprüngliche Manifest und prüft
Evidenzreferenzen weiterhin dagegen.

Phase 2C implementiert keinen neuen Modellprovider und passt Ollama nicht an.

## Ausführungskomposition

`ContextBriefOrientationExecutor` komponiert die bestehende Phase-2-Pipeline:

1. Request deterministisch selektieren;
2. selektierte Dateien über den bestehenden Provider laden;
3. Manifest ausschließlich durch den unveränderten Context Builder erzeugen;
4. Brief durch `ContextBriefBuilder` ableiten;
5. Request und Brief an ein injiziertes brief-fähiges Backend übergeben;
6. dessen Ergebnis gegen das ursprüngliche Manifest validieren;
7. bestehende `OrientationResponse` erzeugen.

Der Executor fügt keine Pfade hinzu, verändert keine Reihenfolge und speichert
keinen Kontext.

## Tests

```bash
make test
```

Die Phase-2C-Tests decken ab:

- Erhaltung und explizite Nummerierung der Manifest-Reihenfolge;
- Immutabilität von Brief und Einträgen;
- Abwesenheit von Dokumenttext und Prompt;
- vollständige Erhaltung von Source Reference, Revision, Hash und Provenienz;
- deterministische UTF-8-Dokumentlänge;
- erneute Manifest-Integritätsprüfung;
- Gleichheit wiederholter Brief-Erzeugung;
- vollständige Ausführung über einen brief-fähigen Test-Backend-Port und die
  bestehende Validation.

## Backend-Unabhängigkeit

Der Brief ist frei von Ollama-, Modell-, API- und Promptformaten. Jeder spätere
lokale oder Cloud-Adapter kann denselben Contract konsumieren, ohne dass Selector,
Provider, Context Builder oder Brief Builder provider-spezifisch werden.

Das bedeutet noch nicht, dass bestehende Phase-1-Backends automatisch
brief-fähig sind. Eine explizite Adapter- oder Rendering-Phase ist erforderlich,
bevor ein Modell Dokumentinhalte in einem providerspezifischen Eingabeformat
erhält.

## Zukünftiges Prompt Rendering

Eine spätere, separat verantwortete Rendering-Schicht kann die Brief-Reihenfolge
und Provenienz verwenden, um Manifest-Inhalte in ein Backendformat zu übertragen.
Sie muss Prompt-Schema, Content-Zugriff, Größenlimits und Providerfähigkeiten
explizit besitzen. Diese Verantwortung gehört weder in `ContextBriefBuilder` noch
in den Brief-Contract.

Phase 2C erzeugt daher bewusst keinen Markdown-Block, System Prompt, Chat-Request
oder Modell-Tokenstrom.

## Grenzen

- keine Prompt Templates oder LLM-Formatierung
- keine Markdown-Generierung
- kein Token-Budget oder Truncation
- keine Zusammenfassung, Interpretation oder Ranking
- kein semantisches Retrieval
- keine Embeddings oder Vector Database
- keine Library- oder Builder-Hub-Integration
- kein neuer Provider und keine Runtime-Änderung
- keine persistierte Brief-Historie

Phase 2C schafft ausschließlich die deterministische, auditierbare Grenze zwischen
geladenem Manifest und zukünftiger Backend-Präsentation.
