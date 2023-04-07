# downloads all events from calendar in specified time.
import warnings
from datetime import datetime

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import authentication
import userConfig


def initialize():
    creds = Credentials.from_authorized_user_file("token.json", authentication.get_scopes())
    service = build(serviceName="calendar", version="v3", credentials=creds)
    return service


def download_appointments() -> list:
    """start_date & end_date must be in iso-format.
    Downloads all appointments in specified time period. Valid token.json must exist."""
    # setup configuration
    config = userConfig.get_pref()
    utc_start = config["start_date"].isoformat() + "Z"
    utc_end = config["end_date"].isoformat() + "Z"
    cal_id = convert_name_to_id(config["cal_name"])
    print(f"checking this timeframe: {utc_start} - {utc_end}")
    # download events
    events_result = initialize().events().list(calendarId=cal_id, timeMin=utc_start, timeMax=utc_end,
                                               maxResults=10,  # todo change to 10000, Results capped at 2500
                                               singleEvents=True, orderBy='startTime').execute()
    raw_events = events_result.get('items', [])
    events = []
    for count, event in enumerate(raw_events):
        events.append({"start": event["start"].get("dateTime"),
                       "end": event["end"].get("dateTime"),
                       "summary": event["summary"] if ("summary" in event) else "",
                       "description": event["description"] if ("description" in event) else ""})

    print(f"num of events: {len(events)}")
    if not len(events) == 0:
        print(f"\tstart: {event['start'].get('dateTime')}\n"
              f"\tend:   {event['end'].get('dateTime')}\n")
    else:
        print("no events found")
    return events


def get_calendar_names() -> list:
    """Downloads all available calendar names"""
    cal_names = []
    cal_raw = initialize().calendarList().list().execute()
    for calendar in cal_raw["items"]:
        cal_names.append(calendar["summary"])
    return cal_names


def convert_name_to_id(name: str) -> str:
    """Searches for corresponding Calendar ID. If unavailable returns 'primary' and warns"""
    cal_raw = initialize().calendarList().list().execute()
    cal_id = "primary"
    found = False
    for calendar in cal_raw["items"]:  # search for corresponding calendar id
        if calendar["summary"] == name:
            cal_id = calendar["id"]
            found = True
    if name == "primary" and not found:
        warnings.warn("Calendar name not found")
    return cal_id


if __name__ == '__main__':
    print("----")
    cals = convert_name_to_id("Garten")
    print(cals)
