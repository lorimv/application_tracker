"""module housing all spreadsheet-related functions
"""
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from . import credentials
from .mailer import send_mail
from .config_handler import get_config_value, set_config_value

# TODO maybe add refresh() allowing users to inform tracker when app is denied
# (currently this must be done manually in the user's slides account)


def create_tracker():
    """initializes tracker spreadsheet

    Return:
        str: id of new spreadsheet
    """
# TODO ensure create_tracker is also called when trackerId is set, but invalid
# (aka user manually deleted tracker file in their drive account
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

    return tracker['spreadsheetId']


def update_tracker():
    """Adds user inputs to the tracker
    """
    service = build('sheets', 'v4', credentials=credentials)
    tracker_id = get_config_value('Tracker', 'trackerId')
    if tracker_id == '':  # ...there is no trackerId in ini file...
        tracker_id = create_tracker()

    # TODO insert data from command line into second row of tracker
    insert_range = "A2:H2"
    result = service.spreadsheets().values().append(
        spreadsheetId=tracker_id, range=insert_range)


def get_email_info():
    """returns the email, company name, job position from any
    non-followed up outstanding applications
    """
    tracker_id = get_config_value('Tracker', 'trackerId')
    if tracker_id == '':
        return []

    # up here we will configure 'range' vars to include columns for company,
    # position, and emails

    # check if an app is in progress ('Yes') ->
    # check if an app has been followed up ('No') ->
    # check if an app is ready to be followed up (app date >= today's date) ->
    # output job title, company name, email address

    service = build('sheets', 'v4', credentials=credentials)
    email_info = []

    valid_cells = 'A2:H'

    outstanding_apps = service.spreadsheets().values().get(
        spreadsheetId=tracker_id, range=valid_cells).execute()

    values = outstanding_apps.get('values', [])

    if values:
        one_week_ago = datetime.today() - timedelta(days=7)
        for row in values:
            app_date = datetime.strptime(row[2], '%m/%d')
            if (row and row[3] == 'No' and row[4] == 'Yes'
               and row[6] != ''  # there is an email listed
               and app_date <= one_week_ago):  # bout a week ago
                email_info.append(row)
    # TODO figure out how to keep track of which rows to update column D
    # (row should be an object that contains row num as parameter)
    return email_info


def email_scheduler(email_info):
    """this fn will be responsible for calling send_mail on each necessary row
    for each spreadsheet row in email_info list...
    Params:
        email_info ([str]): rows (individual applcs) needed to pass into
                            mailer.py's send_mail()
    """
    for row in email_info:
        send_mail(row[0], row[1], row[2], row[6])
        # TODO set column D (Followed up) to Yes
