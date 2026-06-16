import os
import subprocess

def run_cmd(cmd, cwd=None):
    try:
        res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
        return res.stdout.strip(), res.stderr.strip(), res.returncode
    except Exception as e:
        return "", str(e), 1

root_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and os.path.exists(os.path.join(d, ".git")) and d != 'bobtrader' and not d.startswith('.')]

if 'node_modules' in root_dirs: root_dirs.remove('node_modules')

print(f"Syncing {len(root_dirs)} submodules...")

for d in root_dirs:
    print(f"\n>>> Syncing {d}")
    url = f"https://github.com/candlestixxx/{d}.git"
    if d == "realestatecrm": url = "git@github.com:candlestixxx/realestatecrm.git"
    elif d == "re-agent-workflow-media-1": url = "https://github.com/candlestixxx/re-agent-workflow-media-1"
    elif d == "brokeragentworkflow": url = "https://github.com/candlestixxx/brokeragentworkflow"
    
    # Ensure remote is correct
    run_cmd(f"git remote set-url origin {url}", cwd=d)
    run_cmd("git fetch --all --tags", cwd=d)
    
    # Get all remote branches
    out, _, _ = run_cmd("git branch -r", cwd=d)
    remote_branches = [b.strip() for b in out.splitlines() if "origin/" in b and "HEAD" not in b]
    
    if not remote_branches:
        print(f"[{d}] No remote branches found.")
        continue

    # Identify primary branch
    primary = "main"
    if "origin/master" in remote_branches:
        primary = "master"
    
    print(f"[{d}] Primary branch is {primary}. Merging all remote branches...")
    
    # Ensure local branch exists
    run_cmd(f"git checkout -b {primary}", cwd=d)
    run_cmd(f"git checkout {primary}", cwd=d)
    
    # Pull primary first
    run_cmd(f"git pull origin {primary} --no-edit", cwd=d)
    
    # Merge others
    for rb in remote_branches:
        branch_name = rb.replace("origin/", "")
        if branch_name != primary:
            print(f"[{d}] Merging {rb}...")
            run_cmd(f"git merge {rb} --no-edit", cwd=d)
            run_cmd("git add .", cwd=d)
            run_cmd("git commit -m \"chore: sync with remote branch\"", cwd=d)
    
    # Final add and commit
    run_cmd("git add .", cwd=d)
    run_cmd("git commit -m \"chore: update submodule state after monorepo reconfiguration\"", cwd=d)

print("\nAll submodules synced and merged.")
