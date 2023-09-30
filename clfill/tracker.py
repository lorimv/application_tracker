from googleapiclient.discovery import build
from . import credentials
from .mailer import send_mail
from .config_handler import get_config_value, set_config_value
# import json

def create_tracker():
    service = build('sheets', 'v4', credentials=credentials)

    tracker_body = {
        'properties': {
            'title': 'clfill_application_tracker'
        },
        'sheets': [
            {
                'data': [
                    {
                        'rowData': [
                            {'values': [
                                {'Company': 'Header1'},
                                {'Job Title': 'Header2'},
                                {'App Date': 'Header3'},
                                {'Followed Up': 'Header4'},
                                {'In Progress': 'Header5'},
                                {'Location': 'Header6'},
                                {'Company Email': 'Header7'},
                                {'Other': 'Header8'}]
                             }
                        ]
                    }
                ]  # jesus
            }
        ]
    }

    tracker = service.spreadsheets().create(body=tracker_body).execute()
    set_config_value('Tracker', 'trackerId', tracker['spreadsheetId'])


def update_tracker():
    """updates tracker, calling email follow up functions
    """
    # TODO write logic for document editor functions

    service = build('drive', 'v3', credentials=credentials)
    if get_config_value('Tracker', 'trackerId') == '':  # ...there is no trackerId in ini file...
        tracker = service.files().create()  # create tracker, add id to ini TODO we now are using drive api vs sheets, update syntax
        set_config_value('Tracker', 'trackerId', tracker.TRACKERS_ID_HERE_TODO)

def get_email_info():
    # returns the email, company name, job position from any non-followed up applications
    tracker_id = (get_config_value('Tracker', 'trackerId'))
    if (tracker_id == ''):  # TODO the place where we store tracker's docId is empty...
        return []
    
    # up here we will configure 'range' vars to include columns for company, position, and emails
    # check if an app is in progress ('Yes') ->
    # check if an app has been followed up ('No') ->
    # check if an app is ready to be followed up (app date >= today's date) ->
    # output job title, company name, email address

    service = build('sheets', 'v4', credentials=credentials)
    email_info = []

    for n in (n):  # TODO edit logic here to add each valid row to email_info array
        result = service.spreadsheets().values().batchGet(
            spreadsheetId=tracker_id, ranges=INSERTRANGEHERE).execute()
        email_info.append(result)
    return email_info


def email_scheduler(email_info):
    """this fn will be responsible for calling send_mail on each necessary row
    for each spreadsheet row in email_info list...
    Params:
        email_info ([str]): rows (individual apps) needed to pass into mailer.send_mail()
    """
    for row in email_info:
        send_mail(row[0], row[1], row[2], row[3])  # TODO actually get params
