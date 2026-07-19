# Open Architecture Questions

## 1. Zweck

Dieses Register hält fehlende Transformationsbelege fest. Es ist keine
Ideensammlung für neue Geometrie. Jeder Eintrag muss durch vorhandene Quellen,
Landmark-Crosswalks oder explizite Transformationsdefinitionen beantwortet werden.

## 2. Prioritätsskala

| Priorität | Bedeutung |
|---|---|
| `P0` | blockiert die Behauptung, dass alle Representations dasselbe Orientation Object zeigen |
| `P1` | blockiert eine zentrale Transformationsroute oder Invariante |
| `P2` | blockiert Reproduzierbarkeit, Vergleich oder Conformance |
| `P3` | verbessert Navigation und Dokumentation, ohne Identität zu blockieren |

## 3. Priorisiertes Missing-Pieces-Register

| Rang | Priorität | Fehlendes Element | Betroffene Kanten | Warum architektonisch wichtig | Benötigter Nachweis |
|---:|---|---|---|---|---|
| 1 | `P0` | Canonical Orientation Object Identity | alle | Ohne gemeinsame ID sind die Visualisierungen nur eine Sammlung ähnlicher Artefakte. | Objekt-ID, Quellversion und Representation-ID auf jedem Visual |
| 2 | `P0` | Landmark Crosswalk | alle ab `T02` | Identität einzelner Punkte, Planeten, Phasen oder Zellen kann nicht verfolgt werden. | 5–10 benannte Landmarken mit ID pro Representation |
| 3 | `P0` | Scarabaeus State Vector | `T04–T07` | Der zentrale Merge Point besitzt keine dokumentierten Variablen. | State-Dictionary mit Namen, Typ, Einheit, Quelle und Update-Rolle |
| 4 | `P0` | Source-to-Engine Coupling | `T04`, `T05` | Chemistry und Tide können nicht reproduzierbar in denselben Engine State überführt werden. | Category-to-state Crosswalk und Tide-Kopplungsregel |
| 5 | `P1` | Phase/Epoch Convention | `T03`, `T05`, `T09–T15` | Nullpunkt, Laufrichtung und Perioden lassen sich sonst nicht vergleichen. | globale Phase Plate mit `t0`, Einheit, Richtung und Perioden-IDs |
| 6 | `P1` | Möbius Seam Mapping | `T06`, `T08` | Randidentifikation und Verlust globaler Handedness bleiben rein metaphorisch. | gepaarte Engine-Zustände, Seam, lokale Charts und Traversal |
| 7 | `P1` | Frequency Cross Axis Definition | `T07`, `T09`, `T10` | Frequenzverhältnis und Phase sind ohne Achsen/Sampling nicht interpretierbar. | Achsen, Einheit, Samplingrate, Fenster und Normalisierung |
| 8 | `P1` | Lissajous Parameter Record | `T08–T11` | Die Kurve kann nicht reproduziert oder rückanalysiert werden. | `A`, `B`, `m`, `n`, `δ`, Parameterintervall und Sample Order |
| 9 | `P1` | Plane-to-Sphere Projection | `T11` | Stellar-Koordinaten sind ohne Projektionsfamilie nicht aus Lissajous ableitbar. | Formel, Zentrum, Pole, Achsen, Singularitäten und Inverse |
| 10 | `P1` | Dodecahedral Landmark Model | `T12`, `T14` | Unklar ist, ob Sterne Faces, Vertices, Zellen oder freie Punkte repräsentieren. | Polyederrahmen, Landmark-Typ, Face-Normalen und Boundary Rule |
| 11 | `P1` | Adams Calendar Specification | `T13–T15` | Calendar Projection bleibt ohne Epoche, Periode und Schaltregel unbestimmt. | Calendar Profile mit Epoch, cycle lengths, labels and timezone |
| 12 | `P1` | Orientation Layer Contract | `T15` | Das Ziel der Normalisierung ist nicht maschinenlesbar definiert. | minimale Felder, Domain Tags, Source References und Lossiness |
| 13 | `P2` | Transition Provenance Record | alle | Renderer- und Parameteränderungen sind nicht unterscheidbar. | Edge-ID, Source/Target IDs, operator version, parameters, timestamp |
| 14 | `P2` | Lossiness Profile | `T02`, `T06–T15` | Nicht injektive Kanten können fälschlich als äquivalent gelten. | preserved/derived/aggregated/hidden/lost pro Feld |
| 15 | `P2` | Renderer Definitions | alle Visualisierungskanten | Darstellungslogik bleibt implizit im Bild. | Renderer-ID, Input Profile, Output Profile, deterministic config |
| 16 | `P2` | Merge Provenance | Scarab- und Lissajous-Merge | Zielwerte lassen sich nicht auf den jeweiligen Eingang zurückführen. | field-level source references für beide Inputs |
| 17 | `P2` | Invertibility/Conformance Profiles | alle | Rückprojektion und Äquivalenz werden sonst überbehauptet. | Testfälle und Toleranzen je Kante |
| 18 | `P3` | Transition Visualization Plates | alle | Operatoren bleiben trotz Text schwer vergleichbar. | die unten beschriebenen Übergangsplatten |

