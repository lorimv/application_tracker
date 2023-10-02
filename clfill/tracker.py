from googleapiclient.discovery import build
from . import credentials
from .mailer import send_mail
from .config_handler import get_config_value, set_config_value
# TODO maybe add refresh() allowing users to inform tracker when app is denied
# (currently this must be done manually in the user's slides account)


def create_tracker():
    """initializes tracker spreadsheet
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


def update_tracker():
    """Adds user inputs to the tracker
    """
    service = build('sheets', 'v4', credentials=credentials)
    if get_config_value('Tracker', 'trackerId') == '':  # ...there is no trackerId in ini file...
        create_tracker()

    # TODO insert data from command line into second row of tracker


def get_email_info():
    """returns the email, company name, job position from any
    non-followed up outstanding applications
    """
    tracker_id = get_config_value('Tracker', 'trackerId')
    if tracker_id == '':
        return []

    # up here we will configure 'range' vars to include columns for company, position, and emails
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
        email_info = [value for value in values if value and value[3] == 'No'
                      and value[4] == 'Yes' and value[2] >= 'TODAY\'S DATE + 1 WEEK']
    # TODO finish third check where C (App Date) was bout a week ago

    return email_info


def email_scheduler(email_info):
    """this fn will be responsible for calling send_mail on each necessary row
    for each spreadsheet row in email_info list...
    Params:
        email_info ([str]): rows (individual applcs) needed to pass into mailer.send_mail()
    """
    # TODO ensure email_scheduler properly sets column D ('Followed up?')
    for row in email_info:
        send_mail(row[0], row[1], row[2], row[3])  # TODO actually get params
