#!/usr/bin/env python3
import os
import sys
import requests
api_url = "https://copr.fedorainfracloud.org/api_2"
api_login = os.environ["copr_login"]
api_token = os.environ["copr_token"]
project_id = int(os.environ["copr_projectid"])

r = requests.get("%s/projects/%s/chroots" % (api_url, project_id))
if not r.ok:
    print(r.json().get("message", "Error returned, but no message"))
    sys.exit(1)

chroots = [i.get("chroot").get("name") for i in r.json().get("chroots")]

gh_url = "https://api.github.com/repos/{}/{}/releases/latest".format(
    os.environ["CIRCLE_PROJECT_USERNAME"],
    os.environ["CIRCLE_PROJECT_REPONAME"]
)
gh = requests.get(gh_url)
if not gh.ok:
    print("Failed to fetch latest Github release")
    print(gh.json())
    sys.exit(1)

assets = gh.json().get("assets")
if len(assets) > 1:
    print("More than 1 asset uploaded to Github, unexpected")
    sys.exit(1)
asset = assets[0].get("browser_download_url")
if not asset.endswith(".src.rpm"):
    print("Github asset is not a .src.rpm")
    sys.exit(1)

metadata = {
    'chroots': chroots,
    'project_id': project_id,
    'srpm_url': asset,
}

r = requests.post("%s/builds" % api_url,
                  auth=(api_login, api_token),
                  json=metadata)
if r.status_code != 201:
    print(r.json().get("message", "Error returned, but no message"))
    sys.exit(1)
print("Build started at {}".format(r.headers["Location"]))
