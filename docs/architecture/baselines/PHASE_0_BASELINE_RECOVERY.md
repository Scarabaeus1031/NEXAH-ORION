# NEXAH ORION — Phase 0 Baseline Recovery

Status: Baseline Recovery Map
Datum: 19. Juli 2026
Scope: Zuordnung des realen eingefrorenen NEXAH-Repositories zur beschlossenen ORION-Architektur
Keine Implementierungsfreigabe

---

## 0. Ergebnis in einem Satz

Der eingefrorene NEXAH-Stand bleibt vollständig und unverändert als autoritative Baseline erhalten; ORION entsteht als neues Repository oberhalb seiner publizierten Verträge, während Library und Builder Hub unabhängige Ownership-Grenzen behalten.

Es wird in Phase 0 kein bestehendes Modul umbenannt, herausgelöst oder gelöscht.

## 0.1 Verbindliche Klassifikation

Jede Empfehlung in diesem Dokument verwendet genau eine der vereinbarten Klassen:

| Klasse | Bedeutung in Phase 0 |
|---|---|
| **KEEP** | Bestand, Pfad, Verantwortung und Status bleiben unverändert. |
| **MOVE** | Ein noch nicht eingefrorenes Artefakt wechselt in sein künftiges Owner-Repository. Kein bestehender Freeze-Inhalt wird ohne gesonderte Entscheidung verschoben. |
| **SPLIT** | Eine heute gemeinsam dargestellte Verantwortung erhält für künftige Arbeit getrennte Owner. Der bestehende Freeze bleibt physisch intakt. |
| **MERGE** | Doppelte aktive Arbeitskopien werden in einer verantwortlichen Arbeitslinie zusammengeführt; eingefrorene Historie bleibt erhalten. |
| **POSTPONE** | Entscheidung oder Umsetzung wird bewusst bis zu einem benannten Gate vertagt. |
| **REMOVE** | Etwas wird aus der aktiven Workspace-Navigation oder aus einem neuen Repository ausgeschlossen. Es bedeutet nicht automatisch Dateilöschung. |

## 0.2 Nicht verhandelbare Annahmen

- **KEEP** — Der NEXAH Core bleibt eingefroren.
- **KEEP** — ORION wird ein neues Repository.
- **KEEP** — Library bleibt eine unabhängige Verantwortung und ein unabhängiger Entwicklungsbereich.
- **KEEP** — Builder Hub bleibt eine unabhängige Anwendung.
- **KEEP** — Bestehende Modulnamen und öffentlichen Bedeutungen werden nicht umgedeutet.
- **POSTPONE** — Implementierung beginnt erst nach bestätigter Ownership und bestätigten Integrationsports.

---

# 1. Current Repository Inventory

## 1.1 Autoritative Baseline

| Feld | Befund | Klassifikation |
|---|---|---|
| Pfad | `<local-workspace>/repositories/NEXAH` | **KEEP** |
| Remote | `https://github.com/Scarabaeus1031/NEXAH.git` | **KEEP** |
| Branch | `main` | **KEEP** |
| Commit | `9f79bb06210402c40c9ef7d9937ca00d86c092b1` | **KEEP** |
| Commit-Datum | 2026-07-19 17:37:49 +02:00 | **KEEP** |
| Commit-Titel | `Complete Are.na editorial Batch 1 and freeze verified state` | **KEEP** |
| Working Tree | sauber; `main` entspricht `origin/main` | **KEEP** |
| Package | `nexah` 0.7.0, Python ≥ 3.10 | **KEEP** |
| Tracked Files | 8.786 | **KEEP** |
| CI | Python 3.10/3.11/3.12 Smoke; Python 3.12 Test Suite | **KEEP** |

Dieser Commit ist die einzige Baseline für die Migration Map. Spätere Vergleiche referenzieren immer den vollständigen Hash, nicht nur einen Ordnernamen oder den Begriff „Core“.

## 1.2 Primäre Subsysteme im Freeze

| Aktueller Bereich | Dateien | Aktuelle Verantwortung | Autorität | Disposition |
|---|---:|---|---|---|
| `RESEARCH/` | 1.279 | Hypothesen, Experimente, Evidenz, Findings | Evidenz innerhalb lokal deklarierter Grenzen | **KEEP** |
| `ORIENTATION_LANGUAGE/` | 66 | OLS-Spezifikation, Semantik, Conformance, Releases | OLS-Release 1.0.0 ist semantische Autorität | **KEEP** |
| `nexah/` | 70 | installierbare deterministische Implementierung und CLI | Verhalten der Version 0.7 innerhalb dokumentierter Grenzen | **KEEP** |
| `APPLICATIONS/` | 3.704 | Domänenanwendungen und Validierung | Domänenspezifische Realisierung, keine universelle Semantik | **KEEP** |
| `LIBRARY/` | 75 | Registry, Works, Editionen, Reader Journeys, Review | Registry-Identität und kuratierte Library-Entscheidungen | **KEEP** |
| `EDITORIAL_OPERATING_SYSTEM/` | 96 | Review, Erklärung, Governance, kontrollierte Ausführung | menschlich regierte redaktionelle Prozesse | **KEEP** |

Die sechs Bereiche bleiben koordinierte Verantwortungen. ORION wird weder ein siebtes Subsystem innerhalb dieses Freeze-Commits noch ein neuer Ordner in diesem Repository.

## 1.3 Unterstützende Bereiche

