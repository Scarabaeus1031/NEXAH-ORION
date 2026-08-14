# NEXAH Information Architecture Assessment

**Status:** Informative assessment; no restructuring performed

**Observed:** 2026-07-25

## Executive assessment

NEXAH is not missing an architecture. It has strong, scoped authorities and
good local indexes. Its information problem is that ecosystem authority,
repository state, experimental proof, public deployment, and historical source
material are each recorded in different places and on different clocks.

The immediate need is a maintained navigation and status layer. Moving content
before that layer exists would increase ambiguity and risk breaking
provenance.

## What is already well organized

- The NEXAH root README, Repository Map, Architecture index, and System State
  make the main repository unusually navigable for its size.
- The adopted Constitution, released OLS suite, Kernel implementation,
  Applications, Living Library, and Editorial Operating System have explicit
  authority boundaries.
- OLS 1.0 separates conventions, base language, declarations/operators,
  composition, derivations, conformance, and governance into a released suite.
- Research explicitly separates active core work, validation, findings,
  applied cases, theoretical extensions, notes, and history.
- Applications states maturity per program rather than presenting all runnable
  code as validated.
- Library documentation distinguishes Registry identity, approved repository
  sequences, and live Are.na visual publication.
- ORION distinguishes authoritative Markdown from generated visual companions,
  records checksums, and keeps POA design, execution artifacts, representation,
  Human Review, negative evidence, and freeze reports inspectable.
- The Editorial Operating System visual index labels architecture, snapshots,
  vision, and history instead of treating every image as a specification.

## What is fragmented or missing

- No one maintained file records the ecosystem's repositories, exact approved
  revisions, active/frozen state, public deployment state, and next decisions.
- NEXAH's ecosystem map does not yet point to POA-001/002 or to the recent
  ORION-hosted architecture distillation.
- The ORION workspace manifest does not match its connected NEXAH checkout and
  omits locally present Experience and Framework-CI relationships.
- The Library has three visible identities: the canonical NEXAH Registry, an
  unborn local cleanup repository, and an independent remote-pending workspace
  declaration.
- Current public operations state is split between a July 22 launch status and
  a July 24 final handoff.
- Local books, visuals, whiteboards, old clones, and staging directories lack
  a single provenance/status inventory.
- The term `OLI` is requested in ecosystem discussions but is not defined in
  the inspected current Markdown.
- POA artifacts are complete but untracked in the inspected ORION working tree;
  the experimental freeze is therefore not yet visibly a Git freeze.

## Issue register

Severity classes describe the type of response required; they are not numeric
scores.

| Severity | Issue | Evidence and effect | Recommended response |
|---|---|---|---|
| Critical | No ecosystem-wide current revision and authority ledger | The best navigation is in NEXAH; newest POA/release state is in ORION; NEXAHEDRON has no remote | Establish a navigation-only Desk with exact links/revisions after human approval |
| Critical | Connected Core revision conflicts with declared pin | `workspace.yaml` declares `9f79bb…`; connected NEXAH resolves to `57fdd7…` | Record and resolve compatibility deliberately; do not refresh the pin as housekeeping |
| Structural | Ecosystem architecture and newest proof evidence are not cross-indexed | NEXAH owns ecosystem architecture; POA design/evidence/freeze reports are in ORION | Add future cross-links without moving frozen files |
| Structural | Library repository boundary is unresolved | Canonical Registry is in NEXAH; local workbench has no remote; manifest says independent remote pending | Choose an identity after inventory; retain NEXAH Registry authority meanwhile |
| Structural | “Core” names several different scopes | NEXAH Kernel, ORION Core, workspace Core role, `PROTO_CORE`, older architecture Core | Always qualify the owner and scope; do not mass-rename yet |
| Structural | Runtime, certified Core, and POA state share the ORION working tree | New runtime material and frozen POAs are simultaneously untracked/modified | Freeze by explicit commit scope; do not treat working-tree proximity as shared architecture |
| Navigational | POA-001 and POA-002 have no ecosystem entry | Only ORION-local paths expose them | Link both designs, evidence roots, and freeze reports from the future Desk |
| Navigational | Important source material is effectively hidden | Desktop books/visuals and local `.workspace` releases are not in the NEXAH map | Add a provenance inventory; do not ingest or move files yet |
| Navigational | Multiple local NEXAH copies appear usable | Clean canonical checkout, CI checkout, older clone, symlink duplicates, NEXAH-CODEX remote collision | Record canonical checkout and classify the rest before cleanup |
| Navigational | No maintainer onboarding path spans all repositories | Public reader paths exist; maintainer must combine multiple indexes | Make root `NEXAH/DESK.md` the maintainer start page |
| Editorial | Launch status is stale relative to later handoff | July 22 says remotes need creation; July 24 handoff says ORION and Experience are public | Mark the older status superseded only after owner verification |
| Editorial | Governance map wording is internally inconsistent | Root README calls Constitution v1.0 adopted; Repository Map contains provisional-review wording | Correct navigation text in a future editorial pass without altering the Constitution |
| Editorial | Visual titles can imply authority beyond their metadata | Desktop “ecosystem” and “grammar” images are unversioned; NEXAH archive has old grammar tables | Link only through status-bearing indexes |
| Historical | Older layouts remain near active work | `NEXAH_REPO_CLONE` and NEXAH-CODEX retain plausible current names | Add explicit historical/local banners or an external inventory before archiving |
| Historical | Experimental and legacy application lineages remain large | NEXAH properly labels many areas, but external local roots do not | Preserve history; improve entry-point status before any relocation |
| Low priority | Photos library package is opaque | Large local visual package lacks a semantic index visible to this review | Inventory when publication provenance work begins |
| Low priority | Duplicate workspace links and social-preview assets are undocumented | Operational clutter, not semantic conflict | Record, then clean only with owner approval |

