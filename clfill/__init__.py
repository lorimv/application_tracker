"""__init__ module, ensures proper setup of config.ini / credentials
"""
import sys
import os
from oauthlib.oauth2 import AccessDeniedError
from .config_handler import config_exists, create_config
from .auth import get_credentials


if os.getcwd() != "/home/lorimv/Code/application_tracker/clfill":
    print("cwd:")
    print(os.getcwd())
    os.chdir("./clfill")  # TODO LAZY SOLUTION< ONLY FOR TESTING!! FIGURE OUT PACKAGING LATER
    print("changed dir")
# Begin by ensuring config file exists...
if not config_exists():
    create_config()  # ...& creating one with default values if it dne

# FIXME creds is called before --help. This should be moved to main?
try:
    # calls auth's get_path() function on startup...
    credentials = get_credentials()  # I think this is a bad idea, but idk where else to store credentials. (Pickle?)
except ValueError as e:
    # error thrown if get_path() is not configured
    print(e)
    print('Please set CLFILL_KEY_PATH to the path to .json key file')
    print('(Windows cmd: \'set CLFILL_KEY_PATH=<path>\')')
    print('(Linux cmd: \'export CLFILL_KEY_PATH=<path>\')')
    sys.exit()
# TODO add specific exceptions here (read authenticate() documentation!)
except AccessDeniedError as e:
    print(e)
    print("Allow access next time!!!")
    sys.exit()
except Exception as e:
    # any other error
    print(e)
    print('authentication failed!!! (unspecified error)')
    sys.exit()
