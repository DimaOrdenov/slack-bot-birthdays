# -*- coding: utf-8 -*-
from __future__ import print_function
from slackclient import SlackClient
from apiclient import discovery
from oauth2client import client
from oauth2client import tools

import datetime
import json
import httplib2
import os
import oauth2client
import time

import urllib, urllib2, cookielib

print('processing...')

#################################################################################################
######----------------------------------Google Sheets API----------------------------------######
#################################################################################################


class GoogleSheetApi:
    @staticmethod
    def get_credentials():
        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None

        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
        SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
        CLIENT_SECRET_FILE = 'client_secret.json'
        APPLICATION_NAME = 'Google Sheets API Python Quickstart'


        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
        Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    @staticmethod
    def main(CH):
        """Shows basic usage of the Sheets API.

        Creates a Sheets API service object and prints the names and majors of
        students in a sample spreadsheet:
        https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
        """
        #print('Reading sheets...')
        credentials = GoogleSheetApi.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

        spreadsheetId = ''
        rangeName = ''
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range=rangeName).execute()
        json.dump(result,f_log,indent=4,sort_keys=True)
        values = result.get('values', [])
        text_slack = ''
        currentTime = datetime.datetime.now()
        countRow=2
        if not values:
            print('No data found.')
        else:
            for row in values:
                if row[4] != "":
                    text=u'\nTournament '+row[2]+'\n'+row[3]+u' vs. '+row[4]+u'\nBroadcast '+row[5]
                    attach=[{
                    "fallback": u'Match in '+row[1],
                    "title": u'Match in '+row[1],
                    "text": text,
                    "color": "#000000",
                    "thumb_url": "http://s41.radikal.ru/i093/1607/95/1c6cb0f080c6.png"
                    }]
                else:
                    text=u'\nTournament '+row[2]+'\n'+row[3]+u'\nBroadcast '+row[5]
                    attach=[{
                    "fallback": u'Match in '+row[1],
                    "title": u'Match in '+row[1],
                    "text": text,
                    "color": "#000000",
                    "thumb_url": "http://s41.radikal.ru/i093/1607/95/1c6cb0f080c6.png"
                    }]
                if len(row)==8:
                    sheetTime = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                    delta = sheetTime - currentTime
                    delta = delta.total_seconds()-10800
                    if delta < -480:
                        rangeName = 'G'+str(countRow)
                        request = {'values': [['done']]}
                        service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName,body=request,valueInputOption='RAW').execute()
                        rangeName = 'H'+str(countRow)
                        request = {'values': [['checked']]}
                        service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName,body=request,valueInputOption='RAW').execute()
                    if row[7] == 'yes' and delta < -180:
                        if (delta >= -480 and row[6] != 'done'):
                            sc.api_call("chat.postMessage",channel=CH,attachments=attach,as_user="true")
                            rangeName = 'G'+str(countRow)
                            request = {'values': [['done']]}
                            service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName,body=request,valueInputOption='RAW').execute()
                            rangeName = 'H'+str(countRow)
                            request = {'values': [['checked']]}
                            service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=rangeName,body=request,valueInputOption='RAW').execute()
                countRow+=1

#################################################################################################
######----------------------------------Google Sheets API----------------------------------######
#################################################################################################


#Sign In
username = ''
password = ''

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'username' : username, 'j_password' : password})
opener.open('https://accounts.google.com/ServiceLogin?hl=ru&passive=true&continue=https://www.google.ru/%3Fgfe_rd%3Dcr%26ei%3DauqDV9jgCKq8zAX0nLf4Cw%26gws_rd%3Dssl#identifier', login_data)

#Files
#f_channellist = open('channel.list','w')
#f_channelinfo = open('channel.info','w')
#f_log = open('log','w')

#Slack token
token = ''
sc = SlackClient(token)

#JSON to file
#json.dump(sc.api_call("channels.info",channel="C0XS865GU"),f_channelinfo,indent=4,sort_keys=True)
#json.dump(sc.api_call("channels.list"),f_channellist,indent=4,sort_keys=True)

#Starting RTM
timeMessage = None
CH_hello='#testik'
if (sc.rtm_connect()):
    while True:
        #print('Reading...')
        readList = sc.rtm_read()
        print(readList)
        if len(readList)!=0:
            if 'type' in readList[0]:
                #event type
                if readList[0]['type'] == 'user_typing':
                    CH = readList[0]['channel']
                if readList[0]['type'] == 'hello':
                    sc.api_call("chat.postMessage",channel=CH_hello,text="Hi! I am connected!",as_user="true")
                    GoogleSheetApi.main(CH_hello)
                    #sc.api_call("chat.postMessage",channel=CH_hello,text="I will check from "+str(curRow)+" row!",as_user="true")
                if readList[0]['type'] == 'message':
                    if 'text' in readList[0]:
                        #event text
                        if readList[0]['text'] == 'Hi! I am connected!':
                            timeMessage = datetime.datetime.fromtimestamp(float(readList[0]['ts']))
                        if readList[0]['text'] == 'hi':
                            sc.api_call("chat.postMessage",channel=CH,text="Hi <@"+readList[0]['user']+">! What do you want?",as_user="true")
                        if readList[0]['text'] == 'check event':
                            sc.api_call("chat.postMessage",channel=CH,text="Working on it...",as_user="true")
                            #GoogleSheetApi.main()
                            sc.api_call("chat.postMessage",channel=CH,text="Finished!",as_user="true")
                        if readList[0]['text'] == 'server for you':
                            sc.api_call("chat.postMessage",channel=CH,text="Yeah, but I have one now, running on Amazon!",as_user="true")
                        if readList[0]['text'] == 'bye':
                            sc.api_call("chat.postMessage",channel=CH,text="Good bye, thanks for using me! If I need again, I must be restarted using server!",as_user="true")
                            exit(1)
        timeCurrent = datetime.datetime.now()
        if timeMessage != None:
            timeCheck = timeCurrent - timeMessage
            if timeCheck.total_seconds() >= 180:
                GoogleSheetApi.main(CH_hello)
                timeMessage = timeCurrent
        time.sleep(1)
else:
    print ("Connection Failed")
    sc.api_call("chat.postMessage",channel="#general",text="Connection failed!",as_user="true")

#f_channellist.close()
#f_channelinfo.close()
#f_log.close()



print('done')