| Aktueller Bereich | Dateien | Funktion | Disposition |
|---|---:|---|---|
| `ARCHITECTURE/` | 142 | Beziehungen, System State, Methoden, historische und aktuelle Architektur | **KEEP** als Freeze-Dokumentation |
| `GOVERNANCE/` | 12 | provisorische, nicht-kanonische Verfassungsreview | **KEEP** |
| `PROTO_CORE/` | 657 | Demonstrator, Field Layer, historische Implementierungslinien | **KEEP** |
| `EXPERIMENTAL/` | 2.547 | aktive Labs, Prototypen und Archive | **KEEP**; keine ORION-Promotion in Phase 0 |
| `validation/` | 52 | reproduzierbare Kampagnen und kanonische Resultate | **KEEP** |
| `tests/` | 52 | automatisierte Repository- und Package-Verifikation | **KEEP** |
| `testkit/` | 11 | Evidence- und Outcome-Gates | **KEEP** |
| `assets/` | 7 | gepflegte öffentliche Dokumentationsvisuals | **KEEP** |

## 1.4 Implementierter Package-Bestand

| Package-Bereich | Python-Dateien | Tatsächliche Rolle | Disposition |
|---|---:|---|---|
| `nexah/core.py` | 1 | eingefrorene v0.7 State-Space- und Trajektorienanalyse | **KEEP** |
| `nexah/orientation/` | 11 | typisierte Primitives, Evidence, State, Report, Brief, Memory, Probes und Outcome Firewall | **KEEP** |
| `nexah/sources/` | 6 | Array-, Table-, Graph- und IEEE-Source-Adapter | **KEEP** |
| `nexah/backends/` | 4 | deterministische Representation Backends und v0.7-Adapter | **KEEP** |
| `nexah/applications/` | 4 | Network-Orientation-Anwendung und Probes | **KEEP** |
| `nexah/power_systems/` | 8 | IEEE Geometry, Manifest, Operators, Probes und Orientation | **KEEP** |
| `nexah/library/` | 18 | Registry-Zugriff, Queries, Health, Snapshot, Diff, Release und guarded Writer | **KEEP** im Freeze; zukünftige Ownership siehe Abschnitt 3 |
| `nexah/living_concepts/` | 5 | read-only Concept Overlay und Answer Adapter | **KEEP** im Freeze |
| `nexah/cli.py` | 1 | gemeinsame CLI über vorhandene Package-Fähigkeiten | **KEEP** |

Wichtige Namensgrenze:

- `nexah/backends/` meint **Representation Backends**, nicht LLM-/Reasoning-Backends.
- `nexah/orientation/` meint die bestehende deterministische Orientation Layer und ihre Verträge, nicht das neue ORION-Repository.
- `nexah/library/kernel.py` meint abgeleitete Library Queries, nicht den gesamten NEXAH Kernel.

Diese Namen werden im Freeze nicht geändert.

## 1.5 Verifikation und Release-Evidenz

| Evidenz | Befund | Disposition |
|---|---|---|
| Testquellen | 201 explizite `test_*`-Funktionen; Parametrisierung erzeugt zusätzliche Testfälle | **KEEP** |
| dokumentierter X2-Checkpoint | 288 Tests bestanden am 16. Juli 2026 | **KEEP** als datierter Record |
| CI-Konfiguration | vollständige `pytest -q` Suite auf Python 3.12 | **KEEP** |
| Batch 1 | am 19. Juli 2026 angewendet und verifiziert | **KEEP** |
| Batch-1-Health | `pass_with_editorial_warnings`; keine Errors | **KEEP** |
| Traversability | 1/15 → 3/15 direkt begehbar | **KEEP** als datierter Library-Befund |
| aktueller Freeze | Commit und Working Tree verifiziert | **KEEP** |

Die Suite konnte in diesem Phase-0-Workspace nicht erneut ausgeführt werden, weil in den verfügbaren Python-Runtimes `pytest` nicht installiert ist. Es wurden keine Dependencies installiert und der Freeze wurde nicht verändert. Die Testaussage bleibt daher ein Repository-Record, kein neu erzeugter Lauf.

## 1.6 Andere lokale Arbeitskopien

| Pfad | Befund | Disposition |
|---|---|---|
| `<legacy-workspace>/NEXAH_REPO_CLONE` | Stand März 2026; lokale Löschung; nicht aktuell | **REMOVE** aus aktiver Baseline-Navigation; als historische Kopie nicht löschen |
| `<local-research>/ARE.NA LIBRARY CLEANUP` | Git ohne Commit, umfangreicher ungetrackter Library-Workbench-Stand | **POSTPONE** bis Provenance-/Abgleichreview; nicht als Library-Repository deklarieren |
| `<historical-workspace>/NEXAH-CODEX` | historischer separater Bestand; im Core selbst als frozen historical archive zitiert | **KEEP** als historische Referenz, **REMOVE** aus aktiver Entwicklung |
| `<orion-workspace>` | Übergangsworkspace mit Architekturreview, ORION-Architektur und visueller Evidenz | **MOVE** in das neue ORION-Repository beziehungsweise den Architektur-Workspace |
| Builder-Hub-Visualordner | visuelle Quell- und Entwicklungsmaterialien; kein verifiziertes eigenständiges Git-Repository gefunden | **POSTPONE** bis der autoritative Builder-Hub-Repository-Pfad bestätigt ist |

---

# 2. Repository Responsibility Matrix

## 2.1 Current → Target

