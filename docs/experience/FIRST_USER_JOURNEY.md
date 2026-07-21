# NEXAH Alpha — The First Human Experience

- Status: Experience Specification
- Scope: erste vollständige Begegnung eines Menschen mit NEXAH
- Architecture baseline: frozen ORION v1
- LUCY status: Concept Freeze; kein Interface-Akteur
- Repository version: `0.3.0-dev.0`
- Authority: beschreibt die Experience, verändert keine Architektur

## 1. Experience Promise

NEXAH hilft einem Menschen, in einer komplexen Frage Orientierung zu gewinnen,
bevor es mehr Information anbietet.

Die erste Begegnung soll innerhalb von fünf Minuten verständlich machen:

1. NEXAH ist ein Orientierungsraum, kein Chatbot und keine Antwortmaschine.
2. Der Mensch bringt Frage, Situation oder Beobachtung ein und behält die
   Entscheidungshoheit.
3. NEXAH macht Perspektiven, Wege, Evidenz und Grenzen sichtbar.
4. Eine Antwort ist nicht das Ende. Nach ihr folgt ein freiwilliger Moment der
   Reflection.

Die Experience verspricht keine Gewissheit. Sie verspricht eine nachvollziehbare
Orientierung.

## 2. Why Someone Comes Here

Menschen kommen zu NEXAH, wenn sie:

- viele Informationen, aber noch keine klare Richtung haben;
- eine komplexe Sache verstehen wollen, ohne sie vorschnell zu vereinfachen;
- Beziehungen zwischen Perspektiven, Quellen oder Darstellungen sehen möchten;
- wissen wollen, was belegt, unsicher, verborgen oder noch nicht möglich ist;
- nicht nur eine Antwort, sondern einen nachvollziehbaren Weg suchen.

NEXAH ist nicht der richtige Ort für eine schnelle Faktenabfrage, beiläufige
Unterhaltung oder die Delegation einer persönlichen Entscheidung. Das wird nicht
als Warnung eröffnet, sondern durch Form, Tempo und Sprache erfahrbar.

## 3. The Five-Minute Arc

| Zeit | Moment | Der Mensch versteht |
|---|---|---|
| 0:00–0:30 | Ankommen | Hier geht es um Orientierung, nicht um möglichst schnelle Antworten. |
| 0:30–1:30 | Frage öffnen | Ich kann mit einer echten Frage, Situation oder Beobachtung beginnen. |
| 1:30–2:00 | Intention bestätigen | Das System rät nicht; ich bestätige, was untersucht werden soll. |
| 2:00–3:30 | Orientierung sehen | Ich sehe Ergebnis, Weg, Grenzen und Evidenz als unterscheidbare Dinge. |
| 3:30–4:30 | Vertiefen | ORION und Library werden bei Bedarf als Route und Quellenraum sichtbar. |
| 4:30–5:00 | Reflektieren oder gehen | Die Bedeutung und der nächste Schritt bleiben bei mir. |

## 4. Experience Choreography

```text
Blank browser
    ↓
Landing — invitation, not input pressure
    ↓
Open the question — human language
    ↓
Confirm the orientation — LYRA makes intent explicit
    ↓
Explore — ORION prepares a traceable orientation
    ↓
Orient — result, route, evidence and limits
    ↓
Reflect — optional human pause
    ↓
Continue, preserve a summary, or leave
```

Jeder Pfeil benötigt eine bewusste Handlung des Menschen. Es gibt kein
automatisches Weiterlaufen in eine neue Frage, keine ungefragte Empfehlung und
keine simulierte Gesprächsinitiative.

## 5. Complete Walkthrough

### Screen 0 — Blank Browser to Arrival

**Purpose**

Der Übergang vom leeren Browserfenster soll Tempo herausnehmen, ohne eine
Inszenierung zu erzwingen.

**First transition**

Eine ruhige Fläche erscheint sofort. Zuerst werden Wortmarke und ein einzelner
Satz sichtbar; Navigation und Handlungsmöglichkeiten folgen mit einer kurzen,
unaufdringlichen Überblendung. Keine Splash-Sequenz, kein Video, kein künstliches
Warten.

**Microcopy**

> NEXAH
>
> Find your bearing before you search for answers.

**What remains mysterious**

Die volle Architektur, die Namen ORION, LYRA und LUCY sowie die visuellen
Repräsentationsräume werden noch nicht erklärt. Der erste Moment vermittelt
Haltung, nicht Systemkunde.

### Screen 1 — Landing Page

**Immediate understanding**

> Bring a question, a situation, or something you are trying to understand.
>
> NEXAH helps you see the field, trace a path, and understand the limits.

