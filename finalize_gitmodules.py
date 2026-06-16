import os
import subprocess

def run_cmd(cmd, cwd=None):
    try:
        res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
        return res.stdout.strip()
    except:
        return ""

index_output = run_cmd("git ls-files --stage")
submodules = []
for line in index_output.splitlines():
    if line.startswith("160000"):
        parts = line.split()
        if len(parts) >= 4:
            path = parts[3]
            submodules.append(path)

new_gitmodules = ""
for path in submodules:
    name = os.path.basename(path)
    # Most submodules follow this pattern on candlestixxx
    url = f"https://github.com/candlestixxx/{name}.git"
    
    # Exceptions for known existing URLs in the previous correct state
    if name == "realestatecrm":
        url = "git@github.com:candlestixxx/realestatecrm.git"
    elif name == "re-agent-workflow-media-1":
        url = "https://github.com/candlestixxx/re-agent-workflow-media-1" # No .git suffix in previous correctly working one
    elif name == "brokeragentworkflow":
        url = "https://github.com/candlestixxx/brokeragentworkflow"

    new_gitmodules += f'[submodule "{path}"]\n'
    new_gitmodules += f'\tpath = {path}\n'
    new_gitmodules += f'\turl = {url}\n'

with open(".gitmodules", "w") as f:
    f.write(new_gitmodules)

print("Generated corrected .gitmodules with", len(submodules), "entries.")
