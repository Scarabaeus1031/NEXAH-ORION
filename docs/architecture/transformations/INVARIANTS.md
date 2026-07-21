# Orientation Invariants

- F1-Status: Invariant-Vokabular eingefroren; wissenschaftliche Verifikation offen
- Repository-Version: `0.3.0-dev.0`

## 1. Statuscodes

| Code | Status | Bedeutung |
|---|---|---|
| `P` | preserved | unverändert referenziert oder weitergetragen |
| `D` | derived | deterministisch aus dokumentierten Eingaben ableitbar |
| `A` | aggregated | mehrere Werte werden zusammengefasst oder quantisiert |
| `H` | hidden | vorhanden oder referenzierbar, aber nicht primär sichtbar |
| `L` | lost | aus der Representation allein nicht rekonstruierbar |
| `U` | unknown | Erhaltung ist nicht dokumentiert |

Die Tabelle ist eine Architekturhypothese. `P` ist eine Soll-Invariante und noch
kein Nachweis, solange keine Transition Card mindestens Evidenzstatus `E3` besitzt.

## 2. Invariant Matrix

| Representation | identity | phase | periodicity | polarity | orientation | topology | neighborhood | provenance | frequency ratios | epoch | handedness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Planetary Chemistry | `P` | `U` | `U` | `D` | `H` | `U` | `D` | `P` | `U` | `U` | `H` |
| Tide System | `P` | `P` | `P` | `P` | `D` | `H` | `H` | `P` | `D` | `P` | `H` |
| Scarabaeus Engine | `P` | `P` | `P` | `P` | `D` | `D` | `D` | `P` | `D` | `H` | `D` |
| Möbius | `P` | `P` | `P` | `D` | `L` | `P` | `P` locally | `P` | `H` | `H` | `L` globally |
| Lissajous | `P` | `D` | `P` | `D` | `D` | `A` | `P` on parameter / `U` at crossings | `P` | `P` | `H` | `U` |
| Frequency Cross | `P` | `P` | `D` | `H` | `H` | `L` | `L` | `P` | `P` | `H` | `H` |
| Stellar Projection | `P` | `D` | `H` | `D` | `P` | `D` | `D` | `P` | `H` | `D` | `P` if projection fixed |
| Dodecahedral Sky Map | `P` | `A` | `H` | `D` | `P` | `A` | `A` | `P` | `H` | `H` | `P` if frame fixed |
| Calendar | `P` | `P` | `P` | `H` | `D` | `H` | `A` chronological | `P` | `A` | `P` | `H` |
| Orientation Layer | `P` | `A` | `A` | `A` | `D` | `H` | `A` | `P` | `A` | `A` | `H` |

## 3. Invariant Definitions

### I01 — Identity

Die stabile Referenz auf dasselbe Orientation Object `O@V`. Identity muss in
jeder Representation preserved sein. Fehlt sie, ist die Darstellung kein
nachvollziehbarer Zustand des Transform Stack.

### I02 — Phase

Position innerhalb eines deklarierten Zyklus. Eine Phase benötigt Nullpunkt,
Laufrichtung, Einheit und Periodendefinition. Ein bloßer Winkel ohne diese Angaben
ist keine übertragbare Phase.

### I03 — Periodicity

Wiederholungsstruktur und Periodenlänge. Periodicity kann aus einem Spektrum
derived oder in einem Kalender preserved sein. Eine Projektion darf nicht
stillschweigend eine offene Folge zyklisch schließen.

### I04 — Polarity

Explizite Dualität oder Vorzeichenbeziehung. Beispiele können lunar/solar,
positiv/negativ oder innen/außen sein, sind aber ohne Domainprofil nicht
gleichbedeutend.

### I05 — Orientation

Referenzrahmen, Achsen und Laufrichtung. Orientation ist mehr als Position: Sie
bestimmt, wie Koordinaten gelesen und transformiert werden.

### I06 — Topology

Kontinuität, Randidentifikation, Zusammenhang und Flächeneigenschaften. Eine
planare oder spektrale Projektion kann Topologie verlieren, obwohl die
Quellidentität erhalten bleibt.

### I07 — Neighborhood

Welche Punkte oder Zustände als benachbart gelten. Kurvenkreuzungen sind ein
kritischer Fall: Bildpunkte können räumlich identisch wirken, obwohl ihre
Parameterpositionen nicht benachbart sind.

### I08 — Provenance

Kette aus Quellrepresentation, Transition Card, Parametern, Renderer-Version und
Lossiness. Provenance ist die einzige ausnahmslos geforderte Invariante neben
Identity.

### I09 — Frequency Ratios

Verhältnis periodischer Komponenten, beispielsweise `m:n`. Es ist gegenüber
gemeinsamer Skalierung invariant, nicht aber gegenüber Resampling ohne
dokumentierte Samplingrate.

### I10 — Epoch

Referenzzeitpunkt, der Phase mit konkreter Zeit verbindet. Ohne Epoche kann ein
Zyklus geometrisch korrekt, aber kalendarisch unbestimmt sein.

### I11 — Handedness

Lokale oder globale Links-/Rechtsorientierung eines Koordinatenrahmens. Auf einem
Möbiusband existiert keine konsistente globale Handedness; dieser Verlust muss
explizit bleiben.

## 4. Harte Invarianten

Folgende Felder müssen jede Kante überleben oder die Kante ist architektonisch
ungültig:

| Hard invariant | Regel |
|---|---|
| Orientation Object identity | niemals neu erzeugen oder ersetzen |
| Source version | jede Representation bindet denselben immutable Stand |
| Provenance | jede Kante nennt Source, Target, Operator und Parameter |
| Landmark identity | umbenannte oder aggregierte Landmarken benötigen Crosswalk |
| Declared lossiness | nicht injektive Abbildungen nennen verlorene Felder |

Phase, Periodicity, Neighborhood, Epoch und Handedness sind domainabhängig. Sie
können verborgen oder verloren sein, dürfen aber nicht fälschlich als preserved
markiert werden.

## 5. Invariant Tests für eine spätere Implementierung

Noch ohne Code lassen sich die benötigten Conformance-Fragen festhalten:

```text
Identity test:
  source.orientation_object_id == target.orientation_object_id

Provenance test:
  target.source_representation_ids contains source.representation_id

Order test:
  declared ordered landmarks preserve relative order unless lossiness says otherwise

Phase test:
  normalize(source phase) == normalize(target phase) within declared tolerance

Neighborhood test:
  preserved source edges map to target edges or declared aggregated cells

Round-trip test:
  inverse(T(x)) == x only for fields declared invertible
```

Diese Tests sind Spezifikationshinweise, keine autorisierte Implementierung.

## 6. Kritische Invariant-Brüche

1. **Möbius:** globale Orientation und Handedness sind definitionsgemäß nicht
   preserved.
2. **Frequency Space:** Zeitlokalität, räumliche Neighborhood und Topologie können
   verloren gehen.
3. **Lissajous:** geometrische Kreuzungspunkte bewahren nicht automatisch
   parametrische Neighborhood.
4. **Dodecahedral Sky Map:** kontinuierliche Position wird zu einer Zelle
   aggregated.
5. **Calendar:** räumliche Struktur wird auf Zeitphase reduziert.
6. **Orientation Layer:** zu aggressive Normalisierung kann Domainbedeutung
   abflachen; Trace-back-Provenienz ist deshalb verpflichtend.
