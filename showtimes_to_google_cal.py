'''
uses the get_showtime_watchlist module to get all film showings in watchlist during work week.
Offers to create calender events for each movie at free times in calender that aren't during
the work week.

Using google calender's API.
'''

import os

cal_id = os.environ['GOOGLE_CAL_ID']
cal_api_key = os.environ['GOOGLE_CAL_API_KEY']


