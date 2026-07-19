# ORION Representation & Rendering Architecture

- Status: Phase-3A-Architekturspezifikation
- Scope: Repräsentation, Projektion und Rendering
- Implementierungsstatus: nicht implementiert
- Repository-Version: `0.3.0-dev.0`

## 1. Zweck

Dieses Dokument formalisiert Rendering als eigenständige architektonische
Fähigkeit von ORION. Ein identitätsbewahrendes Orientation Object kann in
verschiedene Repräsentationsräume projiziert werden, ohne dass eine Projektion
das Quellobjekt verändert oder ersetzt.

Der Leitsatz lautet:

> One Orientation Object. Many Renderers. Many Representations. One preserved
> source identity.

Phase 3A definiert ausschließlich Architektur. Sie führt keine Renderer-Klassen,
Schemas, Prompt Templates, UI-Komponenten oder Generatoren ein.

## 2. Architekturkontinuität

Diese Spezifikation präzisiert bereits akzeptierte NEXAH-Entscheidungen:

- **P4 — One Kernel, Many Representations**: Eine kanonische Grundlage kann
  mehrere Darstellungen tragen; keine Darstellung wird allein zur Wahrheit.
- **P7 — Preserve Difference and Provenance**: Projektionen bewahren Herkunft
  und machen Unterschiede sichtbar.
- **P9 — Multiple Representations, Explicit Translation**: Übersetzung zwischen
  Repräsentationsräumen ist explizit und versioniert.
- **Lyra Boundary**: Lyra bezeichnet die fachliche Grenze für Sprache,
  Projektion und Translation, nicht eine zweite Wahrheitsschicht.
- **ADR-0007**: Poster, Map, Blueprint, Specification und Atlas sind gekoppelte
  Dokumentationsprojektionen derselben Architekturversion.

Phase 3A reproduziert keine Poster und erklärt keine Metapher zur
Implementierung. Sie extrahiert die stabile Repräsentationsarchitektur.

## 3. Begriffe

### 3.1 Orientation Object

Ein **Orientation Object** ist das identitäts- und versionsgebundene Quellobjekt,
das dargestellt werden soll. Es besitzt eine verantwortliche Autorität und eine
stabile Referenz, anhand derer jede Projektion auf dieselbe Quelle zurückgeführt
werden kann.

Ein Orientation Object kann künftig beispielsweise sein:

- ein kanonisches Kernel-Objekt;
- ein Orientation Graph, Poset oder Lattice;
- eine Neighborhood oder ein Reader Path;
- ein Atlas Object;
- eine freigegebene Architekturversion;
- ein `ContextManifest` oder eine andere ORION-eigene strukturierte Sicht.

Diese Liste definiert keine neuen Laufzeitverträge. Welche Objekttypen tatsächlich
renderbar sind, wird je Typ separat freigegeben.

Die Identität des Orientation Object gehört niemals einem Renderer. Ein Renderer
erhält nur eine read-only Sicht oder Referenz auf eine bestimmte Version.

### 3.2 Representation

Eine **Representation** ist eine immutable Projektion eines Orientation Object in
einen benannten Repräsentationsraum.

Jede Representation muss konzeptionell festhalten:

- die Identität und Version des Orientation Object;
- die Ziel-Domäne und das Zielprofil;
- Renderer-Identität und Renderer-Version;
- deterministische Render-Konfiguration;
- Provenienz der verwendeten Quellen;
- bekannte Auslassungen, Verdichtungen oder Verlustigkeit;
- die eigene Artefaktidentität und Integrität.

Eine Representation ist ein abgeleitetes Artefakt. Sie kann eine eigene ID haben,
erbt daraus aber keine Autorität über das Quellobjekt.

### 3.3 Projection

Eine **Projection** ist die explizite, versionierte Abbildungsvorschrift zwischen
einem Orientation Object und einem Repräsentationsraum. Sie definiert, welche
Strukturen erhalten, reorganisiert, übersetzt oder ausgelassen werden.

Eine Projection:

