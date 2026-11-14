# Structural Map — candlestixxx/workspace

| # | Submodule | Path | Remote URL | Current Commit |
|---|-----------|------|-----------|----------------|
| 1 | brokeragentworkflow | brokeragentworkflow/ | https://github.com/candlestixxx/brokeragentworkflow | a12a677 |
| 2 | excel-legacy-leadgen | excel-legacy-leadgen/ | https://github.com/candlestixxx/excel-legacy-leadgen.git | d271c64 |
| 3 | explorerexedecompiled | explorerexedecompiled/ | https://github.com/candlestixxx/explorerexedecompiled.git | 72262c0 |
| 4 | forclosureworkflow | forclosureworkflow/ | https://github.com/candlestixxx/forclosureworkflow.git | 357b3eb |
| 5 | leadG | leadG/ | https://github.com/candlestixxx/leadG.git | c6f2825 |
| 6 | p2p_service_marketplace | p2p_service_marketplace/ | https://github.com/candlestixxx/p2p_service_marketplace.git | faf0acb |
| 7 | re-agent-workflow-media-1 | re-agent-workflow-media-1/ | https://github.com/candlestixxx/re-agent-workflow-media-1 | 8746bec |
| 8 | realestatecrm | realestatecrm/ | https://github.com/candlestixxx/realestatecrm.git | 9765060 |
| 9 | realestateleadcaller | realestateleadcaller/ | https://github.com/candlestixxx/realestateleadcaller.git | d42a4a2 |
| 10 | realestateprototype | realestateprototype/ | https://github.com/candlestixxx/realestateprototype.git | 6990db1 |
| 11 | skillzhub | skillzhub/ | https://github.com/candlestixxx/skillzhub.git | 00f7885 |
| 12 | socialmediacontentplanner | socialmediacontentplanner/ | https://github.com/candlestixxx/socialmediacontentplanner.git | 10b09e5 |
| 13 | techno_platform_detroit | techno_platform_detroit/ | https://github.com/candlestixxx/techno_platform_detroit.git | 8231ad6 |
| 14 | theta-data-api | theta-data-api/ | https://github.com/candlestixxx/theta-data-api.git | ef15c6f |
| 15 | ultratrader | ultratrader/ | https://github.com/candlestixxx/ultratrader.git | 89e877e |
| 16 | LegacyLeads | LegacyLeads/ | https://github.com/candlestixxx/LegacyLeads.git | a8c4e3f |
| 17 | crowdsourced_dance_club | crowdsourced_dance_club/ | https://github.com/candlestixxx/crowdsourced_dance_club.git | 27a95d7 |
| 18 | Prank-Deck-AI | Prank-Deck-AI/ | https://github.com/candlestixxx/prank-deck-ai.git | a85b2b5 |
| 19 | bobgui | bobgui/ | https://github.com/candlestixxx/bobgui.git | 9bea319 |
| 20 | hyperharness | hyperharness/ | https://github.com/candlestixxx/hyperharness.git | 50c8826 |
| 21 | aicrm | aicrm/ | https://github.com/candlestixxx/aicrm.git | c719013 |
| 22 | psychedelic-speech-engine | psychedelic-speech-engine/ | https://github.com/candlestixxx/psychedelic-speech-engine.git | b5fa4d4 |
| 23 | HyperNexus | HyperNexus/ | https://github.com/HyperNexusllc/HyperNexus.git | e7aba5994 |
| 24 | suno-api | suno-api/ | https://github.com/candlestixxx/suno-api.git | a5d6990 |
| 25 | lumbros.me | lumbros.me/ | https://github.com/candlestixxx/lumbros.me.git | 16261e0 |
| 26 | unitedbeats | unitedbeats/ | https://github.com/UnitedBeatsLLC/unitedbeats_site.git | 3d777a1 |
| 27 | pulse-dashboard | pulse-dashboard/ | https://github.com/candlestixxx/pulse-dashboard.git | efd1c92 |
| 28 | HyperNexus VRL-1 | HyperNexus VRL-1/ | https://github.com/candlestixxx/HyperNexus-VRL-1.git | 0ab941f |

**Notes:**
- 28 submodules: 26 under `candlestixxx` + 1 external (`HyperNexusllc/HyperNexus`) + 1 external (`UnitedBeatsLLC/unitedbeats_site.git`).
- `HyperNexus VRL-1`: Virtual Routing Layer 1 - Universal Multi-Tenant API Gateway and Radial Vector Secret Vault commercialized for United Beats.
- `pulse-dashboard`: Real-time system monitoring dashboard.
- `unitedbeats`: United Beats LLC flagship site and media engine.
- `crowdsourced_dance_club` has a nested submodule `external/auto_dj_script` (robertpelloni/auto_dj_script @ a47e1d3).
- `HyperNexus` (8445980, v1.0.21) has a nested gitlink `lumbros.me` (candlestixxx/lumbros.me @ 16261e0); the old `vendor/deepseek-harness` + `vendor/grok-build` nested submodules were dropped in v1.0.21.
- **lumbros.me** added as a top-level submodule this cycle (was previously only a nested HyperNexus submodule).
- **suno-api**: forked from `gcui-art/suno-api` → `candlestixxx/suno-api` to preserve 5 local Suno-API fix commits (chirp-hawk v6, hCaptcha/Turnstile, media_urls, status=complete wait).
- **robertpelloni upstream tracking** (Step-2 scope):
  - `bobgui` → upstream `robertpelloni/bgtk` (renamed from bobgui); fork is **12,833 commits behind** (v1.0.49 count; full GTK upstream, ignored per upstream-feature clause) — full fetch fails (`invalid index-pack output`, ~870MB repo).
  - `hyperharness` → upstream `robertpelloni/hyperharness`; fork is **169 commits behind** (v1.0.49 count; ignored per upstream-feature clause, monitor-only) — full/deepen fetch fails (~1.1GB repo, 34 nested submodules).
  - `crowdsourced_dance_club` → upstream `robertpelloni/crowdsourced_dance_club`; **synced** (fork 5 ahead / 0 behind) → 0a18ce2.
- **HyperNexus resolved (v1.0.48)**: upstream removed the invalid `go/NUL` path itself and advanced to v1.0.21 (`8445980`). Local v1.0.3 work (`fc731eb`) preserved in local branch `local-v1.0.3-work` before `main` was reset to origin. Push to HyperNexusllc/HyperNexus remains blocked by the account's LFS budget (exceeded).
- `hyperharness` requires `--depth 1` for initial clone; `HyperNexus` ~1.9GB; `bgtk` ~870MB.
- `realestatecrm` remote normalized from SSH to HTTPS. Scripts reorganized upstream: `scripts/LOFTY/` → `scripts/integrations/lofty/` (commit 75a1247).
- `realestateprototype` canonical primary branch is `main` (default branch is `master` on remote).

Root remote: `https://github.com/candlestixxx/workspace.git` (main branch)

**Last verified:** 2026-11-14 (v1.0.50) - 28 active submodules; added `HyperNexus VRL-1` (@ 0ab941f), `unitedbeats` (@ 3d777a1), and `pulse-dashboard` (@ efd1c92).
