"""__init__ module, ensures proper setup of config.ini / credentials"""
import configparser
import sys
from .config_handler import config_exists, create_config
from .auth import authenticate, get_path

# Begin by ensuring config file exists...
if not config_exists():
    create_config()  # ...& creating one with default values if it dne

try:
    # calls auth's get_path() function on startup...
    get_path()
except ValueError as e:
    # ...will exit if user has not configured specified environment var
    print(e)
    print('Please set CLFILL_KEY_PATH to the path to .json key file')
    print('(Windows cmd: \'set CLFILL_KEY_PATH=<path>\')')
    sys.exit()

# once we know environment var exists...
try:
    # ...we call auth's authenticate() and set 'credentials' to the output...
    credentials = authenticate()
except Exception as e:  # TODO specify exception
    # ...which will exit if we cannot authenticate
    print(e)
    print('authentication failed!!!')
    sys.exit()

# if we get here, then 'credentials' now contains the info needed to use the
# api in filler


# TODO maybe place get_path INSIDE authenticate, get_path can then return path,
# aka:
#   try:
#       credentials = authenticate(get_path())
#   except ValueError:
#       "ENV NOT SET!"
#       ...
#   except Exception:
#       "AUTHENTICATE FAILED!"
#       ...
