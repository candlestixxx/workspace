# Memory File — candlestixxx/workspace

## Architectural Observations

### Submodule Topology
- **20 submodules** total, all under `candlestixxx` GitHub org
- **2 primary branch conventions**: Most use `main`, exceptions are `excel-legacy-leadgen` (master), `realestateprototype` (master), `ultratrader` (master)
- **1 nested submodule**: `crowdsourced_dance_club/external/auto_dj_script` (robertpelloni/auto_dj_script)
- **3 robertpelloni forks**: `crowdsourced_dance_club`, `bobgui`, `ultratrader`, `hyperharness` — only `crowdsourced_dance_club` has an active upstream

### Known Constraints

#### hyperharness
- **Size**: 800MB+ repository, extremely large clone
- **Clone strategy**: Use `--depth 1` for initial clone; full clone often times out
- **Submodules**: Contains 34 nested submodules (many stale/archived)
- **Upstream**: robertpelloni/hyperharness — unreachable due to size

#### bobgui
- **Size**: Large repository with 300+ historical GTK tags
- **Tags**: `git fetch` pulls all historical tags; may require `--no-tags` for speed
- **Nested submodules**: 2 (`submodules/juce` and others)

#### realestatecrm
- **URL format**: Uses SSH (`git@github.com:candlestixxx/realestatecrm.git`) unlike all others (HTTPS)
- **Local changes**: Frequently has untracked development artifacts (scripts/, .hypercode/)
- **Modifications**: Frequent local dev changes in working tree

#### brokeragentworkflow
- **Tech stack**: Python backend + Vue.js frontend with Capacitor mobile
- **iOS directory**: Contains CapApp-SPM (Swift Package Manager) setup
- **Local changes**: Often has modified Vue components during dev sessions

#### leadG
- **Tech stack**: Next.js with Prisma ORM
- **Local changes**: Frequently modified next.config.js, Prisma schema, middleware
- **Untracked**: main.py, requirements.txt for Python side scripts

### Design Preferences

1. **Documentation-first**: Every change must be reflected in CHANGELOG.md, STRUCTURAL_MAP.md, and HANDOFF.md
2. **Zero-divergence target**: All feature branches must be at 0:0 with their primaries after every merge cycle
3. **Fast-forward preferred**: Feature branches that haven't diverged should fast-forward merge
4. **Ort strategy**: Used for merges with actual divergence (GitHub's default merge strategy)
5. **Stash-before-merge**: Local changes are always stashed before merges and restored after
6. **Submodule pointers**: Root repo tracks exact commit hashes for each submodule

### Merge Conflict Patterns

| Conflict Type | Resolution Strategy |
|--------------|-------------------|
| VERSION.md in explorerexedecompiled | Accept version bump, preserve feature content |
| package-lock.json across submodules | Regenerate from package.json after merge |
| .gitignore modifications | Preserve session/memory file entries (do not gitignore) |
| LeadTableClient.tsx deletion | Accept upstream simplifications, preserve as untracked |

### Session File Preservation
Per retention directive, the following must NEVER be gitignored:
- `.hypercode/`, `.hypernexus/`, `.hypernexus-session.json`, `.hypernexus_startup_marker`
- `.jules/sessions/`, `.claude/`
- `MEMORY.md`, `HANDOFF.md`, `CHANGELOG.md`, `ROADMAP.md`, `TODO.md`, `VERSION.md`, `IDEAS.md`, `VISION.md`

### Automated Workflows
- **Forward merge**: Feature branch → primary branch (when feature has new remote commits)
- **Reverse merge**: Primary → feature branches (to keep them current)
- **Upstream sync**: robertpelloni repos → candlestixxx forks (periodic)
- **Divergence audit**: All branches checked for 0:0 status after every cycle

---

*Last updated: 2026-07-20 (v1.0.23)*