- besitzt eine deklarierte Quelldomäne und Zieldomäne;
- benennt Erhaltungsregeln und bekannte Informationsverluste;
- erzeugt keine neue fachliche Behauptung;
- verspricht keine Umkehrbarkeit, sofern diese nicht separat bewiesen ist;
- ändert weder Quellidentität noch Quellversion.

„Projection“ ist damit die semantische Abbildungsvorschrift. „Rendering“ ist ihre
deterministische Ausführung.

### 3.4 Renderer

Ein **Renderer** ist eine read-only, provider-unabhängig beschriebene Komponente,
die eine freigegebene Projection deterministisch ausführt.

Ein Renderer darf ausschließlich:

- reorganisieren;
- projizieren;
- anhand expliziter Regeln übersetzen;
- visualisieren beziehungsweise eine Visualisierungsbeschreibung erzeugen.

Ein Renderer darf niemals:

- neue Bedeutung oder neue fachliche Tatsachen erfinden;
- das Orientation Object oder seine Quellen verändern;
- reasonen oder inferieren;
- Dokumente auswählen oder Retrieval ausführen;
- validieren oder kanonische Entscheidungen treffen;
- versteckte Defaults, Modellwissen oder externe Zustände einbringen.

Gleiche Quellidentität, Quellversion, Projection, Renderer-Version und
Konfiguration müssen dieselbe Representation erzeugen.

### 3.5 Rendering

**Rendering** ist der kontrollierte Vorgang, in dem ein Renderer eine Projection
auf ein Orientation Object anwendet und eine immutable Representation erzeugt.

Rendering ist weder Reasoning noch Validation. Conformance- und
Integritätsprüfungen liegen außerhalb des Renderers. Ein fehlgeschlagener Renderer
liefert kein teilweise autorisiertes Ersatzobjekt.

## 4. Identität und Autorität

```text
Orientation Object (identity O, version V)
  ├─ Renderer A / Projection A -> Representation RA -> source O@V
  ├─ Renderer B / Projection B -> Representation RB -> source O@V
  └─ Renderer C / Projection C -> Representation RC -> source O@V
```

`RA`, `RB` und `RC` sind nicht dasselbe Artefakt. Sie stellen jedoch dasselbe
Orientation Object in unterschiedlichen Domänen dar und referenzieren dieselbe
Quellidentität `O@V`.

Folgende Invarianten gelten:

1. Rendering erzeugt keine neue Quellidentität.
2. Keine Representation überschreibt oder mutiert das Orientation Object.
3. Keine Representation wird allein kanonisch, nur weil sie anschaulicher oder
   detaillierter ist.
4. Widerspricht eine Representation ihrer Quelle, ist sie fehlerhaft; sie ändert
   nicht rückwirkend die Quelle.
5. Änderungen am Orientation Object erzeugen eine neue Quellversion und erfordern
   neue Renderings.
6. Änderungen an Projection, Renderer oder Konfiguration erzeugen eine neue
   Representation-Version, auch wenn das Quellobjekt unverändert bleibt.

## 5. Rendering ist nicht Reasoning

Rendering und Reasoning liegen auf verschiedenen Autoritätspfaden:

| Rendering | Reasoning |
|---|---|
| wendet deklarierte Abbildungsregeln an | erzeugt einen untrusted Vorschlag |
| muss bei gleichen Eingaben deterministisch sein | kann modell- oder laufzeitabhängig variieren |
| darf keine neue Bedeutung ergänzen | darf Hypothesen und Schlussfolgerungen vorschlagen |
| verändert die Quelle nicht | verändert die Quelle ebenfalls nicht |
| Ergebnis ist eine Representation | Ergebnis ist ein `ReasoningResult` |
| Conformance wird extern geprüft | Validation bleibt eine separate ORION-Grenze |

Ein Reasoning-Ergebnis kann später selbst zum versionierten Orientation Object
einer Darstellung werden. Das macht den Renderer nicht zum Reasoner und die
Representation nicht zur bestätigten Wahrheit.

## 6. Rendering-Familien

Die folgenden Familien beschreiben zukünftige Repräsentationsräume. Phase 3A
implementiert keine davon.

