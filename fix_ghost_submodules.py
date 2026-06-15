import subprocess
import os

def run(cmd, cwd=None):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd).stdout.strip()

def fix_submodules(repo_path):
    print(f"Fixing submodules in {repo_path}")
    gitmodules_path = os.path.join(repo_path, '.gitmodules')
    
    valid_paths = []
    if os.path.exists(gitmodules_path):
        with open(gitmodules_path, 'r', errors='ignore') as f:
            for line in f:
                if 'path =' in line:
                    valid_paths.append(line.split('=')[1].strip())
    else:
        print("  No .gitmodules found. All gitlinks will be considered untracked.")
    
    changed = False
    out = run("git ls-files --stage", cwd=repo_path)
    for line in out.splitlines():
        if line.startswith("160000"):
            parts = line.split()
            if len(parts) >= 4:
                sub_path = " ".join(parts[3:])
                if sub_path not in valid_paths:
                    print(f"  Removing untracked gitlink: {sub_path}")
                    run(f'git rm --cached "{sub_path}"', cwd=repo_path)
                    changed = True
    
    if changed:
        run('git commit -m "chore: purge ghost submodules to allow recursive sync"', cwd=repo_path)
        return True
    return False

def fix_all_submodules_recursive(repo_path):
    changed_locally = fix_submodules(repo_path)
    
    out = run("git submodule status", cwd=repo_path)
    for line in out.splitlines():
        if not line.startswith('-'):
            parts = line.strip().split()
            if len(parts) >= 2:
                sub_path = parts[1]
                sub_full_path = os.path.join(repo_path, sub_path)
                if os.path.isdir(sub_full_path) and os.path.exists(os.path.join(sub_full_path, ".git")):
                    if fix_all_submodules_recursive(sub_full_path):
                        print(f"  Updating parent {repo_path} for child {sub_path}")
                        run(f'git add "{sub_path}"', cwd=repo_path)
                        run(f'git commit -m "chore: update submodule {sub_path} after internal purge"', cwd=repo_path)
                        changed_locally = True
    return changed_locally

if __name__ == "__main__":
    fix_all_submodules_recursive(os.getcwd())
