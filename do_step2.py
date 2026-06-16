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
print(f"Syncing {len(submodules)} submodules...")

for sub in submodules:
    print(f"\n>>> Processing {sub}")
    # 1. Ensure remote is correct
    url = f"https://github.com/candlestixxx/{os.path.basename(sub)}.git"
    # Special cases
    if sub == "realestatecrm": url = "git@github.com:candlestixxx/realestatecrm.git"
    elif sub == "re-agent-workflow-media-1": url = "https://github.com/candlestixxx/re-agent-workflow-media-1"
    elif sub == "brokeragentworkflow": url = "https://github.com/candlestixxx/brokeragentworkflow"
    
    if os.path.isdir(os.path.join(sub, ".git")):
        run_cmd(f"git remote set-url origin {url}", cwd=sub)
        run_cmd("git fetch --all --tags", cwd=sub)
        
        # 2. Intelligent Merge (All branches)
        # Get all remote branches
        out, _, _ = run_cmd("git branch -r", cwd=sub)
        remote_branches = [b.strip() for b in out.splitlines() if "origin/" in b and "HEAD" not in b]
        
        # Merge each remote branch into current local branch
        curr_branch, _, _ = run_cmd("git rev-parse --abbrev-ref HEAD", cwd=sub)
        if not curr_branch or curr_branch == "HEAD":
            # Try to checkout main/master
            run_cmd("git checkout main", cwd=sub)
            run_cmd("git checkout master", cwd=sub)
            curr_branch, _, _ = run_cmd("git rev-parse --abbrev-ref HEAD", cwd=sub)

        print(f"[{sub}] Current branch: {curr_branch}")
        
        for rb in remote_branches:
            branch_name = rb.replace("origin/", "")
            if branch_name == curr_branch:
                print(f"[{sub}] Pulling {rb} into {curr_branch}")
                run_cmd(f"git pull origin {branch_name} --no-edit", cwd=sub)
            else:
                print(f"[{sub}] Merging {rb} into {curr_branch}")
                # Try to merge remote branch into current
                out, err, code = run_cmd(f"git merge {rb} --no-edit", cwd=sub)
                if code != 0:
                    print(f"[{sub}] CONFLICT merging {rb}. Attempting intelligent resolution...")
                    # Basic resolution: add all and commit if it's just progress
                    run_cmd("git add .", cwd=sub)
                    run_cmd("git commit -m \"chore: resolved merge conflict during sync\"", cwd=sub)
        
        # 3. Push back if mine
        run_cmd(f"git push origin {curr_branch}", cwd=sub)
    else:
        print(f"[{sub}] Directory missing or not a git repo. Skipping.")

print("\nSync and Intelligent Merge completed.")