| Renderer-Familie | Zielraum | Mögliche Projektionen | Ausdrückliche Grenze |
|---|---|---|---|
| Reasoning Renderer | provider-neutrale oder adaptergebundene Reasoning-Eingabe | `ContextBrief`, strukturierte Provider Request | kein Reasoning, kein Promptentwurf in Phase 3A |
| Documentation Renderer | publizierte Dokumentationssicht | Poster, Map, Blueprint, Specification, Atlas | keine Architekturänderung durch Darstellung |
| Diagram Renderer | graphische Strukturbeschreibung | Graph, Flow, Sequence, Dependency Map | keine UI- oder Bildgenerierung |
| Machine/API Renderer | strukturierte maschinenlesbare Sicht | API View, serialized record, exchange projection | kein Transport, keine Mutation und kein öffentlicher Contract ohne Freigabe |
| Book Renderer | sequenzielle Langform | Kapitelstruktur, Reader Path, Buchprojektion | keine Buchgenerierung oder Redaktion |
| Astronomical Renderer | astronomischer Symbol- und Kartenraum | Stars, Constellations, Celestial Map | keine Astronomiealgorithmen oder Tatsachenbehauptungen |
| Geometric Renderer | geometrischer Formraum | Dodecahedron, Spiral, Golden Angle, Möbius | keine numerologische oder ontologische Wahrheit |
| Temporal Renderer | zeitlicher Ordnungsraum | Clock, Calendar, Sequence, Phase | keine Planung, Prognose oder Kalenderintegration |
| Musical Renderer | musikalischer Strukturraum | Intervals, Rhythm, Harmony, Composition | keine Synthese, Aufführung oder ästhetische Inferenz |
| Mathematical Renderer | formaler Strukturraum | Sets, Relations, Posets, Lattices, Equations | kein Beweis oder neue mathematische Behauptung |

Die Namen bezeichnen Domains und Projektionstypen, keine eigenständigen Produkte,
Repositories oder Services. Eine Extraktion benötigt weiterhin eine eigene
Ownership- und Release-Entscheidung.

## 7. Dokumentationsprojektionen

Die fünf Ebenen sind offizielle, gekoppelte Dokumentationsprojektionen:

```text
Published Orientation Object / Architecture Release O@V
  ├─ Level 1: Poster
  ├─ Level 2: Map
  ├─ Level 3: Blueprint
  ├─ Level 4: Specification
  └─ Level 5: Atlas
```

Sie sind keine fünf Projekte und keine lineare Produktionspipeline. Die Pfeilfolge
`Poster → Map → Blueprint → Specification → Atlas` beschreibt zunehmende
Orientierungs- und Detailperspektiven, nicht fünf wechselnde Quellidentitäten.

| Ebene | Leitfrage | Rolle | Normativität |
|---|---|---|---|
| Poster | Warum existiert es? | eine Idee und Richtung sichtbar machen | nicht normativ |
| Map | Wo liegen Elemente und Beziehungen? | Navigation und Überblick | orientierend |
| Blueprint | Wie ist es strukturiert? | Rollen, Schichten und Flows | nach Freigabe architektonisch normativ |
| Specification | Welche Regeln und Verträge gelten? | präzise Implementierungsgrenze | normativ für den benannten Scope |
| Atlas | Wie entstand und entwickelt es sich? | Herkunft, Varianten und Journeys kuratieren | referenziell, nicht ersetzend |

Alle fünf Projektionen müssen dieselbe Architekturrelease-ID referenzieren. Ein
Atlas ersetzt keine Specification; ein Poster kann keinen ADR superseden.

## 8. Lyra und Repository-Eigentum

Die Representation Architecture liegt fachlich an der bestehenden Lyra Boundary.
Lyra ist zunächst keine eigene Runtime und kein eigenes Repository. Gemäß der
stabilen Architektur verbleiben freigegebene Projektionen und Renderer zunächst
innerhalb des ORION-Eigentums, bis mehrere Konsumenten oder ein unabhängiger
Releasezyklus eine Extraktion rechtfertigen.

Wichtige Abgrenzung:

- Die vorhandenen `nexah/backends/` im frozen NEXAH Core sind deterministische
  **Core Representation Backends**.