| Verantwortung | Current Owner | Target Owner | Zugriff von ORION | Disposition |
|---|---|---|---|---|
| publizierte Semantik und Conformance | `ORIENTATION_LANGUAGE/` im Freeze | NEXAH Core/OLS Release bleibt autoritativ | lesen über versionierte Release-Referenz | **KEEP** |
| deterministische Kernel-Berechnung | `nexah/core.py` | NEXAH Core | aufrufen über stabilen Port/Adapter | **KEEP** |
| Orientation Primitives und Evidenztypen | `nexah/orientation/` | NEXAH Core | konsumieren; nicht duplizieren | **KEEP** |
| Representation Backends | `nexah/backends/` | NEXAH Core | als deterministische Werkzeuge konsumieren | **KEEP** |
| Source Adapters | `nexah/sources/` | NEXAH Core | nur über deklarierte Inputs/Outputs | **KEEP** |
| Domain Applications | `APPLICATIONS/`, `nexah/applications/`, `nexah/power_systems/` | bestehende Application Owner; Builder Hub separat | ORION darf Requests bedienen, übernimmt aber keine Domänenautorität | **KEEP** |
| Library Identity und kuratierte Inhalte | `LIBRARY/` | unabhängige Library | read-only Context-/Query-Port | **SPLIT** physische Zukunftsownership vom Freeze; Freeze bleibt unverändert |
| Library Runtime Operations | `nexah/library/` | unabhängige Library für neue Entwicklung | Adapter, niemals direkter Dateizugriff als Dauervertrag | **SPLIT** |
| Living Concepts/Knowledge Contracts | EOS + `nexah/living_concepts/` | Library/EOS-Governance | read-only Contextquelle | **KEEP** im Freeze; zukünftige Entwicklung beim Library/EOS-Owner |
| Human Editorial Governance | `EDITORIAL_OPERATING_SYSTEM/` | Library/EOS und Builder-Flows | ORION respektiert Approval- und Effect-Policy | **KEEP** |
| Research und Findings | `RESEARCH/` | NEXAH Research | nur referenzierte Evidenz; keine automatische Promotion | **KEEP** |
| Validation und Testkits | `validation/`, `tests/`, `testkit/` | jeweiliger Current Owner | Referenz für ORION-Conformance; keine Ownership-Übernahme | **KEEP** |
| Request Lifecycle und Run State | nicht als modellgestütztes System vorhanden | neues ORION-Repository | eigener Owner | **SPLIT** aus dem früher breit verwendeten Begriff „Orientation Core“ |
| Context Planning und Context Manifest | nicht implementiert | neues ORION-Repository | eigener Owner | **SPLIT** |
| Reasoning Backend Routing | nicht implementiert | neues ORION-Repository | eigener Owner | **SPLIT** |
| LLM-/Model-Adapter | nicht vorhanden | neues ORION-Repository | eigener Owner | **POSTPONE** bis Ports beschlossen sind |
| Result Validation vor Kernel Commands | partiell über bestehende Contracts/Firewalls | ORION orchestriert; Kernel bleibt finaler Validator | gemeinsame Grenze, getrennte Autorität | **SPLIT** |
| Builder UI und Operator Workflow | kein autoritatives Builder-Hub-Repo im untersuchten Bestand | unabhängiger Builder Hub | ORION-Client | **POSTPONE** bis Repo-Identität bestätigt ist |

## 2.2 Autoritätsregeln zwischen Repositories

| Regel | Klassifikation |
|---|---|
| NEXAH Core importiert ORION nicht. | **KEEP** |
| ORION verändert keine Dateien im eingefrorenen NEXAH-Repository. | **KEEP** |
| ORION behandelt OLS-Dokumente und Core-Verträge als versionierte externe Authority. | **KEEP** |
| ORION erhält keine semantische Autorität durch die Fähigkeit, Modelle aufzurufen. | **KEEP** |
| Library-Inhalte werden nicht in ORION kopiert, um eine lokale Schatten-Library zu erzeugen. | **KEEP** |
| Builder Hub spricht mit ORION über versionierte Request-/Result-Verträge. | **POSTPONE** bis Contract Ownership beschlossen ist |
| Provider-SDKs und Modellnamen erscheinen nur im zukünftigen ORION-Adapterbereich. | **POSTPONE** bis Implementierungsphase |

---

# 3. Module Ownership Matrix

## 3.1 Deterministischer Core

| Aktuelles Modul | Current Ownership | Target Ownership | ORION-Beziehung | Disposition |
|---|---|---|---|---|
| `nexah/core.py` | Implementation / v0.7 Baseline | Core | deterministisches Tool hinter Core Port | **KEEP** |
| `nexah/orientation/base.py` | Contract-Infrastruktur | Core | kompatible Serialisierung konsumieren | **KEEP** |
| `nexah/orientation/primitives.py` | operative Grundtypen | Core | referenzieren, nicht neu definieren | **KEEP** |
| `nexah/orientation/evidence.py` | Provenance, Evidence, Uncertainty | Core | ORION-Claims müssen darauf abbildbar sein | **KEEP** |
| `nexah/orientation/state.py` | `OrientationState` | Core | möglicher deterministischer Input-Snapshot | **KEEP** |
| `nexah/orientation/report.py` | `OrientationReport` | Core | geprüfte Core-Ausgabe als Context/Result-Bestandteil | **KEEP** |
| `nexah/orientation/generator.py` | deterministische Report-Erzeugung | Core | nicht durch LLM-Generator ersetzen | **KEEP** |
| `nexah/orientation/brief.py` | backendunabhängiger Orientation Brief | Core | ORION darf ihn referenzieren oder als Evidenz einbetten | **KEEP** |
| `nexah/orientation/probes.py` | read-only Perspektiven und Synthese | Core | deterministische Review-Perspektiven nutzbar | **KEEP** |
| `nexah/orientation/outcome_firewall.py` | Evidence-/Outcome-Gate | Core | ORION kann keine Umgehung autorisieren | **KEEP** |
| `nexah/orientation/memory.py` | append-only Episoden und Retrieval | Core | Core-Episoden sind Contextquelle, nicht ORION-Run-Memory | **SPLIT** der künftigen Memory-Verantwortung |

