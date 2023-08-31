import os
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

def set_creds():
    credentials_path = os.environ.get('DOCS_PATH')

    if credentials_path == None:
        raise ValueError("Environmental var DOCS_PATH is not set.")
    
    with open(credentials_path, 'r') as credentials_file:
        credentials = Cre ##get creds here

    return credentials_json

try: 
    credentials = set_creds()
except ValueError as e:
    credentials_json = None
    print(e)
    print("Please set DOCS_PATH to the path to .json key file")
    print("(Windows: \'set <varname>=<value>\')")