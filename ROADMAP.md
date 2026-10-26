# Workspace Roadmap

## Phase 1: Monorepo Consolidation (Completed)
- Initialize monorepo at `candlestixxx/workspace`.
- Sanitize submodules (removed 94 forks, kept 14 original repos).

## Phase 2: Synchronization & Reconciliation (Completed)
- Comprehensive dual-direction merge across all submodules.
- Upstream sync (where applicable).
- Conflict resolution and feature preservation.

## Phase 3: Build & Deployment Automation (In Progress)
- ✅ Disk freed to 22GB as of v1.0.45 — full fetch re-attempted; large-repo fetch (bgtk/HyperNexus) still fails with "invalid index-pack output" (network, not disk).
- [x] Global versioning and changelog tracking (v1.0.23).
- [x] Submodule structural map maintained.
- [x] Feature branch divergence tracking and reconciliation across 24 submodules.
- [x] Forward-merged 12 feature branches across 11 submodules (v1.0.23).
- [x] Reverse-merged primary branches into 35+ feature branches (v1.0.23).
- [x] Forward-merged 7 feature branches across 7 submodules (v1.0.38); skipped 3 redundant/regressive AI branches.
- [x] Forward-merged 9 feature branches across 7 submodules (v1.0.42) — brokeragentworkflow v0.46-0.48, excel Next.js UI, forclosureworkflow dashboard/S3, re-agent v2.14-2.15, skillzhub Edge/WebCrypto + dependabot, techno DM v5.1-5.3, pse v1.5.0 Gradio/Docker/audio-reactive; skipped 4 redundant/competing branches.
- [x] v1.0.47: fast-forwarded 5 submodules (realestatecrm +34, forclosureworkflow +2, socialmediacontentplanner +2, LegacyLeads +2, re-agent +1) + forward-merged skillzhub dependabot 8-pkg bump.
- [x] v1.0.48: HyperNexus v1.0.3→v1.0.21 (go/NUL resolved upstream; local v1.0.3 work preserved in local-v1.0.3-work); fast-forwarded 7 submodules (realestatecrm +87, socialmediacontentplanner +11, leadG +10, forclosureworkflow +8, re-agent +6, LegacyLeads +4, explorerexedecompiled +2).
- [x] hyperharness recovery from broken state (v1.0.23).
- [x] Documentation foundation: VISION.md, MEMORY.md, DEPLOY.md, IDEAS.md created (v1.0.23).
- [x] Validate all execution scripts across submodules.
- [ ] Standardize CI/CD across submodules.
- [ ] Execute full system build/deployment sequence.

## Phase 4: Expansion (In Progress)
- [x] Re-add relevant submodules: Prank-Deck-AI, bobgui, hyperharness (v1.0.19).
- [x] Add aicrm (agentic real estate CRM) + HyperNexus orchestration kernel (v1.0.35).
- [x] Add psychedelic-speech-engine (speech-to-music video pipeline) (v1.0.36).
- [x] Add suno-api (local Suno music backend for psychedelic-speech-engine) (v1.0.37).
- [ ] Optimize monorepo performance and disk space (hyperharness at 900MB+).
- [ ] Implement automated periodic submodule reconciliation tooling.
- [ ] Clean up hyperharness nested submodules (34 submodules, many stale/archived).

## Phase 5: Stabilization
- [ ] Standardize CI/CD across all 24 submodules.
- [ ] Schedule periodic reconciliation (weekly automated check).
- [ ] Monitor hyperharness and bobgui for upstream robertpelloni changes.
- [ ] **Blocked:** complete upstream merge for bobgui→bgtk (1472 behind) and hyperharness (146 behind) — large-repo fetch still fails (`invalid index-pack output`) even with 22GB free (v1.0.45); need LFS/partial-clone/proxy fix.
- [ ] Consider sparse checkout optimization for contributors needing only specific submodules.
- [ ] Explore cross-submodule integration layer (message bus between real estate projects).
