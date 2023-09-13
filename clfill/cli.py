import argparse
from filler import method

##TODO TODO TODO TODO this function is default (do cli last)
def parse_args() -> argparse.Namespace: 
    parser = argparse.ArgumentParser(description='cover letter filler')
    parser.add_argument('bait', help='Stand-in arg.')
    parser.add_argument('switch', help='Stand-in arg.')
    parser.add_argument('output', help='Stand-in arg.')
    parser.add_argument('-v', '--verbose', help='Verbose output.', action='store_true')
    parser.add_argument('-i', '--ignore-path-check', help="Stand-in arg.\n" + 
                        "Stand-in arg -- line 2", action="store_true")
    parser.add_argument('-dt', '--dont-use-tempdir', help="Prevent the tool from creating a temporary directory when creating the exploit.\n" + 
                        "Instead, create the intermediate folders in current working directory.", action="store_true")
    parser.add_argument("-pt", "--preserve-temp", help="Preserve the temporary directory after creating the exploit. Has no effect if -dt or --dont-use-tempdir is not specified.")
    return  parser.parse_args()

def query():
    # Demo function, asks user info needed to fill doc
    print("Hola hola")

    print("Let's start by getting the name of the company: ")
    company_long = input()

    print("yeah aight now the shortened company name: ")
    company_short = input()

    print("Position name (full)?")
    position_long = input()

    print("Now tha shortened position name")
    position_short = input()
    

def main():
    # good enough for now
    query()
    method() # maybe arguments into filler (docs)  & tracker (sheets), mailer will use info from spreadsheet when -m

if __name__ == '__main__':
    main()
