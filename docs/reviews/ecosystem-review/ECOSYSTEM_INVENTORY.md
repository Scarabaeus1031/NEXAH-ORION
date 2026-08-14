# NEXAH Ecosystem Inventory

**Status:** Informative ecosystem review

**Observed:** 2026-07-25

**Review root:** `NEXAH-ORION/docs/reviews/ecosystem-review/`

This directory is used because the active workspace already has a
`docs/reviews/` area and this work reviews several repositories. It is not a
new architecture authority. The adopted NEXAH Constitution and each
repository's own frozen architecture retain their existing authority.

## Method and evidence labels

The inventory uses local Git metadata, checked-out files, workspace manifests,
release handoffs, and documented public references. It does not infer
responsibility from a directory name alone.

| Label | Meaning |
|---|---|
| Verified | Directly observed in the filesystem, Git metadata, or a checked-out artifact |
| Documented, unverified | Asserted by repository documentation but not independently confirmed during this review |
| Unresolved | Available evidence conflicts or does not establish identity, status, or ownership |
| High confidence | Multiple current primary documents or Git facts agree |
| Medium confidence | One primary source exists, but currency or external state is unverified |
| Low confidence | Historical, local-only, incomplete, or ambiguous evidence |

Exact revisions below describe the inspected checkouts, not necessarily their
remote default branches.

## Repository and workspace inventory

| Repository or root | Local path / reference | Inspected branch and revision | Observed responsibility | Relationship and status | Confidence |
|---|---|---|---|---|---|
| NEXAH Research & Framework | `/Users/tho2020/Documents/GitHub/NEXAH` · `https://github.com/Scarabaeus1031/NEXAH.git` | `main` · `57fdd7ea21944aba19ed2bc3c2a9254b8b20da8c` · clean | Ecosystem governance, research, canonical OLS, maintained Kernel track, applications, Library Registry, Editorial Operating System, long-term record | Canonical ecosystem repository and best current ecosystem front door; Constitution v1.0 is its highest governance document | High |
| NEXAH-ORION | `/Users/tho2020/Documents/NEXH x LLAMA _orion_` · `https://github.com/Scarabaeus1031/NEXAH-ORION.git` | `codex/orion-orientation-operators` · `d34fbb2f99334534f4db89465a29f8bdb16d14d3` · working tree already modified | Certified deterministic navigation/processing repository; ORION architecture, expression work, architecture plates, POA designs and evidence | Independent repository governed across the ecosystem by the NEXAH Constitution; current home of POA-001 and POA-002 | High |
| Connected NEXAH checkout | `NEXAH-ORION/.workspace/repositories/NEXAH` → `/Users/tho2020/Documents/GitHub/NEXAH` | Actual `57fdd7ea…`; manifest declares `main` at `9f79bb06210402c40c9ef7d9937ca00d86c092b1` read-only | Connected Core/Framework authority for the ORION workspace | The symlink target and declared pin differ; no pin was changed in this review | High for fact; unresolved compatibility meaning |
| NEXAH Framework CI checkout | `NEXAH-ORION/.workspace/repositories/NEXAH-framework-ci` | `codex/limit-actions-permissions` · `105074f88573f0d091fa9a56ee858d20a5aac877` · clean | A second checkout of the same NEXAH remote for CI-oriented work | Operational duplicate, not a separate ecosystem authority and not declared in `workspace.yaml` | High |
| NEXAH Experience | `NEXAH-ORION/.workspace/repositories/nexah-experience` · `https://github.com/Scarabaeus1031/NEXAH-Experience.git` | `codex/dependency-maintenance` · `7473736ff5e6077fda41e7302b041e79e57673e3` · clean | Source for `nexah.de`: public presentation, Library, Living Atlas, Laboratory, Reading Spaces, and public onboarding | Public/intellectual entrance; does not own OLS semantics, ORION, or the Human Workspace | High for source role; live deployment documented, unverified |
| NEXAHEDRON | `/Users/tho2020/Documents/NEXAHEDRON` | `codex/phase-i-2-vertical-slice` · `f273ae5009b15f5f7606b494276b906fc72cfe2b` · clean · no Git remote | Human-facing reference Workspace and Laboratory application for `nexahedron.com` | Release-candidate source is local; ORION is pinned upstream; a private Sites deployment and pending public/DNS work are documented | High for local role; medium for deployment; repository identity unresolved |
| NEXAH Library cleanup/workbench | `/Users/tho2020/Documents/ARE.NA LIBRARY CLEANUP` | Unborn `main`; no commit or remote; 39 status entries | Local Library Registry cleanup, reader-journey reviews, phase work, and supporting scripts | Evidence supports a staging/workbench role. `workspace.yaml` separately describes a future independent Library repository as remote-pending | Medium; repository authority unresolved |
| Older NEXAH clone | `/Users/tho2020/Documents/NEXAH_REPO_CLONE` · NEXAH remote | `main` · `a0539b9a951de557fbf71f4b0a3526708f3cbecc` · 1 status entry | Earlier layout with `FRAMEWORK`, `ENGINE`, `BUILDER_LAB`, `DISCOVERY_ENGINE`, and related roots | Historical/legacy checkout of the NEXAH lineage; it must not compete with the clean canonical checkout | High |
| NEXAH-CODEX | `/Users/tho2020/Documents/GitHub/NEXAH-CODEX` · remote points to the NEXAH repository | `main` · `cc1962237940867becb7beb7d4d9fb9f6b613253` · 22 status entries | Frozen 2025 exploratory Codex, module registry, glossary, systems, and visuals | README identifies it as an exploratory archive; remote identity is misleading for a separate local lineage | High for historical status; low for remote intent |
| Scarabaeus1033 System v1.0 | `/Users/tho2020/Documents/GitHub/Scarabaeus1033-System-v1.0` · its own GitHub remote | `main` · `c5d030482a13082fededc42a60e04de2c503a111` · 1 status entry | `MANIFEST.md` and broad Scarabaeus modules | Adjacent historical lineage; no inspected current NEXAH authority delegates responsibility to it | Low |
| NEXAH Outreach | `/Users/tho2020/Documents/NEXAH OUTREACH` | Unborn `main`; no commit or remote; 3 status entries | Outreach operating-system notes and contact/resonance CSVs | Local operational planning, outside technical and semantic authority | Medium |
| Undocumented duplicate links | `NEXAH-ORION/.workspace/repositories/NEXAH 2` and `NEXAH 3` | One resolves to the current NEXAH checkout; one points into a temporary pin path | Local connection artifacts | Not declared by `workspace.yaml`; should be recorded before any cleanup | Medium |

