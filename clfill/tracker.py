from googleapiclient.discovery import build
from . import credentials
from .mailer import send_mail
from .config_handler import get_config_value, set_config_value
# import json

# I think the function will CREATE a spreadsheet if not created...
# ...then store the ID in a permanent place for future use

def update_tracker():
    # TODO write logic for document editor functions

    service = build('drive', 'v3', credentials=credentials)
    if (get_config_value('Tracker', 'trackerId') == ''):  # ...there is no trackerId in ini file...
        tracker = service.drive().create()  # create tracker, add id to ini TODO we now are using drive api vs sheets, update syntax
        set_config_value('Tracker', 'trackerId', tracker.TRACKERS_ID_HERE_TODO)

def get_email_info():
    # returns the email, company name, job position from any non-followed up applications
    if (get_config_value('Tracker', 'trackerId') == ''):  # TODO the place where we store tracker's docId is empty...
        return []

    # up here we will configure 'range' vars to include columns for company, position, and emails
    # check if an app is in progress ('Yes') ->
    # check if an app has been followed up ('No') ->
    # check if an app is ready to be followed up (app date >= today's date) ->
    # output job title, company name, email address
    email_info = []

    for n in (n):  # TODO edit logic here to add each valid row to email_info array
        service = build('drive', 'v3', credentials=credentials)
        result = service.spreadsheets().values().batchGet(
            spreadsheetId=OURSHEETID, ranges=INSERTRANGEHERE).execute()
        email_info.append(result)
    return result

def email_scheduler(email_info):
    # this fn will be responsible for calling send_mail on each necessary row
    # for each spreadsheet row in email_info list...
    send_mail()
    return
