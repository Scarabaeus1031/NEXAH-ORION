# Target Ecosystem Architecture

**Status:** Informative low-disruption proposal; not implemented

**Basis:** Existing repositories, authorities, and responsibilities only

This target does not add a NEXAH layer or redesign OLS. It makes the present
responsibility boundaries navigable with fewer competing status statements.

## Target in one rule

Keep authority with its current owner; add one NEXAH-maintained Desk that
links exact repository-local sources, revisions, states, evidence, and public
surfaces without copying their content.

## A. Repository-level model

```text
NEXAH Research & Framework
  owns: Constitution, ecosystem architecture, research, OLS, maintained
        Kernel, domain applications, Library Registry, Editorial OS
  links:
    NEXAH-ORION
      owns: ORION architecture, deterministic processor/navigation
            implementation, POA designs and evidence
    NEXAH-Experience
      owns: nexah.de source and public interpretation
    NEXAHEDRON
      owns: Human-facing Workspace source for nexahedron.com
    Are.na
      owns: live visual Library content and editorial sequence

Historical/local archives
  preserve: prior lineages, source books, visuals, staging, and workbenches
  own no current semantics merely by containing related material
```

No additional repository is required to reach this target.

The Library should remain canonically represented by `NEXAH/LIBRARY/` until an
approved independent repository has a remote identity, migration record, and
authority handoff. Builder Hub remains pending and is not included as a
present target owner.

## Repository responsibility rules

| Owner | Canonical responsibility | Must not absorb |
|---|---|---|
| NEXAH | Ecosystem governance/architecture; research; released OLS; maintained Kernel; repository-domain applications; Library identity; editorial architecture | ORION implementation details, web deployment code, live Are.na order |
| NEXAH-ORION | ORION architecture and implementation; POA design/evidence/freeze records for its architectural claims | OLS semantic authority, ecosystem Constitution, Human interpretation |
| NEXAH-Experience | Public explanation and onboarding source for `nexah.de` | Specifications, Kernel/ORION authority, Workspace state |
| NEXAHEDRON | Reference Human Workspace application and its release/deployment source | Ecosystem architecture or OLS authority |
| Are.na | Live visual Library publication and browsing | NEXAH Registry identity or technical specification |
| Local/historical archives | Provenance-preserving source and prior states | Current authority unless explicitly adopted elsewhere |

## B. Main NEXAH repository model

The existing top-level organization should remain. The target adds navigation,
not a parallel taxonomy.

```text
NEXAH/
├── DESK.md                       proposed maintainer control surface
├── README.md                     public/repository front door
├── REPOSITORY_MAP.md             directory navigation
├── GOVERNANCE/                   adopted governance
├── ARCHITECTURE/                 ecosystem architecture and NEXAH system state
├── RESEARCH/                     hypotheses, experiments, scientific evidence
├── ORIENTATION_LANGUAGE/         released language, grammar, vocabulary,
│                                 operator contracts, adopted semantic formats
├── nexah/                        maintained Kernel implementation
├── APPLICATIONS/                 domain applications and applied research
├── LIBRARY/                      canonical editorial identity and Registry
├── EDITORIAL_OPERATING_SYSTEM/   editorial architecture/governance/execution
├── PROTO_CORE/                   demonstrators and prototype lineages
├── validation/ tests/ testkit/   repository-scoped verification
├── docs/                         cross-system reader documentation
└── existing archive areas        preserved historical material
```

Directory guidance:

- **Formats** do not require a universal top-level directory. Adopted semantic
  rules live with OLS; implementation schemas live with their implementation;
  publication formats live with their surface; experimental formats remain
  research or history.
- **Experiments** remain with the claim owner. Scientific experiments remain
  in Research/Applications; ORION POAs remain in ORION.
- **Examples** remain beside the specification or implementation whose scope
  they demonstrate.
- **Onboarding** remains audience-specific. `README.md` is the repository/public
  front door, `DESK.md` is the maintainer front door, and `nexah.de` is the
  public Experience.
- **Archive** should use existing archive/history areas. A new global archive
  is unnecessary until local roots have provenance inventories.

## C. Source-of-truth matrix

