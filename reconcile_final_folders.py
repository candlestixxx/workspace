import os
import shutil
import subprocess

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()

def main():
    workspace_root = os.getcwd()
    archive_dir = os.path.abspath(os.path.join(workspace_root, "..", "robertpelloni"))
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    # Folders/Files to keep
    keep_list = [
        ".git", ".gemini", ".github", ".hypernexus", ".pi", ".pi-lens", "logs", 
        "scripts", "docs", "tests", "research", "supabase", "node_modules",
        "GEMINI.md", "MEMORY.md", "ROADMAP.md", "TODO.md", "CHANGELOG.md", 
        "VERSION", "VERSION.current", "VERSION.md", "VISION.md", "LICENSE",
        "STRUCTURAL_MAP.md", "SUBMODULE_DASHBOARD.md", "SUBMODULE_INVENTORY.md", 
        "SUBMODULE_MAP.md", "AI_CONTRIBUTION_REPORT.json", "AI_CONTRIBUTION_REPORT.md", 
        "codebuff.json", "pyproject.toml", "uv.lock", "package.json", "package-lock.json",
        "playwright.config.ts", ".vibe-config.json", ".python-version",
        ".jules", ".kilocode", ".letta", ".playwright-mcp", ".pytest_cache", ".serena", ".idea"
    ]

    # Add verified submodules (top-level only)
    out = run("git config -f .gitmodules --get-regexp path")
    for line in out.splitlines():
        if line:
            path = line.split()[1]
            top_level = path.split('/')[0]
            keep_list.append(top_level)

    items = os.listdir(workspace_root)
    for item in items:
        if item in keep_list or item.startswith("reconcile") or item.startswith("cleanup") or item.startswith("fix") or item.startswith("restore"):
            continue
            
        item_path = os.path.join(workspace_root, item)
        print(f"\nArchiving: {item}")
        
        target_path = os.path.join(archive_dir, item)
        if os.path.exists(target_path):
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            target_path = f"{target_path}_{timestamp}"

        print(f"  Moving {item} to {target_path}...")
        try:
            # Try to remove from git if it's tracked
            os.system(f'git rm -r --cached "{item}"')
            shutil.move(item_path, target_path)
        except Exception as e:
            print(f"  Failed to move {item}: {e}")

    print("\nFinal folder cleanup complete.")

if __name__ == "__main__":
    main()
