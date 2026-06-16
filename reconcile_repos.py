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

kept_submodules = []
removed_submodules = []

for path in submodules:
    name = os.path.basename(path).lower()
    # Check if it's a robert fork
    is_robert = name in robert_repos
    
    if is_robert and name != "ultratrader":
        removed_submodules.append(path)
    else:
        kept_submodules.append(path)

print(f"Keeping {len(kept_submodules)} submodules.")
print(f"Removing {len(removed_submodules)} submodules.")

# Create new .gitmodules content
new_gitmodules = ""
for path in kept_submodules:
    name = os.path.basename(path)
    # Special cases if needed, but assuming standard candlestixxx URL
    url = f"https://github.com/candlestixxx/{name}.git"
    new_gitmodules += f'[submodule "{path}"]\n'
    new_gitmodules += f'\tpath = {path}\n'
    new_gitmodules += f'\turl = {url}\n'

with open(".gitmodules_new", "w") as f:
    f.write(new_gitmodules)

# Create a script to remove the others
with open("remove_submodules.sh", "w") as f:
    for path in removed_submodules:
        f.write(f"git rm --cached {path}\n")
        f.write(f"rm -rf {path}\n") # Be careful with this, but it's what's requested
