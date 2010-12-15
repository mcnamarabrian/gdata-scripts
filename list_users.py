"""
list_users.py

Created by Brian Mcnamara on 2010-07-09.
Copyright (c) 2010. All rights reserved.
"""
ADMIN_EMAIL='user@domain.com'
ADMIN_PASSWORD='password'
DOMAIN='domain.com'

import gdata.apps.service

client = gdata.apps.service.AppsService(email=ADMIN_EMAIL, domain=DOMAIN, password=ADMIN_PASSWORD)
client.ProgrammaticLogin()

domain_users = []
user_feed = client.RetrieveAllUsers()

for user_entry in user_feed.entry:
	domain_users.append(user_entry.login.user_name)

# Print out a listing of users in the domain
for user in domain_users:
    print user


