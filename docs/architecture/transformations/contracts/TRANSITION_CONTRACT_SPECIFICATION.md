# TransitionContract Specification

- Status: Phase-3C-Architekturspezifikation
- Schema name: `orion.transition-contract`
- Schema version: `0.1-draft`
- Runtime status: nicht ausführbar; Phase 4A besitzt nur eine planning-only
  Metadatenprojektion dieses Katalogs
- Repository-Version: `0.3.0-dev.0`

## 1. Zweck

Ein `TransitionContract` macht eine Kante des Representation Graph zu einem
inspizierbaren, testbaren und unabhängig versionierten Architekturgegenstand. Er
beschreibt, wie eine Source Representation in eine Target Representation
überführt werden darf und welche Identität, Provenienz und Invarianten dabei
erhalten, abgeleitet, aggregiert, verborgen oder verloren werden.

Ein TransitionContract:

- implementiert keinen Operator;
- enthält keinen Renderer-Code;
- autorisiert keine Kernel-Mutation;
- ruft kein Modell und keinen Provider auf;
- ersetzt keine Evidenz durch Annahmen;
- markiert unbekannte Operatoren ausdrücklich als `unknown`.

Die Spezifikation ist provider-unabhängig. Zukünftige Renderer, Validatoren oder
Reasoning-Komponenten dürfen denselben Contract referenzieren, ohne dessen
Ownership oder Bedeutung zu verändern.

## 2. Beziehung zu bestehenden Contracts

Phase 3C ergänzt ausschließlich Architektur-Dokumentation. Folgende bestehende
Runtime-Verträge bleiben unverändert:

- `OrientationRequest`
- `ContextManifest`
- `ContextBrief`
- `ReasoningBackend`
- `ReasoningResult`
- `OrientationResponse`

`TransitionContract` wird in Phase 3C weder in `src/orion/contracts.py` noch als
öffentliches Schema implementiert. Eine spätere Runtime-Repräsentation benötigt
eine eigene Freigabe und gegebenenfalls eine ADR.

## 3. Normatives Contract-Modell

Jede Contract-Datei muss sieben normative Blöcke enthalten: Identifikation,
Input Contract, Output Contract, Transformation, Preserved Invariants,
Lossiness, Evidence und Validation. Die Blöcke müssen folgende Felder enthalten:

| Feld | Bedeutung | Regel |
|---|---|---|
| Contract ID | stabile Contract-Identität | entspricht registrierter Transition-ID `T01–T15` |
| Contract version | Version dieser Kantenbeschreibung | unabhängig von Source-, Target- und Renderer-Version |
| Status | `draft`, `specified`, `verifiable`, `executable`, `retired` | Phase 3C verwendet ausschließlich `draft` |
| Evidence level | `E0–E4` | darf vorhandene Evidenz nicht überschätzen |
| Operator status | `unknown`, `candidate`, `documented`, `verified` | `unknown` blockiert Ausführung |
| Input representation | erlaubter Source-Representation-Typ | muss zur Graphkante passen |
| Output representation | erlaubter Target-Representation-Typ | muss zur Graphkante passen |
| Input coordinate system | Koordinatenprofil der Source | `unknown` ist zulässig; keine implizite Wahl |
| Input units | Einheiten der Source-Felder | pro Feld oder ausdrücklich `unknown`/`not applicable` |
| Input epoch | Zeitreferenz der Source | `required`, `conditional`, `not applicable` oder `unknown` |
| Input representation version | Version des konkreten Source-Artefakts | zur Ausführung verpflichtend; Phase 3C registriert keine |
| Output coordinate profile | erwartetes Target-Koordinatenprofil | darf kein Renderer-Layout als Semantik ausgeben |
| Output renderer compatibility | Anforderungen an spätere Renderer | Contract-ID und -Version müssen unterstützt werden |
| Output representation version | Version des erzeugten Target-Artefakts | wird später vom Renderer gebunden; derzeit `unknown` |
| Shared identity | Bindung an dasselbe Orientation Object | Source und Target referenzieren dasselbe `O@V` |
| Required parameters | Parameter ohne Default, die für die Kante nötig sind | fehlender Wert macht Contract nicht ausführbar |
| Optional parameters | Parameter, deren Fehlen die Semantik nicht verändert | keine versteckten Defaults |
| Preconditions | Bedingungen vor einer Transformation | müssen extern prüfbar sein |
| Postconditions | Bedingungen am Zielartefakt | dürfen keine neue fachliche Wahrheit behaupten |
| Preserved invariants | unverändert weitergetragene Felder | mindestens Identity und Provenance |
| Visibility gained | im Ziel besser ablesbare Information | kein behaupteter Quellinformationsgewinn |
| Information hidden | weiterhin referenzierbar, aber nicht primär sichtbar | nicht mit `lost` verwechseln |
| Declared lossiness | aus dem Target allein nicht rekonstruierbare Information | erforderlich für jede nicht injektive Kante |
| Candidate mathematics | bereits in Phase 3B dokumentierter Kandidat | darf `unknown` sein; keine neue Formel |
| Invertibility | `yes`, `locally`, `partially`, `unknown`, `no` | gilt nur für deklarierte Felder und Parameter |
| Future renderer requirements | Voraussetzungen eines späteren Renderers | keine Implementierung in Phase 3C |
| Future validation tests | deklarative spätere Conformance-Prüfungen | keine Testimplementierung in Phase 3C |
| Missing evidence | für Spezifikation oder Ausführung fehlende Belege | darf nicht durch Annahmen ersetzt werden |
| Required datasets | minimal benötigte, versionierte Fixtures oder Crosswalks | `none identified` oder `unknown` ist zulässig |
| Failure conditions | Bedingungen für deterministisches Scheitern | unbekannte Operatoren und Pflichtparameter führen zum Abbruch |
| Open questions | blockierende Unklarheiten | bleiben explizit sichtbar |