**Primary actions**

- `Begin with a question`
- `Explore an example`

**Quiet secondary action**

- `What is NEXAH?`

**Navigation**

Die erste Ansicht besitzt nur die Wortmarke sowie die zurückhaltenden Einträge
`About`, `Library` und `Principles`. Es gibt kein Dashboard, keinen Login-Zwang,
keine Seitenleiste, keine Chatblase und keinen blinkenden Cursor in einem großen
Promptfeld.

**Interaction**

`Begin with a question` führt in einen fokussierten Frageraum. `Explore an
example` öffnet dieselbe Reise mit einem klar als Beispiel markierten Inhalt.
`What is NEXAH?` zeigt drei kurze Aussagen:

> NEXAH reveals relationships.
>
> ORION traces possible routes.
>
> You decide what the orientation means.

ORION wird hier erstmals benannt, aber nicht erklärt. LYRA und LUCY bleiben im
Hintergrund.

### Screen 2 — Open the Question

**Purpose**

Der Mensch soll eine Frage öffnen können, ohne eine Syntax lernen oder mit einer
Persona sprechen zu müssen.

**Prompt**

> What are you trying to find your way through?

**Supporting copy**

> Start with a question, an observation, or a situation. It does not need to be
> perfectly phrased.

**Input form**

Eine ruhige, mehrzeilige Schreibfläche. Darunter drei freiwillige Startpunkte:

- `I want to understand…`
- `I want to compare…`
- `I want to trace how…`

Sie bilden bestehende LYRA-Vokabeln ab, ohne diese Terminologie vom Erstbesucher
zu verlangen.

**Primary action**

- `Continue`

**Secondary actions**

- `Use an example`
- `Back`

**Empty state**

`Continue` bleibt ruhig deaktiviert. Nach einer bewussten Aktivierung ohne Text
erscheint lediglich:

> Begin with what you have. A few words are enough.

**Unsupported or overly broad input**

NEXAH ergänzt keine vermutete Bedeutung. Die Seite antwortet nicht mit einer
scheinbar intelligenten Vermutung, sondern öffnet Screen 3 zur Klärung.

### Screen 3 — Confirm the Orientation

**Purpose**

LYRA übersetzt im Hintergrund die menschliche Formulierung in vorhandene
ORION-Begriffe. Sie wird nicht als Bot, Figur oder Gesprächspartner dargestellt.
Die Experience zeigt nur die nachvollziehbare Übersetzung.

**Heading**

> Let us make sure the direction is yours.

**Confirmation card**

> You want to understand:
> **[plain-language objective]**
>
> Starting from:
> **[known source or “not yet specified”]**
>
> Looking toward:
> **[known target or “not yet specified”]**

**Actions**

- `Yes, orient this`
- `Adjust`
- `Start again`

**Clarification state**

Wenn Source, Target oder Intention fehlen oder mehrdeutig sind, wird genau eine
begrenzte Klärung zurzeit gezeigt:

> Which starting point do you mean?

Nur vorhandene, verständlich benannte Möglichkeiten dürfen angeboten werden.
`I’m not sure yet` ist immer eine gültige Antwort und führt zu den bekannten
Startpunkten oder zurück zur Frage. Es wird nichts geraten und kein neuer
Request-Typ eingeführt.

**Unknown representation or unsupported intent**

> NEXAH cannot map that term to a known orientation yet.
>
> You can revise the wording or inspect the available starting points.

Actions: `Revise`, `See known starting points`, `End here`.

Der Human bestätigt den Übergang zu ORION ausdrücklich mit `Yes, orient this`.

### Screen 4 — Exploration in Progress

**Purpose**

Das Warten zeigt nachvollziehbare Arbeit, ohne Denken, Bewusstsein oder
Gewissheit zu simulieren.

**Heading**

> Building an orientation…

**Visible stages**

1. `Reading the request`
2. `Finding registered paths`
3. `Checking evidence and limits`
4. `Preparing the orientation`

Nur tatsächlich bekannte Zustände werden angezeigt. Keine erfundenen
Fortschrittsprozente, kein „I am thinking“, keine wechselnden Unterhaltungssätze.

**Actions**

- `Stop`
- `What is happening?`

`What is happening?` öffnet eine kurze Erklärung von ORION:

> ORION is checking known representations, registered routes, evidence, and
> blockers. It does not invent a missing route.

Hier wird ORION sichtbar, weil sein Verfahren für Vertrauen relevant ist.

**Long-running state**

> This is taking longer than expected. You can keep waiting or return to your
> confirmed question.

