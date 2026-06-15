import os
import subprocess
import datetime

def run_cmd(cmd, cwd=None):
    try:
        res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
        return res.stdout.strip(), res.stderr.strip(), res.returncode
    except Exception as e:
        return "", str(e), 1

def save_dirty_submodules(root_dir):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    recovery_branch = f"recovery/session_{timestamp}"
    
    stdout, _, _ = run_cmd("git submodule status --recursive", cwd=root_dir)
    submodules = []
    for line in stdout.splitlines():
        parts = line.strip().split()
        if len(parts) >= 2:
            # line might start with + or - or U or space
            path = parts[1]
            submodules.append(path)

    for sub in submodules:
        sub_path = os.path.join(root_dir, sub)
        if not os.path.isdir(os.path.join(sub_path, ".git")):
            continue
            
        status, _, _ = run_cmd("git status --porcelain", cwd=sub_path)
        if status:
            print(f"[*] Saving dirty changes in {sub}...")
            run_cmd(f"git checkout -b {recovery_branch}", cwd=sub_path)
            run_cmd("git add .", cwd=sub_path)
            run_cmd(f"git commit -m \"Auto-save progress before sync {timestamp}\"", cwd=sub_path)
            # Switch back to whatever was before? Or just stay there?
            # Better to stay on the recovery branch so the update can merge it if needed.
            print(f"    Saved to {recovery_branch}")

if __name__ == "__main__":
    save_dirty_submodules(os.getcwd())
