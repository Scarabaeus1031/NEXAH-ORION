# Orientation Transform Stack

- Status: Phase-3B-Repräsentationskartografie
- Scope: bestehende Repräsentationen und ihre Übergänge
- Implementierungsstatus: keine Implementierung
- Repository-Version: `0.3.0-dev.0`
- F1-Status: Graphidentität und Layer eingefroren; Mathematik bewusst offen

## 1. Zweck

Der Orientation Transform Stack beschreibt die vorhandenen Visualisierungen als
Koordinatensichten desselben zugrunde liegenden Orientation Object. Er behauptet
weder eine neue Geometrie noch eine wissenschaftliche Theorie. Er dokumentiert:

- welche Rolle jede Repräsentation im Gesamtfluss besitzt;
- welche Eingabe und Ausgabe sie konzeptionell hat;
- welche Koordinaten sichtbar beziehungsweise verborgen werden;
- welche Identität über alle Projektionen erhalten bleiben muss;
- wo mathematische Operatoren dokumentiert oder noch unbekannt sind.

Der Stack ist eine Navigationsarchitektur. Kandidatengleichungen sind mögliche
Formalisierungen einer Kante, keine Bestätigung ihrer historischen Verwendung.

## 2. Zentrale Annahme

Alle Zustände referenzieren dasselbe Orientation Object `O@V`:

```text
O = underlying Orientation Object identity
V = immutable source version
R_i = representation i of O@V
T_ij = declared transformation from R_i to R_j
```

Für jede Kante gilt konzeptionell:

```text
R_j = T_ij(R_i; parameters)
source(R_j) = source(R_i) = O@V
```

Eine neue Representation besitzt eine eigene Artefaktidentität, aber keine neue
Quellidentität. „Informationsgewinn“ bedeutet bessere Beobachtbarkeit oder eine
neue Koordinatensicht. Ohne zusätzliche Quelle erzeugt eine deterministische
Transformation keine neue Quellinformation.

## 3. Evidenzskala

| Code | Bedeutung |
|---|---|
| `E0` | Systemname oder Existenz genannt; Übergang nicht dokumentiert |
| `E1` | strukturelle Beziehung aus Visualsprache oder Reihenfolge plausibel |
| `E2` | gemeinsame Landmarken oder Variablen in beiden Darstellungen sichtbar |
| `E3` | Transformationsregel und Parameter dokumentiert |
| `E4` | Transformation ausführbar und mit Conformance-Test verifiziert |

Phase 3B darf `E0` oder `E1` nicht sprachlich zu `E3` aufwerten. Der derzeitige
Bestand ist überwiegend `E0–E1`, weil keine vollständigen Crosswalks,
Projektionsparameter oder ausführbaren Operatoren vorliegen.

## 4. Verbesserte Stack-Hypothese

Die vorgeschlagene lineare Folge wird in vier Funktionsklassen gegliedert:

```text
FOUNDATION
Reality
  -> Observation

SOURCE REPRESENTATIONS
Observation
  -> Planetary Chemistry
  -> Lunar / Solar Dynamics

INTEGRATION
Planetary Chemistry ----┐
                        ├-> Scarabaeus Engine
Lunar / Solar Dynamics -┘

PARALLEL ANALYSIS AND PROJECTION
Scarabaeus Engine
  ├-> Möbius Topology ---------┐
  └-> Frequency Space ---------┼-> Lissajous Geometry
                               └<- analytical reverse projection

SPATIAL AND DISCRETE CARTOGRAPHY
Lissajous Geometry
  -> Stellar Projection
       ├-> Dodecahedral Sky Map -> Calendar Projection
       └-------------------------> Calendar Projection

NORMALIZATION
Calendar Projection
  -> Orientation Layer
```

### Korrekturen gegenüber der linearen Hypothese

1. **Planetary Chemistry und Lunar/Solar Dynamics sind parallele Quellen.**
   Eine kategoriale Korrespondenz und ein periodisches Signal sind verschiedene
   Koordinatenfamilien. Sie können erst im Scarabaeus Engine zusammengeführt
   werden, wenn ihre Kopplung explizit ist.
