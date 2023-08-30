import os
import json

def initialize_creds():
    credentials_path = os.environ.get('DOCS_PATH')

    if credentials_path == None:
        raise ValueError("Environmental var DOCS_PATH is not set.")
    
    with open(credentials_path, 'r') as credentials_file:
        credentials_json = json.load(credentials_file)

    return credentials_json

try: 
    credentials_json = initialize_creds()
except ValueError as e:
    credentials_json = None
    print(e)