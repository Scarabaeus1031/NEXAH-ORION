# Transition Cards

## 1. Verwendung

Jede Card beschreibt genau eine Kante aus dem
[`Representation Graph`](REPRESENTATION_GRAPH.md). Candidate Mathematics ist eine
mögliche Koordinatenoperation, keine Behauptung über wissenschaftliche Gültigkeit
oder die historische Konstruktion der Visualisierung.

Invertibility verwendet ausschließlich die erlaubten Werte `yes`, `locally`,
`partially`, `unknown` und `no`.

Phase 3C formalisiert diese Cards als einzeln versionierte Contracts im
[`TransitionContract-Katalog`](contracts/TRANSITION_CONTRACT_SPECIFICATION.md).

## T01 — Reality → Observation

| Feld | Inhalt |
|---|---|
| Source | Reality |
| Target | Observation |
| Shared Identity | Ein beobachtetes Ereignis muss eine stabile Source Reference erhalten; vollständige Reality-Identität ist außerhalb ORION nicht beweisbar. |
| Coordinate Change | nicht formalisierter Weltzustand → Beobachter-, Zeit-, Instrument- und Messkoordinaten |
| Invariant Fields | Quellreferenz, soweit verfügbar; Zeitpunkt; Beobachter; Instrumentprofil |
| Derived Fields | Messwert, Einheit, Unsicherheit, Beobachtungsfenster |
| Lost Fields | nicht beobachtete Freiheitsgrade und alles außerhalb des Messfensters |
| Transformation Type | primary observation / sampling |
| Candidate Mathematics | `y=H(x)+ε`; nur allgemeines Messmodell |
| Required Parameters | Observer, instrument, units, timestamp, sampling rule, uncertainty model |
| Invertible? | no |
| Evidence Status | `E1`; Observe Before Naming ist stabil, ein Observation Contract fehlt. |
| Open Questions | Was darf als Observation gelten? Wie werden Unsicherheit und fehlende Werte dargestellt? |

## T02 — Observation → Planetary Chemistry

| Feld | Inhalt |
|---|---|
| Source | Observation |
| Target | Planetary Chemistry |
| Shared Identity | Observation-ID und beobachtete Entity-ID |
| Coordinate Change | Mess-/Beschreibungskoordinaten → diskrete Klassen und Korrespondenzrelationen |
| Invariant Fields | Entity-ID, Source Reference, Provenienz |
| Derived Fields | class ID, planetary/chemical correspondence, polarity, relation weight |
| Lost Fields | Rohmessung, Unsicherheitsstruktur und kontinuierliche Dynamik, sofern nicht referenziert |
| Transformation Type | categorical projection |
| Candidate Mathematics | `p=E(c)` beziehungsweise Relation `R⊆Observation×Category`; `E` unbekannt |
| Required Parameters | Taxonomieversion, Lookup-Tabelle, Einheiten, Konfliktregel |
| Invertible? | partially |
| Evidence Status | `E0`; Zustand benannt, Crosswalk nicht verfügbar. |
| Open Questions | Sind Zuordnungen one-to-one, many-to-many oder gewichtet? Welche Kategorien sind Quelle statt Metapher? |

## T03 — Observation → Lunar/Solar Dynamics

| Feld | Inhalt |
|---|---|
| Source | Observation |
| Target | Lunar/Solar Dynamics |
| Shared Identity | Observation-ID, Zeitpunkt und referenzierte Himmelskörper/Zyklen |
| Coordinate Change | zeitgebundene Beobachtungen → Phasen- und harmonische Koordinaten |
| Invariant Fields | Timestamp, Epoche, Einheit, Quellprovenienz |
| Derived Fields | lunar phase, solar phase, periods, amplitudes, relative phase, beat |
| Lost Fields | nichtperiodische Details und kategoriale Chemistry-Beziehungen |
| Transformation Type | temporal/harmonic projection |
| Candidate Mathematics | `T(t)=A_L cos(ω_Lt+φ_L)+A_S cos(ω_St+φ_S)` |
| Required Parameters | `A_L`, `A_S`, `ω_L`, `ω_S`, `φ_L`, `φ_S`, epoch, sampling interval |
| Invertible? | partially |
| Evidence Status | `E0–E1`; Periodensicht plausibel, konkrete Größen fehlen. |
| Open Questions | Werden physikalische Tiden, symbolische Phasen oder beide dargestellt? Welche Einheit besitzt `T`? |

