# slack-bot-birthdays
This bot was written for organization and have restricted usage. Using Google Sheets API and prebuild sheet bot informs managers about birthdays everyday and every last day of month.

## Google Sheets API
Full documentation could be found [here](https://developers.google.com/sheets/api/)

> Some info about credentials file, username, password and used sheet

* Name of credentials file:

`CLIENT_SECRET_FILE = 'client_secret.json'`

His path:
```
home_dir = os.path.expanduser('~')
credential_dir = os.path.join(home_dir, '.credentials')
```

This options goes with Google API "Try out", so you don't need to change them if you setting up API using Google's Instructions.

* Google username and password:
```
username = ''
password = ''
```

* Sheet ID and cell range:
```
spreadsheetId = ''
rangeName = ''
```

How to find Sheet ID and correct format for range of cells you can find in Google's Instructions.

In this task Sheet has columns **Name**, **Surname**, **Nickname**, **Position**, **Chief**, **Date**.

## Slack API and SlackClient Python libs
Full documentation about API could be found [here](https://api.slack.com/). Here you can find how to get token, read info about scopes and get all possible commands.

Full documentation about SlackClient library for Python could be found [here](http://slackapi.github.io/python-slackclient/).

## Some handsome comments about the code
*Comming soon*
