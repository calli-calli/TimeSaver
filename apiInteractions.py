# downloads all events from calendar in specified time.
from datetime import datetime

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import configparser
import authentication


# todo: after updating userConfig
# change "DEFAULT"-Section for settings to "CURRENT"


def download_appointments() -> list:
    """Downloads all appointments in specified time period. Valid token.json must exist."""

    # load configuration
    config = configparser.ConfigParser()
    config.read("config.ini")
    utc_start = config["DEFAULT"]["start_date"]
    utc_end = config["DEFAULT"]["end_date"]

    now = datetime.utcnow().isoformat() + 'Z'

    creds = Credentials.from_authorized_user_file("token.json", authentication.get_scopes())
    service = build(serviceName="calendar", version="v3", credentials=creds)

    # todo calendar id should be flexible -> primary when default
    events_result = service.events().list(calendarId='primary', timeMin=utc_start, timeMax=utc_end, maxResults=10000,
                                          singleEvents=True, orderBy='startTime').execute()  # maxResults capped at 2500
    raw_events = events_result.get('items', [])
    print(type(raw_events))
    events = []
    for count, event in enumerate(raw_events):
        events.append({"start": event["start"].get("dateTime"),
                       "end": event["end"].get("dateTime"),
                       "summary": event["summary"] if ("summary" in event) else "",
                       "description": event["description"] if ("description" in event) else ""})
    print(len(events))
    return events


if __name__ == '__main__':
    download_appointments()
