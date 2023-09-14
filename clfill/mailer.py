from googleapiclient.discovery import build
from email.message import EmailMessage

from . import credentials
from .tracker import get_mail_info
import json

# this is the module that will auto-send follow up emails when -m is called
# im thinking it will have access to a tracker (spreadsheet) fn that returns company name & job title

def method():
    # TODO write logic for follow-up email functions

    service = build('gmail', 'v1', credentials=credentials)

    message = EmailMessage()
    message.set_content('Hello ' + COMPANY_NAME + ',\n\n'

                        'My name is ' + MY_NAME + '. I am writing to follow up on my application for the ' +
                        POSITION_NAME + ' role at ' + COMPANY_NAME + ' on [date].\n\n'
                        'I remain excited about the possibility of joining your team and '
                        'contributing to its success. I believe my [specific job-related skills]'
                        ' make me a strong candidate for the position, and I would love to discuss '
                        'the opportunity even further.\n\n'

                        'Please let me know of any questions I can answer or additional information '
                        'I can provide. Thank you for your consideration. I look forward to speaking soon!\n\n'

                        'Warm regards,\n'
                        'Lorenzo Vega')

    message['To'] = COMPANY_EMAIL
    message['From'] = MY_EMAIL
    message['Subject'] = ('Application for ' + POSITION_NAME + ' at ' + COMPANY_NAME)
