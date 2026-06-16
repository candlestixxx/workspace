import os
import subprocess

def run_cmd(cmd, cwd=None):
    try:
        res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
        return res.stdout.strip()
    except:
        return ""

def get_robert_repos():
    with open("robertpelloni_repos.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

robert_repos = get_robert_repos()
def is_git_repo(d):
    git_path = os.path.join(d, ".git")
    return os.path.exists(git_path)

dirs = [d for d in os.listdir(".") if os.path.isdir(d) and is_git_repo(d)]

print(f"{'Directory':<40} {'Remote URL':<60} {'Action'}")
print("-" * 120)

for d in dirs:
    url = run_cmd("git remote get-url origin", cwd=d)
    name = d.lower()
    is_robert = any(r.lower() == name for r in robert_repos)
    is_candlestixxx = "candlestixxx" in url.lower()
    
    action = "KEEP"
    if "robertpelloni" in url.lower() and name != "ultratrader":
        action = "REMOVE (robert url)"
    elif is_robert and name != "ultratrader":
        action = "REMOVE (robert fork name)"
    elif not is_candlestixxx and name != "ultratrader":
        action = "REMOVE (not candlestixxx)"
    
    print(f"{d:<40} {url:<60} {action}")
