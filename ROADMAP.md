# ROADMAP

## Phase 1: Consolidation (Completed)
- [x] Unify all project submodules under a single monorepo layout.
- [x] Fix broken `.gitmodule` pointers in heavily nested repositories.
- [x] Establish global `.gitignore` and version control structure.

## Phase 2: Feature Branch Resolution (Completed)
- [x] Complete "Intelligent Merge Engine" execution over heavily conflicted projects (`borg`, `jules-autopilot`, `fwber`).
- [x] Rebase and integrate active feature branches.

## Phase 3: Global Build Orchestration
- [ ] Connect `build.bat` to all submodule build pipelines.
- [ ] Connect `start.bat` to orchestrate multiple sub-services concurrently.