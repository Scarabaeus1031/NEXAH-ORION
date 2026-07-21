# Representation Matrix

- F1-Status: Repräsentationsrollen eingefroren; unbekannte Evidenz bleibt unbekannt
- Repository-Version: `0.3.0-dev.0`

## 1. Leseregel

Die Matrix vergleicht die zehn benannten Repräsentationen. „Dimension“ bezeichnet
die minimale konzeptionelle Koordinatendimension, nicht die Pixel- oder
Layoutdimension eines Posters. `unknown` bleibt bewusst unbekannt, bis ein
Visual-Crosswalk oder Contract vorliegt.

„Visible Information“ ist Information, die in dieser Darstellung leichter
abgelesen werden kann. Sie ist kein neu erzeugtes Wissen. „Renderer“ bezeichnet
eine zukünftige Renderer-Familie, keine implementierte Klasse.

## 2. Matrix

| Representation | Coordinate Space | Dimension | Primary Variables | Visible Information | Hidden Information | Information Loss | Renderer | Status |
|---|---|---:|---|---|---|---|---|---|
| Planetary Chemistry | diskrete Kategorien und Relationsgraph | diskret / `n` | entity ID, class, correspondence, polarity, weight | Zugehörigkeit, planetare/chemische Korrespondenz, Relation | kontinuierliche Zeit, Bahn, Frequenz, Epoche | Rohmessungen und Dynamik können in Klassen aggregiert werden | Atlas/Correspondence Renderer | `E0`; Taxonomie und Crosswalk fehlen |
| Tide System | Zeit-/Phasenraum, optional harmonische Ebene | 1D Zeit plus Komponenten | `t`, `A_L`, `A_S`, `ω_L`, `ω_S`, `φ_L`, `φ_S` | Perioden, Phase, Beat, Verstärkung, Auslöschung | kategoriale Entitäten, räumliche Topologie | Einzelereignisse und nichtperiodische Anteile können verschwinden | Tide/Phase Renderer | `E0–E1`; Einheiten und Epoche fehlen |
| Scarabaeus Engine | dynamischer Zustandsraum oder Zustandsgraph | `n`, unknown | state vector `x`, parameters `p`, phase, transitions | integrierter Zustand, Kopplung, Bewegung, Wiederkehr | vollständige Quellbeiträge, sofern nicht separat referenziert | Quellen können in einem gemeinsamen State aggregiert werden | Engine/Orbital Renderer | `E0–E1`; State Contract fehlt |
| Möbius | topologischer Quotientenraum | 2D Fläche in optionaler 3D-Einbettung | `u`, `v`, seam, local orientation | Kontinuität, Randpaarung, Twist, Seitenwechsel | Frequenzen, absolute Zeit, globale Handedness | globale Orientierung geht verloren; Engine-Variablen werden stark reduziert | Topology Renderer | `E0–E1`; Seam Mapping fehlt |
| Lissajous | parametrisierte kartesische Ebene | 2D plus Parameter | `x(t)`, `y(t)`, `m:n`, `δ`, `A`, `B` | Frequenzverhältnis, Phase, Symmetrie, Kreuzungen | absolute Zeit, Quellklassen, Flächenstruktur | unterschiedliche Parametrisierungen können dieselbe Kurvenspur besitzen | Parametric Curve Renderer | `E1`; konkrete Parameter fehlen |
| Frequency Cross | Frequenz-/Phasenraum | mindestens 2D | frequency axes, amplitude, phase, ratio | Moden, Resonanz, Phasenrelation, Frequenzverhältnis | absolute Lage, Ereignisfolge, topologische Seam | Zeitlokalität und räumliche Nachbarschaft können verloren gehen | Spectral/Frequency Renderer | `E0–E1`; Achsen und Sampling fehlen |
| Stellar Projection | sphärischer Richtungsraum | 2D Mannigfaltigkeit | longitude/RA, latitude/declination, point ID | Richtung, Pole, sphärische Nähe, Konstellation | planare Distanz und Lissajous-Kreuzungen | projektionsabhängige metrische Verzerrung | Stellar/Spherical Renderer | `E0–E1`; Projektionsformel fehlt |
| Dodecahedral Sky Map | polyhedrale beziehungsweise sphärische Zellstruktur | diskrete 2D-Zellen auf 3D-Körper | face/cell ID, edge, vertex, adjacency | Adresse, Region, diskrete Nachbarschaft, Navigation | genaue Position innerhalb der Zelle | kontinuierliche Kugelkoordinate wird quantisiert | Polyhedral Sky Renderer | `E0–E1`; Landmark-/Cell-Regel fehlt |
| Calendar | zyklische oder diskrete Zeitachse | 1D zyklisch plus Labels | epoch `t0`, period `P`, phase `θ`, date/index | Datum, Sequenz, Wiederkehr, benannte Phase | räumliche Metrik, Topologie, Frequenzdetails | Winkel und Zellen werden zu Zeitsegmenten aggregiert | Calendar/Temporal Renderer | `E0–E1`; Adams-Regel fehlt |
| Orientation Layer | normalisierter, typisierter Orientierungsraum | minimal 1D zyklisch; Contract unknown | normalized phase `τ`, source refs, domain tags | Vergleichbarkeit, Trace-back, domain-neutrale Navigation | domänenspezifische Details, sofern nicht referenziert | mögliche semantische Abflachung bei zu aggressiver Normalisierung | Orientation Normalization Renderer | `E1`; Contract und Lossiness-Profil fehlen |

## 3. Koordinatenfamilien

| Familie | Representations | Gemeinsame Eigenschaft |
|---|---|---|
| categorical | Planetary Chemistry | diskrete Entitäten und Relationen |
| temporal/periodic | Tide, Calendar, Orientation Layer | Phase, Periode, Epoche, Modulo-Ordnung |
| dynamic | Scarabaeus Engine | Zustand und Übergang |
| topological | Möbius | Kontinuität und Randidentifikation |
| spectral/parametric | Frequency Cross, Lissajous | Frequenz, Phase und parametrische Spur |
| spherical/polyhedral | Stellar, Dodecahedral Sky Map | Richtung, Region und Nachbarschaft |

## 4. Informationsbilanz

Für eine deterministische Transformation `R_j=T(R_i)` gilt ohne zusätzliche
Quelle konzeptionell die Data-Processing-Grenze:

```text
source information available in R_j
  <= source information available in R_i
```

Die Spalte „Visible Information“ bezeichnet deshalb einen Gewinn an
Ablesbarkeit, Adressierbarkeit oder Vergleichbarkeit. Tatsächliche zusätzliche
Information ist nur an Merge Points möglich, an denen mehrere bereits
provenienzgebundene Eingänge zusammengeführt werden:

- Planetary Chemistry + Tide System → Scarabaeus Engine;
- Möbius Topology + Frequency Space → Lissajous Geometry, sofern beide Eingänge
  tatsächlich verwendet werden;
- Stellar Phase + Dodecahedral Address → Calendar, sofern die Adressroute gilt.

Auch dort wird keine Theorie erfunden. Die Zielrepresentation kann lediglich die
Information mehrerer Quellen gemeinsam sichtbar machen.

## 5. Repräsentationsidentität

Jede zukünftige Matrixzeile benötigt mindestens:

```text
orientation_object_id
orientation_object_version
representation_id
representation_type
coordinate_profile_id
renderer_id
renderer_version
source_representation_ids
transition_card_ids
provenance
lossiness_status
```

Diese Liste ist eine architektonische Checkliste, kein freigegebenes Schema.
