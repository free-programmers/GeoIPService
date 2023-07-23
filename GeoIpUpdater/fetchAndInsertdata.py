import json
import os
import pathlib
import requests
import subprocess


from GeoIpCore import app
with app.app_context():
    print(app.config)

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
    if not os.path.exists(BASE_DIR / "database"):
        os.mkdir(BASE_DIR / "database")

    repo_url = "https://github.com/free-programmers/IP2Geo-database.git"
    repo_name = "IP2Geo-database"
    repo_owner = "free-programmers"
    repo_size = get_repo_size(repo_owner, repo_name)

    print("Cloning database from github\nThis take a while(Base on Your Internet speed)\nplease wait ...")
    print(f"DataBase Size: {repo_size or '800-2000'} MB")
    result = os.system(f"git clone {repo_url}")

    if not result:
        return False
    else:
        os.rename(BASE_DIR.parent / repo_name, BASE_DIR / "database" / repo_name)
        print("Clone completed successfully")
        print(f"Database is cloned at {BASE_DIR / 'database'}")
        return True


gitInstalled = check_git_installed()
if not gitInstalled:
    raise Exception("Git is not installed !!\ninstall git First")

# if not fetch_database_from_github():
#     raise Exception("Failed to fetch database from github")
#

def add_country_info():
    country_info = BASE_DIR / "database" / "IP2Geo-database" / "Countries-database"

    countries = (os.listdir(country_info))
    for each in countries:
        for c in os.listdir(country_info / each):
            with open(country_info / each / c, mode="r", encoding="utf-8") as f:
                print(json.load(f))


add_country_info()

