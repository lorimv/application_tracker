"""module housing all spreadsheet-related functions
"""
from datetime import datetime, timedelta, date
from googleapiclient.discovery import build
from . import credentials
from .mailer import send_mail
from .config_handler import get_config_value, set_config_value

# TODO maybe add refresh() allowing users to inform tracker when app is denied
# (currently this must be done manually in the user's slides account)


def add_application(company, job_title, location, employer_email):
    """Adds user inputs to the tracker

    Params:
        company (str): company name
        job_title (str): name of the position applied to
        location (str): location of position
        employer_email (str): address to send follow-up email to
    """
    service = build('sheets', 'v4', credentials=credentials)
    tracker_id = get_config_value('Tracker', 'trackerId')
    if tracker_id == '':  # ...there is no trackerId in ini file...
        tracker_id = create_tracker()

    # adds a blank row above all values
    result = service.spreadsheets().values().get(  # TODO check for HttpError
            spreadsheetId=tracker_id, range='A2:H').execute()
    tracker_vals = result.get('values', [])
    if tracker_vals:
        tracker_vals.insert(0, [""] * 8)
    paste = {'values': tracker_vals}

    # clears all values, pastes them one below top row
    service.spreadsheets().values().clear(
            spreadsheetId=tracker_id, range='A2:H').execute()
    result = service.spreadsheets().values().append(
            spreadsheetId=tracker_id, range='A2:H',
            valueInputOption='USER_ENTERED', body=paste).execute()

    # inserts the new application in the top row
    new_application = {
                'values': [
                  [
                    company,
                    job_title,
                    datetime.today().strftime('%m/%d'),
                    "No",
                    "Yes",
                    location,
                    employer_email,
                    ""
                  ]
                ]
              }
    service.spreadsheets().values().update(
            spreadsheetId=tracker_id, range='A2:H2',
            valueInputOption='USER_ENTERED', body=new_application).execute()


def get_email_info():
    """returns the email, company name, job position from any
    non-followed up outstanding applications

    Return:
        [str]: info needed to send email
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
    # TODO bout a week ago check is ALWAYS passing test dates 9/1/23 & 12/30/23
    if values:
        one_week_ago = datetime.today() - timedelta(days=7)
        for row in values:
            try:
                app_date = datetime.strptime(row[2], '%m/%d')
                if (row and row[3] == 'No' and row[4] == 'Yes'
                   and row[6] != ''  # there is an email listed
                   and app_date <= one_week_ago):  # bout a week ago
                    email_info.append(row)
            except ValueError as e:
                print('invalid application date found: ')
                print(e)
            except IndexError as e:
                print('no email found: ')
                print(e)
    # TODO figure out how to keep track of which rows to update() column D
    # (row should be an object that contains row num as parameter)
    return email_info


def email_scheduler(email_info):
    """this fn will be responsible for calling send_mail on each necessary row
    for each spreadsheet row in email_info list...
    Params:
        email_info ([str]): rows (individual applcs) needed to pass into
                            mailer.py's send_mail()
    """
    if email_info == []:  # more efficient than building when not necessary
        return

    service = build('sheets', 'v4', credentials=credentials)
    tracker_id = get_config_value('Tracker', 'trackerId')

    for row in email_info:
        send_mail(row[0], row[1], row[2], row[6])
        # TODO set column D (Followed up) to Yes
        service.spreadsheets().values()


def create_tracker():
    """helper; initializes tracker spreadsheet

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
                                {"userEnteredValue": {"stringValue": 'Company'}},
                                {"userEnteredValue": {"stringValue": 'Job Title'}},
                                {"userEnteredValue": {"stringValue": 'App Date'}},
                                {"userEnteredValue": {"stringValue": 'Followed Up?'}},
                                {"userEnteredValue": {"stringValue": 'In Progress'}},
                                {"userEnteredValue": {"stringValue": 'Location'}},
                                {"userEnteredValue": {"stringValue": 'Company Email'}},
                                {"userEnteredValue": {"stringValue": 'Other'}}]
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