### Memory-Split ohne Codebewegung

| Verantwortung | Owner | Disposition |
|---|---|---|
| State–Report–Outcome Episodes und bestehende Similarity | Core | **KEEP** |
| ORION Run Records, Context Manifests, Modellmetadaten und Replay | ORION | **SPLIT** |
| Modelltraining oder Policy Learning | niemand in Phase 0 | **POSTPONE** |

## 3.2 Adapter und Representation

| Aktuelles Modul | Current Ownership | Target Ownership | ORION-Beziehung | Disposition |
|---|---|---|---|---|
| `nexah/sources/base.py` | Source Contract | Core | deklarierte Source-Batches verwenden | **KEEP** |
| `nexah/sources/{array,table,graph,ieee}.py` | Source Adapter | Core/Application Boundary | keine Verschiebung | **KEEP** |
| `nexah/backends/base.py` | Representation-Backend-Vertrag | Core | nicht als ReasoningBackend umdeuten | **KEEP** |
| `nexah/backends/v07.py` | v0.7 → OrientationState | Core | möglicher Core Adapter | **KEEP** |
| `nexah/backends/graph.py` | Graph Representation Backend | Core | deterministische Graphanalyse | **KEEP** |
| zukünftige Reasoning Backend Ports | nicht vorhanden | ORION | neuer Vertrag nach Ownership-Freigabe | **POSTPONE** |

Der neue ORION-Code muss eine eindeutig getrennte Namespace-Grenze für Modelladapter verwenden. Das ist keine Umbenennung von `nexah/backends`; es verhindert lediglich eine neue Namenskollision.

## 3.3 Applications und Domain Code

| Aktuelles Modul | Current Ownership | Target Ownership | Disposition |
|---|---|---|---|
| `nexah/applications/network_orientation.py` | Applications | Applications im Freeze | **KEEP** |
| `nexah/applications/network_probes.py` | Applications/Validation | Applications im Freeze | **KEEP** |
| `nexah/applications/network_brief.py` | Applications | Applications im Freeze | **KEEP** |
| `nexah/power_systems/*` | Power Systems Application | Applications im Freeze | **KEEP** |
| `APPLICATIONS/orientation_translation/` | Applications mit methodischer Evidenz | Applications | **KEEP**; nicht zu ORION verschieben |
| Builder Hub | externer/noch zu bestätigender Application Owner | unabhängiger Builder Hub | **POSTPONE** bis Repository identifiziert ist |

## 3.4 Library und Editorial Code

| Aktuelles Modul | Current Ownership | Target Ownership | Disposition |
|---|---|---|---|
| `LIBRARY/registry/` | Canonical Library Registry | unabhängige Library | **SPLIT** zukünftige Entwicklung; Freeze-Kopie bleibt |
| `LIBRARY/review/` | Library Review und Operations Evidence | unabhängige Library | **SPLIT** |
| `nexah/library/registry.py` | Registry Loader/Validator | Library Implementation | **SPLIT** |
| `nexah/library/kernel.py` | abgeleitete Paths/Queries/Recommendations | Library Implementation | **SPLIT**; nicht ORION |
| `nexah/library/arena.py` | read-only Connector | Library Integration | **SPLIT** |
| `nexah/library/editorial_writer.py` | approval-gated Public Writer | Library Execution | **SPLIT**; ausdrücklich nicht ORION |
| `nexah/library/{health,release,snapshot,editorial,...}.py` | Library Operations | Library | **SPLIT** |
| `nexah/living_concepts/*` | Editorial Explanation Layer | Library/EOS | **KEEP** im Freeze, künftige Ownership Library/EOS |
| `EDITORIAL_OPERATING_SYSTEM/*` | Governance und kontrollierte Ausführung | unabhängige Editorial/Library Governance | **KEEP** im Freeze |

`SPLIT` bedeutet hier: Neue Library-Arbeit erhält einen unabhängigen Owner. Es bedeutet nicht, dass Phase 0 Dateien aus dem Freeze entfernt oder kopiert.

## 3.5 Tests und Evidenz

| Aktueller Bereich | Owner | ORION-Verwendung | Disposition |
|---|---|---|---|
| `tests/contracts/` | Core | Compatibility-Referenz | **KEEP** |
| `tests/backends/` | Core | Representation-Conformance-Referenz | **KEEP** |
| `tests/sources/` | Core | Source-Boundary-Referenz | **KEEP** |
| `tests/applications/` | Applications | keine ORION-Ownership | **KEEP** |
| `tests/power_systems/` | Applications | keine ORION-Ownership | **KEEP** |
| `tests/library/` | Library | spätere Library-Port-Fixtures separat ableiten | **KEEP** |
| `tests/living_concepts/` | EOS/Library | read-only Contract-Referenz | **KEEP** |
| `validation/` | Implementation/Application Evidence | Golden-Source referenzieren, nicht übernehmen | **KEEP** |
| `testkit/observed_evidence/` | Cross-cutting Evidence Gate | Policy-/Acceptance-Referenz | **KEEP** |
| zukünftige ORION Contract-/Conformance-Tests | ORION | eigener Testbestand | **POSTPONE** bis Verträge beschlossen sind |

---

# 4. Workspace Structure

## 4.1 Ist-Zustand

Aktuelle NEXAH-Arbeit war zum Zeitpunkt der Erhebung über mehrere lokale Pfade verteilt. Nur der als `<local-workspace>/repositories/NEXAH` bezeichnete Checkout ist als aktuelle, saubere Freeze-Baseline verifiziert. Der damalige ORION-Workspace war noch kein Commit-basiertes Projekt.

