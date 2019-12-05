from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class GCalendar(object):

    def __init__(self, config_path):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar.events', 'https://www.googleapis.com/auth/calendar']
        self.setup_calendar_service()
        self.config_path

    def setup_calendar_service(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.config_path + 'token.pickle'):
            with open(self.config_path + 'token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.config_path + 'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.config_path + 'token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

    def create_event(self, event):
        event = self.service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: {}'.format(event.get('htmlLink')))

    def get_all_event_ids(self):
        page_token = None
        event_ids = []
        while True:
            events = self.service.events().list(calendarId='primary', pageToken=page_token).execute()
            for event in events['items']:
                event_ids.append(event['id'])
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        return event_ids
        
    def delete_all_events(self):
        event_ids = self.get_all_event_ids()
        for event_id in event_ids:
            self.service.events().delete(calendarId='primary', eventId=event_id).execute() 
        print(f"Deleted {len(event_ids)} events")