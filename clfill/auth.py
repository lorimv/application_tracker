from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/drive']

def set_credentials():
    credentials_path = os.environ.get('CLFILL_KEY_PATH')

    if not credentials_path:
        raise ValueError("Environmental var CLFILL_KEY_PATH is not set.")


def authenticate():
    print('authenticate() called')