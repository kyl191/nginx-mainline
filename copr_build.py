#!/usr/bin/env python3
import json, os, sys
import requests
api_url = "https://copr.fedorainfracloud.org/api_2"
api_login = os.environ["copr_login"]
api_token = os.environ["copr_token"]

r = requests.get("%s/projects/%s/chroots" % (api_url, os.environ["copr_projectid"])).json()
chroots = []
for i in r.get("chroots"):
    chroots.append(i.get("chroot").get("name"))

metadata = {
    'chroots': chroots,
    'project_id': int(os.environ["copr_projectid"]),
}
files = {
    "srpm": (os.path.basename(sys.argv[1]), open(sys.argv[1], 'rb'), 'application/x-rpm'),
    "metadata": ('', json.dumps(metadata))
}
r = requests.post("%s/builds" % api_url, auth=(api_login, api_token), files=files)
