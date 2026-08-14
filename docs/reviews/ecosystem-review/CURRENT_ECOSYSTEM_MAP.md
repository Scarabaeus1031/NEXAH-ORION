# Current NEXAH Ecosystem Map

**Status:** Informative description of observed state

**Observed:** 2026-07-25

This map describes the ecosystem as it exists. It does not promote a new
architecture, merge scopes, or change an existing authority.

## High-level map

```text
                         NEXAH ECOSYSTEM CONSTITUTION
                                      |
                 NEXAH Research & Framework repository
     +----------------+---------------+---------------+----------------+
     |                |               |               |                |
  Research       OLS 1.0          Kernel v0.7     Applications     Library /
  evidence       semantics        implementation   and validation   Editorial OS
     |                |               |               |                |
     |                +---------------+---------------+                |
     |                                |                                |
     +-------------------------- NEXAH-ORION --------------------------+
                                      |
                         processor / navigation evidence
                                      |
                         POA-001 and POA-002 records
                                      |
                +---------------------+--------------------+
                |                                          |
      NEXAH Experience source                         NEXAHEDRON source
            nexah.de                              nexahedron.com Workspace
       public interpretation                         Human session
                |
       Library / Atlas / Reading Spaces
                |
              Are.na
     live visual publication source

GitHub = versioned source/specification/evidence publication
Local Desktop and legacy clones = source material, staging, or archive;
                                      not current authority by proximity
```

The drawing is deliberately not a single execution pipeline. Research,
semantics, implementation, applications, editorial identity, and publication
have different authorities and maturity.

## Repository relationships

| From | To | Observed relationship | Role distinction |
|---|---|---|---|
| NEXAH Constitution | All ecosystem repositories | Highest adopted governance baseline | Governance, not executable behavior |
| NEXAH Research | Architecture / OLS / Applications | Research may supply evidence and proposals | Adoption is explicit; research does not silently define released semantics |
| OLS 1.0 | Kernel and ORION | Declares semantics and conformance expectations | Language is authority; implementation is not |
| NEXAH Kernel | Applications and Editorial Operating System | Maintained implementation track used by repository-local work | Executable behavior, scoped by evidence |
| NEXAH | ORION | NEXAH defines ecosystem/semantic context; ORION owns its certified deterministic navigation/processing scope | Independent repositories with cross-repository governance |
| ORION workspace | Connected NEXAH checkout | Manifest declares a read-only pinned Core authority | Actual connected revision differs from the manifest pin |
| ORION | POA-001 / POA-002 | Frozen design, implementation evidence, representation, review, and freeze reports | Experimental evidence for narrow claims, not general OLS validity |
| ORION | NEXAHEDRON | NEXAHEDRON pins/uses ORION at a declared boundary | Workspace remains Human-facing; ORION remains processor/navigation source |
| NEXAH | Experience | Root README identifies Experience as public source | Presentation does not become specification |
| Library Registry | Are.na | Registry owns stable NEXAH identity/classification; Are.na owns visual source content and live sequence | Identity and publication remain separate |
| Experience | `nexah.de` | Static public Experience source to public host | Source and live deployment state are separate |
| NEXAHEDRON | `nexahedron.com` | Workspace source to intended public custom domain | Local source verified; public state documented but unverified |

## Knowledge flow

```text
Research question
  -> bounded experiment / source
  -> evidence and limitations
  -> architecture or language proposal
  -> explicit review and adoption
  -> released OLS / maintained architecture
```

The repository already rejects a shortcut from research result to universal
semantic authority.

## Implementation flow

```text
Released semantics or repository-local contract
  -> independently owned implementation
  -> declared application/example
  -> deterministic output or record
  -> verification against the declared scope
```

An implementation may demonstrate behavior. It does not redefine the OLS by
producing an output.

## Validation flow

```text
Architecture claim
  -> frozen POA design
  -> immutable request / observation / OLS expression
  -> bounded Processor execution
  -> immutable Result
  -> derived Representation
  -> Human Review
  -> negative-case evidence + checksums
  -> Freeze Report
```

For POA-002 the Processor branch has two independent Results and an
Equivalence Review before representation. All artifacts remain inside
`NEXAH-ORION/docs/experiments/` and `NEXAH-ORION/examples/poa-*`.

