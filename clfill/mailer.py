"""responsible for sending emails
"""
import base64
from email.message import EmailMessage
from os.path import exists

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

        body_text = read_body()

        message = EmailMessage()
        # for some reason that eludes me sent emails have no wrapping
        # but recieved ones do

        # anyway, body.txt is written with fstring formatting
        message.set_content(body_text.format(company=company_name,
                            position=position_name, date=app_date,
                            name=MY_NAME, skills=get_skills(position_name)))

        message['To'] = company_email
        # message['From'] = MY_EMAIL
        message['Subject'] = f'Application for {position_name} at {company_name}'

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }

        send_message = service.users().messages().send(
                       userId='me', body=create_message).execute()
        print('email sent!!!')
        # print("just kidding. debug !")
        # print(company_name)
        # print(company_email)
        # print(app_date)
    except HttpError as e:
        print(e)
        print('Invalid email!')
        print('Manual follow up required')
        print(f'Company: {company_name}')
        print(f'Position: {position_name}')
        send_message = None

    return send_message


def read_body():
    """Reads body text from body.txt file

    Return:
        str: text to be sent in email

    """
    if not exists('config/body.txt'):
        create_body()

    with open('config/body.txt', 'r', encoding='utf8') as file:
        body_text = file.read()

    return body_text


def create_body():
    """creates a default body.txt

    """
    with open('config/body.txt', 'w', encoding='utf8') as file:
        file.write("THIS IS THE DEFAULT EMAIL BODY\n"
                   "\n"
                   "My name:             {name}\n"
                   "Company:             {company}\n"
                   "Position:            {position}\n"
                   "Application date:    {date}\n"
                   "Skills:              {skills}\n")


def get_skills(applied_position):
    """a function to read a position, fill email with appropriate skills

    """
    skill_dict = {  # perhaps this should also be in a json but I think it's fine rn
            'embedded': 'experience with low-level memory management and understanding of C makes',
            'test': 'experiences with unit testing frameworks and agile development make',
            'system': 'experience with a diverse range of operating systems and scripting languages makes',
            'systems': 'experience with a diverse range of operating systems and scripting languages makes',
            'sysadmin': 'experience with a diverse range of operating systems and scripting languages makes',
            'C++': 'history with Agile C++ development makes',
            'engineer': 'experience working with a diverse team in an Agile environment',
            'developer': 'experience working with a diverse team in an Agile environment'
    }
    skills = ''
    for position, relevant_skill in skill_dict.items():
        if position in applied_position:
            skills += relevant_skill
            break
    if skills == '':
        print('Fill out skills section:')
        print(f'I believe my .... [write MAKE/S] ...me a good candidate for the {applied_position} position')
        skills = input()

    return skills
