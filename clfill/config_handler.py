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
    # TODO figure out packaging cwd (or absolute dir)
    return exists('config/config.ini')


def create_config():
    """Creates config.ini, initializes all values to None

    """
    if not exists('config/'):
        mkdir('config/')

    config = configparser.ConfigParser()

    config.add_section('Tracker')
    config.set('Tracker', 'trackerId', '')

    config.add_section('Mailer')
    config.set('Mailer', 'myEmail', '')  # Should we ask here? Additionally,
    config.set('Mailer', 'myName', '')   # should setup be done with cli?

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
    config.read('config/config.ini')

    value = config[section][key]  #TODO may throw an error instantly, CHECK DOCS

    if not value:  # if value is (somehow) not in file yet, add it now
        config.set(section, key, '')
        with open('config/config.ini', 'w', encoding='utf8') as configfile:
            config.write(configfile)
        value = config[section][key]
    # TODO maybe quit + ask user to do initialize command if no value
    return value


def set_config_value(section, key, value):
    """Sets value for the selected element of config.ini

    Args:
        section (str): section of .ini file we're looking in
        key (str): key associated with the value we want to set
        value (str): the value we would like to set key to
    """
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    config[section][key] = value

    with open('config/config.ini', 'w', encoding='utf8') as configfile:
        config.write(configfile)
