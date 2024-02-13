"""module housing all spreadsheet-related functions
"""
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from . import credentials
from .mailer import send_mail
from .config_handler import get_config_value, set_config_value

# TODO maybe add refresh() allowing users to inform tracker when app is denied
# (currently this must be done manually in the user's slides account)
# TODO open tracker for user in browser?


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
    try:
        result = service.spreadsheets().values().get(
                spreadsheetId=tracker_id, range='A2:H').execute()
    except HttpError as e:
        print('Invalid trackerId in .ini file,')
        print('ensure tracker is still in drive')
        print(e)
        return
    tracker_vals = result.get('values', [])
    if tracker_vals:
        tracker_vals.insert(0, [""] * 8)
    paste = {'values': tracker_vals}  # mypy doesnt like this?

    # clears all values, pastes them one below top row
    service.spreadsheets().values().clear(
            spreadsheetId=tracker_id, range='A2:H').execute()
    result = service.spreadsheets().values().append(
            spreadsheetId=tracker_id, range='A2:H',
            valueInputOption='USER_ENTERED', body=paste).execute()
    # mypy knows body is type ValueRange, but doesn't know what ValueRange is

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
                }  # type: ignore
    service.spreadsheets().values().update(
            spreadsheetId=tracker_id, range='A2:H2',
            valueInputOption='USER_ENTERED', body=new_application).execute()


def email_scheduler():
    """calls send_mail using the email, company name, job position from any
    outstanding applications ready for followup
    """
    tracker_id = get_config_value('Tracker', 'trackerId')
    if tracker_id == '':
        return

    # up here we will configure 'range' vars to include columns for company,
    # position, and emails

    # check if an app is in progress ('Yes') ->
    # check if an app has been followed up ('No') ->
    # check if an app is ready to be followed up (app date >= today's date) ->
    # output job title, company name, email address

    service = build('sheets', 'v4', credentials=credentials)

    valid_cells = 'A2:H'

    all_applications = service.spreadsheets().values().get(
        spreadsheetId=tracker_id, range=valid_cells,
        valueRenderOption="FORMULA", dateTimeRenderOption="FORMATTED_STRING"
        ).execute()

    values = all_applications.get('values', [])
    if values:
        for index, row in enumerate(values):  # loop thru all applications
            if ready_for_followup(row):  # if row is ready...
                send_mail(row[0], row[1], row[2], row[6])
                set_followed_up(index, service)


def ready_for_followup(row):
    """tells us whether the application in the given row is ready to be
    followed-up with an email

    Params:
        row ([str]): data contained within a single row of tracker
            (company, job title, app date, followed up,
            in progress, location, email)
    Return:
        bool: T/F should application be followed up
    """
    try:
        temp = datetime.strptime(row[2], '%m/%d')
        one_week_ago = datetime.now() - timedelta(days=7)
        app_date = datetime(datetime.now().year, temp.month, temp.day)
        if (row and row[3] == 'No' and row[4] == 'Yes'
           and row[6] != ''  # there is an email listed
           and app_date <= one_week_ago):  # bout a week ago
            print("app_date: " + app_date.strftime("%m/%d/%Y"))  # verbose?
            print("one_week_ago: " + one_week_ago.strftime("%m/%d/%Y"))
            print()
            return True
        elif row[3] == 'No' and row[4] == 'Yes':
            print('Not ready for follow up')
            print(f'Job: {row[0]}')
            print()
        return False
    except ValueError as e:
        print('Invalid application date found: ')
        print(f'Job: {row[0]}')
        print(f'Date: {row[2]}')
        print(e)
        return False
    except IndexError as e:
        if len(row) == 6 and row[3] == 'No' and row[4] == 'Yes':
            print('Email Missing!')
            print('Manual follow-up required:')
            print(f'Company: {row[0]}')
            print(f'Job Title: {row[1]}')
            print()
        elif len(row) != 6:
            print('A required value does not exist')
            print(e)
            print()
        return False


def set_followed_up(index, service):  # ugly helper, may not be necessary
    """sets the chosen row of tracker as followed up

    Args:
        index (int): index of row to be changed (minus 2)
        service: Sheets API service
    """
    # TODO double check to ensure index isn't stored
    # in scheduler's all_applications obj
    tracker_id = get_config_value('Tracker', 'trackerId')
    if tracker_id == '':
        return

    index += 2

    body = {
        'values': [
          [
            'Yes',
            ]
          ]
        }
    service.spreadsheets().values().update(
         spreadsheetId=tracker_id, range=f'D{index}',
         valueInputOption="RAW",
         body=body
         ).execute()


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
