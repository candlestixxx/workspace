# Workspace TODO

## High Priority
- [x] Push root repository changes (including submodule pointers).
- [x] Verify `warp` and `xrnet` submodule status (initialized and tracked).
- [x] Fix stale `submodules/bobcoin` gitlink in `xrnet`.
- [x] Execute dual-direction intelligent merge across all 16 submodules.
- [x] Fetch all remotes and verify branch reconciliation (v1.0.3).
- [x] Fix submodule tracking — reset 5 submodules from feature-branch `origin/HEAD` to primary branch tracking.
- [x] Repair `xrnet` local main (fast-forwarded to origin/main).
- [ ] Execute full system build/deployment sequence.

## Maintenance
- [ ] Review and update all execution scripts (`start.bat`, `build.bat`) across submodules.
- [ ] Monitor submodule drift and schedule periodic reconciliations.
- [ ] Add AI tool session directories to `.gitignore` in relevant submodules.
- [ ] Rebuild submodule structural map after any pointer changes.

## Long Term
- [ ] Implement a more automated "Intelligent Merge" tool for future syncs.
- [ ] Explore sparse checkout for very large monorepo clones.
