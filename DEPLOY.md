# Deployment Guide — candlestixxx/workspace

## Prerequisites

### Minimum System Requirements
- **OS**: Linux, macOS, or Windows (WSL2 recommended for Windows)
- **Git**: 2.40+ (required for recursive submodule support)
- **Disk Space**: 5GB+ (20 submodules, some large like hyperharness at 800MB+)
- **Network**: Stable broadband connection (initial clone downloads ~3-5GB)
- **SSH** (optional): Required for `realestatecrm` submodule (uses SSH URL)

### Recommended Tools
- GitHub CLI (`gh`) for authenticated operations
- `git-lfs` for large file support (some submodules may use it)

## Initial Setup

### Full Clone (All Submodules)
```bash
git clone --recursive https://github.com/candlestixxx/workspace.git
cd workspace
```

If the recursive clone fails (especially on hyperharness or bobgui), use a two-step approach:

```bash
git clone https://github.com/candlestixxx/workspace.git
cd workspace
git submodule update --init --recursive --depth 1
```

### Sparse Checkout (Specific Submodules Only)
```bash
git clone --filter=blob:none --sparse https://github.com/candlestixxx/workspace.git
cd workspace
# Enable only the submodules you need
git sparse-checkout set realestatecrm leadG
git submodule update --init realestatecrm leadG
```

## Environment Setup Per Submodule

### realestatecrm
```bash
cd realestatecrm
cp .env.example .env
# Edit .env with your DATABASE_URL, API keys, etc.
npm install
npx prisma generate
npm run dev
```

### leadG
```bash
cd leadG
cp .env.example .env
npm install
npx prisma generate
npm run dev
```

### brokeragentworkflow
```bash
cd brokeragentworkflow
# Backend
pip install -r requirements.txt
python main.py
# Frontend
cd frontend
npm install
npm run dev
```

### socialmediacontentplanner
```bash
cd socialmediacontentplanner
npm install
# Web dashboard
cd apps/web && npm run dev
# Mobile app
cd apps/mobile && npx expo start
```

### techno_platform_detroit
```bash
cd techno_platform_detroit
# Backend
npm install
npm run dev
# Mobile
cd mobile
npm install
npx expo start
```

### crowdsourced_dance_club
```bash
cd crowdsourced_dance_club
pip install -r requirements.txt
# Initialize nested submodule
git submodule update --init external/auto_dj_script
python src/main.py
```

### Prank-Deck-AI
```bash
cd Prank-Deck-AI
npm install
npm run dev
```

### hyperharness
```bash
cd hyperharness
# This is a large repo - ensure you have 2GB+ free
npm install
# Check nested submodules
git submodule status
```

### Other Submodules
Most submodules follow standard patterns:
- Node.js projects: `npm install && npm run dev`
- Python projects: `pip install -r requirements.txt && python main.py`
- Check individual `README.md` files for specific instructions

## Updating the Workspace

### Daily Sync
```bash
cd workspace
git pull
git submodule update --init --recursive
```

### Full Reconciliation (After Feature Branch Changes)
```bash
# In each submodule with feature branches:
cd <submodule>
git checkout main
git fetch origin
# Forward merge features
git merge origin/<feature-branch>
# Push
git push origin main
# Reverse merge
git checkout <feature-branch>
git merge main
git push origin <feature-branch>
```

## CI/CD Integration

### Root-Level Versioning
The workspace uses a single version file:
```bash
cat VERSION.md  # e.g., 1.0.23
```

### Automated Checks
A recommended CI pipeline should:
1. Verify all submodule pointers match remote primary branches
2. Check for 0:0 divergence across all feature branches
3. Validate CHANGELOG.md has entry for current version
4. Ensure STRUCTURAL_MAP.md is up to date

## Troubleshooting

### hyperharness clone timeout
Use shallow clone: `git clone --depth 1 https://github.com/candlestixxx/hyperharness.git`

### SSH authentication failure (realestatecrm)
Either add your SSH key to GitHub, or change the remote URL:
```bash
cd realestatecrm
git remote set-url origin https://github.com/candlestixxx/realestatecrm.git
```

### Detached HEAD in submodules
```bash
cd <submodule>
git checkout main  # or master
git pull
```

### Modified submodule content after pull
```bash
cd <submodule>
git stash        # Save local changes
git pull
git stash pop    # Restore local changes
```

---

*Last updated: 2026-07-20 (v1.0.23)*