2. **Möbius und Frequency Space sind parallele Projektionen.** Möbius beschreibt
   Topologie und Randidentifikation; Frequency Space beschreibt Moden, Perioden
   und Phasen. Keine der beiden Sichtweisen folgt zwingend aus der anderen.
3. **Frequency → Lissajous ist Synthese; Lissajous → Frequency ist Analyse.** Die
   Richtungen verwenden unterschiedliche Operatoren und sind nur unter bekannten
   Parametern teilweise invers.
4. **Stellar → Calendar besitzt einen direkten Pfad.** Eine Winkelphase kann ohne
   dodekaedrische Diskretisierung in eine Kalenderphase überführt werden.
5. **Dodecahedral Sky Map → Calendar ist eine optionale Adressprojektion.** Sie
   quantisiert räumliche Position vor der Zeitabbildung und ist deshalb stärker
   verlustbehaftet.

## 5. Layer-Katalog

### L0 — Reality

- **Purpose:** bezeichnet die nicht vom System erzeugte Quelle von Beobachtung.
- **Input:** keiner innerhalb der Architektur.
- **Output:** beobachtbare Ereignisse oder Zustände.
- **Coordinate system:** nicht festgelegt; Reality ist keine ORION-Datenstruktur.
- **Invariants:** nicht durch ORION garantierbar.
- **Visible:** nichts ohne Beobachtungsoperation.
- **Hidden:** grundsätzlich alles, was nicht beobachtet wird.
- **Loss/Gain:** nicht als Renderer-Kante quantifizierbar.
- **Mathematics:** keine festgelegt.
- **Renderer:** keiner.
- **Evidence:** `E0`; philosophischer Startpunkt.
- **Open:** Was ist der zulässige beobachtbare Scope?

### L1 — Observation

- **Purpose:** bindet eine Beobachtung an Standpunkt, Zeitpunkt und Provenienz.
- **Input:** Ereignis oder Zustand aus Reality.
- **Output:** versionierter Observation Record oder äquivalente Referenz.
- **Coordinate system:** Observer, time, measured variables, units.
- **Invariants:** Quellreferenz, Beobachter, Zeit, Messkontext.
- **Visible:** ausgewählte mess- oder beschreibbare Merkmale.
- **Hidden:** alles außerhalb des Instruments oder Beobachtungsfensters.
- **Loss/Gain:** Auswahl erzeugt unvermeidliche Unvollständigkeit; Provenienz wird
  als Orientierungsinformation sichtbar.
- **Mathematics:** Sampling beziehungsweise Messabbildung `y=H(x)+ε`, nur als
  Kandidat.
- **Renderer:** Observation/Measurement View, noch nicht definiert.
- **Evidence:** `E1` aus dem stabilen Prinzip Observe Before Naming.
- **Open:** Observation Contract, Unsicherheit, Einheiten und Sampling.

### L2A — Planetary Chemistry

- **Purpose:** ordnet beobachtete Entitäten kategorialen planetaren,
  chemischen oder relationalen Korrespondenzen zu.
- **Input:** Observation Records.
- **Output:** klassifizierte Entitäten und Korrespondenzen.
- **Coordinate system:** diskrete Kategorien, Tabellen, Graphknoten und Relationen.
- **Invariants:** Entitäts-ID und Quellprovenienz müssen erhalten bleiben.
- **Visible:** Klassen, Zugehörigkeiten, Korrespondenzen und Polaritäten.
- **Hidden:** kontinuierliche Dynamik, zeitlicher Verlauf und genaue Phase.
- **Loss/Gain:** Relationen werden lesbar; Messdetails können aggregiert werden.
- **Mathematics:** Lookup, Relation oder Encoding `p=E(c)`; nicht dokumentiert.
- **Renderer:** Atlas/Table/Correspondence Renderer; nicht implementiert.
- **Evidence:** `E0` für den genannten Zustand.
- **Open:** Taxonomie, Einheitensystem und Crosswalk zum Scarabaeus Engine.

### L2B — Lunar / Solar Dynamics

- **Purpose:** stellt periodische lunare und solare Einflüsse oder Referenzzyklen
  dar.
