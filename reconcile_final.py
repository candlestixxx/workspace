import subprocess
import os
import shutil
import urllib.request
from urllib.error import HTTPError

def run(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.stdout.strip()
    except Exception as e:
        print(f"  Error running command {cmd}: {e}")
        return ""

def check_url(url):
    print(f"Checking {url}...")
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status == 200
    except HTTPError as e:
        if e.code == 404:
            return False
        return False
    except Exception as e:
        print(f"  Error checking URL: {e}")
        return False

def main():
    workspace_root = os.getcwd()
    archive_dir = os.path.abspath(os.path.join(workspace_root, "..", "robertpelloni"))
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    # Infrastructure folders to keep
    keep_list = [
        ".git", ".gemini", ".github", ".hypernexus", ".pi", ".pi-lens", "logs", 
        "scripts", "docs", "tests", "research", "supabase", "node_modules",
        ".jules", ".kilocode", ".letta", ".playwright-mcp", ".pytest_cache", 
        ".serena", ".idea", ".vibe-config.json", "pyproject.toml", "uv.lock",
        "package.json", "package-lock.json", "playwright.config.ts", "GEMINI.md",
        "MEMORY.md", "ROADMAP.md", "TODO.md", "CHANGELOG.md", "VERSION",
        "VERSION.current", "VERSION.md", "VISION.md", "LICENSE", "STRUCTURAL_MAP.md",
        "SUBMODULE_DASHBOARD.md", "SUBMODULE_INVENTORY.md", "SUBMODULE_MAP.md",
        "AI_CONTRIBUTION_REPORT.json", "AI_CONTRIBUTION_REPORT.md", "codebuff.json"
    ]

    # These are submodules we WANT to keep if they exist in candlestixxx
    submodules = []
    out = run("git config -f .gitmodules --get-regexp path")
    for line in out.splitlines():
        if line:
            submodules.append(line.split()[1])

    items = os.listdir(workspace_root)
    for item in items:
        if item in keep_list or item == "reconcile_final.py" or item == "cleanup_repos.ps1" or item == "cleanup_remaining.py" or item == "fix_ghost_submodules.py" or item == "intelligent_merge_v5.py" or item == "resolve_conflicts.py":
            continue
            
        item_path = os.path.join(workspace_root, item)
        print(f"\nEvaluating: {item}")
        
        # Check if it exists in candlestixxx
        # If it's a submodule, we check its name. If it's just a folder, we check its name.
        url = f"https://github.com/candlestixxx/{item}"
        # Some items might have nested paths like bobmani/hymnmania, but os.listdir gives bobmani
        
        should_keep = False
        if item in submodules:
            # Re-verify URL in .gitmodules
            sub_url = run(f"git config -f .gitmodules submodule.{item}.url")
            if "candlestixxx" in sub_url:
                # Double check the web URL
                web_url = sub_url.replace("git@github.com:", "https://github.com/").replace(".git", "")
                if check_url(web_url):
                    should_keep = True
                    print(f"  [KEEP] Submodule {item} exists in candlestixxx.")
        else:
            if check_url(url):
                should_keep = True
                print(f"  [KEEP] Folder {item} exists as a repo in candlestixxx.")
        
        if not should_keep:
            print(f"  [ARCHIVE] {item} does not exist in candlestixxx (or belongs to robertpelloni).")
            target_path = os.path.join(archive_dir, item)
            target_parent = os.path.dirname(target_path)
            if not os.path.exists(target_parent):
                os.makedirs(target_parent)
            
            if os.path.exists(target_path):
                print(f"  Target {target_path} already exists. Appending timestamp.")
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                target_path = f"{target_path}_{timestamp}"

            print(f"  Moving {item} to {target_path}...")
            try:
                # Remove from git index
                run(f'git rm -r --cached "{item}"')
                # Remove from .gitmodules if present
                if item in submodules:
                    run(f"git config -f .gitmodules --remove-section submodule.{item}")
                
                # Use robust move (handle locked files)
                if os.path.isdir(item_path):
                    shutil.move(item_path, target_path)
                else:
                    shutil.move(item_path, target_path)
            except Exception as e:
                print(f"  Failed to move {item}: {e}")
                # Try to use powershell for locked files if possible, or just skip
                if "used by another process" in str(e):
                    print(f"  Item {item} is locked. Manual intervention might be needed for this one.")

    print("\nFinal reconciliation complete.")

if __name__ == "__main__":
    main()
