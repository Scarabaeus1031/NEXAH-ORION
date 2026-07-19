# Release Checklist

## Scope and ownership

- [ ] Release scope has one named owner.
- [ ] No external repository change is implied by this release.
- [ ] Cross-repository changes have recorded approvals.
- [ ] Postponed work is explicit.

## Decisions and documentation

- [ ] All included architecture decisions are accepted ADRs.
- [ ] Superseded ADRs link to their replacements.
- [ ] Current architecture and contributor documentation agree.
- [ ] `CHANGELOG.md` and release notes are updated.

## Version and compatibility

- [ ] `VERSION` follows the versioning policy.
- [ ] Tag and `VERSION` will match.
- [ ] Compatibility matrix pins every tested external revision.
- [ ] Breaking, deprecated and unknown surfaces are named.

## Verification

- [ ] `./scripts/check-workspace` passes.
- [ ] `./scripts/release-check` passes.
- [ ] Required future code, contract and acceptance checks pass.
- [ ] Secrets, model weights, private data and raw runs are absent.

## Publication

- [ ] Release notes state capabilities and non-capabilities.
- [ ] Annotated tag is created from the reviewed commit.
- [ ] Published artifacts are traceable to that tag.
- [ ] Rollback or corrective-release procedure is known.