- **Input:** zeitgebundene Observation Records.
- **Output:** Phasen, Perioden, Amplituden und relative Zyklen.
- **Coordinate system:** Zeit, Winkelphase oder harmonische Komponenten.
- **Invariants:** Perioden-ID, Phase, Laufrichtung, Epoche und Provenienz.
- **Visible:** Überlagerung, Beat, Verstärkung und Auslöschung.
- **Hidden:** kategoriale Planetary-Chemistry-Zuordnungen.
- **Loss/Gain:** Zyklusbeziehungen werden sichtbar; Einzelereignisse können in
  periodischen Aggregaten verschwinden.
- **Mathematics:** harmonische Superposition als Kandidat.
- **Renderer:** Tide/Phase Renderer; nicht implementiert.
- **Evidence:** `E0–E1`.
- **Open:** physikalische Größe, Einheiten, Epoche und Engine-Kopplung.

### L3 — Scarabaeus Engine

- **Purpose:** integriert kategoriale Parameter und dynamische Zyklen zu einem
  gemeinsamen Orientation State.
- **Input:** Planetary-Chemistry-Zuordnungen und Lunar/Solar Dynamics.
- **Output:** zeitabhängiger Zustandsvektor oder Zustandsgraph.
- **Coordinate system:** unbekannter Engine State Space.
- **Invariants:** Orientation-Object-ID, Entitäts-IDs, Phase und Provenienz.
- **Visible:** Kopplung, Bewegung, Zustand, Übergänge und Wiederkehr.
- **Hidden:** vollständige Quelltaxonomie und Rohbeobachtungen können hinter
  Parametern liegen.
- **Loss/Gain:** integrierte Dynamik wird sichtbar; Ursprungsbeiträge können ohne
  Source Map ununterscheidbar werden.
- **Mathematics:** `x_(t+1)=F(x_t,p,T(t))` als Platzhalter, nicht als Theorie.
- **Renderer:** Engine/Orbital State Renderer; nicht definiert.
- **Evidence:** `E0–E1`.
- **Open:** Zustandsvariablen, Update-Regel, Einheiten und Quellkopplung.

### L4A — Möbius Topology

- **Purpose:** zeigt Kontinuität, Randidentifikation und Seitenwechsel des Engine
  State Space.
- **Input:** Scarabaeus-Zustandspfad und deklarierte Randpaarung.
- **Output:** topologische Projektion mit Seam und lokaler Orientierung.
- **Coordinate system:** Quotientenraum eines Streifens.
- **Invariants:** Pfadkontinuität, Quellidentität und lokale Nachbarschaft.
- **Visible:** Wiederkehr nach Twist, identifizierte Grenzen, lokale Charts.
- **Hidden:** globale Zeitgeschwindigkeit und viele Engine-Parameter.
- **Loss/Gain:** Topologie wird sichtbar; globale Handedness geht verloren.
- **Mathematics:** `(u,0)~(L-u,1)` als Standardkandidat.
- **Renderer:** Topology Renderer; nicht implementiert.
- **Evidence:** `E0–E1`.
- **Open:** Welche Zustände bilden die gepaarten Ränder?

### L4B — Frequency Space

- **Purpose:** zerlegt Engine- oder Kurvendynamik in Frequenz, Amplitude und Phase.
- **Input:** zeitlich geordnete Zustandsspur.
- **Output:** Spektrum oder Frequency Cross.
- **Coordinate system:** Frequenzachsen, komplexe Amplituden, Phasenwinkel.
- **Invariants:** Frequenzverhältnisse und Phase bei dokumentiertem Sampling.
- **Visible:** dominante Moden, Resonanz und Phasenbeziehung.
- **Hidden:** absolute Position, lokale Ereignisreihenfolge und Topologie.
- **Loss/Gain:** Moden werden explizit; Zeitlokalität kann verloren gehen.
- **Mathematics:** DFT/Fourier-Projektion als Kandidat.
- **Renderer:** Spectral/Frequency Renderer; nicht implementiert.
- **Evidence:** `E0–E1`.
- **Open:** Signalquelle, Fenster, Samplingrate und Achsendefinition.

### L5 — Lissajous Geometry

- **Purpose:** projiziert zwei periodische Komponenten und ihre Phasenrelation in
  eine ebene Kurve.
- **Input:** Frequenzpaar und Phase; optional ein beobachteter Pfad aus der
  Möbius-Projektion.
