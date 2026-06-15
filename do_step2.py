import subprocess
import os
import sys

def run(cmd, cwd='.'):
    process = subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.returncode, process.stdout.decode().strip(), process.stderr.decode().strip()

def process_repo(path):
    print(f"--- Processing {path} ---")
    
    # Commit any local changes to ensure clean working directory
    _, status, _ = run("git status --porcelain", cwd=path)
    if status:
        print("  Committing local changes...")
        run("git add .", cwd=path)
        run('git commit -m "chore: auto checkpoint before intelligent merge"', cwd=path)
    
    # Determine primary branch (main or master)
    primary = "main"
    if run("git show-ref --verify refs/heads/master", cwd=path)[0] == 0:
        primary = "master"
        
    # Upstream sync
    print(f"  Syncing {primary} with upstream...")
    run(f"git checkout {primary}", cwd=path)
    run("git fetch --all --tags", cwd=path)
    
    # Try merging upstream/primary if it exists, otherwise origin/primary
    if run(f"git show-ref --verify refs/remotes/upstream/{primary}", cwd=path)[0] == 0:
        run(f"git merge upstream/{primary} --no-edit", cwd=path)
    else:
        run(f"git merge origin/{primary} --no-edit", cwd=path)
        
    # Get all local branches
    code, branches_out, _ = run("git branch --format='%(refname:short)'", cwd=path)
    if code != 0:
        return
        
    branches = [b for b in branches_out.splitlines() if b and b != primary and not b.startswith('(no branch')]
    
    for branch in branches:
        print(f"  Intelligent Merge for branch: {branch}")
        
        # 1. Forward merge: Feature -> Main
        run(f"git checkout {primary}", cwd=path)
        code_m, _, _ = run(f"git merge {branch} --no-edit", cwd=path)
        if code_m != 0:
            print(f"    Conflict in {branch} -> {primary}. Resolving using both...")
            run("git merge --abort", cwd=path)
            run(f"git merge {branch} -X ours --no-edit", cwd=path) # Prefer main's changes
            
        # 2. Reverse merge: Main -> Feature
        run(f"git checkout {branch}", cwd=path)
        code_r, _, _ = run(f"git merge {primary} --no-edit", cwd=path)
        if code_r != 0:
            print(f"    Conflict in {primary} -> {branch}. Resolving...")
            run("git merge --abort", cwd=path)
            run(f"git merge {primary} -X theirs --no-edit", cwd=path) # Prefer main's changes into feature
            
    # Leave on primary branch
    run(f"git checkout {primary}", cwd=path)

def main():
    process_repo(".")
    
    code, submodules_raw, _ = run("git submodule foreach --recursive \"pwd\"")
    for line in submodules_raw.splitlines():
        if line.startswith("Entering '"):
            sub_path = line[10:-1]
            process_repo(sub_path)

if __name__ == '__main__':
    main()
