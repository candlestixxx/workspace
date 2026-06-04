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
    _, branch, _ = run_command("git rev-parse --abbrev-ref HEAD", cwd=path)
    if branch == "HEAD": return

    code_check, _, _ = run_command(f"git rev-parse --verify origin/{branch}", cwd=path)
    if code_check == 0:
        code, out, _ = run_command(f"git log origin/{branch}..{branch} --oneline", cwd=path)
        if code == 0 and out:
            run_command(f"git push origin {branch}", cwd=path)
    else:
        run_command(f"git push origin {branch}", cwd=path)

def main():
    submodules_raw_code, submodules_raw, _ = run_command("git submodule foreach --recursive \"pwd\"")
    for line in submodules_raw.splitlines():
        if line.startswith("Entering '"):
            sub_path = line[10:-1]
            push_repo(sub_path, sub_path)

    run_command("git add .")
    run_command("git commit -m \"chore: version bump 1.1.0 & repository synchronization\"")
    push_repo(".", "root")

if __name__ == "__main__":
    main()
