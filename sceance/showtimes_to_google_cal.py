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
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

TOKEN_FILE = "token.pickle"
CRED_FILE = "credentials.json"

MY_PATH = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = 'data/'

COLOR = {
    'purple': '\033[95m',
    'cyan': '\033[96m',
    'darkcyan': '\033[36m',
    'blue': '\033[94m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'bold': '\033[1m',
    'underline': '\033[4m',
    'end': '\033[0m',
}

def bold(word):
    return COLOR['bold']+word+COLOR['end']

def underline(word):
    return COLOR['underline']+word+COLOR['end']

def build_and_add_event(service, film, theater, showtime, timezone):
    '''builds an event object and adds it to the google calendar'''
    start_time = showtime
    end_time = start_time+datetime.timedelta(hours=int(film.length[0]), minutes=int(film.length[1]))

    event = {
        'summary': f'{film.name} at {theater.name}',
        'location': theater.address,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': timezone,
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created for {underline(film.name)} at {theater.name} at {start_time.strftime('%b %d %Y %H:%M')}:\n{event.get('htmlLink')}")

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
                os.path.join(MY_PATH, f"{DATA_PATH}{CRED_FILE}"), SCOPES, autogenerate_code_verifier=True
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_projection_events(projection_list, timezone):
    '''gets credentials, builds calendar API object and for each projection, builds and sends an event to your calendar'''
    creds = get_creds()
    service = build('calendar', 'v3', credentials=creds)
    for project in projection_list:
        build_and_add_event(service, *project, timezone)
