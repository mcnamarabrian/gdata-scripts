"""
list_nicknames.py

Created by Brian Mcnamara on 2010-07-09.
Copyright (c) 2010. All rights reserved.
"""

import gdata.apps.service
import sys

# Variable Definitions
nicknames = []
target_user = sys.argv[1]
ADMIN_EMAIL="admin@domain.com"
DOMAIN="domain.com"
PASSWORD="password"

client = gdata.apps.service.AppsService(email=ADMIN_EMAIL, domain=DOMAIN, password=PASSWORD)
client.ProgrammaticLogin()

user_feed = client.RetrieveNicknames(target_user)

for nickname in user_feed.entry:
	nicknames.append(nickname.title.text)
	
print "There are", len(nicknames), "nicknames for", target_user
print str(nicknames)