- ORION-`ReasoningBackend` bezeichnet den austauschbaren Reasoning-Port.
- Zukünftige ORION-Renderer gehören zur Lyra-/Representation-Boundary.

Diese drei Begriffe dürfen weder zusammengelegt noch durch Umbenennung
umgedeutet werden. Phase 3A verschiebt und vendort keinen Core-Code.

## 9. Verhältnis zur bestehenden Context Pipeline

Die deterministische Context Pipeline bleibt unverändert:

```text
OrientationRequest
  -> DocumentSelector          what is selected
  -> RepositoryContextProvider
  -> ContextBuilder
  -> ContextManifest           what exactly exists
  -> ContextBriefBuilder
  -> ContextBrief              how context is described
```

`ContextBrief` zeigt bereits Eigenschaften einer Representation: immutable,
deterministisch, geordnet, provenienzgebunden und vom Quellmanifest getrennt.
Phase 3A erklärt den bestehenden Contract jedoch nicht rückwirkend zu einem
allgemeinen Representation-Schema.

Eine spätere Reasoning-Rendering-Pipeline kann konzeptionell lauten:

```text
Orientation Object / ContextBrief
  -> declared Reasoning Projection
  -> Reasoning Renderer
  -> provider-neutral reasoning representation
  -> provider adapter
  -> provider request
```

Prompt Rendering, Provider Messages und Modellformatierung bleiben separat und
sind nicht Teil von Phase 3A.

## 10. Provider-Unabhängigkeit

Die Rendering Architecture ist provider-unabhängig, weil Quellidentität,
Projection, Representation und Renderer-Conformance keine LLM- oder
Runtime-Objekte voraussetzen.

Ein domänenspezifischer Zielraum kann ein deklariertes Providerprofil besitzen.
Providerdetails dürfen dann erst in einem terminalen Adapter oder explizit
providergebundenen Renderer erscheinen. Sie dürfen niemals in das Orientation
Object, eine allgemeine Projection oder andere Renderer-Familien zurückfließen.

Ein Providerwechsel verändert deshalb höchstens die terminale Representation und
deren Renderer-Version, nicht die Identität des Orientation Object.

## 11. Verlustigkeit und Äquivalenz

Nicht jede Projection kann alle Eigenschaften ihrer Quelle zeigen. Verlustigkeit
ist zulässig, sofern sie explizit und reproduzierbar ist.

Für jede spätere Projection sind mindestens zu klären:

- welche Identitäten und Relationen erhalten bleiben;
- welche Informationen ausgelassen oder verdichtet werden;
- ob Ordnung, Richtung und Kardinalität erhalten bleiben;
- ob Round-trip oder nur Trace-back zur Quelle möglich ist;
- welche Equivalence- oder Conformance-Prüfung außerhalb des Renderers gilt.

„Gleiche Quelle“ bedeutet nicht „identische Representations“. „Gleiche Bedeutung“
darf nur innerhalb eines definierten Äquivalenzprofils behauptet werden.

## 12. Zukünftige Rendering-Pipeline

Eine spätere Implementierung kann folgende logische Schritte besitzen:

```text
Orientation Object Reference
  -> resolve immutable source version
  -> choose an explicit Projection
  -> invoke a versioned Renderer
  -> produce immutable Representation
  -> run external integrity/conformance checks
  -> deliver to a consumer or terminal adapter
```

Die konkrete API, Paketstruktur, Serialisierung und Persistenz werden erst in
einer Implementierungsphase entschieden. Phase 3A autorisiert keine Klassen oder
Schemas aus diesem Ablauf.

## 13. Rendering-Prinzipien

### R1 — One Object, Many Representations

Mehrere Darstellungen referenzieren dieselbe Quellidentität, ohne sie zu ersetzen.

### R2 — Identity Before Appearance

Quellidentität und Version werden vor Stil, Layout oder Zielmedium gebunden.

### R3 — Deterministic Projection

Gleiche freigegebene Eingaben erzeugen dieselbe Representation.

### R4 — Read Only

Rendering besitzt keine Mutation der Quelle und keine kanonischen Effekte.

### R5 — No Hidden Meaning

Ein Renderer erfindet, folgert oder ergänzt keine Bedeutung.

