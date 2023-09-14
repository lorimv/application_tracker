import os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_path():
    ## TODO this is pretty redundant now
    credentials_path = os.environ.get('CLFILL_KEY_PATH')
    if not credentials_path:
        raise ValueError('Environmental var CLFILL_KEY_PATH is not set.')

# uses path environment variable to locate credentials file, then returns Credentials obj
def authenticate():
    # store path from environment variable (TODO maybe repace with arg like in old version)
    credentials_path = os.environ.get('CLFILL_KEY_PATH')
    # create Flow instance using specified path
    flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
    credentials = flow.run_local_server(port=0)
    return credentials