| Topic | Preferred authoritative location | Derived or public views |
|---|---|---|
| Ecosystem Constitution | `NEXAH/GOVERNANCE/ECOSYSTEM_CONSTITUTION.md` | Repository governance summaries |
| Ecosystem architecture | `NEXAH/ARCHITECTURE/README.md` and accepted NEXAH architecture records | NEXAH README visual/map; future Desk status links |
| Ecosystem current-state navigation | Proposed `NEXAH/DESK.md` | Generated views may come later, but never become authority |
| NEXAH implementation maturity | `NEXAH/ARCHITECTURE/SYSTEM_STATE.md` | README summary |
| OLS grammar, vocabulary, operator contracts, semantics | Released suite under `NEXAH/ORIENTATION_LANGUAGE/SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/` | Companion guidance and OLS canonical visual |
| OLI | None until an existing authority defines the term | No alias should be invented |
| Canonical semantic formats | OLS only when adopted by an OLS release | Implementation carriers and renderings remain scoped |
| NEXAH Kernel implementation | `NEXAH/nexah/` plus release/test records | Demonstrators and applications |
| ORION architecture/runtime | ORION's own architecture/release indexes and source | Plates and downstream integrations |
| POA designs | `NEXAH-ORION/docs/experiments/POA_*_*.md` | Desk milestone links |
| POA implementations/evidence | `NEXAH-ORION/examples/poa-*/` | Static representations and Human Review |
| POA conclusions | Corresponding freeze reports in ORION | NEXAH Desk status only |
| Domain applications | `NEXAH/APPLICATIONS/<domain>/` unless an independent repository is explicitly governed | Public demonstrations |
| Human Workspace application | NEXAHEDRON repository after remote identity resolution | `nexahedron.com` deployment |
| Library identity | `NEXAH/LIBRARY/` Registry | Experience catalog and Are.na views |
| Live Library visual content/order | Are.na | Repository snapshots and approved reader sequences |
| Public Experience source | NEXAH-Experience repository | `nexah.de` |
| Visual architecture companions | Each owning repository's indexed visual source | Generated PNGs and website renditions |
| Deployment procedure/state | Deployable's repository plus dated operations handoff | Desk status row |
| Historical source | Its preserved repository/archive with a status record | Curated references only |

## D. Lifecycle model

The repositories already use maturity and status labels. The target makes them
consistent without pretending that validation and publication are the same
event.

```text
draft -> active research -> candidate -> frozen
                                      |
                                      +-> validated (for a declared claim)
                                      +-> published (for a declared audience)

superseded current work -> historical -> archived
```

| State | Minimum meaning |
|---|---|
| Draft | Editable working material with no stability claim |
| Active research | Investigated with explicit open questions and evidence limits |
| Candidate | Proposed bounded artifact awaiting named review/approval |
| Frozen | Content and scope fixed at an exact revision/digest |
| Validated | A declared test or experiment passed; the validation scope is named |
| Published | Exposed to its intended audience at a named release/source |
| Historical | Retained to explain development but no longer current |
| Archived | Inactive historical material retained with provenance and a replacement or terminal status |

`validated` and `published` are properties that may coexist with a primary
lifecycle state. A published research artifact is not thereby validated, and a
validated local proof is not thereby public.

Transitions require:

1. an owner;
2. an exact artifact/revision;
3. the declared scope;
4. evidence or approval appropriate to the transition;
5. a link to the prior state; and
6. an update to the Desk status, not a rewrite of history.

## Public versus internal material

- Public specifications and evidence live in versioned canonical repositories.
- `nexah.de` interprets and routes; it links authority rather than duplicating
  normative text.
- `nexahedron.com` provides the Human Workspace; session output does not become
  architecture.
- Are.na publishes visual Library material; the Registry remains in NEXAH.
- Local workbenches, source books, and visual archives stay internal until
  provenance, rights, identity, and publication state are recorded.
- Operations handoffs may contain deployment details that should not be copied
  into conceptual architecture.

## Research, implementation, language, and formats

Research produces scoped evidence. Architecture records adopted
responsibilities. OLS defines released semantics. Implementations execute
declared behavior. Applications apply behavior in a domain. Formats remain
owned by the layer that gives them meaning.

This preserves the repository's existing rule:

```text
research evidence
  -> explicit adoption
  -> semantic or architectural authority
  -> implementation
  -> scoped verification
```

There is no automatic promotion based on file extension, visual quality,
runtime success, or publication.

## Naming conventions

- Use exact repository names: `NEXAH`, `NEXAH-ORION`, `NEXAH-Experience`,
  `NEXAHEDRON`.
- Qualify overloaded nouns: “NEXAH Orientation Kernel,” “ORION certified
  Core,” “OLS operator contract,” “Library Operator Concept.”
- Use `OLS` only for the existing Orientation Language authority.
- Do not use `OLI` in authoritative navigation until its source definition is
  identified.
- Include status and date in snapshots and operational reports.
- Include scope/version in frozen experiment and release names.
- Do not rename historical paths merely to make them conform; add context
  first.

## Archive policy

1. Inventory identity, source, revision/date, authority, and replacement.
2. Add a visible historical/archive status before moving anything.
3. Preserve Git history and original checksums where present.
4. Do not archive the only copy of evidence or source material.
5. Do not use an archive as a silent dumping ground for unresolved authority.
6. Require human approval for repository archival, remote changes, or
   destructive local cleanup.

## Onboarding target

```text
Public reader -> nexah.de
Repository reader -> NEXAH/README.md
Maintainer -> NEXAH/DESK.md
Specification reader -> OLS release index
Developer -> owning implementation README
Evidence reviewer -> claim-local experiment/validation index
Human Workspace user -> nexahedron.com
Visual Library reader -> Library Registry/Atlas -> Are.na
```

The Desk is therefore not a new public portal or software service. It is a
short, maintained Markdown control surface that sends each reader to the
existing authority.
