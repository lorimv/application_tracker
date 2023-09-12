from . import credentials
from googleapiclient.discovery import build
import json

# this is the module that will auto-send follow up emails when -m is called

##TODO 'documentId' environmental var?
# TODO when should it be set up? 

def method():
    ##TODO write logic for follow-up email functions

    service = build("mail", "v1", credentials=credentials)
