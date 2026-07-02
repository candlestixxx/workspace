# Workspace TODO

## High Priority
- [x] Add all 4 missing repos as submodules (LegacyLeads, bobgui, crowdsourced_dance_club, hyperharness).
- [x] Forward-merge 7 feature branches with unique progress into primary branches.
- [x] Reverse-merge main back into 11 stale feature branches across 6 submodules.
- [x] Resolve merge conflicts (explorerexedecompiled).
- [x] Synchronize 19 submodules and reconcile all feature branches (v1.0.8).
- [ ] Execute full system build/deployment sequence.

## Maintenance
- [ ] Review and update all execution scripts (`start.bat`, `build.bat`) across submodules.
- [ ] Monitor submodule drift and schedule periodic reconciliations.
- [ ] Add AI tool session directories to `.gitignore` in relevant submodules.
- [ ] Rebuild submodule structural map after any pointer changes.

## Long Term
- [ ] Implement a more automated "Intelligent Merge" tool for future syncs.
- [ ] Explore sparse checkout for very large monorepo clones (hyperharness, bobgui are 800MB+).