## 4. Undokumentierte Übergänge

### Q01 — Observation Boundary

Wo endet Reality und wo beginnt eine versionierbare Observation? Benötigt werden
Beobachter, Zeitpunkt, Instrument, Einheit, Scope und Unsicherheit. Ohne diese
Grenze können spätere Visualisierungen nicht auf dieselbe Beobachtung zurückgeführt
werden.

### Q02 — Planetary Chemistry → Scarabaeus

Welche kategorialen Felder werden unverändert referenziert, welche numerisch
codiert und welche verworfen? Ist die Zuordnung injektiv, gewichtet oder
many-to-many?

### Q03 — Tide → Scarabaeus

Ist Lunar/Solar Dynamics:

- ein externer Treiber;
- ein interner Engine-Takt;
- ein Messsignal;
- oder eine parallele Darstellung desselben bereits berechneten Zustands?

Diese Rollen sind architektonisch verschieden.

### Q04 — Scarabaeus → Möbius

Welche Engine-Grenzen werden identifiziert? Ein Möbiusband ist nur dann eine
Transformation und nicht bloß ein Symbol, wenn Seam, Randpaarung und Zustandsroute
dokumentiert sind.

### Q05 — Möbius → Lissajous

Es existiert keine kanonische Standardabbildung. Benötigt wird eine explizite
Beobachtungsfunktion `h`, die zwei Lissajous-Achsen aus einem Möbius-Pfad ableitet.

### Q06 — Frequency Cross ↔ Lissajous

Welche Frequenzkomponenten bilden `x` und `y`? Bleiben komplexe Phase, Sampling
und Parameterzeit erhalten? Die Hin- und Rückrichtung benötigen getrennte Cards
und Operatoren.

### Q07 — Lissajous → Stellar

Ist die Abbildung stereographisch, gnomonisch, equirektangular oder domäneneigen?
Die Projektionsfamilie bestimmt Pole, Verzerrung, Singularitäten und
Invertierbarkeit.

### Q08 — Stellar → Dodecahedral

Welcher Polyederbestandteil adressiert einen Sternpunkt? Eine Face-Zuordnung,
Vertex-Zuordnung und duale Zellkarte besitzen unterschiedliche Neighborhoods.

### Q09 — Stellar/Dodecahedral → Calendar

Der direkte Winkelpfad und der diskrete Zellpfad müssen entweder als zwei
verschiedene Calendar Representations markiert oder durch ein Äquivalenzprofil
verbunden werden.

### Q10 — Calendar → Orientation

Welche Kalenderdetails bleiben nur referenziert und welche werden normalisiert?
Eine einzige Zahl `τ` genügt nicht, wenn Domain, Epoche und Lossiness nicht
erreichbar bleiben.

## 5. Fehlende mathematische Operatoren

| Operator-ID | Kante | Minimal erforderliche Definition | Status |
|---|---|---|---|
| `OP-OBSERVE` | `T01` | Sampling-/Observation Map und Unsicherheit | missing |
| `OP-CHEM-ENCODE` | `T02`, `T04` | Taxonomie- und Engine-Encoding | missing |
| `OP-TIDE-PHASE` | `T03` | harmonische Variablen, Einheiten, Epoche | candidate only |
| `OP-ENGINE-COUPLE` | `T05` | Kopplung von Tide und State Update | missing |
| `OP-MOBIUS-QUOTIENT` | `T06` | Engine-to-strip map und boundary pairing | partial candidate |
| `OP-MOBIUS-OBSERVE` | `T08` | Pfad und 2D observation map `h` | missing |
| `OP-SPECTRAL` | `T07`, `T10` | Signal-, Sampling- und Fourier/Fit-Profil | partial candidate |
| `OP-LISSAJOUS` | `T09` | vollständiger Parametersatz | partial candidate |
| `OP-SPHERE` | `T11` | konkrete plane-to-sphere projection | missing |
| `OP-DODECA-CELL` | `T12` | cell assignment and boundary rule | partial candidate |
| `OP-ANGLE-TIME` | `T13` | epoch, period and selected angle | partial candidate |
| `OP-CELL-CALENDAR` | `T14` | lookup/permutation from cell to interval | missing |
| `OP-ORIENT-NORMALIZE` | `T15` | Orientation Contract and normalization | partial candidate |