Actions: `Keep waiting`, `Return to question`, `Stop`.

### Screen 5 — The Orientation

**Purpose**

Das Ergebnis ist keine Chatnachricht. Es ist eine ruhige, prüfbare
Orientierungsfläche.

**Top line**

> Your orientation

Direkt darunter steht eine kurze LYRA-Erklärung in Alltagssprache. Sie darf den
Status des ORION Reports vereinfachen, aber niemals verändern.

**Canonical layout**

1. **What we can say** — die verständliche Kernaussage oder der dokumentierte
   Planstatus.
2. **The path** — Source, Target, registrierte Schritte und Alternativen als
   einfache Map.
3. **What supports this** — Evidence Summary und Quellenanzahl.
4. **What remains uncertain** — Blocker, unbekannte Felder, Lossiness und
   Grenzen.
5. **What was not produced** — explizite Nicht-Ergebnisse, falls vorhanden.

**Primary actions**

- `Explore the path`
- `See evidence`
- `Pause and reflect`

**Secondary actions**

- `Show alternatives` — nur wenn der Report Alternativen enthält
- `Inspect the report`
- `Ask a next question`
- `End here`

**Success state**

> A valid orientation report was produced from the registered path.

Die Experience unterscheidet weiterhin Ergebnis, Evidenz, Interpretation und
menschliche Bedeutung.

**Blocked state**

> There is a registered route, but it cannot currently be completed.
>
> No target representation was produced.

Darunter werden nur vorhandene Blocker gezeigt, beispielsweise `Missing
Operator`, `Missing Contract` oder `Missing Renderer`. Der Zustand besitzt
dieselbe visuelle Würde wie ein Erfolg: kein rotes Scheitern, keine Beschönigung.

**No registered route**

> No registered route connects these representations yet.
>
> NEXAH will not invent one.

Actions: `Show known alternatives`, sofern vorhanden, `Revise direction`, `End
here`.

**Validation or invariant failure**

> The orientation stopped because a required condition did not hold.
>
> The existing result has not been promoted or rewritten.

Der konkrete Check bleibt unter `Inspect the report` sichtbar.

### Screen 6 — Explore the Path

**Purpose**

Dieser Raum zeigt die Orientation als Beziehungen, nicht als lange
Antwortprosa.

**View**

Eine reduzierte Map mit aktuellem Source, Target, Transition IDs, Status und
Alternativpfaden. Auswahl eines Schritts zeigt:

- was hinein- und hinausgeht;
- welche Invarianten erhalten bleiben sollen;
- welche Information sichtbar, verborgen oder verloren wird;
- welchen Evidence Level und Capability Status der Schritt besitzt.

**Microcopy**

> One orientation. Several possible views.

**Actions**

- `Return to orientation`
- `Compare alternatives`
- `See evidence for this step`

ORION bleibt hier sichtbar als Name der Navigation. Es erscheint nicht als
Stimme und übernimmt keine Entscheidung.

### Screen 7 — The Library Trail

**When the Library appears**

Die Library erscheint erst, wenn ein Mensch `See evidence` oder einen
Quellenhinweis auswählt. Sie konkurriert nicht mit dem ersten Eindruck und wird
nicht als endloser Suchindex präsentiert.

**Heading**

> The sources behind this orientation

**Source cards**

Jede Karte zeigt nur nachvollziehbare Metadaten:

- Titel und Source Identifier;
- Dokumentpfad oder Werkreferenz;
- Version oder Revision, sofern vorhanden;
- Provenance;
- Evidence Role;
- welche Aussage oder welcher Pfadabschnitt darauf verweist.

**Microcopy**

> Sources support the orientation. They do not make the decision for you.

**Actions**

- `Inspect source`
- `Show where this was used`
- `Return to orientation`

Wenn keine Library-Quelle beteiligt war:

> This orientation does not currently reference a Library source.

Die Library bleibt eine unabhängige Wissensautorität. Die Experience lässt nicht
vermuten, ORION oder LYRA hätten ihre Inhalte erzeugt.

### Screen 8 — Reflection

**Where LUCY appears**

LUCY erscheint nicht als Produktname, Figur, Chatpartner oder ausführende
Komponente. Der LUCY Concept Freeze wird als Experience-Prinzip wirksam: Die
Seite schafft nach dem Ergebnis einen freiwilligen, stillen Reflexionsraum. Der
Human reflektiert.

**Transition**

Die Informationsdichte nimmt ab. Map und Quellen treten zurück, das Ergebnis
bleibt als kleine Referenz sichtbar. Keine neue Analyse startet.

**Heading**

> Before you continue…

**Reflection invitations**

