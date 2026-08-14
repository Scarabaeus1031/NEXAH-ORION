# The NEXAH Desk

**Status:** Proposal only; not the live Desk

**Recommended future location:** `NEXAH/DESK.md`

**Recommended owner:** NEXAH ecosystem architecture maintainer under the
adopted Constitution

## Decision

The future Desk should begin as one short, hand-maintained Markdown file at the
root of the canonical NEXAH Research & Framework repository.

It should not be a dashboard, database, registry, protocol, or new authority.
It should link the exact authoritative material owned elsewhere and record only
current navigation facts: repository identity, approved revision, lifecycle
state, public status, open owner decisions, and the next bounded actions.

## Why the Desk belongs in NEXAH

The NEXAH repository already owns the ecosystem Constitution, ecosystem
architecture, released OLS, Research, Kernel, Applications, Library identity,
and the best existing Repository Map. ORION, Experience, NEXAHEDRON, and
Are.na retain their own responsibilities. Placing a link index in NEXAH makes
the ecosystem understandable without making NEXAH a runtime or publication
monolith.

The current ORION `.workspace` is valuable maintainer evidence, but it is a
local operational assembly with a stale pin and undeclared checkouts. It cannot
be the canonical ecosystem Desk.

## Minimum Desk control surface

The live file should fit on a few screens and contain:

1. **Last verified** — date, maintainer, and exact NEXAH revision.
2. **Ecosystem map** — one link to the authoritative architecture and one
   maintained visual companion.
3. **Repository status** — canonical remote, approved revision/tag, state,
   dirty/clean only when observed, owner, and local path only in a private
   maintainer view.
4. **Active projects** — existing named work only, with owner and source.
5. **Frozen milestones** — OLS release, ORION baseline, POA-001, POA-002, and
   other explicitly frozen records.
6. **Research threads** — links to current Research and Applications status,
   not copied hypotheses.
7. **Application status** — maintained, active research, experimental, legacy,
   or independent product.
8. **Publication and website status** — `nexah.de`, `nexahedron.com`, GitHub,
   and Are.na, each with “last externally verified.”
9. **Unresolved decisions** — only decisions with a named owner and evidence
   link.
10. **Next recommended actions** — at most three bounded organizational
    actions.

## Proposed first Desk content

### Start here

| Need | Authority |
|---|---|
| Ecosystem purpose and public route | `NEXAH/README.md` |
| Governance | `NEXAH/GOVERNANCE/ECOSYSTEM_CONSTITUTION.md` |
| Repository navigation | `NEXAH/REPOSITORY_MAP.md` |
| Ecosystem architecture | `NEXAH/ARCHITECTURE/README.md` |
| NEXAH implementation state | `NEXAH/ARCHITECTURE/SYSTEM_STATE.md` |
| OLS 1.0 | `NEXAH/ORIENTATION_LANGUAGE/README.md` and released suite |
| ORION | `NEXAH-ORION/README.md`, architecture index, and certified baseline |
| POA-001 / POA-002 | ORION experiment designs, example evidence, and freeze reports |
| Public Experience | NEXAH-Experience source and `nexah.de` |
| Human Workspace | NEXAHEDRON source and `nexahedron.com` |
| Living Library | `NEXAH/LIBRARY/README.md`, Atlas, and Are.na |

### Repository status at this review

| Repository | Inspected revision | State | Immediate status issue |
|---|---|---|---|
| NEXAH | `57fdd7ea21944aba19ed2bc3c2a9254b8b20da8c` | Active, clean checkout | Differs from ORION's declared connected pin |
| NEXAH-ORION | `d34fbb2f99334534f4db89465a29f8bdb16d14d3` | V1 baseline plus modified working tree | POA and later review/runtime work require scoped commits |
| NEXAH-Experience | `7473736ff5e6077fda41e7302b041e79e57673e3` | Release source, clean checkout | Live OVH upload status unverified |
| NEXAHEDRON | `f273ae5009b15f5f7606b494276b906fc72cfe2b` | Release candidate, clean local checkout | No remote; public access/DNS documented pending |
| Library workbench | No commit | Local staging/cleanup | Canonical relationship to `NEXAH/LIBRARY/` unresolved |

This table is review evidence, not a permanent approval of the listed
revisions.

### Frozen milestones

| Milestone | Authority and evidence | Scope note |
|---|---|---|
| OLS 1.0 | NEXAH OLS release | Released semantics only |
| ORION V1 | ORION certified baseline/release records | ORION declared scope |
| POA-001 | ORION design, one Processor implementation, artifacts, review, freeze report | One frozen experimental slice |
| POA-002 | ORION design, independent Processor B, equivalence evidence, freeze report | Semantic equivalence for one frozen capability |

No Desk summary may broaden a freeze report's conclusion.

### Current research and applications

The Desk should link, not reproduce:

- `NEXAH/RESEARCH/README.md` for active research and JANUS;
- `NEXAH/APPLICATIONS/README.md` for maturity-labelled domain work;
- `NEXAH/LIBRARY/README.md` and Editorial Operating System status for Library
  and editorial work; and
