# Workspace TODO

## High Priority
- [x] v1.0.44: commit realestatecrm MyPlus Neighborhood → Lofty pipeline scripts (`b5efa0f`); record stale pointers (psychedelic-speech-engine `b5fa4d4`, suno-api `a5d6990`); push root + realestatecrm. Full fetch deferred (disk 100%, 2.8GB free).
- [ ] **Free up disk** before any full fetch/build (psychedelic-speech-engine 9.1GB working tree is top candidate).
- [x] Add all missing repos as submodules (20: Prank-Deck-AI, bobgui, hyperharness added v1.0.19).
- [x] Execute forward merge cycle v1.0.23: 12 feature branches across 11 submodules.
- [x] Execute reverse merge cycle v1.0.23: 35+ feature branches across 14 submodules.
- [x] Recover hyperharness from broken state (deinit + shallow clone, v1.0.23).
- [x] Create missing documentation: VISION.md, MEMORY.md, DEPLOY.md, IDEAS.md (v1.0.23).
- [x] Commit and push root repo changes (documentation, submodule pointers) — v1.0.37.
- [ ] **Resolve large-repo fetch** (`invalid index-pack output`) to complete robertpelloni upstream merges for bobgui→bgtk (~870MB, 1472 behind) and hyperharness (~1.1GB, 146 behind).

## Maintenance
- [x] Review root execution scripts — none present at root level.
- [ ] Monitor submodule drift and schedule periodic reconciliations.
- [x] Add AI tool session directories to `.gitignore` in relevant submodules.
- [x] Rebuild submodule structural map after pointer changes (v1.0.23).
- [x] Handle local dev modifications: leadG (.gitignore), realestatecrm (notification center + MLS scrub), brokeragentworkflow (.gitignore), aicrm (full buildout) — v1.0.35.
- [ ] Clean up hyperharness nested submodules (34 submodules, many stale).
- [x] Sync robertpelloni upstream for crowdsourced_dance_club + auto_dj_script (v1.0.36).
- [x] Push aicrm v0.13.0 + psychedelic-speech-engine engine implementation (v1.0.36).
- [x] Add suno-api submodule + forward-merge skillzhub dependabot js-yaml bump (v1.0.37).
- [x] Forward-merge 7 feature branches across 7 submodules; skip 3 redundant/regressive (v1.0.38).
- [ ] Review realestateleadcaller merge — verify `src/proxy.ts` removal intentional (replaced by SSE route).
- [x] Integrate Prank-Deck-AI `init-safe-architecture` visual analyzer WITHOUT core-orchestrator deletion (v1.0.39).
- [x] Forward-merge psychedelic-speech-engine workspace-isolation + `--voice` feature branch (v1.0.39).
- [x] Forward-merge psychedelic-speech-engine `--prompt-style` + `--subtitle-style` (v1.2.0) (v1.0.40).
- [x] Push aicrm MLS/Realcomp status sync + property creation fields (v1.0.40).
- [x] Commit aicrm help center / onboarding tour / color wheel WIP (v1.0.39).
- [x] Forward-merge brokeragentworkflow (Broker Workflow Phase 46 + Native Plugin v0.45.0), p2p interactive maps, + 4 docs/maintenance branches; commit aicrm Inngest/agents + pse batch_links + realestatecrm command palette (v1.0.41).
- [x] Forward-merge skillzhub FFprobe Go + dependabot, techno_platform_detroit Event Reviews, socialmediacontentplanner worker, pse BPM shaders; fork suno-api → candlestixxx to preserve 5 Suno fixes (v1.0.43).
- [ ] Free disk space (~12GB left) before attempting bgtk/hyperharness robertpelloni upstream syncs.
- [x] Forward-merge 9 branches across 7 submodules (brokeragentworkflow v0.46-0.48, excel Next.js UI, forclosureworkflow dashboard/S3, re-agent v2.14-2.15, skillzhub Edge/WebCrypto + dependabot, techno DM v5.1-5.3, pse v1.5.0 Gradio/Docker/audio-reactive); skip aicrm Phase2/3 (already in main), realestateprototype Next.js migration, socialmediacontentplanner lockfile churn, Prank-Deck-AI competing branches (v1.0.42).

## Long Term
- [ ] Implement automated "Intelligent Merge" tool for future syncs.
- [ ] Standardize CI/CD across 20 submodules.
- [ ] Explore sparse checkout for large monorepo clones.
- [ ] Consider cross-submodule shared library extraction (@workspace/shared-types).
- [ ] Evaluate Bazel/Nx for unified build orchestration.
