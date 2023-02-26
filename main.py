import authentication
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from google.oauth2.credentials import Credentials


# If modifying these scopes, delete the file token.json.
import userConfig

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Prints the start and name of the next 10 events on the user's calendar."""

    authentication.Authentication(SCOPES)
    config = userConfig.get_user_config()
    userConfig.save_config(config)
    # todo api interactions


if __name__ == '__main__':
    main()
