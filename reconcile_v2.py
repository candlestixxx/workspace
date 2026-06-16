import os
import subprocess

def run_cmd(cmd, cwd=None):
    try:
        res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
        return res.stdout.strip()
    except:
        return ""

def get_robert_repos():
    with open("robertpelloni_repos.txt", "r") as f:
        return [line.strip().lower() for line in f if line.strip()]

robert_repos = get_robert_repos()

# Get all submodules from git index
index_output = run_cmd("git ls-files --stage")
submodules = []
for line in index_output.splitlines():
    if line.startswith("160000"):
        parts = line.split()
        if len(parts) >= 4:
            path = parts[3]
            submodules.append(path)

print(f"Found {len(submodules)} submodules in index.")

# Exceptions to keep even if they are in robert_repos
exceptions = ["ultratrader", "bobtrader", "foreclosureworkflow", "forclosureworkflow"]

kept_submodules = []
removed_submodules = []

for path in submodules:
    name = os.path.basename(path).lower()
    # Check if it's a robert fork
    is_robert = name in robert_repos
    is_exception = any(ex in name for ex in exceptions)
    
    if is_robert and not is_exception:
        removed_submodules.append(path)
    else:
        kept_submodules.append(path)

print(f"Keeping {len(kept_submodules)} submodules.")
print(f"Removing {len(removed_submodules)} submodules.")

# Create new .gitmodules content
new_gitmodules = ""
for path in kept_submodules:
    name = os.path.basename(path)
    url = f"https://github.com/candlestixxx/{name}.git"
    new_gitmodules += f'[submodule "{path}"]\n'
    new_gitmodules += f'\tpath = {path}\n'
    new_gitmodules += f'\turl = {url}\n'

with open(".gitmodules_new", "w") as f:
    f.write(new_gitmodules)

# Create a PowerShell script to remove the others (more reliable on this system)
with open("remove_submodules.ps1", "w") as f:
    for path in removed_submodules:
        # Use git rm -f to handle the "staged content different" error
        f.write(f"git rm -f --cached '{path}'\n")
        f.write(f"if (Test-Path '{path}') {{ Remove-Item -Recurse -Force '{path}' }}\n")