### R6 — Explicit Domain and Profile

Jede Representation benennt Zieldomäne, Projection und Renderer-Version.

### R7 — Provenance Always Survives

Jede Representation bleibt auf Orientation Object, Version und Quellen
zurückführbar.

### R8 — Lossiness Must Be Declared

Auslassungen und Verdichtungen sind Teil des Projection-Profils, keine versteckten
Renderer-Entscheidungen.

### R9 — Validation Remains External

Renderer validieren weder fachliche Wahrheit noch Backend-Ergebnisse.

### R10 — Representation Is Not Authority

Anschaulichkeit, Schönheit oder technische Präzision übertragen keine neue
Entscheidungsautorität.

## 14. Architektur-Risiken

| Risiko | Folge | Architekturkontrolle |
|---|---|---|
| Renderer beginnt zu reasonen | abgeleitete Bedeutung erscheint deterministisch | strikte No-Inference-Grenze und Conformance-Tests |
| Representation wird mit Quelle verwechselt | Darstellung überschreibt Autorität | Quell-ID und Quellversion verpflichtend referenzieren |
| visuelle Metapher wird Spezifikation | Poster bestimmt technische Wahrheit | ADR-0007 und Normativität je Projektion |
| Providerformat dringt in Orientation Objects | Modellwechsel verändert Domänenverträge | terminale Adaptergrenze |
| Verlustigkeit bleibt unsichtbar | falsche Äquivalenz zwischen Domains | explizites Lossiness-Profil |
| Renderer validiert eigene Ausgabe | fehlende unabhängige Kontrolle | externe Integritäts- und Conformance-Grenze |
| Renderer-Familien werden vorschnell Services | unnötige Repositories und Ownership-Brüche | Extraktion nur durch separate ADR |
| Core Representation Backends werden umgedeutet | Autoritätsgrenzen kollabieren | unveränderte Core-Ownership und eindeutige Terminologie |

## 15. Out of Scope

Phase 3A enthält ausdrücklich nicht:

- Prompt Engineering oder Prompt Templates;
- semantisches Retrieval, Embeddings oder Vector Databases;
- UI-, API- oder Renderer-Implementierung;
- Bild-, Diagramm-, Poster- oder Buchgenerierung;
- musikalische Synthese;
- Astronomie- oder Geometriealgorithmen;
- mathematische Beweissysteme;
- Token-Budgetierung oder Modellformatierung;
- neue Runtime-, Provider-, Kernel-, Library- oder Builder-Hub-Integration;
- ein allgemeines `Representation`-Schema oder Renderer-SDK.

## 16. Bedingungen für die Implementierungsphase

Vor dem ersten Renderer müssen mindestens entschieden werden:

1. welcher konkrete Orientation-Object-Typ als erste Quelle dient;
2. welches Projection-Profil freigegeben ist;
3. welche Identität, Version und Provenienz eine Representation serialisiert;
4. welche Verlustigkeit erlaubt ist;
5. welche externe Conformance-Prüfung gilt;
6. wo die Lyra Boundary im aktuellen Repository physisch abgebildet wird;
7. ob ein neuer öffentlicher Contract eine ADR und Schema-Version benötigt.

Erst danach beginnt Implementierung. Phase 3A beendet die Architekturdefinition,
nicht die Renderer-Entwicklung.

## 17. Acceptance Criteria

Die Representation Architecture ist erfüllt, wenn:

- Orientation Object, Representation, Projection, Renderer und Rendering klar
  getrennt sind;
- eine Quelle mehrere immutable Domain-Projektionen tragen kann;
- jede Projektion Identität, Version und Provenienz bewahrt;
- Renderer deterministisch, read-only und frei von Reasoning bleiben;
- die fünf Dokumentationsebenen als gekoppelte Projektionen derselben
  Architekturversion behandelt werden;
- Providerdetails die allgemeine Rendering Architecture nicht verändern;
- Core Representation Backends, ORION Reasoning Backends und Lyra Renderer
  getrennte Verantwortlichkeiten behalten;
- keinerlei Renderer-Implementierung aus Phase 3A abgeleitet oder vorweggenommen
  wird.
