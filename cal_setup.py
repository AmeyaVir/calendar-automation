# from googleapiclient.discovery import build
# import pickle
# from google_auth_oauthlib.flow import InstalledAppFlow
#
# scopes = ['https://www.googleapis.com/auth/calendar']
#
# flow = InstalledAppFlow.from_client_secrets_file("client_secret.json",scopes = scopes, redirect_uri = "http://127.0.0.1:8050/calendar-sync")
# flow.redirect_uri = 'http://127.0.0.1:8050/calendar-sync'
# print(flow.client_type)
# print(flow.redirect_uri)
# credentials = flow.run_console()
# service = build('calendar','v3',credentials = credentials)
#
# print(service.events())

from __future__ import print_function
from dash_google_oauth.google_auth import GoogleAuth
import pandas as pd
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
def getCalAuth(df):
  SCOPES = ['https://www.googleapis.com/auth/calendar']
  creds = None
  flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json', SCOPES, redirect_uri=r"https://cal-automation.herokuapp.com/login")
  creds = flow.run_local_server(port=0)
  with open('token.json', 'w') as token:
    token.write(creds.to_json())
  service = build('calendar', 'v3', credentials=creds)
  for events in df.index:
    print(str(df.loc[events]['Start Date'])+"T"+str(df.loc[events]['Start Time']))
    event = {
      'summary': df.loc[events]['Subject'],
      'start':{
        'dateTime': str(df.loc[events]['Start Date'])+"T"+str(df.loc[events]['Start Time'])+"+05:30",
      },
      'end':{
        'dateTime': str(df.loc[events]['Start Date']) + "T" + str(df.loc[events]['End Time'])+"+05:30",
      }
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
  return event.get('htmlLink')

# def getnewCal(app):
#   FLASK_SECRET_KEY = "Ameya18"
#
#   GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent"
#   GOOGLE_AUTH_SCOPE = "https://www.googleapis.com/auth/calendar"
#   GOOGLE_AUTH_TOKEN_URI = "https://oauth2.googleapis.com/token"
#   GOOGLE_AUTH_REDIRECT_URI = "http://127.0.0.1:8050/login"
#   GOOGLE_AUTH_USER_INFO_URL = "https://www.googleapis.com/userinfo/v2/me"
#   GOOGLE_AUTH_CLIENT_ID = "550396994206-5o6q7tb3rsrs5ektotost0dkqotfdtmo.apps.googleusercontent.com"
#   GOOGLE_AUTH_CLIENT_SECRET = "oRO6Fc3u4yx4j7u_SlNc67cM"
#   auth = GoogleAuth(app)
#   return auth
