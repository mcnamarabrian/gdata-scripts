"""
provisioning_postini_from_gapps_accounts.py

Created by Brian Mcnamara on 2010-07-09.
Copyright (c) 2010. All rights reserved.
"""

# The purpose of this script is to generate a single text file that contains the necessary
# information to build a valid Postini batch file based upon information stored in the specified
# Google Apps domain.
#
# Users are added, user nicknames are defined as Postini aliases, and groups are added as aliases
# to the defined admin user.

import gdata.apps.service
import gdata.apps.groups.service

# These variables should be changed for the specific Google Apps domain
ADMIN_EMAIL="ADMIN@DOMAIN.COM"
DOMAIN="DOMAIN.COM"
PASSWORD="APPS_PASSWORD"
POSTINI_ADMIN="POSTINI_ADMIN_ACCOUNT"
POSTINI_ADDUSER_OPTIONS="OPTIONS_TO_ADDUSER_COMMAND"  # eg. ", welcome=0"


############################################
# NO NEED TO CHANGE BELOW FOR NORMAL USAGE #
############################################

# Authenticate to standard Apps service
service = gdata.apps.service.AppsService(email=ADMIN_EMAIL, domain=DOMAIN, password=PASSWORD)
service.ProgrammaticLogin()

domain_users = []
user_feed = service.RetrieveAllUsers()

# Put listing of all Google Apps domain users in an array
for user_entry in user_feed.entry:
	domain_users.append(user_entry.login.user_name)


# Authenticate to Groups service
groups_service = gdata.apps.groups.service.GroupsService(email=ADMIN_EMAIL, domain=DOMAIN, password=PASSWORD)
groups_service.ProgrammaticLogin()

domain_groups = []
group_feed = groups_service.RetrieveAllGroups()

# Put listing of all Google Apps group email in an array
for group_entry in group_feed:
	domain_groups.append(group_entry['groupId'])

# Open file for writing
# Default file name is DOMAIN.batch
output = open('./' + DOMAIN + '.batch', 'w')

# Iterate through each user in the array
for user in domain_users:
	# Speficy Postini batch adduser options
	output.write('adduser %s@%s%s\n' % (user, DOMAIN, POSTINI_ADDUSER_OPTIONS))
	
	# Retrieve nicknames for the specified user and add the values to an array
	user_nicknames = []
	for nickname in service.RetrieveNicknames(user).entry:
		user_nicknames.append(nickname.title.text)
	
	# Iterate through each nickname in the array
	for nickname in user_nicknames:
		# Speficy Postini batch addalias options
		output.write('addalias %s@%s, %s@%s\n' % (user, DOMAIN, nickname, DOMAIN))
		
for group_name in domain_groups:
	output.write('addalias %s, %s\n' % (POSTINI_ADMIN, group_name))
