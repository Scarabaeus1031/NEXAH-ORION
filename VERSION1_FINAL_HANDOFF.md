# NEXAH Version 1 — Final Handoff

- Status date: 2026-07-24
- Architecture: frozen
- Version 1 scope: frozen
- Repository work: complete for the reviewed working copies; ORION freeze prepared
- Publication decision: **NO-GO until the Remaining Owner Actions are complete**

This handoff records the final repository state. It introduces no architecture,
capability, roadmap or Version 2 work. Every remaining item below requires a
release-owner decision, an immutable release revision, deployment
infrastructure or factual legal confirmation.

## Repository Status

### NEXAH

- Working copy:
  `.workspace/repositories/NEXAH-framework-ci`
- Upstream:
  `https://github.com/Scarabaeus1031/NEXAH.git`
- Reviewed base revision:
  `cc402e8adca47baa7e86b86e4e074d5c6eb9a402`
- Branch:
  `codex/limit-actions-permissions`
- Repository role:
  Research & Framework repository.
- Implemented:
  the README front door now identifies NEXAH, its scientific responsibility,
  its non-responsibilities and the public transitions to nexah.de, ORION and
  NEXAHEDRON.
- Existing public essentials verified:
  README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, LICENSE, LICENSE-DOCS,
  LICENSES and CITATION.
- Verification:
  `302 passed`; the reported dependency deprecation warnings do not represent
  repository test failures.
- Formatting:
  `git diff --check` passes.
- Remaining repository work:
  none before release selection.
- Release state:
  the reviewed README change is not yet committed or published.

### ORION

- Working copy:
  repository root containing this document.
- Upstream:
  `https://github.com/Scarabaeus1031/NEXAH-ORION.git`
- Release revision:
  the immutable commit containing this handoff and the ORION Version `1.0.0`
  release state.
- Branch:
  `codex/orion-orientation-operators`
- Repository role:
  certified deterministic Core.
- Implemented:
  the README now states the certified Version 1 boundary without presenting
  historical Runtime, Gateway or LYRA work as certified Core responsibility.
  `CITATION.cff` is present and is enforced by the workspace check. The
  Phase VII README corpus entry was rebound to the approved public front-door
  text and its exact SHA-256 revision.
- Existing public essentials verified:
  README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, LICENSE, LICENSE-DOCS,
  LICENSES and release documentation.
- Verification:
  architecture consistency, frozen-responsibility boundaries, all ten
  Architecture Plates and workshop checks pass. The focused Phase VII corpus
  suite passes `7/7`; all 26 certified proof scripts replay byte-identically.
- Full test result:
  the isolated ORION suite passes `546` tests with `11` intentional skips:
  one opt-in Ollama integration and ten downstream pin checks. In the connected
  workspace, those ten checks stop only because NEXAHEDRON still pins the
  preceding ORION revision and fingerprint.
- Core dependency:
  the workspace check passes against a clean checkout of the declared NEXAH
  Core revision
  `9f79bb06210402c40c9ef7d9937ca00d86c092b1`.
- Formatting:
  `git diff --check` passes.
- Remaining repository work:
  none. After the immutable release commit, dependent repositories must update
  the ORION pin and fingerprint and replay their complete verification.
- Release state:
  Version `1.0.0` release commit prepared; tag and publication remain owner
  actions.

### Experience

- Working copy:
  `.workspace/repositories/nexah-experience`
- Upstream:
  `https://github.com/Scarabaeus1031/NEXAH-Experience.git`
- Reviewed base revision:
  `82240753895e23b7cc9bdc66a14161ca11e49cf8`
- Branch:
  `codex/dependency-maintenance`
- Repository role:
  public and intellectual website implementation for nexah.de.
- Implemented:
  the public front door, header, footer, ecosystem placement, Visitor Guide,
  accessibility page, imprint and privacy presentation follow the approved
  editorial model. Stale editorial assertions in the site tests were replaced
  with the approved Version 1 public language. `CITATION.cff` is present.
- Verification:
  the complete pinned-source verification succeeds against the documented
  immutable ORION source revision
  `2610de440c71f8d5901e22f88239296716efdc5b`.
  Astro reports zero errors, warnings and hints; `55` tests pass; `206` pages
  build; no broken internal links are reported.