## T04 — Planetary Chemistry → Scarabaeus Engine

| Feld | Inhalt |
|---|---|
| Source | Planetary Chemistry |
| Target | Scarabaeus Engine |
| Shared Identity | Orientation Object, Entity-IDs und Category Source References |
| Coordinate Change | kategorialer Relationsraum → Engine-Parameter oder initialer Zustandsvektor |
| Invariant Fields | Entity-ID, category ID, relation provenance |
| Derived Fields | engine parameter `p_i`, initial state component, coupling weight |
| Lost Fields | Taxonomiedetails, falls nur numerischer Parameter erhalten bleibt |
| Transformation Type | merge input / parameter encoding |
| Candidate Mathematics | `x_0=E(c_1,…,c_n)` oder `p_i=W c_i`; Operator `E/W` unbekannt |
| Required Parameters | Category-to-state crosswalk, scale, units, normalization, missing-category rule |
| Invertible? | unknown |
| Evidence Status | `E0`; keine State-Variable-Zuordnung dokumentiert. |
| Open Questions | Welche Chemistry-Felder treiben welche Engine-Achsen? Bleibt der Crosswalk im Ziel erhalten? |

## T05 — Lunar/Solar Dynamics → Scarabaeus Engine

| Feld | Inhalt |
|---|---|
| Source | Lunar/Solar Dynamics |
| Target | Scarabaeus Engine |
| Shared Identity | Orientation Object, phase source IDs, epoch and cycle IDs |
| Coordinate Change | harmonische Zeitkoordinaten → externer Treiber, Takt oder interne Phase des Engine State |
| Invariant Fields | phase, periodicity, epoch, direction, source provenance |
| Derived Fields | forcing term, beat state, phase-lock indicator |
| Lost Fields | getrennte lunare/solare Beiträge, falls nur Summensignal gespeichert wird |
| Transformation Type | merge input / periodic forcing |
| Candidate Mathematics | `x_(t+1)=F(x_t,p,T(t))`; konkrete Kopplung `F` unknown |
| Required Parameters | coupling strength, timestep, initial phase, epoch, sampling rule |
| Invertible? | unknown |
| Evidence Status | `E0`; Rolle des Tide Systems im Engine nicht dokumentiert. |
| Open Questions | Ist Tide Ursache, Takt, Messgröße oder parallele Darstellung? Werden Einzelkomponenten erhalten? |

## T06 — Scarabaeus Engine → Möbius Topology

| Feld | Inhalt |
|---|---|
| Source | Scarabaeus Engine |
| Target | Möbius Topology |
| Shared Identity | Orientation Object und referenzierter Zustandspfad |
| Coordinate Change | dynamischer Zustandsraum → topologischer Quotientenraum mit Randidentifikation |
| Invariant Fields | path continuity, local neighborhood, state landmark IDs, provenance |
| Derived Fields | seam position, paired boundary states, local orientation, twist count |
| Lost Fields | globale Handedness, absolute Geschwindigkeit, nicht dargestellte State-Variablen |
| Transformation Type | visualization-only topological projection |
| Candidate Mathematics | `(u,0)~(L-u,1)`; Zuordnung `x→(u,v)` unknown |
| Required Parameters | strip coordinates, boundary pair, seam, direction, embedding profile |
| Invertible? | locally |
| Evidence Status | `E0–E1`; Möbius-Name liefert Topologie, Engine-Seam fehlt. |
| Open Questions | Welche Engine-Zustände werden identifiziert? Ist der Twist strukturell oder nur visuell? |

