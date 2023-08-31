import os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_path():
    credentials_path = os.environ.get('CLFILL_KEY_PATH')
    if not credentials_path:
        raise ValueError('Environmental var CLFILL_KEY_PATH is not set.')
    return credentials_path

def authenticate(credentials_path):
    flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
    credentials = flow.run_local_server(port=0)
    return credentials