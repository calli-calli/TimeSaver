# downloads all events from calendar in specified time.
import warnings
from datetime import datetime

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import authentication
import userConfig

_SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def _initialize():
    authentication.Authentication(_SCOPES)
    creds = Credentials.from_authorized_user_file("token.json", authentication.get_scopes())
    service = build(serviceName="calendar", version="v3", credentials=creds)
    return service


def _validate(events):
    if not userConfig.get_pref("all_day")["all_day"]:
        for i, event in enumerate(events):
            if event["all_day"]:
                events.pop(i)
    return events


def download_appointments() -> list:
    """Downloads all appointments in specified time period. Valid token.json must exist."""
    # setup configuration
    config = userConfig.get_pref()
    utc_start = config["start_date"].isoformat() + "Z"
    utc_end = config["end_date"].isoformat() + "Z"
    cal_id = convert_name_to_id(config["cal_name"])
    # download events
    events_result = _initialize().events().list(calendarId=cal_id, timeMin=utc_start, timeMax=utc_end,
                                                maxResults=10000,  # Results capped at 2500
                                                singleEvents=True, orderBy='startTime').execute()
    raw_events = events_result.get('items', [])

    events = []
    for count, event in enumerate(raw_events):
        if not (event["start"].get("dateTime") is None):  # Get data for "normal" events
            all_day = False
            start = event["start"].get("dateTime")
            start = start[:-6]
            end = event["end"].get("dateTime")
            end = end[:-6]
        else:  # Get start- and end-time for "all day"-events
            all_day = True
            start = event["start"].get("date") + "T16:00:00"
            end = event["end"].get("date") + "T16:00:00"
        events.append({"start": datetime.fromisoformat(start),
                       "end": datetime.fromisoformat(end),
                       "summary": event["summary"] if ("summary" in event) else "",
                       "description": event["description"] if ("description" in event) else "",
                       "all_day": all_day})
    events = _validate(events)
    return events


def get_calendar_names() -> list:
    """Downloads all available calendar names"""
    cal_names = []
    cal_raw = _initialize().calendarList().list().execute()
    for calendar in cal_raw["items"]:
        cal_names.append(calendar["summary"])
    return cal_names
    # return["primary"]


def convert_name_to_id(name: str) -> str:
    """Searches for corresponding Calendar ID. If unavailable returns 'primary' and warns"""
    cal_raw = _initialize().calendarList().list().execute()
    cal_id = "primary"
    found = False
    for calendar in cal_raw["items"]:  # search for corresponding calendar id
        if calendar["summary"] == name:
            cal_id = calendar["id"]
            found = True
    if name != "primary" and not found:
        warnings.warn("Calendar name not found")
    return cal_id


if __name__ == '__main__':
    pass