## T07 — Scarabaeus Engine → Frequency Space

| Feld | Inhalt |
|---|---|
| Source | Scarabaeus Engine |
| Target | Frequency Space |
| Shared Identity | Orientation Object, source signal ID and sampled interval |
| Coordinate Change | zeit-/zustandsgeordnete Spur → Frequenz, Amplitude und Phase |
| Invariant Fields | frequency ratios and relative phase under documented sampling |
| Derived Fields | spectral coefficients, dominant modes, resonance indicators |
| Lost Fields | Zeitlokalität, absolute Position und räumliche Neighborhood bei globaler Fourier-Projektion |
| Transformation Type | analytical projection |
| Candidate Mathematics | `X_k=Σ_(n=0)^(N-1) x_n exp(-2πikn/N)` |
| Required Parameters | selected signal, sampling rate, window, interval, normalization, detrending |
| Invertible? | yes bei vollständigem komplexem Spektrum; sonst partially |
| Evidence Status | `E1`; Standardoperation plausibel, konkrete Frequency-Cross-Achsen fehlen. |
| Open Questions | Welches Engine-Signal wird analysiert? Werden Phase und negative Frequenzen gespeichert? |

## T08 — Möbius Topology → Lissajous Geometry

| Feld | Inhalt |
|---|---|
| Source | Möbius Topology |
| Target | Lissajous Geometry |
| Shared Identity | Orientation Object, path ID and traversal order |
| Coordinate Change | Pfad auf Quotientenfläche → beobachtete 2D-Kurve |
| Invariant Fields | path order, periodic closure, selected landmarks, provenance |
| Derived Fields | planar coordinates, crossings, apparent symmetry |
| Lost Fields | Flächenkoordinate, seam context, global non-orientability |
| Transformation Type | visualization-only local chart / observation map |
| Candidate Mathematics | `γ(t)=h(q(u(t),v(t)))`; `q` Quotient, `h` unknown observation map |
| Required Parameters | path `u(t),v(t)`, chart, seam handling, projection `h`, phase origin |
| Invertible? | no, sofern nur die Kurvenspur bleibt |
| Evidence Status | `E0`; keine kanonische Möbius→Lissajous-Abbildung bekannt. |
| Open Questions | Welche Eigenschaft der Möbius-Bahn bestimmt die beiden Lissajous-Achsen? |

## T09 — Frequency Space → Lissajous Geometry

| Feld | Inhalt |
|---|---|
| Source | Frequency Space |
| Target | Lissajous Geometry |
| Shared Identity | Orientation Object, component IDs, frequency ratio and phase relation |
| Coordinate Change | Frequenz-/Phasenparameter → parametrisierte kartesische Kurve |
| Invariant Fields | ratio `m:n`, relative phase `δ`, component order, provenance |
| Derived Fields | curve points, symmetry, closure period, crossings |
| Lost Fields | absolute epoch and spectral components not selected for the two axes |
| Transformation Type | parametric synthesis / visualization projection |
| Candidate Mathematics | `x=A sin(mt+δ)`, `y=B sin(nt)` |
| Required Parameters | `A`, `B`, `m`, `n`, `δ`, parameter interval, sampling density |
| Invertible? | partially |
| Evidence Status | `E1`; mathematically starke Kandidatenkante, konkrete Werte fehlen. |
| Open Questions | Welche Frequenzachsen werden gewählt? Ist die Curve geschlossen oder zeitlich begrenzt? |

## T10 — Lissajous Geometry → Frequency Space

