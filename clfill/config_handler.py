import configparser
from os.path import exists
from os import mkdir

def config_exists():
    return exists('config/config.ini')

def create_config():
    if not exists('config'):
        mkdir('config')

    config = configparser.ConfigParser()

    config.add_section('Tracker')
    config.set('Tracker', 'trackerId', None)

    config.add_section('Mailer')
    config.set('Mailer', 'myEmail', None)
    config.set('Mailer', 'myName', None)

    with open('config/config.ini', 'w', encoding='utf8') as configfile:
        config.write(configfile)

# TODO add getter with str args, returning requested values &
#      gathering user input if values are empty. THIS MODULE ACTS AS
#      INTERFACE WITH CONFIGFILE
def get_value(section, key):
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    # TODO add logic to ask user for values if empty

    return config[section][key]
