# clfill v 0.9.1

Python command line application that uses the google docs API to fill in a tracker spreadsheet, then send emails to companies following up on apps

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

I may implement a separate cover letter template flag that generates a starter cl when called with -n

Will finish readme when program is 1.0.

## TODO list:
Add parent company variable?

Text color is applied to the box, not the row. So when rows are shifted down in add\_application(), edge rows become the wrong color

Clean set\_follow\_up(), find out if creating services or passing services as args is best practice

Properly implement global credential object to build service instead of \_\_init\_\_.py

Getting dates from spreadsheets doesn't get the year. The spreadsheet displays month/date, but stores month/date/year when accessed in browser. However api seems to only have access to month/date
**UPDATE**: the spreadsheet in browser does not store year, it just autofills current year (%Y) after month/day

Multithread (maybe) to autoscan -m while adding a new application? Then alter cli flags (no flag acts like -n & -m at the same time, a flag to skip scan for follow ups, another to skip adding app)

Sanitize inputs? will a ' or " break the program?

Use the actual keyring libraries to save user_credentials
