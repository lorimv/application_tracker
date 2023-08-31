from .auth import authenticate, get_path

try: 
    get_path()
except ValueError as e:
    print(e)
    print('Please set CLFILL_KEY_PATH to the path to .json key file')
    print('(Windows cmd: \'set CLFILL_KEY_PATH=<path>\')')
    exit()

try:
    credentials = authenticate()
except Exception as e:
    print(e)
    print('authentication failed!!!')
    exit()