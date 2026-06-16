import subprocess
import os
import shutil

def run(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.stdout.strip()
    except Exception as e:
        print(f"  Error: {e}")
        return ""

def check_url_curl(url):
    if url.startswith("git@github.com:"):
        url = url.replace("git@github.com:", "https://github.com/").replace(".git", "")
    elif url.endswith(".git"):
        url = url[:-4]
    
    print(f"Checking {url}...")
    out = run(f'curl -I -s -L --connect-timeout 2 --max-time 5 -o /dev/null -w "%{{http_code}}" "{url}"')
    return out == "200"

def main():
    workspace_root = os.getcwd()
    archive_dir = os.path.abspath(os.path.join(workspace_root, "..", "candlestixxx"))
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    out = run("git config -f .gitmodules --get-regexp path")
    submodules = [line.split()[1] for line in out.splitlines() if line]

    for sub in submodules:
        print(f"\nProcessing: {sub}")
        url = run(f'git config -f .gitmodules submodule."{sub}".url')
        if not url: continue

        should_archive = False
        final_url = url

        if "candlestixxx" in url:
            # Check for candlestixxx migration
            candlestixxx_url = url.replace("candlestixxx", "candlestixxx")
            if check_url_curl(candlestixxx_url):
                print(f"  [MIGRATE] {sub} moved to candlestixxx.")
                final_url = candlestixxx_url
                run(f'git config -f .gitmodules submodule."{sub}".url {final_url}')
                if os.path.exists(os.path.join(sub, ".git")):
                    run(f"git remote set-url origin {final_url}", cwd=sub)
            else:
                print(f"  [ARCHIVE] {sub} only exists under candlestixxx.")
                should_archive = True
        else:
            # External or already migrated
            if not check_url_curl(url):
                print(f"  [ARCHIVE] {sub} source {url} is 404.")
                should_archive = True
            else:
                print(f"  [KEEP] {sub} exists at {url}.")

        if should_archive:
            target_path = os.path.join(archive_dir, sub)
            target_parent = os.path.dirname(target_path)
            if not os.path.exists(target_parent): os.makedirs(target_parent)
            
            print(f"  Archiving {sub} to {target_path}")
            run(f'git rm -r --cached "{sub}"')
            run(f'git config -f .gitmodules --remove-section submodule."{sub}"')
            
            sub_path = os.path.join(workspace_root, sub)
            if os.path.exists(sub_path):
                if os.path.exists(target_path): shutil.rmtree(target_path, ignore_errors=True)
                try:
                    shutil.move(sub_path, target_path)
                except Exception as e:
                    print(f"  Failed to move: {e}")

    print("\nReconciliation complete.")

if __name__ == "__main__":
    main()
