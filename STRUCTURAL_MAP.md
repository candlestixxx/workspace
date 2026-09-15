# Structural Map — candlestixxx/workspace

| # | Submodule | Path | Remote URL | Current Commit |
|---|-----------|------|-----------|----------------|
| 1 | brokeragentworkflow | brokeragentworkflow/ | https://github.com/candlestixxx/brokeragentworkflow | 2382d99 |
| 2 | excel-legacy-leadgen | excel-legacy-leadgen/ | https://github.com/candlestixxx/excel-legacy-leadgen.git | d271c64 |
| 3 | explorerexedecompiled | explorerexedecompiled/ | https://github.com/candlestixxx/explorerexedecompiled.git | 31a4794 |
| 4 | forclosureworkflow | forclosureworkflow/ | https://github.com/candlestixxx/forclosureworkflow.git | aaa3ff7 |
| 5 | leadG | leadG/ | https://github.com/candlestixxx/leadG.git | dc3589f |
| 6 | p2p_service_marketplace | p2p_service_marketplace/ | https://github.com/candlestixxx/p2p_service_marketplace.git | 115aaa3 |
| 7 | re-agent-workflow-media-1 | re-agent-workflow-media-1/ | https://github.com/candlestixxx/re-agent-workflow-media-1 | 49bb626 |
| 8 | realestatecrm | realestatecrm/ | https://github.com/candlestixxx/realestatecrm.git | 4d5abb1 |
| 9 | realestateleadcaller | realestateleadcaller/ | https://github.com/candlestixxx/realestateleadcaller.git | 93298b1 |
| 10 | realestateprototype | realestateprototype/ | https://github.com/candlestixxx/realestateprototype.git | 7c40d91 |
| 11 | skillzhub | skillzhub/ | https://github.com/candlestixxx/skillzhub.git | 9e1e0ea |
| 12 | socialmediacontentplanner | socialmediacontentplanner/ | https://github.com/candlestixxx/socialmediacontentplanner.git | 4e5ca53 |
| 13 | techno_platform_detroit | techno_platform_detroit/ | https://github.com/candlestixxx/techno_platform_detroit.git | 0f2b67b |
| 14 | theta-data-api | theta-data-api/ | https://github.com/candlestixxx/theta-data-api.git | ef15c6f |
| 15 | ultratrader | ultratrader/ | https://github.com/candlestixxx/ultratrader.git | 89e877e |
| 16 | LegacyLeads | LegacyLeads/ | https://github.com/candlestixxx/LegacyLeads.git | a76c08e |
| 17 | crowdsourced_dance_club | crowdsourced_dance_club/ | https://github.com/candlestixxx/crowdsourced_dance_club.git | 0a18ce2 |
| 18 | Prank-Deck-AI | Prank-Deck-AI/ | https://github.com/candlestixxx/prank-deck-ai.git | a85b2b5 |
| 19 | bobgui | bobgui/ | https://github.com/candlestixxx/bobgui.git | 9bea319 |
| 20 | hyperharness | hyperharness/ | https://github.com/candlestixxx/hyperharness.git | 50c8826 |
| 21 | aicrm | aicrm/ | https://github.com/candlestixxx/aicrm.git | b724cca |
| 22 | psychedelic-speech-engine | psychedelic-speech-engine/ | https://github.com/candlestixxx/psychedelic-speech-engine.git | fdea36a |
| 23 | HyperNexus | HyperNexus/ | https://github.com/HyperNexusllc/HyperNexus.git | 4fe0e1c |
| 24 | suno-api | suno-api/ | https://github.com/candlestixxx/suno-api.git | f609d44 |

**Notes:**
- 24 submodules: 23 under `candlestixxx` + 1 external (`HyperNexusllc/HyperNexus` — aicrm orchestration kernel).
- `crowdsourced_dance_club` has a nested submodule `external/auto_dj_script` (robertpelloni/auto_dj_script @ a47e1d3).
- **suno-api**: forked from `gcui-art/suno-api` → `candlestixxx/suno-api` (v1.0.43) to preserve 5 local Suno-API fix commits (chirp-hawk v6, hCaptcha/Turnstile, media_urls, status=complete wait).
- **robertpelloni upstream tracking** (Step-2 scope):
  - `bobgui` → upstream `robertpelloni/bgtk` (renamed from bobgui); fork is **1472 commits behind** — full fetch fails (`invalid index-pack output`, ~870MB repo).
  - `hyperharness` → upstream `robertpelloni/hyperharness`; fork is **146 commits behind** — full/deepen fetch fails (~1.1GB repo, 34 nested submodules).
  - `crowdsourced_dance_club` → upstream `robertpelloni/crowdsourced_dance_club`; **synced** (fork 5 ahead / 0 behind) → 0a18ce2.
- `hyperharness` requires `--depth 1` for initial clone; `HyperNexus` ~1.9GB; `bgtk` ~870MB.
- `realestatecrm` remote normalized from SSH to HTTPS.
- `realestateprototype` canonical primary branch is `main` (default branch is `master` on remote).

Root remote: `https://github.com/candlestixxx/workspace.git` (main branch)

**Last verified:** 2026-09-15 (v1.0.43) — 24 active submodules.