- Formatting:
  `git diff --check` passes.
- Remaining repository work:
  none before release selection.
- Release state:
  the reviewed editorial working tree is not yet committed, published or
  deployed.

### NEXAHEDRON

- Working copy:
  `/Users/tho2020/Documents/NEXAHEDRON`
- Upstream:
  no Git remote is configured.
- Reviewed base revision:
  `95e3523eacd1eeb583ad51514651c4f990c936f5`
- Branch:
  `codex/phase-i-2-vertical-slice`
- Repository role:
  Human-facing reference implementation.
- Implemented:
  repository front-door language, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY,
  software and documentation licensing, license inventory, citation metadata,
  contact, imprint, privacy, accessibility, robots, sitemap, favicon, social
  metadata, 404 handling, Visitor Guide, public footer and the Human-owned
  Orientation Record path are present. The empty post-confirmation state has
  been removed from the reviewed journey.
- Verification:
  application checks and production build pass; `69` application tests and
  `4` real ORION Gateway integration tests pass. The anonymous local journey
  reaches the Human-owned Orientation Record and crosses the ORION boundary
  only after explicit confirmation.
- Formatting:
  `git diff --check` passes.
- Remaining repository work:
  the ORION dependency revision and canonical-content fingerprint cannot be
  finalized until ORION has its immutable release commit. No other in-repository
  Version 1 capability is required.
- Release state:
  the repository has no public remote, no immutable release commit and no
  deployed public revision. Its existing readiness report therefore remains
  **NO-GO** for immediate publication.

## Remaining Owner Actions

Only actions that cannot be completed safely from the current repositories are
listed here.

1. **Release owner — approve the exact file set in the remaining downstream
   working trees.** ORION is frozen by the Version 1 release commit. Separate
   unrelated local changes in the other repositories before committing them.
2. **Release owner — choose the remaining public component versions and tag
   names.** ORION is fixed at `1.0.0` with the recommended tag `v1.0.0`; other
   component identities remain owner decisions.
3. **ORION and NEXAHEDRON owners — freeze the final handoff.**
   After the ORION release commit exists, calculate its canonical-content
   fingerprint, update NEXAHEDRON's `docs/upstream/orion-v1/SOURCE.yaml` and
   matching architecture assertion, then rerun both complete suites. This is
   the sole known technical release gate.
4. **NEXAH Core owner — confirm the declared ORION Core dependency.**
   Use a clean checkout of
   `9f79bb06210402c40c9ef7d9937ca00d86c092b1`, or formally approve a replacement
   pin before changing `workspace.yaml`.
5. **Repository owner — create or designate the public NEXAHEDRON repository.**
   Add the remote, repository description, topics, default branch, protection
   rules, security contact and canonical links.
6. **Publishing owner — push the reviewed NEXAH, ORION, Experience and
   NEXAHEDRON commits.** Confirm that every public link targets the published
   repository rather than a local or unavailable destination.
7. **Legal owner — confirm factual legal data.**
   Approve the responsible entity, postal and contact details, hosting
   provider, processing locations, log retention, recipients, copyright
   notices, license references and the canonical maintenance relationship
   between nexah.de and nexahedron.com. Repository text is not legal approval.
8. **Domain and hosting owner — provision nexahedron.com.**
   Confirm DNS, TLS, canonical redirects, hosting ownership and anonymous public
   availability.
9. **Website owner — deploy the exact reviewed Experience revision to
   nexah.de** and confirm that the public Visitor Guide and ecosystem links
   match the release commits.
10. **GitHub organization owner — update the organization profile and repository
    ordering** so that nexah.de is the public entrance, NEXAH is Research &
    Framework, ORION is the certified Core and NEXAHEDRON is the Human-facing
    reference implementation.
11. **Release owner — decide whether the public NEXAHEDRON deployment exposes an
    ORION endpoint.** If none is deployed, the existing unavailable boundary
    must remain explicit and the public claim must stop at the Human-owned
    Orientation Record. No simulated response may replace it.
12. **Release owner — sign the final GO decision** only after the deployed,
    anonymous walkthrough and all immutable-pin checks below pass.

## Deployment Checklist

- [ ] All four reviewed working trees have owner-approved immutable commits;
      ORION is complete when this release commit is selected.
