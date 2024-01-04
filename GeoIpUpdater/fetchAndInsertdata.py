import os
import pathlib
import requests
import subprocess




BASE_DIR = pathlib.Path(__file__).parent

def get_repo_size(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    r = requests.get(url)
    if r.status_code == 200:
        response_json = r.json()
        return response_json["size"]
    else:
        return False


def check_git_installed():
    try:
        result = subprocess.run(['git', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
                                universal_newlines=True)
        git_version = result.stdout.strip()
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    except Exception as e:
        print(e)
        return False


def fetch_database_from_github() -> bool:
    ...


gitInstalled = check_git_installed()
if not gitInstalled:
    raise Exception("Git is not installed !!\ninstall git First")





fetch_database_from_github()

