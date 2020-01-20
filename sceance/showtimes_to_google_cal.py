# -*- coding: utf-8 -*-

'''
uses the get_showtime_watchlist module to get all film showings in watchlist during work week.
Offers to create calender events for each movie at free times in calender that aren't during
the work week.

Using google calender's API.
'''

import os
import os.path

import datetime
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

TOKEN_FILE = "token.pickle"
CRED_FILE = "credentials.json"

MY_PATH = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = 'data/'

TIME_ZONE = "Europe/Paris"

def build_and_add_event(service, film, theater, showtime):
    '''builds an event object and adds it to the google calendar'''
    start_time = showtime
    end_time = start_time+datetime.timedelta(hours=int(film.length[0]), minutes=int(film.length[1]))

    event = {
        'summary': f'{film.name} at {theater.name}',
        'location': theater.address,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': TIME_ZONE,
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': TIME_ZONE,
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

def get_creds():
    '''gets and returns user credentials either from a token or creates a new token if said token expired'''
    creds = None
    token_file = os.path.join(MY_PATH, f"{DATA_PATH}{TOKEN_FILE}")
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(MY_PATH, f"{DATA_PATH}{CRED_FILE}"), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_projection_events(projection_list):
    '''gets credentials, builds calendar API object and for each projection, builds and sends an event to your calendar'''
    creds = get_creds()
    service = build('calendar', 'v3', credentials=creds)
    for project in projection_list:
        print(project)
        build_and_add_event(service, *project)
