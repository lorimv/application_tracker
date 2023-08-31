import os
import json
import __init__

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

def get_creds():
    while __init__.credentials == None:
        __init__.credentials = ""

        Credentials