import subprocess
import os

def run_command(cmd, cwd=None):
    try:
        process = subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return process.returncode, stdout.decode().strip(), stderr.decode().strip()
    except Exception as e:
        return -1, "", str(e)

def reconcile_repo(path):
    print(f"\nReconciling {path}...")
    
    # 1. Commit local changes if any
    _, status, _ = run_command("git status --short", cwd=path)
    if status:
        print(f"  Committing local changes...")
        run_command("git add .", cwd=path)
        run_command("git commit -m \"chore: automated checkpoint of local changes during sync 1.1.0\"", cwd=path)

    # Get current branch
    _, current_branch, _ = run_command("git rev-parse --abbrev-ref HEAD", cwd=path)
    
    # Determine main branch name
    main_branch = "main"
    code, _, _ = run_command("git show-ref --verify refs/heads/master", cwd=path)
    if code == 0:
        main_branch = "master"
    
    # 2. Sync main with remotes
    for remote in ["upstream", "origin"]:
        remote_main = f"{remote}/{main_branch}"
        code, _, _ = run_command(f"git show-ref --verify refs/remotes/{remote_main}", cwd=path)
        if code == 0:
            print(f"  Merging {remote_main} into {main_branch}...")
            if current_branch != main_branch:
                run_command(f"git checkout {main_branch}", cwd=path)
            
            code_merge, _, _ = run_command(f"git merge {remote_main} --no-edit", cwd=path)
            if code_merge != 0:
                print(f"    CONFLICT during merge of {remote_main}. Preferring current local main.")
                run_command("git merge --abort", cwd=path)
                run_command(f"git merge {remote_main} -X ours --no-edit", cwd=path)
            
            if current_branch != main_branch:
                run_command(f"git checkout {current_branch}", cwd=path)

    # 3. Identify and reconcile all local feature branches
    _, branches_raw, _ = run_command("git branch --format='%(refname:short)'", cwd=path)
    branches = branches_raw.splitlines()
    for branch in branches:
        if branch == main_branch or branch.startswith("HEAD") or branch == "(no branch)":
            continue
            
        print(f"  Reconciling feature branch: {branch}")
        
        # Forward merge: Feature -> Main
        print(f"    Forward merge: {branch} -> {main_branch}")
        run_command(f"git checkout {main_branch}", cwd=path)
        code_fm, _, _ = run_command(f"git merge {branch} --no-edit", cwd=path)
        if code_fm != 0:
            print("      CONFLICT in forward merge. Preferring feature branch.")
            run_command("git merge --abort", cwd=path)
            run_command(f"git merge {branch} -X theirs --no-edit", cwd=path)
        
        # Reverse merge: Main -> Feature
        print(f"    Reverse merge: {main_branch} -> {branch}")
        run_command(f"git checkout {branch}", cwd=path)
        code_rm, _, _ = run_command(f"git merge {main_branch} --no-edit", cwd=path)
        if code_rm != 0:
            print("      CONFLICT in reverse merge. Preferring main.")
            run_command("git merge --abort", cwd=path)
            run_command(f"git merge {main_branch} -X theirs --no-edit", cwd=path)

    # Return to original branch
    run_command(f"git checkout {current_branch}", cwd=path)

def main():
    # Reconcile root first
    reconcile_repo(".")

    submodules_raw_code, submodules_raw, _ = run_command("git submodule foreach --recursive \"pwd\"")
    for line in submodules_raw.splitlines():
        if line.startswith("Entering '"):
            sub_path = line[10:-1]
            reconcile_repo(sub_path)

if __name__ == "__main__":
    main()
