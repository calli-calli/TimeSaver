# Authentication process with Google auth services. Correct SCOPES must be passed to Authentication.

import os.path

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth import exceptions


# todo if the user doesn't have an old token, authentication will be requested twice this may happen on first run.
#  This authentication flow had some buggy lines removed. Double check on Calendar api documentation.
class Authentication:
    """Authenticates program via Google services."""

    def __init__(self, scopes: list):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token and creds.valid:  # creds.valid is a dirty bugfix
                creds.refresh(Request())  # google.auth.exceptions.RefreshError: ('invalid_grant: Bad Request',
                # {'error': 'invalid_grant', 'error_description': 'Bad Request'})
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())


def get_scopes():
    return Credentials.from_authorized_user_file("token.json").scopes


if __name__ == "__main__":
    _scopes = ['https://www.googleapis.com/auth/calendar.readonly']
    Authentication(scopes=_scopes)


