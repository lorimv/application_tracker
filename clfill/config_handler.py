import configparser
from os.path import exists

def config_exists():
    return exists('config/config.ini')

def create_config():
    config = configparser.ConfigParser()

    config.add_section('Tracker')
    config.set('Tracker', 'trackerId', None)

    config.add_section('Mailer')
    config.set('Mailer', 'userEmail', None)
    config.set('Mailer', 'myName', None)

    with open('config/config.ini', 'w', encoding='utf8') as configfile:
        config.write(configfile)