`/Users/tho2020/Documents/trascripe audio` was screened because it is a Git
root in the search area, but no reliable NEXAH responsibility was established;
it is excluded from the ecosystem map.

## Connected workspace declaration

`NEXAH-ORION/workspace.yaml` declares repositories to be independent and
records:

- `nexah-core` as a pinned, read-only deterministic authority;
- `nexah-orion` as the active reasoning/orchestration repository;
- `nexah-library` as ownership-confirmed but remote-pending; and
- `nexah-builder-hub` as repository-identity-pending.

It also declares local zones for architecture, research, experiments, runs,
reviews, releases, and archive. The declaration is useful operational evidence,
but it is local workspace configuration, not ecosystem governance. Two
additional checkouts are present but absent from the declaration. The Core
revision mismatch is therefore a workspace integrity issue, not a reason to
reinterpret the NEXAH repository.

## Public and external surfaces

| Surface | Canonical reference | Observed role | Verification and status | Confidence |
|---|---|---|---|---|
| `nexah.de` | `https://nexah.de` | Public and intellectual entrance; Visitor Guide; public Library, Living Atlas, Laboratory, and Reading Spaces | Source checkout and an immutable OVH upload package are local. Upload/deployment is documented in handoffs; live state was not independently verified | High role; medium state |
| `nexahedron.com` | `https://nexahedron.com` | Human-facing Workspace and reference Orientation Session | Local application and release-candidate revision verified. Private Sites deployment, custom-domain attachment, DNS and public-access steps are documented; public reachability unverified | High role; medium state |
| GitHub | `https://github.com/Scarabaeus1031/NEXAH` and documented ORION/Experience remotes | Canonical versioned source, specifications, evidence, releases, and repository metadata | NEXAH public page and local remotes verified. ORION/Experience public reachability was not independently confirmed in this review | High for NEXAH; medium for the others |
| Are.na | `https://www.are.na/nexah-scarabaeus1031/channels` | Live visual source content, channel descriptions, and editorial sequence for the public Library | Profile/reference exists; full live channel state was not extracted. NEXAH documentation explicitly separates Are.na visual authority from Registry identity authority | Medium |
| NEXAH Library Registry | `NEXAH/LIBRARY/` | Stable NEXAH Work/Edition/Operator identity and classification | Verified locally; the Registry, not Are.na or a website, is the stated identity authority | High |
| Local release handoff | `NEXAH-ORION/.workspace/releases/` | Operational publication handoff for `nexah.de`, ORION, and NEXAHEDRON | Verified locally; dated 2026-07-24 and more current than the NEXAH root launch status | High |