## What should remain separate

1. **Governance and implementation.** The Constitution governs; no runtime
   output can amend it.
2. **Research and released semantics.** Research may inform OLS only through
   explicit adoption.
3. **OLS and processors.** OLS owns meaning; Kernel and ORION own scoped
   executable behavior.
4. **Applications and examples.** An application has a domain claim and
   evidence boundary; an example demonstrates a declared capability.
5. **Experiment design and evidence.** A frozen design states the claim and
   failure conditions; immutable artifacts show what happened.
6. **Result and representation.** POA evidence already relies on this boundary.
7. **Library identity and live publication.** The Registry and Are.na have
   different authority.
8. **Public Experience and Human Workspace.** `nexah.de` explains and routes;
   NEXAHEDRON hosts the reference session.
9. **Source repositories and deployment records.** A deployed site is not the
   architecture source of truth.
10. **Current and historical visuals.** They may depict the same topic without
    sharing status.

## What may eventually be consolidated

Consolidation here means one canonical index or status statement, not moving
underlying content.

- One ecosystem revision/status ledger.
- One source-of-truth matrix linking repository-local authorities.
- One POA index linking design, implementation, evidence, and freeze report.
- One deployment-status row per public surface, linking the owning repository's
  detailed handoff.
- One local archive inventory connecting Desktop book/visual roots to Library
  Registry identities where evidence permits.
- One explicit explanation of qualified “Core,” “Kernel,” and “Processor”
  usages.

## What should never be consolidated

- OLS semantics with implementation schemas merely because both use JSON.
- Research operators, OLS operator contracts, Library Operator Concepts, and
  ORION capabilities into one universal operator registry.
- Scientific evidence, technical test evidence, and editorial evidence into a
  single undifferentiated evidence store.
- Are.na publication order with Registry identity.
- NEXAH Experience and NEXAHEDRON into one website responsibility.
- Frozen POA artifacts into a mutable generated dashboard.
- Historical books or visuals into technical specifications based on topic or
  title alone.

## Architecture update assessment

| Document or area | Current coverage | Missing recent work | Recommendation |
|---|---|---|---|
| `NEXAH/README.md` | Strong ecosystem front door, six responsibilities, public route, limits | POA-001/002 and exact current repository revisions | Update later with a link to the approved Desk; keep conceptual content stable |
| `NEXAH/REPOSITORY_MAP.md` | Strong directory and reader navigation | Cross-repository status, POAs, current NEXAHEDRON identity | Update navigation after Desk approval |
| `NEXAH/ARCHITECTURE/README.md` | Owns conceptual ecosystem architecture | Recent ORION distillation and implementation-proof status | Add derived links/status only; do not copy ORION documents |
| `NEXAH/ARCHITECTURE/SYSTEM_STATE.md` | Explicit current implementation ground truth for NEXAH | POA evidence, latest web/repository state | Update only facts within its declared implementation scope; cross-repository operations belong in Desk |
| `NEXAH/GOVERNANCE/ECOSYSTEM_CONSTITUTION.md` | Adopted highest governance | Nothing in POA requires a governance change | Remain frozen/adopted |
| `NEXAH/ORIENTATION_LANGUAGE/.../OLS-RELEASE-1.0.0` | Canonical OLS 1.0 release | POA evidence does not extend the language | Remain frozen |
| `NEXAH-ORION/docs/architecture/ORION_ARCHITECTURE.md` and V1 freeze | Frozen ORION architecture | POA outcomes are evidence, not architecture revisions | Remain frozen |
| `NEXAH-ORION/docs/architecture/NEXAH_ARCHITECTURE_DISTILLED.md` | Informative editorial consolidation | Ecosystem repository inventory and public operations | Keep informative; do not elevate into NEXAH governance |
| `NEXAH-ORION/docs/experiments/POA_*` | Complete narrow designs and freeze reports | Git-recorded freeze in inspected tree | Remain content-frozen; commit/tag is separate repository work |
| `NEXAH/LAUNCH_STATUS.md` | July 22 operational state | July 24 handoff advances ORION/Experience and NEXAHEDRON | Candidate to be superseded by a newer dated status after verification; retain historically |
| This ecosystem review | Cross-repository inventory, assessment, target, migration plan, Desk proposal | Owner decisions and externally verified live state | New informative review only; not architecture authority |

No existing architecture document needs to be rewritten to acknowledge
POA-001/002. The minimal correct update is future navigation from the NEXAH
Desk and architecture index to the frozen evidence.

## Visual review

The maintained repositories already support status-bearing visual indexes.
ORION explicitly makes Markdown and accepted ADRs authoritative over plates;
NEXAH Editorial Operating System explicitly distinguishes architecture,
snapshots, vision, and history. Those practices should govern ecosystem
navigation.

The future Desk should link:

- `NEXAH/assets/readme/nexah-orientation-ecosystem-map.png` through the root
  README;
- `NEXAH/ORIENTATION_LANGUAGE/VISUALS/CANONICAL/` through the OLS release;
- `NEXAH-ORION/docs/architecture/plates/README.md`;
- `NEXAH/EDITORIAL_OPERATING_SYSTEM/README.md` visual index; and
- `NEXAH/docs/library/atlas-of-atlases/README.md`.

It should not directly present Desktop images, raw scientific plots, or
historical grammar tables as current architecture. A new canonical ecosystem
visual is not a prerequisite for the Desk. If created later, its authoritative
text, date, scope, editable source, generated derivatives, and review rule must
first be named.