- **Output:** parametrisierte 2D-Trajektorie.
- **Coordinate system:** kartesische Ebene plus Parameter `t`.
- **Invariants:** Frequenzverhältnis, relative Phase und Parameterreihenfolge.
- **Visible:** Kopplungsverhältnis, Wiederholung, Symmetrie und Kreuzungen.
- **Hidden:** absolute Zeit, Quelldomäne und Möbius-Flächenstruktur.
- **Loss/Gain:** Phasenrelation wird geometrisch sichtbar; verschiedene
  Parametrisierungen können dieselbe Kurvenspur erzeugen.
- **Mathematics:** `x=A sin(mt+δ)`, `y=B sin(nt)` als Standardkandidat.
- **Renderer:** Parametric Curve Renderer; nicht implementiert.
- **Evidence:** `E1` aufgrund des Namens, Parameter fehlen.
- **Open:** Achsen, Frequenzen, Phase, Amplituden und Möbius-Beobachtungsfunktion.

### L6 — Stellar Projection

- **Purpose:** überführt eine parametrisierte Geometrie in Richtungen oder Punkte
  einer Himmels-/Kugeldarstellung.
- **Input:** Lissajous-Punkte mit stabiler Reihenfolge.
- **Output:** sphärische Punkte, Sterne oder Konstellationen.
- **Coordinate system:** Kugel, Rektaszension/Deklination oder deklarierte
  alternative Winkelkoordinaten.
- **Invariants:** Punktidentität, Reihenfolge, Provenienz und gewählte Orientierung.
- **Visible:** Richtung, sphärische Nähe, Pole und Konstellationsstruktur.
- **Hidden:** planare Metrik und Kreuzungsstruktur.
- **Loss/Gain:** räumliche Orientierung wird sichtbar; die planare Geometrie wird
  projektionsabhängig verzerrt.
- **Mathematics:** stereographische oder andere explizite Kugelprojektion; offen.
- **Renderer:** Stellar/Spherical Renderer; nicht implementiert.
- **Evidence:** `E0–E1`.
- **Open:** Projektionszentrum, Pole, Singularitäten und Achsenkonvention.

### L7 — Dodecahedral Sky Map

- **Purpose:** diskretisiert den stellaren Raum in adressierbare Regionen und
  Nachbarschaften.
- **Input:** sphärische Punkte oder Richtungen.
- **Output:** Face-/Cell-Adressen und dodekaedrische Nachbarschaft.
- **Coordinate system:** dodekaedrische Flächen, Kanten, Ecken oder duale Zellen.
- **Invariants:** Quellpunkt-ID und Zellzuordnung; Nachbarschaft nur nach
  deklarierter Quantisierung.
- **Visible:** diskrete Region, Adressierung und navigierbare Nachbarschaft.
- **Hidden:** exakte Position innerhalb einer Zelle.
- **Loss/Gain:** stabile Adresse wird sichtbar; kontinuierliche Position wird
  quantisiert.
- **Mathematics:** sphärische Voronoi-/Face-Zuordnung als Kandidat.
- **Renderer:** Polyhedral Sky Renderer; nicht implementiert.
- **Evidence:** `E0–E1`.
- **Open:** Sind Sterne Faces, Vertices, Cell Centers oder freie Punkte?

### L8 — Calendar Projection

- **Purpose:** bindet Phase oder räumliche Adresse an eine zyklische Zeitachse.
- **Input:** stellare Winkelphase und optional dodekaedrische Zelladresse.
- **Output:** Kalenderposition, Phase, Sequenz oder benannter Zeitraum.
- **Coordinate system:** diskrete oder kontinuierliche Kalenderzeit mit Epoche.
- **Invariants:** Reihenfolge, Zyklusposition, Epoche und Provenienz.
- **Visible:** Datum, Wiederkehr, Phase und zeitliche Navigation.
- **Hidden:** räumliche Metrik und Topologie der Vorstufe.
- **Loss/Gain:** zeitliche Lesbarkeit wird gewonnen; räumliche Details werden
  reduziert.
- **Mathematics:** `t=t0+Pθ/(2π) mod P`; konkrete Adams-Regel offen.
- **Renderer:** Calendar/Temporal Renderer; nicht implementiert.
- **Evidence:** `E0–E1`.
- **Open:** Epoche, Periodenlänge, Schaltregel, Zeitzone und Adams-Spezifikation.

