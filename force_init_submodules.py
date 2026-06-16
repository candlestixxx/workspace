import os
import subprocess

def run_cmd(cmd, cwd=None):
    try:
        res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
        return res.stdout.strip(), res.stderr.strip(), res.returncode
    except Exception as e:
        return "", str(e), 1

def get_submodules():
    index_output, _, _ = run_cmd("git ls-files --stage")
    subs = []
    for line in index_output.splitlines():
        if line.startswith("160000"):
            parts = line.split()
            if len(parts) >= 4:
                subs.append(parts[3])
    return subs

submodules = get_submodules()
print(f"Force-initializing {len(submodules)} submodules...")

for sub in submodules:
    print(f"\n>>> {sub}")
    url = f"https://github.com/candlestixxx/{os.path.basename(sub)}.git"
    if sub == "realestatecrm": url = "git@github.com:candlestixxx/realestatecrm.git"
    elif sub == "re-agent-workflow-media-1": url = "https://github.com/candlestixxx/re-agent-workflow-media-1"
    elif sub == "brokeragentworkflow": url = "https://github.com/candlestixxx/brokeragentworkflow"

    if not os.path.isdir(os.path.join(sub, ".git")):
        print(f"[{sub}] No .git found. Initializing...")
        if not os.path.isdir(sub):
            os.makedirs(sub)
        
        run_cmd("git init", cwd=sub)
        run_cmd(f"git remote add origin {url}", cwd=sub)
    else:
        print(f"[{sub}] .git exists. Updating remote...")
        run_cmd(f"git remote set-url origin {url}", cwd=sub)

    print(f"[{sub}] Fetching and merging...")
    run_cmd("git fetch --all --tags", cwd=sub)
    # Get primary branch from remote
    out, _, _ = run_cmd("git remote show origin", cwd=sub)
    primary = "main"
    if "HEAD branch: master" in out: primary = "master"
    
    print(f"[{sub}] Primary branch is {primary}. Merging all remote branches...")
    
    # Ensure we are on a branch
    curr, _, _ = run_cmd("git rev-parse --abbrev-ref HEAD", cwd=sub)
    if curr == "HEAD":
        run_cmd(f"git checkout -b {primary}", cwd=sub)
    
    # Intelligent merge logic
    out, _, _ = run_cmd("git branch -r", cwd=sub)
    remote_branches = [b.strip() for b in out.splitlines() if "origin/" in b and "HEAD" not in b]
    
    for rb in remote_branches:
        branch_name = rb.replace("origin/", "")
        print(f"[{sub}] Merging {rb}...")
        run_cmd(f"git merge {rb} --no-edit", cwd=sub)
        # Handle conflicts
        run_cmd("git add .", cwd=sub)
        run_cmd("git commit -m \"chore: sync with remote branch\"", cwd=sub)

print("\nDone.")
