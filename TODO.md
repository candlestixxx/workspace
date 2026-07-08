# Workspace TODO

## High Priority
- [x] Add all 4 missing repos as submodules (LegacyLeads, bobgui, crowdsourced_dance_club, hyperharness).
- [x] Forward-merge 7 feature branches with unique progress into primary branches.
- [x] Reverse-merge main back into 11 stale feature branches across 6 submodules.
- [x] Resolve merge conflicts (explorerexedecompiled).
- [x] Synchronize 19 submodules and reconcile all feature branches (v1.0.8).
- [x] Forward-merge 4 new remote feature branches (forclosureworkflow S3, excel-legacy-leadgen video, leadG tooltips, socialmediacontentplanner RN/RAG) (v1.0.9).
- [x] Reverse-merge main into 12 feature branches across 5 submodules (v1.0.9).
- [x] Execute full system build/deployment sequence (v1.0.9).
- [x] Forward-merge 9 feature branches with unique progress (v1.0.11).
- [x] Reverse-merge primary branches into 24 feature branches across 11 submodules (v1.0.11).

## Maintenance
- [x] Review and update all execution scripts (`start.bat`, `build.bat`) across submodules.
- [ ] Monitor submodule drift and schedule periodic reconciliations.
- [ ] Add AI tool session directories to `.gitignore` in relevant submodules.
- [x] Rebuild submodule structural map after any pointer changes.
- [x] Remove `bobgui` and `hyperharness` submodules (could not clone — 800MB+ timeout / empty repo).
- [x] Forward-merge 6 feature branches with unique progress into primary branches (v1.0.10).
- [x] Reverse-merge primary branches into 7 feature branches across 4 submodules (v1.0.10).

## Long Term
- [ ] Implement a more automated "Intelligent Merge" tool for future syncs.
- [ ] Explore sparse checkout for very large monorepo clones (hyperharness, bobgui are 800MB+).