## 4.2 Ziel-Workspace

```text
NEXAH_WORKSPACE/
├── 00_INBOX/
│   └── unreviewed/                         # niemals autoritativ
├── 10_ARCHITECTURE/
│   ├── baselines/
│   │   └── NEXAH-9f79bb06.yaml            # Hash, Remote, Status, Owner
│   ├── reviews/
│   └── visual_evidence/
├── 20_REPOSITORIES/
│   ├── NEXAH/                              # read-only/frozen working policy
│   ├── nexah-orion/                        # neues Repository
│   ├── nexah-library/                      # unabhängiger Owner, wenn bestätigt
│   └── nexah-builder-hub/                  # unabhängiger Owner, wenn bestätigt
├── 30_LIBRARY_WORKBENCH/
│   ├── incoming/
│   ├── reconciliation/
│   └── publication_queue/
├── 40_RESEARCH_LOCAL/
├── 50_EXPERIMENTS/
│   ├── orion-context/
│   └── backend-evaluations/
├── 60_RUNS_LOCAL/
│   ├── manifests/
│   ├── outputs/
│   └── evaluations/
├── 70_REVIEWS/
├── 80_RELEASES/
└── 90_ARCHIVE/
    ├── repository-clones/
    └── visual-lineage/
```

## 4.3 Workspace-Migration

| Empfehlung | Klassifikation |
|---|---|
| Den Freeze-Hash in einem Workspace-Baseline-Manifest festhalten. | **KEEP** |
| Den verifizierten Checkout `<local-workspace>/repositories/NEXAH` zunächst an seinem sicheren Ort belassen und im Workspace referenzieren. | **KEEP** |
| Den älteren `NEXAH_REPO_CLONE` aus allen aktiven Such- und Entwicklungswegen entfernen. | **REMOVE** |
| `NEXAH_REASONING_ARCHITECTURE_REVIEW.md`, `ORION_ARCHITECTURE.md` und dieses Dokument in `nexah-orion/docs/architecture/` überführen. | **MOVE** |
| Die sechs neueingebrachten Poster als Visual Evidence katalogisieren, nicht als Specification kopieren. | **MOVE** nach `10_ARCHITECTURE/visual_evidence` oder ORION-Docs-Referenz, abhängig von Rechten |
| Builder-Hub-Construction-PNGs vor einer Repository-Aufnahme auf Quelle, Rechte, Version und Dubletten prüfen. | **POSTPONE** |
| Den uncommitted `ARE.NA LIBRARY CLEANUP`-Workbench mit dem Freeze commitweise/inhaltlich abgleichen. | **POSTPONE** |
| Nach erfolgreichem Abgleich nicht-kanonische Dubletten aus der aktiven Navigation ausschließen. | **MERGE** in eine dokumentierte Library-Workbench-Linie; keine automatische Dateimischung |
| Caches, `__pycache__`, `.pytest_cache`, `.mypy_cache`, `*.egg-info`, lokale Outputs und Modellgewichte nicht in neue Repositories übernehmen. | **REMOVE** aus Migrationsumfang |

Keine dieser Empfehlungen autorisiert eine Dateiverschiebung in Phase 0. Sie definiert nur die Zielplätze und Owner.

---

# 5. Repository Map

## 5.1 Current State

```text
<local-workspace>/repositories/NEXAH @ 9f79bb06
│
├── RESEARCH                         evidence authority
├── ORIENTATION_LANGUAGE             semantic authority
├── nexah                            deterministic implementation
│   ├── core                         frozen v0.7 analysis
│   ├── orientation                  typed orientation contracts
│   ├── sources                      source adapters
│   ├── backends                     representation backends
│   ├── applications                 maintained network application
│   ├── power_systems                IEEE application implementation
│   ├── library                      Library runtime operations
│   └── living_concepts              read-only explanation pilot
├── APPLICATIONS                     domain/application authority
├── LIBRARY                          identity and editorial records
├── EDITORIAL_OPERATING_SYSTEM       human governance/execution
├── ARCHITECTURE                     current-state description
├── PROTO_CORE                       reference and lineage
├── EXPERIMENTAL                     labs and archives
├── validation                       reproducible campaigns
├── tests                            repository verification
└── testkit                          evidence admission gates
```

## 5.2 Target State

```text
NEXAH WORKSPACE
│
├── NEXAH CORE REPOSITORY @ frozen hash
│   ├── six existing subsystem responsibilities
│   ├── deterministic `nexah` package
│   ├── OLS authority
│   ├── existing evidence and validation
│   └── historical Library/EOS snapshot retained intact
│
├── NEXAH ORION REPOSITORY
│   ├── architecture and ADRs
│   ├── OrientationRequest / Run ownership
│   ├── Context planning / manifest ownership
│   ├── reasoning backend boundary
│   ├── result validation / audit / replay
│   └── adapters to versioned Core, Library and model interfaces
│
├── NEXAH LIBRARY REPOSITORY
│   ├── Registry and editorial identity
│   ├── Works, Editions, Reader Journeys
│   ├── Library operations and guarded execution
│   └── knowledge contracts and publication governance
│
└── NEXAH BUILDER HUB REPOSITORY
    ├── Operator-facing application
    ├── request construction
    ├── context/result/diff inspection
    └── approval interaction
```

## 5.3 Erlaubte Abhängigkeiten

```text
Builder Hub ───────────────► ORION public contracts
ORION ─────────────────────► Core public contracts/ports
ORION ─────────────────────► Library read/query contracts
ORION ─────────────────────► external model runtimes through adapters
Library ───────────────────► Core contracts only where already governed

Core ───────────────X──────► ORION
Core ───────────────X──────► model/provider SDKs
Library ────────────X──────► ORION internals
Builder Hub ────────X──────► Core private modules
Models ─────────────X──────► direct Kernel or Library mutation
```