- [ ] Public repository visibility and canonical repository URLs are confirmed.
- [ ] NEXAHEDRON has a configured public remote.
- [ ] ORION is checked against a clean checkout of its declared NEXAH Core pin.
- [ ] NEXAHEDRON is pinned to the final ORION release commit and exact
      canonical-content fingerprint.
- [ ] Experience is generated from its documented immutable source pin.
- [ ] The exact reviewed Experience revision is deployed to nexah.de.
- [ ] The exact reviewed NEXAHEDRON revision is deployed to nexahedron.com.
- [ ] Production environment variables contain no local paths or development
      endpoints.
- [ ] If ORION is exposed, its endpoint, media type and failure behavior match
      the reviewed boundary; otherwise unavailability remains explicit.
- [ ] DNS, TLS, canonical host redirects and canonical URLs are correct.
- [ ] `robots.txt`, sitemap, favicon, page titles, metadata, OpenGraph data and
      404 behavior are verified on the deployed hosts.
- [ ] Contact, imprint, privacy, accessibility, copyright, licensing and
      security-disclosure links are reachable from both public footers.
- [ ] The legal owner has confirmed all deployment-specific facts.
- [ ] Every ecosystem map and contextual front door answers: where am I, what
      does this place own, and where do I continue?
- [ ] All outbound repository, Visitor Guide, Position Paper, Library, ORION
      and NEXAHEDRON links are checked from an unauthenticated browser.
- [ ] Mobile navigation and keyboard-only navigation are checked on the hosted
      revisions.
- [ ] No unpublished, private or localhost URL appears on a public surface.
- [ ] Hosted logs contain no secrets or unexpected personal material.

## Release Checklist

- [ ] The Public Release Claim is byte-identical wherever it is reproduced.
- [ ] The Version 1 Release Manifest names the exact public commit for every
      participating repository.
- [ ] Component version metadata agrees with the owner-approved release names.
- [ ] Changelogs and release notes describe only implemented Version 1 scope.
- [ ] NEXAH, ORION, Experience and NEXAHEDRON repository front doors state role,
      non-role, maturity and next destination consistently.
- [ ] NEXAH full test suite passes on its release commit.
- [ ] ORION `./scripts/release-check` passes on the final release
      commit with clean, declared dependencies.
- [ ] Experience `pnpm verify` passes from the pinned source revision.
- [ ] NEXAHEDRON checks, production build, application tests and real Gateway
      integration tests pass after the final ORION pin update.
- [ ] `git diff --check` passes and every release repository is clean.
- [ ] Canonical proofs and fingerprints are replayed from fresh clones.
- [ ] The anonymous path succeeds:
      discover NEXAH → understand the ecosystem → choose a path → begin an
      Orientation → reach the Human-owned Orientation Record → inspect the
      Version 1 limits → return to the ecosystem.
- [ ] Release archives contain required licenses, notices and citation files.
- [ ] Public tags/releases are created from the verified commits.
- [ ] Release notes link the Public Release Claim, Visitor Guide, Position
      Paper, protocol, governance and repository-specific verification.
- [ ] A final post-publication link and smoke check is recorded.
- [ ] The release owner records **GO**.

## Recommended Order

1. Review and separate the current changes in each working tree.
2. Approve component version and tag names.
3. Commit and verify NEXAH.
4. Commit ORION, verify it against the clean declared NEXAH Core pin and record
   the final ORION commit.
5. Bind NEXAHEDRON to that ORION commit and canonical-content fingerprint.
6. Run the complete ORION and NEXAHEDRON regression suites until the immutable
   cross-repository gate is green.
7. Commit and verify NEXAHEDRON; create and configure its public repository.
8. Commit and verify Experience from its immutable source pin.
9. Confirm legal and operational facts.
10. Publish all repositories and update the GitHub organization front door.
11. Deploy nexah.de and nexahedron.com from the exact reviewed commits.
12. Execute the anonymous hosted walkthrough, link check, accessibility check
    and canonical-URL check.
13. Populate the Release Manifest with final commit identities and
    fingerprints.
14. Create the public Version 1 tags/releases.
15. Perform the post-publication smoke check and record the final **GO**.

Until steps 1–13 are complete, the repositories are release-candidate working
copies rather than a reproducible public Version 1 release.