## Information-space inventory

| Space | Current location(s) | Intended and observed contents | Overlap, gap, or unclear ownership | Likely future home |
|---|---|---|---|---|
| Research | `NEXAH/RESEARCH/`; applied work in `NEXAH/APPLICATIONS/`; historical/prototype work in `EXPERIMENTAL/` and `PROTO_CORE/`; local ORION source material | Foundations, core concepts, JANUS, validation, findings, applied cases, figures, translations, theory, notes, and history | Research and applied implementation coexist but are locally indexed and status-labelled. Research does not automatically become released semantics | Remain in NEXAH Research; domain work remains in Applications when that is its current accountable context |
| Ecosystem architecture | `NEXAH/ARCHITECTURE/`, especially `README.md` and `SYSTEM_STATE.md` | Six-responsibility model, current implementation state, methods, boundaries, archived diagrams | Does not index the newest ORION architecture distillation or POA-001/002; current cross-repository revision state is scattered | NEXAH `ARCHITECTURE/` remains owner; a future root Desk links current states without copying architecture |
| ORION architecture | `NEXAH-ORION/docs/architecture/`, ADRs, releases, plates | Frozen ORION model, representation and transition architecture, operator and LYRA material, recent informative NEXAH/OLS reviews | Rich but repository-local; recent review documents can look ecosystem-authoritative despite informative status | Remain in ORION; ecosystem Desk links its canonical index and frozen baseline |
| OLS | `NEXAH/ORIENTATION_LANGUAGE/` | Published OLS 1.0 semantic authority: OLS-0 conventions, OLS-1 base language, OLS-2 declarations/operator contracts, OLS-3 profiles/composition, OLS-4 derivations/transitions, OLS-5 conformance/testing, OLS-6 extensions/versioning/governance, companion OLS-I and releases | ORION has informative extraction and machine-readable architecture reviews, but they do not replace the released suite | Canonical OLS remains in `NEXAH/ORIENTATION_LANGUAGE/` |
| OLI | No exact current `OLI` term found in the inspected Markdown | No verified definition, release, or owner | `OLS-I` exists as a companion designation, but the review has no evidence that `OLS-I` and `OLI` are synonyms | Do not create or assign a home until the term is defined by existing authority |
| Grammar | Released OLS suite, particularly OLS-1 through OLS-4; older grammar visuals in NEXAH archives and Desktop | Normative grammar in text; conceptual/historical grammar tables and images elsewhere | Visual and older terminology can be mistaken for normative grammar | Released OLS specification only; visuals remain explicitly derived or historical |
| Operators | `NEXAH/ORIENTATION_LANGUAGE/SPECIFICATION/OLS-2`; NEXAH Library controlled Operator Concepts; ORION operator architecture; research operators such as JANUS | Different operator scopes: semantic contracts, editorial concepts, executable ORION capabilities, and research mechanisms | Shared word, distinct authorities. These must not be collapsed into a universal registry | Each existing authority retains its scoped definitions; cross-links state scope |
| Vocabulary | OLS suite and registries; NEXAH glossary material; historical `NEXAH-CODEX/NEXAH_GLOSSARY_DUAL.md` | Normative OLS terms, local repository vocabulary, and historical terminology | No single glossary should silently override OLS or repository-local contracts | OLS vocabulary in OLS; ecosystem Desk points to scoped glossaries |
| Formats | OLS carriers/representations where adopted; ORION contracts and representation specifications; implementation JSON/SVG/Markdown artifacts; historical UDF/XVA source material outside canonical repos | Semantic carriers, implementation schemas, publication forms, and experimental formats | “Format” currently spans normative, implementation, and historical material; no evidence supports one universal format authority | OLS owns only adopted semantic format rules; implementation formats remain with their owner; historical formats remain research/archive |
| Canonical examples | OLS release examples; NEXAH demonstrator and Network Orientation; ORION examples | Specification examples, maintained demonstrations, and repository-local usage examples | Canonical within scope, not ecosystem-wide proof | Keep beside the authority or implementation they demonstrate |
| Experiments | NEXAH Research/Applications/validation; `NEXAH-ORION/docs/experiments/`; `NEXAH-ORION/examples/poa-*` | Scientific experiments and frozen architecture proof designs | POA index is currently local to ORION and absent from the NEXAH ecosystem navigation | POA design/freeze documents remain in ORION; future Desk adds a link and status |
| Evidence | Research validation records; tests/testkit; POA committed artifacts, checksums, reviews, and negative cases | Scientific evidence, implementation verification, and frozen experimental evidence | Different evidence kinds are correctly separate but not summarized ecosystem-wide | Remain with the claim and experiment; Desk records location and frozen status |
| Freeze reports | `NEXAH-ORION/docs/experiments/POA_001_FREEZE_REPORT.md`, `POA_002_FREEZE_REPORT.md`; other ORION release/review reports | Scope-limited conclusions and frozen boundaries | Present locally but currently untracked in the inspected ORION working tree | Remain in ORION; commit/tag approval is a Phase 0 action |
| Applications | `NEXAH/APPLICATIONS/`; NEXAHEDRON as an independent product; Experience as presentation | Network Orientation, Orientation Translation, power systems, dynamical systems, demos, adapters, navigation prototypes; Human Workspace | Application status ranges from verified illustrative to active research and legacy | Domain applications remain in NEXAH unless independently governed; products retain their repository |
| Kernel / implementation | `NEXAH/nexah/`, `PROTO_CORE/`, tests; ORION `src/` | Maintained Orientation Kernel v0.7, demonstrators/prototypes, independent ORION implementation | “Core” is used for the certified ORION scope, workspace pin role, and older prototype paths; scope must be stated every time | Keep separate implementation owners and use qualified names |
| Runtime | ORION `src/orion_runtime/` and runtime documents; NEXAH implementation runtime paths | Newer ORION runtime work and repository-specific implementation | Not part of POA frozen claims; working-tree state is not a released ecosystem baseline | Owning implementation repository only |
| Books / Library | `NEXAH/LIBRARY/`, `docs/library/atlas-of-atlases/`; Desktop `ARE.NA UPLOADED BOOKS`; Are.na | Canonical identity/metadata, approved reader sequence, public visual content, and a large local source/publishing archive | Desktop source tree is extensive, unversioned, and not a technical specification | Registry and approved sequences stay in NEXAH; source archives require an index, not relocation into specifications |
| Atlas | `NEXAH/docs/library/atlas-of-atlases/` with 72 source images; research/application atlases; Are.na | Reader onboarding atlas plus scientific or application-specific atlases | “Atlas” has editorial and scientific meanings; context is essential | Keep with its owning Library, research, or application context |
| Visual archive | NEXAH maintained assets and architecture visuals; ORION plates; Desktop visual directories; Photos library package | Authoritative companions, current/conceptual visuals, snapshots, generated plots, and unindexed creative material | Local visual archives lack version/status/authority metadata | Link maintained visual indexes; inventory local archives before any curation |
| Public website | NEXAH Experience source and `nexah.de` | Public presentation and onboarding | Deployment status is split between older launch status and newer handoff | Experience repository/source and operations record |
| Laboratory website | NEXAHEDRON and `nexahedron.com` | Human-facing Workspace/Orientation Session | Local source lacks remote; public access and DNS are pending/documented | NEXAHEDRON repository once identity is resolved |
| Onboarding | NEXAH README/Repository Map; Experience Visitor Guide; Kernel `START_HERE`; Library Atlas | Audience-specific entry routes exist | No maintainer route spans repositories, milestones, deployment, and archives | Future NEXAH root `DESK.md`; public onboarding stays on `nexah.de` |
| Glossary | OLS vocabulary, repository-local terms, historical dual glossary | Several scoped vocabularies | Historical glossary can appear current; no ecosystem authority order is summarized | Link scoped glossaries and state authority; do not merge automatically |
| Governance | `NEXAH/GOVERNANCE/` and Constitution v1.0; ORION local cross-repository governance | Adopted ecosystem baseline plus repository procedures | Some README text in the map still describes a constitution review as provisional while the root README says adopted | NEXAH Governance; resolve editorial inconsistency by cross-link, not governance rewrite |
| Deployment | Experience docs; NEXAHEDRON release reports; ORION `.workspace/releases/` | Build, immutable input, OVH, Sites, DNS, smoke-test, and handoff records | Current state is distributed and time-sensitive | Each deployable owns procedure; Desk records current status and latest dated handoff |
| Historical archive | `NEXAH/ARCHITECTURE/archive`, `RESEARCH/HISTORY`, `APPLICATIONS/archive`, `EXPERIMENTAL`, NEXAH-CODEX, old clone, local Desktop roots | Preserved development lineage and prior models | Several local roots look active without a consistent banner/index | Preserve in place until identity and history are recorded; add status/navigation before any move |