## 4. Konzeptionelle Form

Die folgende Form ist eine Dokumentationsschablone, kein freigegebenes YAML-
Schema:

```yaml
contract_id: T00
contract_version: 0.1-draft
status: draft
evidence_level: E0
operator_status: unknown

input_representation:
  type: Source Representation
  version: required at execution time
  required_object: source representation instance
  mandatory_metadata: []
  coordinate_system: unknown
  units: unknown
  epoch: unknown

output_representation:
  type: Target Representation
  version: produced by renderer
  required_metadata: []
  coordinate_profile: unknown
  renderer_compatibility: contract-aware and provider-independent

identity_binding:
  rule: target.orientation_object_ref == source.orientation_object_ref

parameters:
  required: []
  optional: []

preconditions: []
postconditions: []
preserved_invariants: []
visibility_gained: []
information_hidden: []
declared_lossiness: []
candidate_mathematics: unknown
invertibility: unknown
future_renderer_requirements: []
future_validation_tests: []
missing_evidence: []
required_datasets: []
failure_conditions: []
open_questions: []
```

## 4.1 Normative Dokumentstruktur

Jede Datei `Txx.md` verwendet in dieser Reihenfolge:

1. Identifikationstabelle mit ID, Name, Source, Target, Contract-Version,
   Status, Evidenz, Operatorstatus und Invertibility;
2. `Input Contract`;
3. `Output Contract`;
4. `Transformation`;
5. `Preserved Invariants`;
6. `Lossiness`;
7. `Evidence`;
8. `Validation`.

Zusätzliche Erläuterungen sind zulässig, dürfen diese Felder aber nicht ersetzen.

## 5. Identity Binding

Jede Transformation muss konzeptionell folgende Gleichheit bewahren:

```text
target.orientation_object_id
  == source.orientation_object_id

target.orientation_object_version
  == source.orientation_object_version
```

Das Target erhält eine neue `representation_id`, aber keine neue
`orientation_object_id`. An den Merge Points Scarabaeus Engine (`T04`, `T05`)
und Lissajous Geometry (`T08`, `T09`) muss das gemeinsame Target alle tatsächlich
beteiligten Source Representation IDs referenzieren. Jede einzelne Kante behält
dennoch ihre eigene Contract-ID.

## 6. Provenienzpflicht

Ein später durch diesen Contract erzeugtes Target muss mindestens referenzieren:

```text
transition_contract_id
transition_contract_version
source_representation_ids
source_orientation_object_id
source_orientation_object_version
renderer_id
renderer_version
operator_id or explicit unknown marker
resolved required parameters
resolved optional parameters
lossiness declaration
evidence level used for execution
```

Phase 3C definiert diese Angaben nur architektonisch. Es wird kein
Provenienzschema implementiert.

## 7. Parameterregeln

1. Required Parameters besitzen keinen impliziten Default.
2. Ein unbekannter Required Parameter bleibt `unknown`; er wird nicht geschätzt.
3. Ein Optional Parameter darf nur fehlen, wenn die Contract-Semantik unverändert
   bleibt.
4. Einheit, Koordinatenrahmen, Epoche, Richtung und Sampling gehören zum Parameter,
   nicht in freie Rendererlogik.
5. Ein Parameterwechsel erzeugt eine neue Representation, aber nicht automatisch
   eine neue Contract-Version.
6. Eine semantische Änderung des Parameterprofils erfordert eine neue
   Contract-Version.

## 8. Operatorstatus

| Status | Bedeutung | Darf ausgeführt werden? |
|---|---|---|
| `unknown` | kein Operator dokumentiert | nein |
| `candidate` | Phase 3B nennt mögliche Mathematik, Parameter/Beleg fehlen | nein |
| `documented` | Operator und Parameterprofil vollständig spezifiziert | erst nach separater Implementierungsfreigabe |
| `verified` | Implementierung und Conformance nachgewiesen | ja, außerhalb Phase 3C |

Ein bekannter mathematischer Name wie Fourier, Möbius oder stereographisch reicht
nicht für `documented`. Source Field Mapping, Parameter und Lossiness müssen
ebenfalls festgelegt sein.

## 9. Evidence Level und Contract Status

Evidence Level und Contract Status sind getrennt:

