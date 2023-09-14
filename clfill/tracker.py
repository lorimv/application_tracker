from . import credentials
from googleapiclient.discovery import build
import json

# I think the function will CREATE a spreadsheet if not created...
# ...then store the ID in a permanent place for future use

def track():
    # TODO write logic for document editor functions

    service = build('sheets', 'v4', credentials=credentials)
    if ():  # the place where we store tracker's docId is empty...
        tracker = service.sheets().create()
        # store tracker's id

def get_mail_info():
    # returns the email, company name, job position from any non-followed up applications    
    if ():  # the place where we store tracker's docId is empty...
        return []

    # up here we will configure 'range' vars to include columns for company, position, and emails
    # check if an app is in progress ('Yes') ->
    # check if an app has been followed up ('No') ->
    # check if an app is ready to be followed up (app date >= today's date) ->
    # output job title, company name, email address
    mailinfo = []
    service = build('sheets', 'v4', credentials=credentials)
    result = service.spreadsheets().values().batchGet(
        spreadsheetId=OURSHEETID, ranges=INSERTRANGEHERE).execute()
    return result
    # here's where we add company name, job position, email from any job w/ "No" in followed up section

    return mailinfo
