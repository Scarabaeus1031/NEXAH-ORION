# NEXAH Ecosystem Migration Plan

**Status:** Informative plan; not executed

**Principle:** Establish identity and navigation before relocation.

Every action below requires a separate implementation decision. “Affected
paths” names the likely scope; it does not authorize a write.

## Phase 0 — Freeze and record

| Action | Reason | Affected paths / surfaces | Risk | Dependencies | Reversibility | Order | Human approval |
|---|---|---|---|---|---|---:|---|
| Record pre-change revisions and working-tree states for NEXAH, ORION, Experience, and NEXAHEDRON | A cross-repository map is not reproducible without exact inputs | Repository Git metadata; future Desk | Low | Confirm canonical checkout per repository | Fully reversible documentation | 1 | Yes for canonical designation |
| Commit POA-001 and POA-002 in an isolated, reviewed ORION commit | The inspected frozen artifacts are currently untracked; frozen evidence needs a versioned identity | `docs/experiments/`, `examples/poa-001/`, `examples/poa-002/` | Medium because ORION has unrelated working-tree changes | Re-run replay/checksum checks; separate unrelated runtime work | Commit can be reverted, but published history remains | 2 | Yes |
| Optionally apply explicit POA freeze tags or signed release records | Makes the experimental freeze independently addressable | ORION Git tags/releases | Medium; tags imply stable identity | Approved naming and exact freeze commit | Tags should not be moved; deletion is disruptive | 3 | Yes, required |
| Resolve the connected NEXAH revision mismatch without changing it automatically | ORION declares `9f79bb…`, while the connected checkout is `57fdd7…` | `workspace.yaml`, `.workspace/repositories/NEXAH` | High if compatibility is assumed | Owner selects approved pin or qualifies newer revision | Decision is reversible before publication; pin changes require revalidation | 4 | Yes, required |
| Record the latest verified deployment state | July 22 launch status and July 24 handoff conflict | NEXAH launch status, ORION release handoffs, public surfaces | Medium; external state can change | Owner/operations confirmation | Documentation is reversible | 5 | Yes |
| Preserve checksums of frozen files before navigation edits | Confirms later work did not change frozen evidence | POA and frozen architecture documents | Low | Exact committed freeze set | Fully reversible | 6 | No, if read-only |

## Phase 1 — Navigation only

| Action | Reason | Affected paths / surfaces | Risk | Dependencies | Reversibility | Order | Human approval |
|---|---|---|---|---|---|---:|---|
| Add a concise root `NEXAH/DESK.md` | Provides one maintainer control surface without moving authority | NEXAH root | Low | Phase 0 revision record; approve owner/maintenance rule | Delete/revert file | 1 | Yes |
| Link the Desk from NEXAH README and Repository Map | Makes it discoverable while preserving public entry routes | `NEXAH/README.md`, `REPOSITORY_MAP.md` | Low | Desk approved | Revert links | 2 | Yes |
| Add one source-of-truth and repository-status table to the Desk | Eliminates competing interpretations | Desk only, links to repository-local sources | Low | Canonical sources confirmed | Revert table | 3 | Yes |
| Add a POA milestone index | Makes design, implementation, evidence, and freeze report discoverable | Desk links to ORION paths/revision | Low | POA freeze commit exists | Revert links | 4 | Yes |
| Add a public-surface status section | Makes `nexah.de`, NEXAHEDRON, GitHub, and Are.na responsibilities explicit | Desk links to owning sources/handoffs | Low; state becomes stale | Named update owner and “last verified” date | Revert/update | 5 | Yes |
| Add local archive/workbench references with “non-authoritative” labels | Prevents hidden material from competing with canonical repositories | Desk or a linked local inventory | Low | Paths confirmed; avoid exposing private data publicly | Revert links | 6 | Yes if published |
| Cross-link this review from ORION's reviews index, if one is maintained | Preserves review discoverability without promoting it to architecture | `NEXAH-ORION/docs/reviews/` index only | Low | Review accepted | Revert link | 7 | Yes |

No file move, rename, source copy, digest refresh, pin update, or deployment
belongs in Phase 1.

## Phase 2 — Resolve sources of truth

| Action | Reason | Affected paths / surfaces | Risk | Dependencies | Reversibility | Order | Human approval |
|---|---|---|---|---|---|---:|---|
| Approve the source-of-truth matrix | Makes authority independent of local folder proximity | NEXAH Desk and existing indexes | Medium | Repository-owner review | Amend by recorded decision | 1 | Yes, required |
| Resolve `OLI` terminology | No current definition or owner was found | OLS/architecture navigation only | High if guessed | Locate existing source or explicitly decide it is absent | A bad alias is hard to unwind after publication | 2 | Yes, required |
| Designate the current Library authority and workbench status | Canonical Registry, local unborn repo, and remote-pending declaration conflict | `NEXAH/LIBRARY`, local cleanup repo, `workspace.yaml` | High | Editorial owner and provenance review | Status labels reversible; transfers are not yet authorized | 3 | Yes, required |
| Mark older launch/status documents as superseded by date, not delete them | Prevents stale operational instructions from appearing current | `NEXAH/LAUNCH_STATUS.md`, ORION handoffs | Medium | External status verified | Notice can be revised | 4 | Yes |
| Add qualified terminology guidance for Core/Kernel/Processor | Avoids false equivalence without a rename campaign | Desk and repository maps | Low | Owners confirm scope wording | Reversible | 5 | Yes |
| Mark duplicate historical documents as derived or historical | Reduces competing source-of-truth signals | Identified architecture/status indexes | Medium | Replacement and authority confirmed | Notices reversible | 6 | Yes |

