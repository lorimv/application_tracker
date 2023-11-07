# clfill v 0.9

Python command line application that uses the google docs API to fill in cover letter based on template on user's acct.

## When run:
-n flag:
Ensures user has filled in proper credentials ->
Asks user the job title & company name ->
Copies info to sheet in user's acct

-m flag:
Reads tracker based on Id in config.ini ->
Loops to see if any should be followed up ->
Sends email to listed address if needed ->
Sets followed up to Yes after email is sent


(I know this is like driving a nail with a sledgehammer but I wanted to learn api and cli's/python packages)

I also plan to implement a separate cover letter template flag that generates a starter cl when called with -n

Will finish readme when program is 1.0.

## TODO list:
Text color is applied to the box, not the row. So when rows are shifted down in add_application(), edge rows become the wrong color

Logs 'not ready for follow up' even for denied apps (very annoying)

Clean set_follow_up(), find out if creating services or passing services as args is best practice

Properly implement global credential object to build service instead of __init__.py

Getting dates from spreadsheets doesn't get the year. The spreadsheet displays
month/date, but stores month/date/year when accessed in browser. However api
seems to only have access to month/date