Alle Pfeile sind Ownership- und Vertragsrichtungen, keine Implementierungsfreigabe.

## 5.4 Konkrete Integrationskandidaten aus dem Freeze

Diese Kandidaten werden inventarisiert, aber noch nicht als öffentliche Ports beschlossen:

| Freeze-Artefakt | Mögliche Target-Nutzung | Disposition |
|---|---|---|
| `OrientationState` | Core Snapshot für ORION Context | **KEEP** als Kandidat; Port-Entscheidung **POSTPONE** |
| `OrientationReport` | deterministische Core-Ausgabe | **KEEP** als Kandidat |
| `OrientationBrief` | evidenzgebundenes menschliches Artefakt | **KEEP** als Kandidat |
| `Evidence`, `Provenance`, `Uncertainty` | gemeinsame Claim-/Evidence-Abbildung | **KEEP**; Cross-Repo-Schemaentscheidung **POSTPONE** |
| `SourceBatch` | strukturierter Input zu deterministischen Backends | **KEEP** |
| `BackendResult` | interne Representation-Backend-Grenze | **KEEP**; nicht als ORION Result verwenden |
| `OutcomeFirewall` | bestehende Outcome-Admission-Policy | **KEEP** |
| `ConceptAnswerAdapter` | read-only Library Contextquelle | **KEEP**; externer Port **POSTPONE** |
| `OrientationQueries` | read-only Library Queryquelle | **KEEP**; externer Port **POSTPONE** |

---

# 6. Migration Steps

## Step 0 — Freeze Identity Record

- **KEEP** — Baseline auf Commit `9f79bb06210402c40c9ef7d9937ca00d86c092b1` festlegen.
- **KEEP** — Remote, Branch, Package-Version und Working-Tree-Status dokumentieren.
- **POSTPONE** — Tagging oder Release-Erstellung, bis bestätigt ist, ob bereits ein offizieller Freeze-Tag existiert.

**Gate:** Jede spätere Map nennt Hash und Repository, nicht nur „NEXAH Core“.

## Step 1 — Ownership Registry

- **KEEP** — die sechs bestehenden Subsystem-Owner unverändert übernehmen.
- **SPLIT** — neue ORION-Verantwortungen separat registrieren: Runs, Context, Reasoning Backends, Result Validation, Audit/Replay.
- **SPLIT** — zukünftige Library-Entwicklung vom eingefrorenen Monorepo-Snapshot unterscheiden.
- **POSTPONE** — Builder-Hub-Owner und Repository-URL bestätigen.

**Gate:** Jedes Modul und jedes neue Artefakt besitzt genau einen verantwortlichen Repository-Owner.

## Step 2 — Clean Workspace Manifest

- **MOVE** — die drei ORION-Architekturdokumente in die zukünftige ORION-Dokumentationsstruktur.
- **REMOVE** — historische Clones, Caches und unreviewed Outputs aus aktiven Suchpfaden.
- **KEEP** — historische Bestände in `90_ARCHIVE` oder an ihren vorhandenen sicheren Pfaden; nichts löschen.
- **POSTPONE** — physisches Verschieben bestehender Git-Repositories, bis Remotes, Worktrees und Backups geprüft sind.

**Gate:** `20_REPOSITORIES` verweist pro Verantwortung auf genau eine aktive Arbeitskopie.

## Step 3 — Create ORION Repository Boundary

- **MOVE** — `ORION_ARCHITECTURE.md`, Review und Baseline Recovery als erste normative Dokumentation übernehmen.
- **KEEP** — NEXAH Core als externe eingefrorene Dependency behandeln.
- **POSTPONE** — `src/`, Provider-SDKs, Runtime-Code und Schemas.
- **POSTPONE** — endgültige Programmiersprache und Packaging.

**Gate:** ORION kann als Repository beschrieben werden, ohne eine einzige Core-Datei zu kopieren.

## Step 4 — Port Inventory, noch keine Port-Implementierung

- **KEEP** — existierende Typen und Firewalls als Kandidaten inventarisieren.
- **SPLIT** — Core Orientation Contracts von neuen ORION Run Contracts unterscheiden.
- **POSTPONE** — entscheiden, ob Cross-Repo-Verträge als JSON Schema, Python Package oder neutraler IDL publiziert werden.
- **POSTPONE** — Library- und Builder-Adapter.

**Gate:** Für jeden geplanten Datenfluss sind Owner, Producer, Consumer, Authority und Versioning benannt.

## Step 5 — Library Reconciliation

- **KEEP** — der Freeze bleibt unveränderte historische und technische Referenz.
- **MERGE** — den uncommitted Library-Workbench nur über einen nachvollziehbaren Inhalts-/Provenance-Abgleich in eine aktive Library-Linie überführen.
- **REMOVE** — nach dem Abgleich Dubletten aus der aktiven Navigation, nicht automatisch von Disk.
- **POSTPONE** — physische Extraktion von `LIBRARY/` und `nexah/library/`, bis Repository-Historie, Lizenzen, Release-ID und Testownership beschlossen sind.

**Gate:** Es existiert genau eine aktive Library-Authority, und jeder übernommene Record hat Herkunft zum Freeze oder zu einer humanen Entscheidung.

## Step 6 — Builder Hub Identification

- **KEEP** — Builder Hub als unabhängige Anwendung behandeln.
- **POSTPONE** — Repository-Aufbau, bis ein autoritativer Codebestand oder ein bewusster Greenfield-Entscheid vorliegt.
- **REMOVE** — Poster und Construction Visuals aus jeder Interpretation als UI-Spezifikation.

