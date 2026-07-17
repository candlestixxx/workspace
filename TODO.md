# Workspace TODO

## High Priority
- [x] Add all missing repos as submodules (now 20: Prank-Deck-AI, bobgui, hyperharness added v1.0.19).
- [x] Execute forward merge cycle v1.0.19: socialmediacontentplanner (docker-compose fix), realestateprototype (Next.js 14 migration).
- [x] Execute reverse merge cycle v1.0.19: socialmediacontentplanner foundation-build, crowdsourced_dance_club jules-v0.2.0.
- [x] Emergency recovery: restore 15 submodule working trees (v1.0.19).

## Maintenance
- [x] Review root execution scripts — none present at root level.
- [ ] Monitor submodule drift and schedule periodic reconciliations.
- [ ] Add AI tool session directories to `.gitignore` in relevant submodules.
- [x] Rebuild submodule structural map after pointer changes (v1.0.19).

## Long Term
- [ ] Implement automated "Intelligent Merge" tool for future syncs.
- [ ] Standardize CI/CD across 20 submodules.
- [ ] Explore sparse checkout for large monorepo clones.
