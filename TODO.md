# Workspace TODO

## High Priority
- [x] Add all missing repos as submodules (20: Prank-Deck-AI, bobgui, hyperharness added v1.0.19).
- [x] Execute forward merge cycle v1.0.23: 12 feature branches across 11 submodules.
- [x] Execute reverse merge cycle v1.0.23: 35+ feature branches across 14 submodules.
- [x] Recover hyperharness from broken state (deinit + shallow clone, v1.0.23).
- [x] Create missing documentation: VISION.md, MEMORY.md, DEPLOY.md, IDEAS.md (v1.0.23).
- [x] Commit and push root repo changes (documentation, submodule pointers) — v1.0.35.

## Maintenance
- [x] Review root execution scripts — none present at root level.
- [ ] Monitor submodule drift and schedule periodic reconciliations.
- [x] Add AI tool session directories to `.gitignore` in relevant submodules.
- [x] Rebuild submodule structural map after pointer changes (v1.0.23).
- [x] Handle local dev modifications: leadG (.gitignore), realestatecrm (notification center + MLS scrub), brokeragentworkflow (.gitignore), aicrm (full buildout) — v1.0.35.
- [ ] Clean up hyperharness nested submodules (34 submodules, many stale).

## Long Term
- [ ] Implement automated "Intelligent Merge" tool for future syncs.
- [ ] Standardize CI/CD across 20 submodules.
- [ ] Explore sparse checkout for large monorepo clones.
- [ ] Consider cross-submodule shared library extraction (@workspace/shared-types).
- [ ] Evaluate Bazel/Nx for unified build orchestration.