Es wird jeweils nur eine Einladung gezeigt:

> What changed in how you see the question?

oder:

> What remains unresolved for you?

oder:

> Is the next step clearer—or simply different?

**Boundary copy**

> This reflection is yours. You do not need to answer.

**Actions**

- `Stay here`
- `Continue with a new question`
- `Return to the orientation`
- `End here`

Es gibt keinen Countdown, keinen Streak, keine Bewertung der Reflection und
keinen Zwang, Text einzugeben. Schweigen ist ein vollständiger Zustand.

Wenn der Mensch aus der Reflection eine neue Frage formuliert, wird sie nicht
automatisch zu einem ORION Request. Screen 3 verlangt erneut die bewusste
Bestätigung.

### Screen 9 — Next Step or Departure

**Purpose**

Die Reise endet mit Wahlfreiheit, nicht mit Engagement-Druck.

**Heading**

> Where would you like to leave this?

**Actions**

- `Keep a concise summary`
- `Begin a related orientation`
- `Return to the Library trail`
- `End the session`

`Keep a concise summary` bezeichnet das Experience-Ergebnis: Frage,
Orientierungsstatus, Kernaussage, Grenzen, Evidenz- und Provenienzreferenzen. Die
Spezifikation legt weder Dateiformat noch Persistenz fest.

**Closure**

Nach `End the session`:

> You can leave the question here.
>
> The orientation remains a map, not a decision.

Actions: `Return`, `Close`.

Es gibt keine „Are you sure?“-Barriere, keine Benachrichtigungsaufforderung und
keine automatische neue Unterhaltung. Verlassen ist ein respektierter Ausgang.

## 6. Visibility of the Named System

| Name | Wann sichtbar | Wann unsichtbar | Experience-Rolle |
|---|---|---|---|
| **NEXAH** | vom ersten Moment an | nie vollständig | Ort und Haltung der gesamten Experience |
| **ORION** | wenn Route, Verfahren, Evidenz oder Blocker erklärt werden | in der primären Landing-Ansicht, beim freien Formulieren und in Reflection | nachvollziehbare Navigation, niemals Persona |
| **LYRA** | nur in vertiefender Erklärung über das System | im normalen Gebrauch fast vollständig | klare Sprache, Bestätigung und faithful Explanation |
| **LUCY** | als interner Name des Reflection-Prinzips; nicht als handelnde UI-Persona | im gesamten Ausführungspfad | kennzeichnet den freiwilligen menschlichen Reflexionsraum |
| **Library** | auf bewusste Wahl nach oder innerhalb einer Orientation | vor der ersten Frage und in Reflection | Quellen-, Evidenz- und Provenienzraum |
| **Human** | durch Wahlmöglichkeiten und Bestätigung stets wirksam | nie ersetzt | besitzt Intention, Reflection und Entscheidung |

LYRA ist am besten, wenn der Mensch ihre Arbeit bemerkt, aber nicht ihre
Mechanik bedienen muss. ORION ist am besten, wenn es genau dort sichtbar wird,
wo Nachvollziehbarkeit wichtiger ist als Einfachheit.

## 7. Navigation Model

Die Alpha benötigt fünf dauerhafte Orte, aber zeigt nie alle gleichzeitig:

1. **Home** — Haltung und Beginn.
2. **Question** — Formulieren und Bestätigen.
3. **Orientation** — Ergebnis, Route und Grenzen.
4. **Library trail** — verwendete Quellen und Provenienz.
5. **Reflection** — optionaler menschlicher Zwischenraum.

Während einer Reise zeigt eine schmale Orientierungslinie nur die bereits
erreichten Orte. Sie ist Rückweg, nicht Fortschrittszwang. Browser-Zurück führt
zu einem verständlichen vorherigen Zustand und löst keine neue Verarbeitung aus.

## 8. Shared Interaction States

### Empty

Leere Zustände sind Einladungen, keine Defizite:

> No orientation has begun yet.
>
> Start with what you are trying to understand.

### Loading

Loading benennt überprüfbare Prozessschritte, niemals innere Zustände einer
vermeintlichen AI. Abbrechen bleibt möglich.

### Error

Fehler folgen vier Regeln:

1. sagen, was geschehen ist;
2. sagen, was nicht geschehen ist;
3. bestehende Eingabe nicht als verloren darstellen;
4. eine sichere nächste Handlung anbieten.

Generische Form:

> NEXAH could not complete this orientation.
>
> No result was promoted and your confirmed direction has not changed.

Actions: `Try again`, `Return to question`, `Inspect details`, `End here`.

### Required capability unavailable

