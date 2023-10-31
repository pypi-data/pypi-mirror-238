import json
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Calendar:

    def __init__(self, calendarId):
        self.scopes = ['https://www.googleapis.com/auth/calendar.readonly']
        creds = self._get_credentials()
        self.service = build("calendar",
                             "v3",
                             credentials=creds,
                             static_discovery=False)
        self.calendarId = calendarId

    def _get_credentials(self):
        creds = None
        token_json = os.getenv('GOOGLE_CALENDAR_CREDENTIALS')
        if token_json:
            creds = Credentials.from_authorized_user_info(
                json.loads(token_json), self.scopes)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', self.scopes)
            creds = flow.run_local_server(port=0)
        return creds

    def list_events(self, start_date):
        """
        :param start_date: The date filter for the events. Expects an ISO formatted date object
        Example: pendulum.datetime(2020, 9, 1).isoformat()

        :return: Dictionary of event items
        """

        page_token = None
        events = []
        count = 0

        while True:
            events_list = self.service.events().list(
                calendarId=self.calendarId,
                pageToken=page_token,
                timeMin=start_date,
                maxResults=100,
                singleEvents=True,
                orderBy='startTime').execute()

            for event in events_list['items']:
                events.append(event)

            page_token = events_list.get('nextPageToken')

            count += 1

            print(f"Google Calendar: Fetching results from page {count} ...")

            if not page_token:
                break

        print(f"Fetched a total of {len(events)} events.")
        return events
