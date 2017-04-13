# -*- coding: utf-8 -*-
from __future__ import print_function
from slackclient import SlackClient
from apiclient import discovery
from oauth2client import client
from oauth2client import tools

import datetime
import calendar
import json
import httplib2
import os
import oauth2client
import time
import traceback
import re
import ast

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
    def mainMonth():
        """Shows basic usage of the Sheets API.

        Creates a Sheets API service object and prints the names and majors of
        students in a sample spreadsheet:
        https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
        """
        try:
            credentials = GoogleSheetApi.get_credentials()
            http = credentials.authorize(httplib2.Http())
            discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
            service = discovery.build('sheets', 'v4', http=http,
                                discoveryServiceUrl=discoveryUrl)

            spreadsheetId = '' #SHEET ID
            rangeName = '' #CELLS RANGE
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheetId, range=rangeName).execute()
            values = result.get('values', [])
            checkMonth = datetime.date.today().month+1
            countRow=2
            textForAttach=''
            if not values:
                print('No data found.')
            else:
                for row in values:
                    sheetTime = datetime.datetime.strptime(row[4], "%m-%d")
                    sheetTime = sheetTime.date()
                    if sheetTime.month == checkMonth:
                        textForAttach += str(sheetTime.day) + ' ' + GoogleSheetApi.MonthWord(checkMonth) + ' - ' + row[0] + ' - ' + row[2] +'\n'
                        
            attach=[{
                #"fallback": u'\nДни рождения в следующем месяце:\n',
                "text": textForAttach,
                "color": "#7CD197"
            }]
            sc.api_call("chat.postMessage",channel='#testik',text=u"Birthdays of the next month",attachments=attach,as_user="true")
        except Exception as err:
            text = 'Oups, its Google error:\n' + traceback.format_exc()
            sc.api_call("chat.postMessage",channel='#testik',text=text,as_user="true")
            
    @staticmethod
    def mainDaily():
        """Shows basic usage of the Sheets API.

        Creates a Sheets API service object and prints the names and majors of
        students in a sample spreadsheet:
        https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
        """
        try:
            credentials = GoogleSheetApi.get_credentials()
            http = credentials.authorize(httplib2.Http())
            discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
            service = discovery.build('sheets', 'v4', http=http,
                                discoveryServiceUrl=discoveryUrl)

            spreadsheetId = '' #SHEET ID
            rangeName = '' #CELLS RANGE
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheetId, range=rangeName).execute()
            values = result.get('values', [])
            checkDay = datetime.date.today()
            countRow=2
            textForAttach=''
            DictTextForAttach=[]
            if not values:
                print('No data found.')
            else:
                for row in values:
                    sheetTime = datetime.datetime.strptime(row[4], "%m-%d")
                    sheetTime = sheetTime.date()
                    if sheetTime.day == checkDay.day and sheetTime.month == checkDay.month:
                        chiefs = row[3].split('\n')
                        for chief in chiefs:
                            if DictTextForAttach != []:
                                for name in DictTextForAttach:
                                    if name['name'] == chief:
                                        textForAttach = name['text'] + row[0] + ' - ' + row[2] + '\n'
                                        name['text'] = textForAttach
                                        found = 1
                                        break
                                    else:
                                        found = 0
                                if found == 0:
                                    textForAttach = row[0] + ' - ' + row[2] + '\n'
                                    DictTextForAttach.append({'name': chief, 'text': textForAttach})
                            else:
                                textForAttach = row[0] + ' - ' + row[2] + '\n'
                                DictTextForAttach.append({'name': chief, 'text': textForAttach})

            with open('chiefs','r') as f_chiefs:
                chiefs = f_chiefs.read()
                chiefs = chiefs.split('\n')
                del chiefs[-1]
                for row in chiefs:
                    DictFromFile = ast.literal_eval(row)
                    for chief in DictTextForAttach:
                        if DictFromFile['name'].decode('utf-8') == chief['name']:
                            attach=[{
                            "text": chief['text'],
                            "color": "#7CD197"
                            }]
                            sc.api_call("chat.postMessage",channel=DictFromFile['channel'],text=chief['name'] + u', today (' + str(checkDay.day) + ' ' + GoogleSheetApi.MonthWord(checkDay.month) + u') birthdays have:',attachments=attach,as_user="true")
        except Exception as err:
            text = 'Oups, its Google error:\n' + traceback.format_exc()
            sc.api_call("chat.postMessage",channel='#testik',text=text,as_user="true")

    @staticmethod
    def MonthWord(month):
        if month == 1:
            return u'January'
        if month == 2:
            return u'February'
        if month == 3:
            return u'March'
        if month == 4:
            return u'April'
        if month == 5:
            return u'May'
        if month == 6:
            return u'June'
        if month == 7:
            return u'July'
        if month == 8:
            return u'August'
        if month == 9:
            return u'September'
        if month == 10:
            return u'October'
        if month == 11:
            return u'November'
        if month == 12:
            return u'December'


#################################################################################################
######----------------------------------Google Sheets API----------------------------------######
#################################################################################################


