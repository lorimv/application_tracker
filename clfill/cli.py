import argparse
from .tracker import add_application, email_scheduler
from .filler import method

# TODO TODO TODO TODO COMMMANDS!!!!! :)
#   command to edit ini file
#       creates ini if necessary
#       asks user for unfilled user info (name, etc.)
#       pages through (maybe: "Edit 'Tracker' values? (Y/N)"
#           ("Mailer contains empty parameters! Edit? (Y/N)")
#   command to track new application
#       query user for needed info
#       add to tracker
#       additional arg to dump to cover letter
#   command to send emails to ready applications
#       uses tracker fns to read tracker
#       uses mailer to send emails from data gathered by tracker


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='cover letter filler')
    parser.add_argument('-n', '--new-application', help='Add a new application',
                        action="store_true")
    parser.add_argument('-m', '--send-mail', help='Follow up on applications',
                        action="store_true")
    parser.add_argument('-v', '--verbose', help='Verbose output.')
    return parser.parse_args()

def app_query():
    # Demo function, asks user info needed to fill doc
    print("Hola hola")

    print("Let's start by getting the name of the company: ")
    company = input()

    print("Position name (full)?")
    position = input()

    print('location: ')
    location = input()

    print('email: ')
    email = input()

    add_application(company, position, location, email)


def main():
    options = parse_args()

    if options.new_application:
        app_query()
    # good enough for now
    elif options.send_mail:
        email_scheduler()
    # method()  # maybe arguments into filler (docs)  & tracker (sheets), mailer will use info from spreadsheet when -m


if __name__ == '__main__':
    main()
