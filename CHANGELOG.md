# CHANGELOG

## [1.0.2] - 2026-05-25
### Changed
- Executed `Intelligent Merge Engine` for `borg` and `jules-autopilot`.
- Resolved complex merge conflicts in `borg` (Healer Service wiring, package manifests, and MCP configuration).
- Reconciled `jules-autopilot` by integrating `origin/main` changes while preserving local feature drift where applicable.
- Validated all submodule branch states; successfully synced 18 project layers.
- Incremented global version to `1.0.2`.

## [1.0.1] - 2026-05-25
### Changed
- Executed `Executive Protocol`: Fetched updates and synced all submodules across the workspace.
- Identified and auto-saved local submodule changes to prevent data loss.
- Synced `realestatecrm` via fast-forward ORT merge.
- Verified structural integrity of nested `.gitmodules` (resolved `hypercode` tracking issues).
- Created global workspace documentation mapping (`STRUCTURAL_MAP.md`, `ROADMAP.md`, `TODO.md`, `HANDOFF.md`, `VERSION.md`).
- Added placeholder global batch scripts (`start.bat`, `build.bat`) to support global compilation/start sequence.