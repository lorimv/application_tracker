from . import credentials
from tracker import get_mail_info
from googleapiclient.discovery import build
import json

# this is the module that will auto-send follow up emails when -m is called
# im thinking it will have access to a tracker (spreadsheet) fn that returns company name & job title

def method():
    ##TODO write logic for follow-up email functions

    service = build("mail", "v1", credentials=credentials)
