# /usr/bin/python

import re
import sys

import bugzilla

from github import Github
from configobj import ConfigObj

config = ConfigObj('config')
b_user = config.get('user')
g_user, g_repo = tuple(sys.argv[1].split('/'))


g = Github()

repo = g.get_user(g_user).get_repo(g_repo)

bz_numbers = set()
for pr in repo.get_pulls():
    for commit in pr.get_commits():
        headline = commit.commit.message.split('\n', 1)[0]
        tag = re.search('RhBug:[0-9,\s]+\)', headline)
        if tag:
            for bz_number in re.findall('[0-9]+', tag.group(0)):
                bz_numbers.add((bz_number, pr))

bz = bugzilla.Bugzilla(url='https://bugzilla.redhat.com')

for bz_number, pr_url in bz_numbers:
    bug = bz.getbug(bz_number)
    if bug.status in ['NEW', 'ASSIGNED']:
        print(bug)
