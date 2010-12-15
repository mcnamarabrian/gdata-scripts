"""
Name: docs_permission_audit.py

Description: The script will generate a CSV file that shows the rights for all Google Docs documents in a given domain.  The initial intent was to show whether documents are shared with users outside of a given Google Apps domain.

Authors:  Brian McNamara & Brian Dorry (LTech)
"""

import gdata.apps.service
import gdata.gauth
import gdata.docs.client
import gdata.docs.service

# Variable definitions
ADMIN_EMAIL = "admin@domain.com"
ADMIN_PASSWORD = "admin_password"
CONSUMER_KEY = "domain.com"
CONSUMER_SECRET = "random_string" # Pulled from Google Apps Control Panel
domain_users = []
domain_documents = {}
output = open('./' + CONSUMER_KEY + '-GoogleDocsPermissionsAudit.csv', 'w')

# DO NOT MODIFY SCRIPT BELOW THIS POINT

# Gather listing of all users in the domain and put them in an array domain_users
apps_client = gdata.apps.service.AppsService(email=ADMIN_EMAIL, domain=CONSUMER_KEY, password=ADMIN_PASSWORD)
apps_client.ProgrammaticLogin()
user_feed = apps_client.RetrieveAllUsers()

for user_entry in user_feed.entry:
	domain_users.append(user_entry.login.user_name) 
	
# Iterate through each user in the domain_users array and gather document information
for user in domain_users:
	
	# Generate the requestor_id in format user@domain.com and generate oauth_token based on request
	requestor_id = user + '@' + CONSUMER_KEY
	two_legged_oauth_token = gdata.gauth.TwoLeggedOAuthHmacToken(
	    CONSUMER_KEY, CONSUMER_SECRET, requestor_id)
	
	
	# Set parameters for client request
	print "Working on user", user
	docs_client = gdata.docs.client.DocsClient(source="LTech-Docs-Audit-v1")
	docs_client.auth_token = two_legged_oauth_token
	docs_client.ssl = True
	docs_client.http_client.debug = False
	
	# Get list of all documents in a feed
	doc_feed = docs_client.GetDocList()

	# Iterate thru the feed and look at ACL for each document
	for doc in doc_feed.entry:
		print "Working on document", doc.title.text
		if domain_documents.has_key(doc.resource_id.text):
			print "Document previously processed"
		else:
			print "Processing", doc.title.text
			doc_permissions = [doc.title.text,[]]

			#print doc.title.text#, '-> ', doc.resource_id.text
			#domain_documents.append(doc.resource_id.text)
			
			print "Fetching access control list"
			acl_feed = docs_client.GetAclPermissions(doc.resource_id.text)
		
			print "Found", str(len(acl_feed.entry)), "entries"
			for acl_entry in acl_feed.entry:
				print "Adding %s (%s) as %s of %s" %(acl_entry.scope.value, acl_entry.scope.type, acl_entry.role.value, doc.title.text)
				# print '%s - %s - %s (%s)' % (doc.title.text, acl_entry.role.value, acl_entry.scope.value, acl_entry.scope.type)
				doc_permissions[1].append({'role':acl_entry.role.value, 'scope':acl_entry.scope.value, 'type':acl_entry.scope.type})
			
			domain_documents[doc.resource_id.text] = doc_permissions

output.write('document,user,role,type\n')
for key in domain_documents.keys():
	for permission in domain_documents[key][1]:
		output.write("%s,%s,%s,%s\n" % (domain_documents[key][0], permission['scope'], permission['role'], permission['type']))
