import subprocess
import os
import shutil

def run(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.stdout.strip()
    except Exception as e:
        print(f"  Error running command {cmd}: {e}")
        return ""

def check_url_curl(url):
    # Convert git@github.com:user/repo.git to https://github.com/user/repo
    if url.startswith("git@github.com:"):
        url = url.replace("git@github.com:", "https://github.com/").replace(".git", "")
    elif url.endswith(".git"):
        url = url[:-4]
    
    print(f"Checking {url}...")
    # Use curl -I to get headers
    out = run(f'curl -I -s -L --connect-timeout 2 --max-time 5 -o /dev/null -w "%{{http_code}}" "{url}"')
    if out == "200":
        return True
    return False

def main():
    workspace_root = os.getcwd()
    archive_dir = os.path.abspath(os.path.join(workspace_root, "..", "robertpelloni"))
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    # Load submodules from .gitmodules
    submodules = []
    out = run("git config -f .gitmodules --get-regexp path")
    for line in out.splitlines():
        if line:
            parts = line.split()
            if len(parts) >= 2:
                submodules.append(parts[1])

    for sub in submodules:
        print(f"\nProcessing submodule: {sub}")
        url = run(f'git config -f .gitmodules submodule."{sub}".url')
        if not url:
            print(f"  Warning: No URL for {sub}")
            continue

        if check_url_curl(url):
            print(f"  [KEEP] {sub} exists in candlestixxx.")
        else:
            print(f"  [ARCHIVE] {sub} does not exist in candlestixxx.")
            target_path = os.path.join(archive_dir, sub)
            target_parent = os.path.dirname(target_path)
            if not os.path.exists(target_parent):
                os.makedirs(target_parent)
            
            # Remove from git
            run(f'git rm -r --cached "{sub}"')
            run(f'git config -f .gitmodules --remove-section submodule."{sub}"')
            
            sub_path = os.path.join(workspace_root, sub)
            if os.path.exists(sub_path):
                print(f"  Moving {sub} to {target_path}")
                try:
                    if os.path.exists(target_path):
                         shutil.rmtree(target_path, ignore_errors=True)
                    shutil.move(sub_path, target_path)
                except Exception as e:
                    print(f"  Failed to move {sub}: {e}")

    print("\nReconciliation complete.")

if __name__ == "__main__":
    main()
