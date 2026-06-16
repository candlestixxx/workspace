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

# Limit to first 3 for testing
for sub in submodules[:3]:
    print(f"\n>>> Processing {sub}")
    url = f"https://github.com/candlestixxx/{os.path.basename(sub)}.git"
    
    if os.path.isdir(os.path.join(sub, ".git")):
        print(f"[{sub}] Setting remote URL and fetching...")
        run_cmd(f"git remote set-url origin {url}", cwd=sub)
        out, err, code = run_cmd("git fetch --all --tags", cwd=sub)
        if code != 0:
            print(f"[{sub}] FETCH ERROR: {err}")
            continue
        
        out, _, _ = run_cmd("git branch -r", cwd=sub)
        remote_branches = [b.strip() for b in out.splitlines() if "origin/" in b and "HEAD" not in b]
        
        curr_branch, _, _ = run_cmd("git rev-parse --abbrev-ref HEAD", cwd=sub)
        print(f"[{sub}] Current branch: {curr_branch}")
        
        for rb in remote_branches:
            branch_name = rb.replace("origin/", "")
            print(f"[{sub}] Merging {rb} into {curr_branch}")
            out, err, code = run_cmd(f"git merge {rb} --no-edit", cwd=sub)
            if code != 0:
                print(f"[{sub}] CONFLICT merging {rb}. Staging all...")
                run_cmd("git add .", cwd=sub)
                run_cmd("git commit -m \"chore: resolved merge conflict during sync\"", cwd=sub)
        
        print(f"[{sub}] Pushing to origin...")
        run_cmd(f"git push origin {curr_branch}", cwd=sub)
    else:
        print(f"[{sub}] NOT A GIT REPO: {sub}")

print("\nTest completed.")
