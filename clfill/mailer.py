"""responsible for sending emails
"""
import base64
from email.message import EmailMessage

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from . import credentials
from .config_handler import get_config_value

# this is the module that will auto-send follow up emails when -m is called
# im thinking it will take arguments from tracker module that returns company name & email & job title


def send_mail(company_name, position_name, app_date, company_email):
    """Sends follow-up email, according to function parameters

    Args:
        company_name (str): name of company
        position_name (str): name of position
        app_date (str): date application was originally sent
        company_email (str): company's email address

    Returns:
        ???: draft of email ig? need to read documentation again

    """
    MY_NAME = get_config_value('Mailer', 'myName')  # TODO get name (query() in config_handler?)
    # MY_EMAIL = get_config_value('Mailer', 'myEmail')

    # TODO maybe ask for confirmation before sending an email jic

    try:
        # The following code block is the writer/sender for follow-up emails
        service = build('gmail', 'v1', credentials=credentials)

        body_text = read_body() # FIXME grab from body.txt

        message = EmailMessage()
        message.set_content(body_text.format(company=company_name,
                            position=position_name, date=app_date, name=MY_NAME))

        message['To'] = company_email
        # message['From'] = MY_EMAIL
        message['Subject'] = 'Application for ' + position_name + ' at ' + company_name

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }

        # send_message = service.users().messages().send(  # TODO uncomment these!
        #                userId='me', body=create_message).execute()
        print("email sent!!!")
        print("just kidding. debug !")
        print(company_name)
        print(company_email)
        print(app_date)
    except HttpError as e:
        print(e)
        print("Invalid email!")
        print('Manual follow up required')
        print('Company: ' + company_name)
        print('Position: ' + position_name)
        send_message = None
    return None  # FIXME dummy return (sick of sending emails while testing)
    return send_message


def read_body():
    """Reads body text from body.txt file

    Return:
        str: text to be sent in email

    """
    with open('config/body.txt', 'r', encoding='utf8') as file:
        body_text = file.read()
        print(body_text)
        return body_text.strip('\n')