**Gate:** Builder Hub hat einen benannten Repository-Owner und konsumiert nur ORION Public Contracts.

## Step 7 — Phase-0 Closure Review

- **KEEP** — Matrix gegen `REPOSITORY_MAP.md`, `ARCHITECTURE/SYSTEM_STATE.md`, `CONTRIBUTING.md`, Library Architecture und OLS Authority prüfen.
- **POSTPONE** — alle Implementierungsarbeiten, bis Widersprüche geschlossen sind.

**Gate:** Architektur-Ownership ist vollständig, widerspruchsfrei und durch die jeweiligen Owner bestätigt.

---

# 7. What Stays Exactly As It Is

| Bestand | Begründung | Klassifikation |
|---|---|---|
| gesamter Freeze-Commit `9f79bb06` | Baseline und historische Reproduzierbarkeit | **KEEP** |
| sechs Subsysteme und ihre Authority Boundaries | bereits explizit dokumentiert und eingefroren | **KEEP** |
| OLS Release 1.0.0 | kanonische semantische Autorität | **KEEP** |
| `nexah/core.py` v0.7 | charakterisierte eingefrorene Semantik | **KEEP** |
| `nexah/orientation/*` | typisierte deterministische Verträge und Evidence-Grenzen | **KEEP** |
| `nexah/sources/*` | validierte Source-Adapter-Grenze | **KEEP** |
| `nexah/backends/*` | Representation Backends; keine LLM-Adapter | **KEEP** |
| `OutcomeFirewall` | verhindert Outcome-/Memory-Laundering | **KEEP** |
| bestehende Applications und Power Systems | eigene Domänenownership | **KEEP** |
| Library Registry, Batch-1-Record und Writer-Grenzen | human-governed Library-Evidenz | **KEEP** |
| Living Concepts X2 | begrenzter read-only Pilot | **KEEP** |
| Tests, Validation und Testkits | Evidenz des Freeze | **KEEP** |
| PROTO_CORE und EXPERIMENTAL | Entwicklungs- und Evidenzgeschichte | **KEEP** |
| bestehende Namen Q°, JANUS, OrientationState, BackendAdapter usw. | keine unnötige Umbenennung | **KEEP** |

---

# 8. What Moves

In Phase 0 bewegt sich kein eingefrorener Quellcode.

| Artefakt | Von | Nach | Klassifikation |
|---|---|---|---|
| `NEXAH_REASONING_ARCHITECTURE_REVIEW.md` | Übergangsworkspace | `nexah-orion/docs/architecture/evidence/` | **MOVE** |
| `ORION_ARCHITECTURE.md` | Übergangsworkspace | `nexah-orion/docs/architecture/` | **MOVE** |
| `PHASE_0_BASELINE_RECOVERY.md` | Übergangsworkspace | `nexah-orion/docs/architecture/baselines/` | **MOVE** |
| ORION-bezogene visuelle Evidenz | Desktop/Übergangsworkspace | katalogisierte Visual-Evidence-Zone | **MOVE** nach Rechte-/Provenance-Prüfung |
| ältere aktive Clone-Referenzen | aktive Navigation | Archive/History Navigation | **MOVE** logisch; keine Dateilöschung |

Nicht verschoben werden `nexah/orientation`, `nexah/backends`, Library-Code, Tests, Corpora, Applications oder Architecture-Dokumente des Freeze.

---

# 9. What Becomes ORION

Nur Verantwortungen, die im Target bereits beschlossen sind und im Freeze nicht als modellunabhängiger Run Owner implementiert sind, werden ORION.

| Verantwortung | Current State | Target | Klassifikation |
|---|---|---|---|
| `OrientationRequest` Lifecycle | nicht vorhanden | ORION | **SPLIT** vom allgemeinen Orientation-Begriff |
| Run State Machine | nicht vorhanden | ORION | **SPLIT** |
| Context Planning | nicht vorhanden | ORION | **SPLIT** |
| immutable Context Manifest | nicht vorhanden | ORION | **SPLIT** |
| Capability-basiertes Model Routing | nicht vorhanden | ORION | **SPLIT** |
| Reasoning Backend Port | nicht vorhanden | ORION | **SPLIT** |
| Prompt/Message Rendering | nicht vorhanden | ORION | **SPLIT** |
| Reasoning Result Validation | nicht als LLM-Grenze vorhanden | ORION, vor Kernel-Entscheidung | **SPLIT** |
| ORION Run Record und Replay | nicht vorhanden | ORION | **SPLIT** von Core Episodic Memory |
| Proposed Kernel Commands | nicht vorhanden | ORION erzeugt Vorschläge; Kernel entscheidet | **SPLIT** |
| Backend Conformance Corpus | nicht vorhanden | ORION | **POSTPONE** bis Contract-Gate |

Nicht ORION werden:

- Core-Primitives und Core-Invarianten;
- OLS-Semantik;
- Research Findings;
- Domain Applications;
- Library Registry oder Editorial Writer;
- Human Approval;
- bestehende Representation Backends;
- Living Concepts Authority.

---

# 10. What Is Intentionally Postponed