#Sign In
username = '' #Here is your 
password = ''

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'username' : username, 'j_password' : password})
opener.open('https://accounts.google.com/ServiceLogin?hl=ru&passive=true&continue=https://www.google.ru/%3Fgfe_rd%3Dcr%26ei%3DauqDV9jgCKq8zAX0nLf4Cw%26gws_rd%3Dssl#identifier', login_data)

#Files
#f_channellist = open('channel.list','w')
#f_channelinfo = open('channel.info','w')

#Slack token
token = ''
sc = SlackClient(token)

#JSON to file
#json.dump(sc.api_call("channels.info",channel="C0XS865GU"),f_channelinfo,indent=4,sort_keys=True)
#json.dump(sc.api_call("channels.list"),f_channellist,indent=4,sort_keys=True)

#Starting RTM
countMonthCheck = 0
countDailyCheck = 0

CH_hello='#testik'

if (sc.rtm_connect()):
    while True:
        try:
            readList = sc.rtm_read()
            if len(readList)!=0:
                if 'type' in readList[0]:
                    #event type
                    if readList[0]['type'] == 'hello':
                        sc.api_call("chat.postMessage",channel=CH_hello,text="Hi! I am connected!",as_user="true")
                        #GoogleSheetApi.main(CH_hello)
                    if readList[0]['type'] == 'message':
                        if 'text' in readList[0]:
                            #event text
                            if readList[0]['text'] == 'hi, bot':
                                sc.api_call("chat.postMessage",channel=readList[0]['channel'],text="Hi <@"+readList[0]['user']+">!",as_user="true")
                            if readList[0]['text'] == 'add me':
                                sc.api_call("chat.postMessage",channel=readList[0]['channel'],text="Hi <@"+readList[0]['user']+">! Enter your Name and Surname:",as_user="true")
                            if re.search(u'Name=[А-Я][а-яА-Я]+ Surname=[А-Я][а-яА-Я]+', readList[0]['text']):
                                name_str = re.search(u'Name=[А-Я][а-яА-Я]+', readList[0]['text'])
                                surname_str = re.search(u'Surname=[А-Я][а-яА-Я]+', readList[0]['text'])
                                #print(name.group(0))
                                #print(surname.group(0))
                                name = name_str.group(0)
                                name = name[5:]
                                surname = surname_str.group(0)
                                surname = surname[8:]
                                sc.api_call("chat.postMessage",channel=readList[0]['channel'],text=u"Name: "+name+u' Surname: '+surname+' Channel: '+readList[0]['channel'],as_user="true")
                                stringToFile = '{\'name\': \'' + name + ' ' + surname + '\', ' + '\'channel\': \'' + readList[0]['channel'] + '\'}\n'
                                with open('chiefs','a+') as f_chiefs:
                                    f_chiefs.write(stringToFile.encode('utf-8'))
                                sc.api_call("chat.postMessage",channel=readList[0]['channel'],text=" added to Notify List!",as_user="true")
                            if readList[0]['text'] == 'shut down, bot':
                                sc.api_call("chat.postMessage",channel=readList[0]['channel'],text="Good bye, thanks for using me! If I need again, I must be restarted using server!",as_user="true")
                                break
            """FINAL VERSION"""
            #Month. channels = general
            today = datetime.datetime.now()
            today += datetime.timedelta(hours = 3)
            lastMonthDay = today.replace(day = calendar.monthrange(today.year, today.month)[1])
            checkMonthTime1 = datetime.datetime(today.year,today.month,lastMonthDay.day,11,50,0,0)
            checkMonthTime2 = datetime.datetime(today.year,today.month,lastMonthDay.day,12,10,0,0)
            if today >= checkMonthTime1 and today <= checkMonthTime2 and countMonthCheck == 0:
                GoogleSheetApi.mainMonth(CH_list)
                countMonthCheck = 1
            if today > checkMonthTime2:
                countMonthCheck = 0
        
            #Daily. channels = chief
            checkDailyTime1 = datetime.datetime(today.year,today.month,today.day,11,50,0,0)
            checkDailyTime2 = datetime.datetime(today.year,today.month,today.day,12,10,0,0)
            if today >= checkDailyTime1 and today <= checkDailyTime2 and countDailyCheck == 0:
                GoogleSheetApi.mainDaily(CH_list)
                countMonthCheck = 1
            if today > checkDailyTime2:
                countMonthCheck = 0
                
            time.sleep(1)
        except Exception as err:
            text = 'Oups, its Slack API error:\n' + traceback.format_exc()
            sc.api_call("chat.postMessage",channel='#testik',text=text,as_user="true")
            sc.api_call("chat.postMessage",channel='#testik',text="Waiting 5 minutes to restart",as_user="true")
            time.sleep(300)
            sc.rtm_connect()
else:
    print ("Connection Failed")
    sc.api_call("chat.postMessage",channel="#general",text="Connection failed!",as_user="true")

#f_channellist.close()
#f_channelinfo.close()

print('done')