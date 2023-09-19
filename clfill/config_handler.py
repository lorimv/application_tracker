"""Module responsible for all interactions with config.ini file
"""

import configparser
from os.path import exists
from os import mkdir


def config_exists():
    """Checks if the config file has been created

    Returns:
        bool: T/F, does config.ini exist in the proper path?

    """
    return exists('config/config.ini')


def create_config():
    """Creates config.ini, initializes all values to None

    """
    if not exists('config/'):
        mkdir('config/')

    config = configparser.ConfigParser()

    config.add_section('Tracker')
    config.set('Tracker', 'trackerId', None)

    config.add_section('Mailer')
    config.set('Mailer', 'myEmail', None)  # Should we ask here? Additionally,
    config.set('Mailer', 'myName', None)   # should setup be done with cli?

    with open('config/config.ini', 'w', encoding='utf8') as configfile:
        config.write(configfile)


def get_config_value(section, key):
    """Gets value associated with given section/key of config.ini file

    Args:
        section (str): section of .ini file we're looking in
        key (str): key associated with the value we want

    Returns:
        str: corresponding value obtained from .ini file

    """
    if not config_exists():
        create_config()

    config = configparser.ConfigParser()
    config.read('config/config.ini')  # TODO error check here could maybe
                                      #      replace previous if block
    value = config[section][key]

    if not value:  # if value is not assigned yet, set it now
        config.set(section, key, 'TODO')  # TODO write real setter code
        with open('config/config.ini', 'w', encoding='utf8') as configfile:
            config.write(configfile)
        value = config[section][key]

    return value