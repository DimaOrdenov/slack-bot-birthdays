# slack-bot-games-schedule
This bot was written for organization and have restricted usage. Using Google Sheets API and prebuild sheet bot informs channel about games. Bot checks schedule every 3 minutes and send messages on delay of 3-5 minutes after game starts.

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

In this task Sheet has columns **Date/Time**, **Game**, **Tournament**, **Team1**, **Team2**, **Watch link**, **Notified**, **Updated**.

Column *Notified* made to check if game was already notified by bot. This game gets status *Updated* also.

Column *Updated* made to check if some changes was made by users. User must set empty value by himself if he made some changes to game. This will make bot check this row again and inform about game if its possible.

## Slack API and SlackClient Python libs
Full documentation about API could be found [here](https://api.slack.com/). Here you can find how to get token, read info about scopes and get all possible commands.

Full documentation about SlackClient library for Python could be found [here](http://slackapi.github.io/python-slackclient/).

## Some handsome comments about the code
`main(CH)` - method is called to check table for required conditions (3-5 minutes after game start time) and to send message about game. *CH* is parameter for channel where bot should send message.

There is `try except` method in both class methods not to break code execution if some exceptions will appear.

Both class methods have a little api part to get data from Sheet. After getting data, its processing to Slack API call *chat.postMessage*.

Working part starting at `if (sc.rtm_connect()):` and continues till `else` statement with it body. In this part bot connecting to team, working with current date and time to check possible games. There is only one method, so when bot isn't busy checking Sheet user can send some messages to him and get answers. This was made only for educational reasons.

:heavy_exclamation_mark: I've tried to use OOP to make some class with methods and work with it. I think that better realisation could be writing class and executable part separately.

Also there are too many if-else statements and some "code-copies". Better get less of this.

The right way of making multitask bot (get messages and send answers, working on some functions with Google Sheet and more) is using something like multithreading or multiprocessing app. In this way users can use all bot's functions and advantages.
