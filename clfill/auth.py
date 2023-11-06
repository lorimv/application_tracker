"""Module housing all functions responsible for authorizing credentials
"""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/documents',
          'https://www.googleapis.com/auth/gmail.send']


def get_credentials():
    """Gets credentials from cached files, or creates credentials from
    api key and then caches them in /config

    Return:
        credentials: credentials to create stuff

    """
    try:
        user_credentials = credentials.Credentials.from_authorized_user_file('config/credentials.json')
    except FileNotFoundError:
        user_credentials = authenticate(get_path())
        with open('config/credentials.json', 'w', encoding='utf8') as f:
            json.dump(json.loads(user_credentials.to_json()), f)  # maybe only dump if we know it works?
    return user_credentials


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
    user_credentials = flow.run_local_server(port=0)
    return user_credentials
