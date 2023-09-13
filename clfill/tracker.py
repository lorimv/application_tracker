from . import credentials
from googleapiclient.discovery import build
import json

# I think the function will CREATE a spreadsheet if not created...
# ...then store the ID in a permanent place for future use

def track():
    ##TODO write logic for document editor functions

    service = build("sheets", "v1", credentials=credentials)
    if (# the place where we store tracker's docId is empty... 
        tracker = service.sheets().create()
        #store tracker's id

def get_mail_info():
    # returns the email, company name, job position from any non-followed up applications    
    if (#the place where we store tracker's docId is empty...)
        return []

    mailinfo = []
    service = build("sheets", "v1", credentials=credentials)

    # here's where we add company name, job position, email from any job w/ "No" in followed up section

    return mailinfo
