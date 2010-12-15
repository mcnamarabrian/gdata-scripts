"""
retrieving_user_calendars.py

Created by Brian Mcnamara on 2010-09-10.
Copyright (c) 2010. All rights reserved.

The purpose of this script is to list all of the calendars a user has access to.
"""

import gdata.apps.service
import gdata.calendar.service
import gdata.calendar

# These variables should be changed for the specific Google Apps domain
USER_EMAIL="USER@DOMAIN.COM"
USER_PASSWORD="USER_PASSWORD"


############################################
# NO NEED TO CHANGE BELOW FOR NORMAL USAGE #
############################################

# Authenticate to standard Apps service
calendar_service = gdata.calendar.service.CalendarService()
calendar_service.email = USER_EMAIL
calendar_service.password = USER_PASSWORD
calendar_service.source = 'LTech-Calendar-List-0.1'
calendar_service.ProgrammaticLogin()

feed = calendar_service.GetAllCalendarsFeed()
print feed.title.text
for i, a_calendar in enumerate(feed.entry):
  print '\t%s. %s' % (i, a_calendar.title.text,)