| Feld | Inhalt |
|---|---|
| Source | Lissajous Geometry |
| Target | Frequency Space |
| Shared Identity | Orientation Object, trajectory ID and parameter order |
| Coordinate Change | parametrisierte 2D-Spur → geschätzte Frequenz-, Amplituden- und Phasenparameter |
| Invariant Fields | ratios and relative phase only when parameterization and sampling survive |
| Derived Fields | fitted `m`, `n`, `A`, `B`, `δ`, residual/error |
| Lost Fields | geometrische Lage nach ausschließlicher Parameterspeicherung |
| Transformation Type | analytical reverse projection / parameter estimation |
| Candidate Mathematics | Fourier analysis or least-squares fit of the Lissajous model |
| Required Parameters | ordered samples, timestamps, fit model, tolerance, aliasing policy |
| Invertible? | partially |
| Evidence Status | `E1`; analytisch möglich, nicht als bestehender Operator belegt. |
| Open Questions | Ist `t` erhalten? Wie werden Mehrdeutigkeit, Aliasing und verrauschte Kurven behandelt? |

## T11 — Lissajous Geometry → Stellar Projection

| Feld | Inhalt |
|---|---|
| Source | Lissajous Geometry |
| Target | Stellar Projection |
| Shared Identity | Orientation Object, curve-point IDs and parameter order |
| Coordinate Change | kartesische Ebene → Kugelrichtungen oder Himmelskoordinaten |
| Invariant Fields | point identity, order, provenance; orientation only under a fixed projection frame |
| Derived Fields | longitude/right ascension, latitude/declination, spherical distance |
| Lost Fields | planare Metrik und Kreuzungseigenschaften, abhängig von Projektion |
| Transformation Type | primary spatial projection |
| Candidate Mathematics | inverse stereographic map `(X,Y,Z)=(2x,2y,x²+y²-1)/(x²+y²+1)` |
| Required Parameters | projection family, center, scale, poles, axis orientation, singularity policy |
| Invertible? | yes außerhalb deklarierter Singularität für stereographische Projektion; sonst unknown |
| Evidence Status | `E0`; Projektionsfamilie nicht dokumentiert. |
| Open Questions | Sind Punkte tatsächliche Sterne, symbolische Marker oder freie Kugelkoordinaten? |

## T12 — Stellar Projection → Dodecahedral Sky Map

| Feld | Inhalt |
|---|---|
| Source | Stellar Projection |
| Target | Dodecahedral Sky Map |
| Shared Identity | Orientation Object and stellar point IDs |
| Coordinate Change | kontinuierliche Kugelkoordinate → dodekaedrische Face-/Cell-Adresse |
| Invariant Fields | point ID, source direction by reference, cell adjacency, provenance |
| Derived Fields | face ID, local cell coordinate, edge/vertex neighborhood |
| Lost Fields | exakte sphärische Position, wenn nur Cell-ID erhalten bleibt |
| Transformation Type | visualization-only spherical quantization |
| Candidate Mathematics | `cell(p)=argmax_i(n_i·p)` für deklarierte Face-Normalen `n_i` |
| Required Parameters | polyhedron orientation, face normals, tie-break rule, boundary tolerance, local coordinates |
| Invertible? | no bei reiner Cell-ID; partially mit lokaler Zellkoordinate |
| Evidence Status | `E0–E1`; dodekaedrische Adressierung plausibel, Rolle der Sterne offen. |
| Open Questions | Werden Faces, Vertices oder duale Zellen verwendet? Wie werden Grenzpunkte behandelt? |

## T13 — Stellar Projection → Calendar Projection

| Feld | Inhalt |
|---|---|
| Source | Stellar Projection |
| Target | Calendar Projection |
| Shared Identity | Orientation Object, point/phase ID and source epoch reference |
| Coordinate Change | sphärischer Winkel oder Bahnphase → zyklische Zeitkoordinate |
| Invariant Fields | cyclic order, phase, direction, epoch, provenance |
| Derived Fields | date/time index, named phase, recurrence position |
| Lost Fields | latitude/declination and spatial neighborhood when only one angle drives time |
| Transformation Type | primary phase-to-time transformation |
| Candidate Mathematics | `t=t0+(P/(2π))θ mod P` |
| Required Parameters | selected angle `θ`, epoch `t0`, period `P`, direction, calendar rules, timezone |
| Invertible? | partially innerhalb eines bekannten Zyklus |
| Evidence Status | `E0–E1`; notwendige Parameter nicht dokumentiert. |
| Open Questions | Welcher Stellar-Winkel steuert den Kalender? Wie werden mehrere Zyklen kombiniert? |

