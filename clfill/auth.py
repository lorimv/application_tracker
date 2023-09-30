"""Module housing all functions responsible for authorizing credentials
"""

import os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/documents',
          'https://www.googleapis.com/auth/gmail.send']


def get_path():
    """Gets the path to credentials from environmental variable

    Returns:
        str: path to the credentials files

    """
    credentials_path = os.environ.get('CLFILL_KEY_PATH')
    if not credentials_path:
        raise ValueError('Environmental var CLFILL_KEY_PATH is not set.')
    return credentials_path


def authenticate(credentials_path):
    """Locates credentials file, then returns Credentials obj

    Args:
        credentials_path (str): the path to the user's credentials json file

    Returns:
        Credentials: credentials object used to build service

    """
    # create Flow instance using specified path
    flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
    credentials = flow.run_local_server(port=0)
    return credentials

# TODO maybe add ini support, logic to check for ini creds before
# getting path to json credentials user secret & creating flow