- Evidence beschreibt, wie gut der konkrete Übergang im vorhandenen Material
  belegt ist.
- Status beschreibt, wie vollständig und prüfbar der Contract formuliert ist.

Ein Contract kann sauber als `draft` dokumentiert sein und trotzdem nur `E0`
besitzen. Er darf dadurch nicht ausgeführt werden.

Mindestbedingungen für spätere Status:

| Status | Mindestbedingung |
|---|---|
| `draft` | Source, Target, offene Felder und Lossiness benannt |
| `specified` | Operator, Parameter, Preconditions und Postconditions vollständig |
| `verifiable` | konkrete Validation Tests und Fixtures definiert |
| `executable` | Renderer implementiert, Evidence mindestens `E3`, Tests bestanden |
| `retired` | ersetzt oder nicht mehr zulässig; Historie bleibt erhalten |

## 10. Lossiness-Modell

Jedes relevante Feld erhält später einen der Status:

```text
preserved
derived
aggregated
hidden
lost
unknown
```

- `hidden` bedeutet: über Provenienz oder Source Reference weiterhin erreichbar.
- `lost` bedeutet: aus dem Target allein nicht rekonstruierbar.
- `aggregated` bedeutet: mehrere Source-Werte bestimmen einen Target-Wert.
- `unknown` blockiert jede Behauptung von Äquivalenz.

## 11. Renderer-Anforderungen

Ein zukünftiger Renderer, der einen TransitionContract ausführt, muss:

1. exakt eine unterstützte Contract-ID und -Version deklarieren;
2. Source-Typ und Source-Version vor Ausführung prüfen lassen;
3. alle Required Parameters explizit erhalten;
4. deterministisch und read-only sein;
5. Target Identity und vollständige Provenienz erzeugen;
6. deklarierte Lossiness nicht verschweigen;
7. keine unbekannten Felder inferieren;
8. keine Validation oder Kernel-Entscheidung übernehmen.

## 12. Future Validation Test Classes

Die Contract-Dateien dürfen folgende spätere Testklassen verlangen:

| Testklasse | Prüft |
|---|---|
| identity binding | Source und Target referenzieren dasselbe `O@V` |
| provenance completeness | Contract, Renderer, Sources und Parameter sind referenziert |
| deterministic equality | gleiche freigegebene Eingaben erzeugen dasselbe Target |
| invariant preservation | als preserved deklarierte Felder stimmen überein |
| lossiness honesty | verlorene Felder werden nicht als rekonstruierbar behauptet |
| parameter completeness | kein Required Parameter fehlt oder verwendet einen Hidden Default |
| coordinate conformance | Target erfüllt das deklarierte Coordinate Profile |
| round-trip profile | nur deklarierte invertierbare Felder kehren zurück |
| boundary behavior | Seam, Pole, Zellen- und Calendar-Grenzen sind deterministisch |

## 13. Contract-Katalog

| Contract | Transition | Evidence | Operator |
|---|---|---|---|
| [`T01`](T01.md) | Reality → Observation | `E1` | unknown |
| [`T02`](T02.md) | Observation → Planetary Chemistry | `E0` | unknown |
| [`T03`](T03.md) | Observation → Lunar/Solar Dynamics | `E0–E1` | candidate |
| [`T04`](T04.md) | Planetary Chemistry → Scarabaeus Engine | `E0` | unknown |
| [`T05`](T05.md) | Lunar/Solar Dynamics → Scarabaeus Engine | `E0` | unknown |
| [`T06`](T06.md) | Scarabaeus Engine → Möbius Topology | `E0–E1` | candidate |
| [`T07`](T07.md) | Scarabaeus Engine → Frequency Space | `E1` | candidate |
| [`T08`](T08.md) | Möbius Topology → Lissajous Geometry | `E0` | unknown |
| [`T09`](T09.md) | Frequency Space → Lissajous Geometry | `E1` | candidate |
| [`T10`](T10.md) | Lissajous Geometry → Frequency Space | `E1` | candidate |
| [`T11`](T11.md) | Lissajous Geometry → Stellar Projection | `E0` | unknown |
| [`T12`](T12.md) | Stellar Projection → Dodecahedral Sky Map | `E0–E1` | candidate |
| [`T13`](T13.md) | Stellar Projection → Calendar Projection | `E0–E1` | candidate |
| [`T14`](T14.md) | Dodecahedral Sky Map → Calendar Projection | `E0` | unknown |
| [`T15`](T15.md) | Calendar Projection → Orientation Layer | `E1` | candidate |

## 14. Phase-3C-Grenzen

Nicht enthalten sind:

- Runtime- oder Schemaimplementierung;
- Renderer, Validatoren oder Testcode;
- neue Mathematik oder neue Operatoren;
- Kernel-, Library- oder Builder-Hub-Änderungen;
- semantisches Retrieval, Embeddings oder Vector Databases;
- LLM-, Ollama- oder Providerintegration;
- automatische Evidence-Upgrades.

Phase 3C endet mit versionierten, inspizierbaren Contract-Dokumenten. Kein
Contract dieses Katalogs ist bereits ausführbar.