### L9 — Orientation Layer

- **Purpose:** stellt eine domain-neutrale, normalisierte Orientierungssicht für
  Navigation und weitere Projektionen bereit.
- **Input:** Calendar Projection mit vollständiger Trace-back-Provenienz.
- **Output:** normalisierte Orientation Coordinates und Quellreferenzen.
- **Coordinate system:** noch nicht als Contract definiert; mindestens normalisierte
  Zyklusposition und typisierte Referenzen.
- **Invariants:** Orientation-Object-ID, Provenienz und deklarierte Zyklusordnung.
- **Visible:** vergleichbare Orientierung unabhängig von Darstellungskonvention.
- **Hidden:** domänenspezifische Details, sofern sie nicht referenziert werden.
- **Loss/Gain:** Interoperabilität wird sichtbar; Domänenbedeutung darf nicht
  stillschweigend abgeflacht werden.
- **Mathematics:** `τ=((t-t0) mod P)/P` als reine Zyklusnormalisierung.
- **Renderer:** Orientation Normalization Renderer; nicht implementiert.
- **Evidence:** `E1` als Ziel der bestehenden Orientation Architecture.
- **Open:** minimaler Orientation-Contract, Lossiness und zulässige Domains.

## 6. Transformationsklassen

| Klasse | Bedeutung | Kanten |
|---|---|---|
| Primary transformation | verändert den primären Koordinatenraum des Flusses | Reality→Observation, Observation→Sources, Sources→Scarab, Lissajous→Stellar |
| Analytical projection | macht Moden oder Parameter einer bestehenden Sicht explizit | Scarab→Frequency, Lissajous→Frequency |
| Visualization-only projection | ordnet dieselbe Information für Lesbarkeit neu | Scarab→Möbius, Frequency→Lissajous, Stellar→Dodeca |
| Merge | verbindet zwei bereits quellengebundene Koordinatensichten | Chemistry+Tide→Scarab, Möbius+Frequency→Lissajous |
| Normalization | überführt domain-spezifische Koordinaten in einen gemeinsamen Bereich | Calendar→Orientation |

Diese Klassen übertragen keine Autorität. „Visualization-only“ bedeutet nicht
beliebig: Auch eine visuelle Projektion benötigt Identität, Parameter und
Lossiness-Provenienz.

## 7. Architekturregeln

1. Jede Representation referenziert `O@V`.
2. Jede Transformation besitzt eine eindeutige Kanten-ID.
3. Parameter, Epoche, Achsen und Laufrichtung gehören zur Kantenprovenienz.
4. Zusammenführungen bewahren die Provenienz beider Eingänge.
5. Nicht injektive Kanten deklarieren verlorene Felder.
6. Eine Rückkante ist eine eigene Transformation, nicht automatisch die Inverse.
7. Visualisierung ersetzt keine mathematische oder semantische Definition.
8. Unbekannte Operatoren bleiben `unknown`; sie werden nicht aus Ähnlichkeit
   erfunden.
9. Orientation Layer normalisiert Koordinaten, nicht Bedeutung.
10. Keine Kante mutiert das Orientation Object.

## 8. Zugehörige Artefakte

- [`contracts/TRANSITION_CONTRACT_SPECIFICATION.md`](contracts/TRANSITION_CONTRACT_SPECIFICATION.md)
  — provider-unabhängiges Contract-Modell und versionierter Katalog für `T01–T15`.
- [`REPRESENTATION_GRAPH.md`](REPRESENTATION_GRAPH.md) — vollständiger Graph und
  Edge-Typen.
- [`REPRESENTATION_MATRIX.md`](REPRESENTATION_MATRIX.md) — vergleichende
  Repräsentationsmatrix.
- [`TRANSITION_CARDS.md`](TRANSITION_CARDS.md) — eine Card pro Graphkante.
- [`INVARIANTS.md`](INVARIANTS.md) — Invariantenstatus über alle Layer.
- [`OPEN_ARCHITECTURE_QUESTIONS.md`](OPEN_ARCHITECTURE_QUESTIONS.md) — priorisierte
  fehlende Operatoren, Crosswalks und Visualisierungen.