Frozen architecture, the OLS release, and POA content remain unchanged in this
phase.

## Phase 3 — Low-risk relocation

This phase should begin only if navigation and status labels prove
insufficient.

| Action | Reason | Affected paths / surfaces | Risk | Dependencies | Reversibility | Order | Human approval |
|---|---|---|---|---|---|---:|---|
| Move only clearly misplaced current documentation into an existing owner area | Reduce path ambiguity after authority is settled | Exact paths to be proposed individually | Medium | Phase 2 matrix; link audit; Git history plan | Use Git moves and compatibility notes | 1 | Yes, per move |
| Add redirects or compatibility notes for moved links | Preserve citations and onboarding | Former paths and indexes | Low | Approved move list | Reversible | 2 | Yes |
| Separate generated outputs from editable visual sources where not already done | Make provenance clear | Only reviewed visual collections | Medium | Source/derivative inventory and reproducible generation | Usually reversible | 3 | Yes |
| Move superseded local work into a named archive only after provenance capture | Reduce active-looking clutter | Selected local roots, never broad directories | High; data loss/disconnection risk | Backup, manifest, checksums, owner scope | Prefer recoverable move; reversal requires retained paths | 4 | Yes, required |

Do not relocate frozen POAs, OLS releases, Library identities, or repository
roots merely to match the target diagram.

## Phase 4 — Repository boundary cleanup

| Action | Reason | Affected paths / surfaces | Risk | Dependencies | Reversibility | Order | Human approval |
|---|---|---|---|---|---|---:|---|
| Establish NEXAHEDRON remote identity and publish the frozen source revision | Current source has no remote | Local NEXAHEDRON, GitHub | High external state change | Owner creates/approves repository, protection, license, exact commit | Remote publication is not fully reversible | 1 | Yes, required |
| Decide whether Library becomes independent | Workspace declaration and actual authority differ | NEXAH Library, local workbench, possible remote | Very high | Editorial governance, identity migration, link and history plan | Difficult after consumers migrate | 2 | Yes, required |
| Decide whether Builder Hub is still an independent repository | Current declaration is pending and no verified repo was found | Workspace manifest/source material | Medium | Identify current owner and artifacts | Decision reversible before repository creation | 3 | Yes |
| Reconcile or retire duplicate local NEXAH checkouts | Prevent accidental edits against stale lineages | Explicit checked paths only | High if uncommitted content exists | Per-root status, backup, unique-content diff | Prefer archive/trash; do not delete in bulk | 4 | Yes, required |
| Update workspace declaration to match approved relationships | Makes operational configuration truthful | `workspace.yaml` | Medium; pin changes may alter validation | Prior decisions and revalidation | Revertible in Git | 5 | Yes |

No repository split or merge is currently justified. A future change requires
evidence that navigation and explicit ownership cannot maintain the boundary.

## Phase 5 — Public orientation layer

| Action | Reason | Affected paths / surfaces | Risk | Dependencies | Reversibility | Order | Human approval |
|---|---|---|---|---|---|---:|---|
| Confirm audience contract for each surface | Prevents duplicated or competing public authority | `nexah.de`, `nexahedron.com`, GitHub, Are.na | Low | Owners agree roles | Reversible wording | 1 | Yes |
| Verify live deployment state and anonymous access | Documentation is not live-state evidence | Public domains | Medium operational | DNS/TLS/hosting access | Observation is reversible; deployment changes are separate | 2 | Yes for changes |
| Make `nexah.de` the obvious public entrance and link the other surfaces by role | Root README already declares this path | Experience content | Medium editorial | Live verification and link ownership | Revert content | 3 | Yes |
| Link GitHub sources and immutable evidence from public explanations | Makes authority inspectable | Experience/NEXAHEDRON public content | Low | Stable public URLs and revisions | Revert links | 4 | Yes |
| Connect Are.na Works to Registry identities where evidence exists | Makes visual publication traceable without transferring authority | Library docs and public catalog | Medium editorial/provenance | Channel inventory, rights, stable IDs | Mapping can be corrected | 5 | Yes |
| Create a new ecosystem visual only if the approved text map cannot serve the audience | Avoids a second architecture-by-image | NEXAH maintained assets | Medium | Source text, status, author, editable source, review rule | Retire as derived | 6 | Yes |

## Recommended implementation order

1. Obtain approval for the canonical repository/revision list.
2. Create the isolated ORION POA freeze commit and verify it.
3. Resolve the connected NEXAH pin mismatch.
4. Confirm public deployment state.
5. Implement only the Markdown Desk and links.
6. Observe whether navigation solves the problem before approving any move.
7. Resolve Library, NEXAHEDRON, and Builder Hub identities individually.

## Stop conditions

Pause migration if:

- an action would modify frozen OLS, architecture, or POA content;
- a source-of-truth owner is disputed;
- the only copy or provenance of an artifact is uncertain;
- a Git worktree contains unclassified changes;
- a public/live state has not been verified by its owner;
- a move would break immutable references or checksums; or
- “cleanup” would require deleting a broad local root.