| Thema | Frühestes Gate | Klassifikation |
|---|---|---|
| ORION-Programmiersprache und Framework | nach Ownership Registry | **POSTPONE** |
| Request-/Result-Schema-Implementierung | nach Port Inventory | **POSTPONE** |
| Core-Adapter-Code | nach Cross-Repo-Vertragsentscheidung | **POSTPONE** |
| Ollama-/llama.cpp-/Cloud-Adapter | nach Fake-Backend-Vertical-Slice | **POSTPONE** |
| Prompt Templates | nach stabilen Requests und Context Package | **POSTPONE** |
| Context Retrieval und Embeddings | nach Library-/Core-Ports | **POSTPONE** |
| Vector Database | bis ein gemessener Retrieval-Bedarf sie rechtfertigt | **POSTPONE** |
| Multi-Agent-Orchestration | bis ein einzelner Run vollständig beherrscht wird | **POSTPONE** |
| direkte Kernel Writes | bis Commands, Effect Classes und Approval beschlossen sind | **POSTPONE** |
| physische Library-Extraktion aus dem Freeze | bis History, Release und Testownership geklärt sind | **POSTPONE** |
| Builder-Hub-Aufbau | bis autoritatives Repository identifiziert ist | **POSTPONE** |
| Lyra als eigenes Repository | bis unabhängiger Releasezyklus und mehrere Konsumenten existieren | **POSTPONE** |
| Sirius als eigenes Produkt/Repository | bis Produkt- und Deploymentrolle bestätigt ist | **POSTPONE** |
| General Kernel Integration der Living Concepts | bleibt gemäß X2-Status deferred | **POSTPONE** |
| Promotion aus `EXPERIMENTAL/` oder `PROTO_CORE/` zu ORION | bis ein konkreter reproduzierter Bedarf besteht | **POSTPONE** |
| Bereinigung oder Löschung historischer Arbeitskopien | bis Backup und Provenance bestätigt sind | **POSTPONE** |

---

# 11. Migration Decision Register

Dieser Abschnitt fasst jede aktive Empfehlung ohne erläuternden Fließtext zusammen.

| ID | Empfehlung | Klasse |
|---|---|---|
| BR-001 | Commit `9f79bb06` als Baseline pinnen | **KEEP** |
| BR-002 | Freeze-Repository unverändert lassen | **KEEP** |
| BR-003 | sechs Subsystem-Authorities unverändert lassen | **KEEP** |
| BR-004 | ORION als neues Repository anlegen | **SPLIT** |
| BR-005 | neue ORION-Dokumente in dieses Repository überführen | **MOVE** |
| BR-006 | bestehende `nexah/orientation`-Verträge im Core belassen | **KEEP** |
| BR-007 | bestehende `nexah/backends` als Representation Backends belassen | **KEEP** |
| BR-008 | ORION Run Memory von Core Episodic Memory trennen | **SPLIT** |
| BR-009 | neue Library-Arbeit unabhängig besitzen | **SPLIT** |
| BR-010 | physische Library-Extraktion nicht jetzt durchführen | **POSTPONE** |
| BR-011 | Builder Hub unabhängig besitzen | **KEEP** |
| BR-012 | Builder-Codebestand vor Aufbau identifizieren | **POSTPONE** |
| BR-013 | älteren März-Clone aus aktiver Navigation nehmen | **REMOVE** |
| BR-014 | uncommitted Library-Workbench nicht als Authority behandeln | **REMOVE** aus Authority Map |
| BR-015 | Library-Workbench später provenance-basiert konsolidieren | **MERGE** |
| BR-016 | Caches, Outputs und Modellgewichte nicht migrieren | **REMOVE** |
| BR-017 | visuelle Evidenz katalogisieren, nicht implementieren | **MOVE** nach Provenance-Prüfung |
| BR-018 | keine Provider- oder Runtime-Implementierung in Phase 0 | **POSTPONE** |
| BR-019 | keine Promotion historischer Prototypen zu ORION | **POSTPONE** |
| BR-020 | Cross-Repo-Portform erst nach Owner-Bestätigung entscheiden | **POSTPONE** |

---

# 12. Phase-0 Closure Criteria

Phase 0 ist abgeschlossen, wenn alle folgenden Aussagen mit **KEEP** bestätigt werden können:

- **KEEP** — Der autoritative Freeze-Hash und Remote sind dokumentiert.
- **KEEP** — Für alle sechs Current Subsystems bleibt die Authority unverändert.
- **KEEP** — Für jedes aktuelle `nexah`-Modul ist ein Owner benannt.
- **KEEP** — ORION besitzt ausschließlich die neuen Target-Verantwortungen.
- **KEEP** — Kein Freeze-Inhalt wurde verschoben, umbenannt oder neu interpretiert.
- **KEEP** — Library- und Builder-Hub-Ownership sind unabhängig von ORION.
- **KEEP** — Jede geplante Cross-Repo-Verbindung nennt Producer, Consumer, Authority und Versioning Owner.
- **KEEP** — Historische Clones und uncommitted Workbenches sind nicht Teil der Authority Map.
- **KEEP** — Die nächsten Arbeiten sind Architecture Ownership Records und ADRs, nicht Backend-Code.

Bis diese Closure Review erfolgt ist, bleibt die Implementierungsphase **POSTPONE**.

---

# 13. Nächster zulässiger Schritt

Der nächste zulässige Schritt ist ein dokumentarischer Ownership Checkpoint:

1. **KEEP** — Freeze-Hash durch den NEXAH-Core-Owner bestätigen.
2. **KEEP** — Matrix für OLS, Core Implementation, Applications, Library und EOS durch die jeweiligen Owner bestätigen.
3. **SPLIT** — ORION-Owner für Request, Run, Context, Reasoning und Audit formell benennen.
4. **POSTPONE** — den technischen Port noch nicht festlegen.
5. **MOVE** — erst nach Bestätigung die drei ORION-Dokumente in das neu initialisierte ORION-Repository überführen.

Danach kann Phase 1 mit ADRs und Interface Ownership beginnen. Sie beginnt noch nicht mit Backend-Implementierung.
