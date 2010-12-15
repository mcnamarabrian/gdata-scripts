"""
group_blast.py

Created by Brian Mcnamara on 2010-00-28.
Copyright (c) 2010. All rights reserved.
"""

# The purpose of this script is to recreate group membership in Google Apps
# to match the characteristics of a specified CSV file.
# This will save users from manually entering group members when the 

import gdata.apps.service
import gdata.apps.groups.service
import sys

# These variables should be changed for the specific Google Apps domain
ADMIN_EMAIL="admin@domain.com"
DOMAIN="domain.com"
PASSWORD="password"

# The first parameter is the group name
GROUP_NAME = sys.argv[1]
# The second parameter is the CSV file
INFILE = open(sys.argv[2], "r")


############################################
# NO NEED TO CHANGE BELOW FOR NORMAL USAGE #
############################################

# Get listing of users in file INFILE into a list
raw_users = INFILE.readlines()
users = []
for user in raw_users:
	users.append(user.strip())

# Authenticate to Groups service
groups_service = gdata.apps.groups.service.GroupsService(email=ADMIN_EMAIL, domain=DOMAIN, password=PASSWORD)
groups_service.ProgrammaticLogin()

try:
	group_feed = groups_service.RetrieveGroup(GROUP_NAME)
	print "Group already exists.  Attempting to delete group", GROUP_NAME
	groups_service.DeleteGroup(GROUP_NAME)
except gdata.apps.service.AppsForYourDomainException:
	print "Group", GROUP_NAME, "does not exist"

#if group_feed:

print "Adding group", GROUP_NAME
groups_service.CreateGroup(GROUP_NAME+'@'+DOMAIN, GROUP_NAME, '', "Domain")


print "Adding members to group: ", GROUP_NAME
print "This will take some time."
for USER in users:
	print "\tAdding", USER
	groups_service.AddMemberToGroup(USER, GROUP_NAME)
