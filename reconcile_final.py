import os
import subprocess

def run_cmd(cmd, cwd=None):
    try:
        res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
        return res.stdout.strip(), res.stderr.strip(), res.returncode
    except Exception as e:
        return "", str(e), 1

# 1. Identify folders on disk
root_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')]
if 'node_modules' in root_dirs: root_dirs.remove('node_modules')
if 'bobtrader' in root_dirs: root_dirs.remove('bobtrader')

print(f"Folders to be submodules: {root_dirs}")

# 2. Remove bobtrader from index if it exists as a submodule
run_cmd("git rm -f --cached bobtrader")

# 3. Clean index of non-existent submodules
index_output, _, _ = run_cmd("git ls-files --stage")
current_submodules = []
for line in index_output.splitlines():
    if line.startswith("160000"):
        parts = line.split()
        if len(parts) >= 4:
            path = parts[3]
            current_submodules.append(path)

for sub in current_submodules:
    if sub not in root_dirs and sub != 'bobtrader':
        print(f"Removing stale submodule from index: {sub}")
        run_cmd(f"git rm -f --cached {sub}")

# 4. Ensure each folder is a git repo and add to index as submodule
new_gitmodules = ""
for d in root_dirs:
    print(f"\n>>> Checking {d}")
    if not os.path.isdir(os.path.join(d, ".git")):
        print(f"[{d}] Initializing git...")
        run_cmd("git init", cwd=d)
        url = f"https://github.com/candlestixxx/{d}.git"
        # Special cases from before
        if d == "realestatecrm": url = "git@github.com:candlestixxx/realestatecrm.git"
        elif d == "re-agent-workflow-media-1": url = "https://github.com/candlestixxx/re-agent-workflow-media-1"
        elif d == "brokeragentworkflow": url = "https://github.com/candlestixxx/brokeragentworkflow"
        
        run_cmd(f"git remote add origin {url}", cwd=d)
    
    # Add to index if not already there
    run_cmd(f"git add {d}")
    
    # Build .gitmodules
    url = run_cmd(f"git remote get-url origin", cwd=d)[0]
    if not url:
        url = f"https://github.com/candlestixxx/{d}.git"
        if d == "realestatecrm": url = "git@github.com:candlestixxx/realestatecrm.git"
        elif d == "re-agent-workflow-media-1": url = "https://github.com/candlestixxx/re-agent-workflow-media-1"
        elif d == "brokeragentworkflow": url = "https://github.com/candlestixxx/brokeragentworkflow"

    new_gitmodules += f'[submodule "{d}"]\n'
    new_gitmodules += f'\tpath = {d}\n'
    new_gitmodules += f'\turl = {url}\n'

with open(".gitmodules", "w") as f:
    f.write(new_gitmodules)

print("\nFinalizing index...")
run_cmd("git add .gitmodules")
print("Done.")
