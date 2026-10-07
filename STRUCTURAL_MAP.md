# Structural Map — candlestixxx/workspace

| # | Submodule | Path | Remote URL | Current Commit |
|---|-----------|------|-----------|----------------|
| 1 | brokeragentworkflow | brokeragentworkflow/ | https://github.com/candlestixxx/brokeragentworkflow | 49718ba |
| 2 | excel-legacy-leadgen | excel-legacy-leadgen/ | https://github.com/candlestixxx/excel-legacy-leadgen.git | d271c64 |
| 3 | explorerexedecompiled | explorerexedecompiled/ | https://github.com/candlestixxx/explorerexedecompiled.git | 31a4794 |
| 4 | forclosureworkflow | forclosureworkflow/ | https://github.com/candlestixxx/forclosureworkflow.git | b890e53 |
| 5 | leadG | leadG/ | https://github.com/candlestixxx/leadG.git | 1e14cca |
| 6 | p2p_service_marketplace | p2p_service_marketplace/ | https://github.com/candlestixxx/p2p_service_marketplace.git | faf0acb |
| 7 | re-agent-workflow-media-1 | re-agent-workflow-media-1/ | https://github.com/candlestixxx/re-agent-workflow-media-1 | a37c7e9 |
| 8 | realestatecrm | realestatecrm/ | https://github.com/candlestixxx/realestatecrm.git | b967c1c |
| 9 | realestateleadcaller | realestateleadcaller/ | https://github.com/candlestixxx/realestateleadcaller.git | d42a4a2 |
| 10 | realestateprototype | realestateprototype/ | https://github.com/candlestixxx/realestateprototype.git | 6990db1 |
| 11 | skillzhub | skillzhub/ | https://github.com/candlestixxx/skillzhub.git | 92ea2d8 |
| 12 | socialmediacontentplanner | socialmediacontentplanner/ | https://github.com/candlestixxx/socialmediacontentplanner.git | cfc7712 |
| 13 | techno_platform_detroit | techno_platform_detroit/ | https://github.com/candlestixxx/techno_platform_detroit.git | 05fa71e |
| 14 | theta-data-api | theta-data-api/ | https://github.com/candlestixxx/theta-data-api.git | ef15c6f |
| 15 | ultratrader | ultratrader/ | https://github.com/candlestixxx/ultratrader.git | 89e877e |
| 16 | LegacyLeads | LegacyLeads/ | https://github.com/candlestixxx/LegacyLeads.git | ec79893 |
| 17 | crowdsourced_dance_club | crowdsourced_dance_club/ | https://github.com/candlestixxx/crowdsourced_dance_club.git | 0a18ce2 |
| 18 | Prank-Deck-AI | Prank-Deck-AI/ | https://github.com/candlestixxx/prank-deck-ai.git | a85b2b5 |
| 19 | bobgui | bobgui/ | https://github.com/candlestixxx/bobgui.git | 9bea319 |
| 20 | hyperharness | hyperharness/ | https://github.com/candlestixxx/hyperharness.git | 50c8826 |
| 21 | aicrm | aicrm/ | https://github.com/candlestixxx/aicrm.git | c719013 |
| 22 | psychedelic-speech-engine | psychedelic-speech-engine/ | https://github.com/candlestixxx/psychedelic-speech-engine.git | b5fa4d4 |
| 23 | HyperNexus | HyperNexus/ | https://github.com/HyperNexusllc/HyperNexus.git | fc731eb |
| 24 | suno-api | suno-api/ | https://github.com/candlestixxx/suno-api.git | a5d6990 |
| 25 | lumbros.me | lumbros.me/ | https://github.com/candlestixxx/lumbros.me.git | 16261e0 |

**Notes:**
- 25 submodules: 24 under `candlestixxx` + 1 external (`HyperNexusllc/HyperNexus` — aicrm orchestration kernel).
- `crowdsourced_dance_club` has a nested submodule `external/auto_dj_script` (robertpelloni/auto_dj_script @ a47e1d3).
- `HyperNexus` (fc731eb, v1.0.4) has nested submodules: `lumbros.me` (candlestixxx/lumbros.me @ 91b2505), plus optional uninitialized vendor harnesses `vendor/deepseek-harness` and `vendor/grok-build`.
- **lumbros.me** added as a top-level submodule this cycle (was previously only a nested HyperNexus submodule).
- **suno-api**: forked from `gcui-art/suno-api` → `candlestixxx/suno-api` to preserve 5 local Suno-API fix commits (chirp-hawk v6, hCaptcha/Turnstile, media_urls, status=complete wait).
- **robertpelloni upstream tracking** (Step-2 scope):
  - `bobgui` → upstream `robertpelloni/bgtk` (renamed from bobgui); fork is **1472 commits behind** — full fetch fails (`invalid index-pack output`, ~870MB repo).
  - `hyperharness` → upstream `robertpelloni/hyperharness`; fork is **146 commits behind** — full/deepen fetch fails (~1.1GB repo, 34 nested submodules).
  - `crowdsourced_dance_club` → upstream `robertpelloni/crowdsourced_dance_club`; **synced** (fork 5 ahead / 0 behind) → 0a18ce2.
- **HyperNexus remote rewritten**: origin/main (HyperNexusllc/HyperNexus) was force-pushed to a single unrelated commit `1dc334266` containing an invalid Windows path `go/NUL`. Merge is impossible on Windows; local retained at `fc731eb` (6 commits ahead). Needs a Linux/macOS machine to reconcile.
- `hyperharness` requires `--depth 1` for initial clone; `HyperNexus` ~1.9GB; `bgtk` ~870MB.
- `realestatecrm` remote normalized from SSH to HTTPS. Scripts reorganized upstream: `scripts/LOFTY/` → `scripts/integrations/lofty/` (commit 75a1247).
- `realestateprototype` canonical primary branch is `main` (default branch is `master` on remote).

Root remote: `https://github.com/candlestixxx/workspace.git` (main branch)

**Last verified:** 2026-10-07 (v1.0.46) — 25 active submodules; 13 pointers advanced this cycle (8 fast-forwards + 4 forward-merged + realestatecrm re-committed). HyperNexus intentionally pinned at `fc731eb` pending Linux-side reconciliation.