> A required capability is not available right now.
>
> NEXAH has not changed your request or produced an orientation.

Die Experience benennt an dieser Stelle weder Provider noch Backend und
behauptet nicht, einen externen Lifecycle zu verwalten.

### Partial result

> Part of the orientation is available. The missing parts are named below.

Ein partielles Ergebnis wird nicht optisch als vollständig präsentiert.

### Offline or interrupted connection

> The connection was interrupted before the orientation completed.
>
> Return to your confirmed question when you are ready.

Die Spezifikation macht keine Aussage darüber, ob oder wie Eingaben gespeichert
werden.

## 9. Tone and Microcopy Rules

NEXAH spricht ruhig, konkret und ohne anthropomorphe Inszenierung.

**Use**

- `Here is the registered path.`
- `This remains uncertain.`
- `No target representation was produced.`
- `You can stop here.`
- `What does this change for you?`

**Avoid**

- `I think…`
- `I found the truth.`
- `Great question!`
- `Trust me.`
- `You should…`
- `I know how you feel.`
- künstliche Dringlichkeit, Erfolgsanimationen oder Engagement-Sprache.

Microcopy unterscheidet konsequent:

- Ergebnis von Interpretation;
- Evidence von Gewissheit;
- registrierten Pfad von ausgeführter Transformation;
- Systemgrenze von Fehler;
- Reflection von einer neuen Anfrage.

## 10. Visual and Motion Character

Die Alpha wirkt ruhig, großzügig und präzise:

- viel freie Fläche und jeweils ein dominanter Gedanke;
- wenige, semantisch stabile Farben;
- Karten und Pfade nur dort, wo Beziehungen wirklich verständlicher werden;
- Typografie vor Dekoration;
- langsame, kurze Übergänge, die räumliche Kontinuität zeigen;
- keine Partikelkulisse, kein permanenter Kosmos und keine bewegte Geometrie als
  Selbstzweck;
- Reduced Motion erhält dieselbe Informationshierarchie ohne Animation.

Das Schöne entsteht aus Klarheit, Proportion und Ruhe. Das Geheimnisvolle bleibt
in der Tiefe der möglichen Beziehungen, nicht in unklarer Bedienung.

## 11. What Should Remain Mysterious

Innerhalb der ersten fünf Minuten darf offen bleiben:

- wie weit ein Orientation Space künftig reichen kann;
- welche Repräsentationen später hinzukommen;
- welche neuen Beziehungen durch andere Perspektiven sichtbar werden;
- ob Reflection zu einer weiteren Frage führt.

Nicht mysteriös bleiben dürfen:

- wer entscheidet;
- ob etwas belegt, blockiert oder unbekannt ist;
- ob eine Transformation tatsächlich ausgeführt wurde;
- woher eine Aussage stammt;
- ob gerade NEXAH, ORION, Library oder der Human Verantwortung trägt.

Mystery belongs to possibility, never to authority.

## 12. Alpha Experience Boundaries

Diese Journey:

- verwendet ausschließlich bestehende Architekturbegriffe und
  Verantwortungsgrenzen;
- beschreibt keine Backend-, API-, Repository-, Runtime- oder Provider-Lösung;
- macht LUCY nicht zu Software, Agent, Persona oder Ausführungspfad;
- gibt LYRA keine Planungs- oder Interpretationsautorität;
- gibt ORION keine menschliche Entscheidungs- oder Reflection-Autorität;
- verschmilzt die unabhängige Library nicht mit ORION;
- verspricht keine Operator- oder Renderer-Ausführung, die heute nicht existiert.

Buttons und Screens sind Experience-Anforderungen, keine Implementierungs- oder
Schnittstellenspezifikation.

## 13. Acceptance Walkthrough

Die Experience besteht den Alpha-Test, wenn eine erstmals besuchende Person nach
höchstens fünf Minuten in eigenen Worten sagen kann:

1. „NEXAH hilft mir, eine komplexe Frage zu orientieren.“
2. „Es zeigt mir Weg, Quellen, Unsicherheit und Grenzen getrennt.“
3. „ORION navigiert; es entscheidet nicht für mich.“
4. „Ich kann prüfen, woher etwas kommt und warum etwas blockiert ist.“
5. „Nach dem Ergebnis darf ich reflektieren, weiterfragen oder einfach gehen.“

Der wichtigste Erfolgsindikator ist nicht, dass die Person alle Namen kennt. Er
ist, dass sie die Separation of Authority erlebt hat:

> NEXAH opens the space.
>
> ORION traces the route.
>
> LYRA makes it understandable.
>
> The Library shows what supports it.
>
> The Human reflects and decides.