## Important visual inventory

| Visual set | Location | Meaning and authority | Currency | Desk treatment |
|---|---|---|---|---|
| Ecosystem front-door set | `NEXAH/assets/readme/` | Maintained README companions for ecosystem, cycle, infrastructure, laboratory, and JANUS | Current to the inspected NEXAH front door; Markdown remains authority | Link the ecosystem map and front-door image |
| NEXAH current architecture visuals | `NEXAH/ARCHITECTURE/visuals/current/` | Current conceptual architecture companions | Dated/current by repository classification, not independent authority | Link through `ARCHITECTURE/README.md` |
| OLS 1.0 ecosystem visual | `NEXAH/ORIENTATION_LANGUAGE/VISUALS/CANONICAL/orientation-language-ecosystem-ols-1.0.0.png` | Canonical visual companion to the OLS release | Release-compatible; text/release documents remain authority | Link from the OLS row |
| ORION Architecture Plates | `NEXAH-ORION/docs/architecture/plates/` | Ten frozen visual companions with SVG sources, checksums, and named authoritative Markdown | Canonical within ORION documentation v0.3.0-dev.0 / architecture freeze | Link the plate index, not copied images |
| Editorial Operating System visuals | `NEXAH/EDITORIAL_OPERATING_SYSTEM/visuals/` | Architecture, dated snapshot, vision, and history categories explicitly distinguished | Mixed by design | Link its visual index; never flatten statuses |
| Atlas of Atlases | `NEXAH/docs/library/atlas-of-atlases/images/` | Approved reader sequence and supplements | Current Library onboarding artifact | Link the Atlas README, not raw image folder |
| Desktop ecosystem and grammar visuals | `/Users/tho2020/Desktop/NEXAH ECOSYSTEM VISUALS`, `/Users/tho2020/Desktop/GRAMMAR of ORIENTATION_ORION_LYRA` | Unversioned conceptual/status images | Currentness and authority unverified | Record as a visual source archive; do not link as canonical |
| Desktop uploaded books | `/Users/tho2020/Desktop/ARE.NA UPLOADED BOOKS` | Large publication/source archive containing books, atlases, handbook, research guide, and whiteboards | Publication status varies and is not encoded consistently in the filesystem | Index against Library Registry/Are.na before any curation |
| Photos library package | `/Users/tho2020/Documents/NEXAH - TH - Visuals.library` | Opaque local visual collection | Unversioned and not semantically indexed in this review | Archive reference only |

