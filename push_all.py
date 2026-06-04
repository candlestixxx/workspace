import subprocess
import os

def run_command(cmd, cwd=None):
    try:
        process = subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return process.returncode, stdout.decode().strip(), stderr.decode().strip()
    except Exception as e:
        return -1, "", str(e)

def push_repo(path, name):
    print(f"Pushing {name}...")
    # Get current branch
    _, branch, _ = run_command("git rev-parse --abbrev-ref HEAD", cwd=path)
    if branch == "HEAD":
        print(f"  Skipping {name} (detached HEAD)")
        return

    # Check if there are commits to push
    code, out, _ = run_command(f"git log origin/{branch}..{branch}", cwd=path)
    if code == 0 and out:
        print(f"  Pushing commits to origin/{branch}...")
        p_code, p_out, p_err = run_command(f"git push origin {branch}", cwd=path)
        if p_code != 0:
            print(f"  PUSH FAILED: {p_err}")
        else:
            print(f"  PUSH SUCCESS")
    else:
        print(f"  Nothing to push for {name}")

def main():
    # Push submodules first
    submodules_raw_code, submodules_raw, _ = run_command("git submodule foreach --recursive \"pwd\"")
    for line in submodules_raw.splitlines():
        if line.startswith("Entering '"):
            sub_path = line[10:-1]
            push_repo(sub_path, sub_path)

    # Commit and push root
    print("\nCommitting and pushing root...")
    run_command("git add .")
    run_command("git commit -m \"chore: version bump 1.0.9 & repository synchronization\"")
    push_repo(".", "root")

if __name__ == "__main__":
    main()
