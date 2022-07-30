# Authentication process with Google auth services. Correct SCOPES must be passed to Authentication.

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = []


class Authentication:
    def __init__(self, scopes: list):
        self.SCOPES = scopes

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)  # opens browser to get user consent
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())


def get_scopes():
    return Credentials.from_authorized_user_file("token.json").scopes