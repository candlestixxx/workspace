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

exceptions = ["ultratrader", "bobtrader", "foreclosureworkflow", "forclosureworkflow"]

print(f"{'Path':<40} {'Is Robert':<10} {'Is Exception':<12}")
print("-" * 65)

for path in submodules:
    name = path.lower()
    is_robert = name in robert_repos
    is_exception = any(ex in name for ex in exceptions)
    print(f"{path:<40} {str(is_robert):<10} {str(is_exception):<12}")
