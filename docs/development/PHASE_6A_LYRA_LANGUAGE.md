# Phase 6A: LYRA Language

> Diese Architekturbaseline bleibt historisch maßgeblich. Die erste
> deterministische Integration ist in
> [`PHASE_6B_LYRA_INTEGRATION.md`](PHASE_6B_LYRA_INTEGRATION.md) dokumentiert.

## Scope

Phase 6A etabliert LYRA als kanonische menschliche Sprachschicht der bestehenden
ORION-Architektur. Der Scope besteht ausschließlich aus Architektur- und
Entwicklungsdokumentation. Die Repository-Version bleibt `0.3.0-dev.0`.

## Architecture

```text
Human
  ↓ natural-language intention
LYRA translation boundary
  ↓ existing ORION inputs
ORION
  ↓ existing structured results
LYRA explanation boundary
  ↓ faithful human language
Human
```

LYRA übersetzt an beiden Seiten derselben Grenze. Sie liegt nicht im Kernel und
nicht im Ausführungspfad als neue Runtime-Komponente. ORION bleibt für Planning,
Routing, Context, Reasoning-Grenze und Validation verantwortlich.

Die normative Architektur steht in
[`LYRA_ARCHITECTURE.md`](../architecture/lyra/LYRA_ARCHITECTURE.md).

## Input Model

Phase 6A führt keinen neuen Input Contract ein. Die sprachliche Eingabe wird
konzeptionell in vier Gruppen zerlegt:

| Gruppe | Inhalt | Bestehendes ORION-Ziel |
|---|---|---|
| Intent | kanonische LYRA-Vokabel | Objective oder Erklärungsvorgang |
| Subject | benannte Quelle oder vorhandenes Objekt | `OrientationRequest.scope`, `OrientationObject`, Source Reference |
| Target | vorhandene Zielrepräsentation, falls verlangt | `RepresentationTarget` |
| Question mode | Explain, Why, Alternatives, Missing | vorhandene Report-Felder |

Eine allgemeine Reasoning-Anfrage kann als bestehender `OrientationRequest`
beschrieben werden. Eine Navigationsanfrage benötigt die vorhandenen
`OrientationObject`- und `RepresentationTarget`-Eingaben der Transformation
Engine. Diese unterschiedlichen Runtime-Eingänge werden nicht zu einem neuen
Universalvertrag zusammengelegt.

Fehlt eine notwendige Quelle oder ist ein Repräsentationsname nicht registriert,
muss LYRA um Klärung bitten beziehungsweise die Unbekanntheit benennen. Sie darf
den fehlenden Wert nicht erzeugen.

## Output Model

Phase 6A führt auch keinen neuen Output Contract ein. Eine menschliche Erklärung
ist eine treue sprachliche Sicht auf einen vorhandenen `OrientationResponse`
oder `TransformationReport`.

Die Sicht kann enthalten:

- Request- oder Orientation-Object-Identität;
- Quell- und Zielrepräsentation;
- Planstatus und Transition-IDs;
- Alternativpfade;
- Checks, Validierungsstatus und Blocker;
- Evidence Levels, Operatorstatus und Provenienz;
- die ausdrückliche Aussage, dass keine Zielrepräsentation erzeugt wurde.

Sie darf keine Felder hinzufügen, die wie ORION-Ergebnisse wirken. Ein späterer
maschinenlesbarer LYRA-Output benötigt einen separaten Contract und ist nicht
Teil dieser Phase.

## Canonical Vocabulary

Phase 6A reserviert diese menschenbezogenen Ausdrücke:

```text
Observe
Represent
Project
Navigate
Compare
Explain
Inspect
Plan
Validate
Why
Show Alternatives
What is missing?
```

Die verbindliche Abbildung auf bestehende ORION-Konzepte steht in der
Vokabulartabelle der LYRA-Architektur. Die Wörter sind keine Python-Methoden,
Request-Typen, CLI-Befehle oder impliziten Berechtigungen.

## Examples

### Navigation erklären

Human:

> I want to understand how this observation reaches the calendar.

Konzeptionelle LYRA-Abbildung:

```text
Intent: Navigate + Explain
Source: Observation
Target: Calendar Projection
```

Nach ORION-Planung fasst LYRA ausschließlich den tatsächlichen Report zusammen:

> Eine registrierte deterministische Route ist vorhanden. Der Plan ist aktuell
> durch nicht ausführbare Operatoren und fehlende Renderer blockiert. Es wurde
> keine Calendar Projection erzeugt.

### Blocker untersuchen

Human:

> What is missing?

LYRA liest die vorhandenen `TransformationIssue`-Einträge und gruppiert sie
verständlich nach `MissingContract`, `MissingOperator`, `MissingRenderer` oder
anderen tatsächlich enthaltenen Kinds. Es ergänzt keine vermutete Ursache.

### Begründung anzeigen

Human:

> Why?

LYRA nennt die vorhandenen Checks, Issue-Reasons, Contract-Referenzen und Evidence
Levels. Wenn der Report keinen Grund enthält, lautet die Antwort sinngemäß: „Im
vorliegenden Report ist kein weiterer Grund dokumentiert.“

### Alternativen anzeigen

Human:

> Show alternatives.

LYRA gibt ausschließlich `TransformationPlan.alternative_paths` wieder. Eine
leere Liste wird als „keine registrierten Alternativpfade im Plan“ erklärt und
nicht durch eigene Routenvorschläge ergänzt.

## Deterministic translation expectations

Wo strukturierte Werte existieren, ist die Übersetzung deterministisch in ihrer
Bedeutung:

- IDs und Versionen bleiben exakt;
- Transition-Reihenfolge bleibt exakt;
- Statuswerte werden nicht aufgewertet;
- Evidence Levels werden wörtlich erhalten;
- Provenienzreferenzen bleiben zuordenbar;
- `None` oder unbekannt wird nicht durch plausible Prosa ersetzt;
- `blocked` darf nicht als erfolgreiche Transformation beschrieben werden.

Die sprachliche Form darf variieren. Semantische Abweichung vom Report ist nicht
zulässig.

## Runtime boundary

In Phase 6A werden keine Dateien unter `src/orion/` hinzugefügt oder verändert.
Es gibt keinen Parser, Translator, Formatter, Service oder Backend-Port. Auch die
frozen Contracts und die Transformation Engine bleiben unverändert.

## Out of Scope

- AI- oder LLM-Integration;
- Prompt Templates und Prompt Engineering;
- Parser, CLI, API, Chat- oder Web-Interface;
- Builder Hub;
- Operator- oder Renderer-Ausführung;
- Mathematik und Geometrie;
- Provider-Integration und Persistence;
- Kernel-Änderungen;
- wissenschaftliche Validierung;
- Implementierung oder Spezifikation von LUCY.

## Future work

Eine spätere Phase muss vor Implementierung mindestens entscheiden:

1. ob ein eigener versionierter Translation Contract erforderlich ist;
2. wie Mehrdeutigkeit ohne Inferenz sichtbar gemacht wird;
3. wie jede Erklärung auf konkrete Report-Felder zurückverweist;
4. welche Vokabular- und Round-trip-Conformance-Tests gelten;
5. ob die LYRA Boundary physisch innerhalb ORION verbleibt.

Diese Fragen autorisieren noch keine Implementierung.
