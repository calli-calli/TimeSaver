# downloads all events from calendar in specified time.
import datetime

from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

import authentication


def download_appointments(start_date: datetime, end_date: datetime) -> dict:
    """Downloads all appointments in specified time period. Valid token.json must exist."""
    # todo parse datetime params to utc time
    creds = Credentials.from_authorized_user_file("token.json", authentication.get_scopes())
    service = build(serviceName="calendar", version="v3", credentials=creds)
    events_result = service.events().list(calendarId='primary', timeMin=,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
# try:
#     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     service = build('calendar', 'v3', credentials=creds)
#
#     # Call the Calendar API
#     now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
#     print('Getting the upcoming 10 events')
#     events_result = service.events().list(calendarId='primary', timeMin=now,
#                                           maxResults=10, singleEvents=True,
#                                           orderBy='startTime').execute()
#     events = events_result.get('items', [])
#
#     if not events:
#         print('No upcoming events found.')
#         return
#
#     # Prints the start and name of the next 10 events
#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         print(start, event['summary'])
#
# except HttpError as error:
#     print('An error occurred: %s' % error)
