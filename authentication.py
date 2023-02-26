# Authentication process with Google auth services. Correct SCOPES must be passed to Authentication.

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth import exceptions


class Authentication:
    """Authenticates program via google services. Passed scopes are used"""

    def __init__(self, scopes: list):

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            try:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())  # buggy, explanation in catch statement
                else:
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
                    creds = flow.run_local_server(port=0)  # opens browser to get user consent
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
            except exceptions.RefreshError:
                # traceback.print_exc() Requesting a refresh may not be supported for the license this product is
                # using. This Error is handled via the manual creation of a new token.
                pass
            finally:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
                creds = flow.run_local_server(port=0)  # opens browser to get user consent
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())


def get_scopes():
    return Credentials.from_authorized_user_file("token.json").scopes
