# Workspace TODO

## High Priority
- [x] Push root repository changes (including submodule pointers).
- [x] Remove `warp` and `xrnet` submodules (repos deleted from GitHub).
- [x] Fix `origin/HEAD` on 6 submodules pointing to feature branches instead of primary branch.
- [x] Remove dead `upstream` remote from `ultratrader`.
- [x] Reverse-merge main into stale feature branches in `realestatecrm`.
- [x] Synchronize 15 submodules and reconcile feature branches (v1.0.7).
- [ ] Execute full system build/deployment sequence.

## Maintenance
- [ ] Review and update all execution scripts (`start.bat`, `build.bat`) across submodules.
- [ ] Monitor submodule drift and schedule periodic reconciliations.
- [ ] Add AI tool session directories to `.gitignore` in relevant submodules.
- [ ] Rebuild submodule structural map after any pointer changes.

## Long Term
- [ ] Implement a more automated "Intelligent Merge" tool for future syncs.
- [ ] Explore sparse checkout for very large monorepo clones.
