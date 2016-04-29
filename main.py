# /usr/bin/python

import re
import sys

from github import Github
from configobj import ConfigObj

config = ConfigObj('config')
b_user = config.get('user')
g_user, g_repo = tuple(sys.argv[1].split('/'))

g = Github()

repo = g.get_user(g_user).get_repo(g_repo)

for pr in repo.get_pulls():
    print(pr)