A newer canonical ecosystem visual may eventually be useful, but only after the
textual source-of-truth and revision ledger are settled. No new visual is
needed to complete this review.

## Unresolved questions

1. Which exact NEXAH revision is approved for ORION compatibility:
   `workspace.yaml`'s `9f79bb…` or the connected checkout's `57fdd7…`?
2. Are POA-001 and POA-002 intentionally uncommitted in the inspected ORION
   working tree, or is a freeze commit/tag pending?
3. Does `OLI` name an existing concept outside the inspected Markdown, or was
   `OLS-I` intended? The terms must not be equated without evidence.
4. Will the Library remain an authority area inside NEXAH, or is the
   remote-pending independent repository still intended? The filesystem does
   not establish a separate canonical remote.
5. What is the canonical repository identity for NEXAHEDRON? Its source has no
   remote and the handoff says GitHub creation remains pending.
6. Is `nexah-builder-hub` still intended as an independent application? Only a
   pending workspace declaration and local source material were found.
7. Which deployment record is operationally current? The 2026-07-24 final
   handoff is newer than `NEXAH/LAUNCH_STATUS.md` and conflicts with several of
   its pending-GitHub statements.
8. Which local Desktop book and visual roots correspond to Registry Works,
   published Are.na channels, drafts, or superseded material?
