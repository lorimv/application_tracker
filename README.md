# hola hola

Python command line application that uses the google docs API to fill in cover letter based on template on user's acct.

## When run:
Ensures user has filled in proper credentials ->
Asks user the job title & company name ->
Copies template doc in user's acct, then replaces corresponding words

(I know this is like driving a nail with a sledgehammer but I wanted to learn api and cli's/python packages)

I also plan to simultaneously add this information to a spreadsheet, and add a command that will use email API to automatically follow up on applications.

Will finish readme when program is complete.

## TODO list:
Finish the tracker module, properly update sheet when emails are sent

Complete CLI support

Implement global credential object to build service, and allow user to store their login
(Singleton, and then pickle object? is that even possible? figure out)

Getting dates from spreadsheets doesn't get the year. The spreadsheet displays
month/date, but stores month/date/year when accessed in browser. However api
seems to only have access to month/date