- ORION's own roadmap/status only when it is an approved current record.

### Public surfaces

| Surface | Responsibility | Current review state |
|---|---|---|
| `nexah.de` | Public/intellectual entrance and audience navigation | Source and upload artifact verified; live update unverified |
| `nexahedron.com` | Human-facing Workspace | Source/release candidate verified; public DNS/access unverified |
| GitHub | Versioned specifications, source, evidence, and revisions | NEXAH verified public; other remotes documented/configured |
| Are.na | Live visual Library source and editorial browsing | Referenced and partially observed; detailed live state unverified |

### Unresolved decisions

1. Approve the NEXAH revision used by ORION and resolve the manifest/checkout
   mismatch.
2. Approve and record the POA freeze commit/tag scope.
3. Decide NEXAHEDRON's remote repository identity.
4. Decide whether the Library remains inside NEXAH or receives an explicit
   authority handoff.
5. Define `OLI` from existing evidence or remove it from current navigation.
6. Reconcile the current deployment handoff with the older launch-status file.

### Next three actions

1. Record and approve exact canonical repository revisions, including the
   connected NEXAH pin.
2. Version the already-frozen POA-001/002 artifacts in one isolated,
   verified ORION change.
3. Add the navigation-only root Desk and cross-links after those identities
   are stable.

## Maintenance rules

- Every status row names an owner, exact source, last verified date, and scope.
- Links point to repository-local authority; the Desk does not copy normative
  definitions.
- External state says “documented, unverified” until checked.
- Historical records are superseded by a dated link, never silently rewritten.
- Frozen documents and checksums are never refreshed to make the Desk pass.
- A changed repository revision requires review of dependent pins and evidence.
- Keep only three next actions. The Desk is an orientation surface, not a
  backlog database.
- If the Markdown file becomes difficult to maintain, first reduce its content.
  A generated dashboard is justified only after stable ownership and source
  data exist.

## Final synthesis

### What is NEXAH's current source of truth?

NEXAH has scoped sources of truth rather than one universal document. The
adopted Constitution governs the ecosystem; the NEXAH Architecture and System
State describe its responsibility model and current NEXAH implementation
frontier; the OLS release owns semantics; each implementation, experiment,
Library surface, and website owns its declared scope.

### Where is the current desk?

It is fragmented across `NEXAH/README.md`, `REPOSITORY_MAP.md`,
`ARCHITECTURE/SYSTEM_STATE.md`, ORION's `workspace.yaml`, repository-local
indexes, POA freeze reports, and `.workspace/releases/`.

### Why is it difficult to find?

The ecosystem's conceptual authority is well indexed in NEXAH, but newer proof,
revision, deployment, website, and local archive state lives in other
repositories or unversioned workspaces. Those records also have different
dates and occasionally conflict.

### What should become the future desk?

A root `NEXAH/DESK.md`: short, manually maintained, link-only, revision-aware,
and owned under the existing ecosystem architecture responsibility.

### Which repository owns ecosystem architecture?

The canonical NEXAH Research & Framework repository, under its adopted
Constitution. ORION owns ORION architecture, not ecosystem governance.

### Where should OLS / OLI live?

OLS remains in `NEXAH/ORIENTATION_LANGUAGE/`. No verified `OLI` authority was
found. `OLS-I` must not be renamed or treated as `OLI` without primary
evidence.

### Where should canonical formats live?

Adopted semantic format rules live with OLS. Implementation-specific carriers
and schemas live with their implementation; publication formats live with
their surface; experimental/historical formats stay in research or archive.
There is no evidenced need for a universal format repository.

### Where should applications live?

Repository-domain applications remain in `NEXAH/APPLICATIONS/`. Independently
governed products such as NEXAHEDRON and the public Experience retain their
own repositories.

### Where should POA designs, implementations, evidence, and freeze reports live?

They should remain where the frozen design placed them: designs and freeze
reports in `NEXAH-ORION/docs/experiments/`, implementation and immutable
evidence in `NEXAH-ORION/examples/poa-*`. The Desk should link them; nothing
should be moved.

### What should the public surfaces be responsible for?

- `nexah.de`: public explanation, visitor orientation, and routing.
- `nexahedron.com`: Human-facing reference Workspace and Orientation Session.
- GitHub: versioned specifications, source, evidence, releases, and revision
  identity.
- Are.na: live visual Library content, editorial sequence, and browsing, while
  the NEXAH Registry retains identity authority.

### What are the three highest-priority organizational actions?

1. Approve a cross-repository revision/source-of-truth ledger.
2. Commit and identify the already-frozen POA evidence without mixing unrelated
   working-tree changes.
3. Add the minimal root Desk and its navigation links.

### What should explicitly not be changed yet?

Do not change frozen architecture, OLS 1.0, POA design/evidence, connected
pins, repository boundaries, Library ownership, historical paths, public DNS,
or local archives as part of documentation cleanup. Do not begin POA-003 or
create a software dashboard, universal registry, universal format, or new
ecosystem layer.