## Public-access flow

```text
New public reader
  -> nexah.de
     -> Visitor Guide / Library / Living Atlas / Laboratory / Reading Spaces
     -> NEXAHEDRON for a Human-facing Orientation Session
     -> GitHub for specifications, source, evidence, and revisions
     -> Are.na for visual Library publication and browsing

Maintainer
  -> NEXAH README + REPOSITORY_MAP + ARCHITECTURE/SYSTEM_STATE
     -> repository-local indexes
     -> ORION workspace/release records
     -> deployment handoffs
     -> local archives when provenance work is required
```

The public reader has a documented entrance. The maintainer does not yet have
one complete control surface.

## Present sources of truth

There is no single file that is source of truth for every responsibility.

| Topic | Current preferred authority | Qualification |
|---|---|---|
| Ecosystem governance | `NEXAH/GOVERNANCE/ECOSYSTEM_CONSTITUTION.md` | Adopted constitutional baseline |
| Ecosystem responsibility model | `NEXAH/README.md`, `NEXAH/ARCHITECTURE/README.md` | Root map is the best current navigation; architecture details responsibility |
| Current NEXAH implementation state | `NEXAH/ARCHITECTURE/SYSTEM_STATE.md` | Explicitly named as current ground truth by Architecture README |
| Released OLS semantics | `NEXAH/ORIENTATION_LANGUAGE/SPECIFICATION/RELEASES/OLS-RELEASE-1.0.0/` | Canonical published semantic authority |
| Kernel behavior | `NEXAH/nexah/` plus its tests/release record | Implementation authority, not semantic authority |
| ORION architecture | `NEXAH-ORION/docs/architecture/README.md` and frozen architecture/release records | Repository-local authority under ecosystem governance |
| POA designs and conclusions | `NEXAH-ORION/docs/experiments/` | Narrow frozen experimental scopes |
| POA implementation evidence | `NEXAH-ORION/examples/poa-001/`, `examples/poa-002/` | Immutable artifacts, replay, negative cases, checksums |
| Library identity | `NEXAH/LIBRARY/` Registry | Stable identity/classification |
| Live visual Library | Are.na | Visual content and live editorial sequence, as stated by Library docs |
| Public Experience source | NEXAH-Experience repository | `nexah.de` source |
| Human Workspace source | local NEXAHEDRON repository | Remote identity unresolved |
| Latest operational handoff | `NEXAH-ORION/.workspace/releases/VERSION1_FINAL_HANDOFF.md` | Dated, local operations record; not architecture |

## Duplicated or ambiguous areas

1. **Core / Kernel naming:** the NEXAH Kernel, ORION certified Core, a workspace
   `nexah-core` role, and older `PROTO_CORE`/architecture paths all use related
   language for different scopes.
2. **Ecosystem architecture visibility:** the main NEXAH architecture owns the
   ecosystem model, while the newest OLS/infrastructure/distillation reviews
   and POA evidence live in ORION and are not indexed upstream.
3. **Library identity:** NEXAH currently contains the canonical Registry, a
   local Library workbench exists without a remote, and `workspace.yaml`
   describes an independent remote-pending Library.
4. **Repository copies:** several NEXAH checkouts, symlinks, an old layout, and
   NEXAH-CODEX coexist locally.
5. **Operational state:** `NEXAH/LAUNCH_STATUS.md` predates a later final
   handoff and still lists creation of ORION/Experience remotes as pending.
6. **Visual meaning:** current, snapshot, vision, historical, scientific-output,
   publication-source, and unversioned Desktop images coexist.
7. **OLS / OLI:** OLS and `OLS-I` are evidenced; an `OLI` authority or
   definition is not.

## The current desk

The actual desk is a route, not a place:

```text
NEXAH/README.md
  + NEXAH/REPOSITORY_MAP.md
  + NEXAH/ARCHITECTURE/SYSTEM_STATE.md
  + NEXAH-ORION/workspace.yaml
  + NEXAH-ORION/.workspace/releases/
  + repository-local READMEs and freeze reports
```

The first three files form the best authoritative ecosystem front door. The
remaining files carry newer cross-repository, POA, and operational state. This
fragmentation is why a maintainer cannot currently open one file and determine
both authority and current work.
