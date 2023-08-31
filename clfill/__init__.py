import os
from auth import authenticate, set_credentials
    
try: 
    credentials = set_credentials()
except ValueError as e:
    print(e)
    print('Please set CLFILL_KEY_PATH to the path to .json key file')
    print('(Windows cmd: \'set CLFILL_KEY_PATH=<path>\')')

