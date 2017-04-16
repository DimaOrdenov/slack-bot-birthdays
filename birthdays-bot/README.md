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
`mainMonth()` - method is called to check birthdays at last day of month.

`mainDaily()` - method is called to check birthdays every day.

There is `try except` method in both class methods not to break code execution if some exceptions will appear.

Both class methods have a little api part to get data from Sheet. After getting data, its processing to Slack API call *chat.postMessage*. Method `mainDaily` has additional work with data as it needs to be sent to different users.

`MonthWord(month)` - method is called to get name of **month** (1-12).

Working part starting at `if (sc.rtm_connect()):` and continues till `else` statement with it body. In this part bot connecting to team, working with current date and time. Also, there is a little registration part in `if re.search(u'Name=[A-Z][a-zA-Z]+ Surname=[A-Z][a-zA-Z]+', readList[0]['text']):` "if-statement"'s body. User can send *add me* message to bot and it will ask him to send his name and surname that must be valid to this regural expression in statement. (Of course *add me* isn't required as bot checks text of message and doesnt wait for some answer)

A little registration is necessary to put all chiefs in one file. On next check bot will compare Sheet with file and send messages only to chiefs.

:heavy_exclamation_mark: I've tried to use OOP to make some class with methods and work with it. I think that better realisation could be writing class and executable part separately.

Also there are too many if-else statements and some "code-copies". Better get less of this.