## T14 — Dodecahedral Sky Map → Calendar Projection

| Feld | Inhalt |
|---|---|
| Source | Dodecahedral Sky Map |
| Target | Calendar Projection |
| Shared Identity | Orientation Object, cell/landmark ID and cycle reference |
| Coordinate Change | diskrete polyhedrale Adresse → Zeitsegment oder Kalenderlabel |
| Invariant Fields | cell order if declared, source point reference, provenance |
| Derived Fields | period index, segment boundaries, calendar label |
| Lost Fields | intra-cell position, sphärische Distanz und nicht verwendete Polyederstruktur |
| Transformation Type | visualization-only addressed temporal projection |
| Candidate Mathematics | lookup `calendar_segment=L(cell_id)` oder `d=(d0+kΔ) mod P` |
| Required Parameters | cell ordering, lookup table, epoch, segment duration, boundary rule |
| Invertible? | partially bei bijektiver Lookup-Tabelle; sonst no |
| Evidence Status | `E0`; keine Cell-to-Time-Zuordnung verfügbar. |
| Open Questions | Wie werden 12 Faces, 20 Vertices oder 30 Edges auf Calendar Units abgebildet? |

## T15 — Calendar Projection → Orientation Layer

| Feld | Inhalt |
|---|---|
| Source | Calendar Projection |
| Target | Orientation Layer |
| Shared Identity | Orientation Object, calendar representation ID, epoch and cycle ID |
| Coordinate Change | domain-spezifische Kalenderzeit → normalisierte Orientation Coordinates |
| Invariant Fields | source identity, cyclic order, provenance, declared phase origin |
| Derived Fields | normalized phase `τ`, domain tag, comparable cycle position |
| Lost Fields | Calendar Labels, lokale Konventionen und Details, sofern nicht referenziert |
| Transformation Type | normalization layer |
| Candidate Mathematics | `τ=((t-t0) mod P)/P`, `0≤τ<1` |
| Required Parameters | epoch `t0`, period `P`, timezone/calendar profile, lossiness profile |
| Invertible? | partially mit vollständiger Source Reference und Parametern |
| Evidence Status | `E1`; Zielarchitektur plausibel, Orientation Contract fehlt. |
| Open Questions | Welche minimalen Felder gehören zur Orientation Layer? Wie bleibt Domainbedeutung erreichbar? |

## 2. Card-Abdeckung

| Graphkante | Card | Vollständig beschrieben |
|---|---|---|
| Reality → Observation | `T01` | ja |
| Observation → Planetary Chemistry | `T02` | ja |
| Observation → Lunar/Solar Dynamics | `T03` | ja |
| Planetary Chemistry → Scarabaeus Engine | `T04` | ja |
| Lunar/Solar Dynamics → Scarabaeus Engine | `T05` | ja |
| Scarabaeus Engine → Möbius Topology | `T06` | ja |
| Scarabaeus Engine → Frequency Space | `T07` | ja |
| Möbius Topology → Lissajous Geometry | `T08` | ja |
| Frequency Space → Lissajous Geometry | `T09` | ja |
| Lissajous Geometry → Frequency Space | `T10` | ja |
| Lissajous Geometry → Stellar Projection | `T11` | ja |
| Stellar Projection → Dodecahedral Sky Map | `T12` | ja |
| Stellar Projection → Calendar Projection | `T13` | ja |
| Dodecahedral Sky Map → Calendar Projection | `T14` | ja |
| Calendar Projection → Orientation Layer | `T15` | ja |

Keine zusätzliche Graphkante ist implizit autorisiert.