## 6. Fehlende Renderer-Definitionen

Benötigt werden keine Implementierungen, sondern zunächst Renderer Profiles:

| Renderer Profile | Input | Output | Kritische Definition |
|---|---|---|---|
| Chemistry Atlas Renderer | categorized observations | correspondence atlas | taxonomie, ordering, legend |
| Tide Renderer | phase components | tide/phase view | epoch, units, superposition |
| Scarabaeus State Renderer | engine state | orbital/state view | state axes and landmark mapping |
| Möbius Renderer | topology profile | strip/surface view | seam and local charts |
| Lissajous Renderer | parametric profile | ordered curve | axes, phase and sampling |
| Frequency Cross Renderer | spectrum | frequency view | axes, complex phase and scale |
| Stellar Renderer | spherical points | sky projection | projection family and frame |
| Dodecahedral Sky Renderer | spherical cells | polyhedral map | orientation and cell semantics |
| Calendar Renderer | calendar state | temporal view | epoch, labels and cycle rules |
| Orientation Renderer | normalized state | domain-neutral view | preserved references and lossiness |

## 7. Fehlende Provenienz

Jede vorhandene Visualisierung sollte mindestens folgende Sidecar-Angaben erhalten:

```text
orientation_object_id
orientation_object_version
representation_id
representation_type
source_representation_ids
transition_card_ids
renderer_profile_id
renderer_version
operator_ids
parameters
landmark_crosswalk_version
phase_epoch_profile
lossiness_profile
evidence_sources
```

Dies ist eine Dokumentationsanforderung, noch kein Runtime-Schema.

## 8. Fehlende Landmark- und Phase-Mappings

### Landmark Minimum Set

Es sollten zunächst fünf bis zehn bereits vorhandene Landmarken ausgewählt werden.
Für jede Representation wird nur eingetragen:

```text
preserved | renamed | derived | aggregated | hidden | lost | unknown
```

Neue Landmarken werden in Phase 3B nicht erfunden.

### Phase Minimum Set

Jede zyklische Darstellung benötigt:

- phase origin;
- direction;
- period ID and length;
- units;
- epoch;
- wrap/modulo rule;
- relation to preceding phase coordinate.

## 9. Fehlende Visualisierungsplatten

Diese Platten zeigen Übergänge, keine neuen Repräsentationswelten:

| Rang | Platte | Zweck |
|---:|---|---|
| 1 | Canonical Landmark Crosswalk | dieselben Referenzpunkte über alle Zustände verfolgen |
| 2 | Phase and Epoch Transfer Plate | Nullpunkt, Richtung und Periode von Tide bis Calendar zeigen |
| 3 | Scarabaeus State Vector Plate | Engine-Achsen, Einheiten und Quellfelder sichtbar machen |
| 4 | Möbius Seam and Cut Plate | Randpaarung und lokalen Orientation Flip zeigen |
| 5 | Frequency-to-Lissajous Plate | Frequenzpaar, Phase und resultierende Kurve nebeneinanderstellen |
| 6 | Plane-to-Sphere Plate | Projektionszentrum, Pole, Verzerrung und inverse Route zeigen |
| 7 | Sphere-to-Dodecahedron Plate | Zellen, Normals, Grenzen und Tie-Break-Regel zeigen |
| 8 | Stellar/Cell-to-Calendar Plate | direkte und diskrete Calendar Route vergleichen |
| 9 | Information Loss Plate | preserved/hidden/lost pro Kante zeigen |
| 10 | Transition Provenance Strip | IDs, Versionen, Operatoren und Parameter unter jedem Visual zeigen |

## 10. Empfohlene Schließungsreihenfolge

1. `P0`: Orientation Object ID und Representation IDs an allen Visuals ergänzen.
2. `P0`: Canonical Landmark Crosswalk erstellen.
3. `P0`: Scarabaeus State Vector und beide Source-to-Engine-Mappings dokumentieren.
4. `P1`: gemeinsame Phase/Epoch Convention festlegen.
5. `P1`: Frequency Cross ↔ Lissajous als erste vollständig parametrisierte Kante
   auf Evidenzniveau `E3` bringen.
6. `P1`: Stellar → Dodecahedral und Stellar → Calendar dokumentieren.
7. `P1`: Möbius-Kanten erst formalisieren, nachdem Seam und Observation Map
   vorhanden sind.
8. `P1`: Orientation Layer Contract zuletzt aus den belegten Invarianten ableiten.

Diese Reihenfolge fügt keine Geometrie hinzu. Sie erhöht ausschließlich
Traceability und Navigierbarkeit des vorhandenen Systems.
