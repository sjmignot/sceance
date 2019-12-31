# -*- coding: utf-8 -*-

'''
uses the get_showtime_watchlist module to get all film showings in watchlist during work week.
Offers to create calender events for each movie at free times in calender that aren't during
the work week.

Using google calender's API.
'''

from __future__ import print_function
import os
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
TIME_ZONE = 'France/Paris'
DATA_PATH = 'data/'
TOKEN_FILE = "token.pickle"
CRED_FILE = "credentials.json"

def build_and_add_event(service, film, theater, showtime):
    start_time = showtime.isoformat()
    end_time = start_time+datetime.timedelta(hours=film.film_length[0], minutes=film.film_length[1])

    event = {
      'summary': f'{film.name} at theater.name',
      'location': theater.address,
      'start': {
        'dateTime': start_time,
        'timeZone': TIME_ZONE,
      },
      'end': {
        'dateTime': end_time,
        'timeZone': 'America/Los_Angeles',
      },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()

def get_creds():
    creds = None
    if os.path.exists(DATA_PATH+TOKEN_FILE):
        with open(DATA_PATH+TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                DATA_PATH+CRED_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(DATA_PATH+TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

def create_projection_events(projection_list):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = get_creds()

    service = build('calendar', 'v3', credentials=creds)
    for project in projection_list:
        build_event(service, *project)
