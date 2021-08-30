import pandas as pd
import datetime as dt
import time
import imaplib
import email
from io import StringIO


# import requests module
import requests


def getDataBase(username, password):
  imap_host = 'imap.mail.gov.in'
  imap_user = username
  imap_pass = password
  imap = imaplib.IMAP4_SSL(imap_host)
  imap.login(imap_user, imap_pass)
  imap.select('Inbox')

  tmp, msgs = imap.search(None, 'SUBJECT', '"Attendance record"')
  msgs = msgs[0].split()

  df = pd.DataFrame()
  for emailid in msgs:
    resp, data = imap.fetch(emailid, '(RFC822)')
    email_body = data[0][1].decode('UTF-8')
    m = email.message_from_string(email_body)
    if m.get_content_maintype() != 'multipart':
      continue

    for part in m.walk():
      if part.get_content_maintype() == 'multipart':
        continue
      if part.get('Content-Disposition') is None:
        continue

      filename = part.get_filename()
      if filename is not None:
        s = str(part.get_payload(decode=True), 'utf-8')
        data = StringIO(s)
        temp_df = pd.read_csv(data)
        temp_df['Course'] = filename.split()[0]
        temp_df['Filename'] = filename
        df = df.append(temp_df)
  print(df.head())
  return df


def processExcel(name):
  name = name + ".csv"
  cal_excel = pd.read_csv(name)
  cal_excel = cal_excel.rename(columns={'Week 1st to 11th': 'Week', 'Unnamed: 1': 'Date', 'Unnamed: 2': 'Day'})
  dic_col = dict()
  # initial timeslot
  for time in cal_excel.columns[3:]:
    time_upd = time.replace(" hrs", "")
    list_time = [dt.datetime.strptime(item, "%H:%M") for item in time_upd.split("-")]
    print(type(dic_col))
    entry = {time: list_time[0]}
    print(entry)
    dic_col.update(entry)
  cal_excel = cal_excel.rename(columns=dic_col).fillna(method='ffill')
  return cal_excel

def generateLabTable(df_schedule):
    df_updated = pd.DataFrame()
    timings_list = df_schedule.loc[0][3:].index
    for index in df_schedule.index:
      list_enter = [df_schedule.loc[index]['Date']]
      for time in timings_list:
        list_enter.append(time)
        for entry in df_schedule.loc[index][time].split("/"):
          list_enter.append(entry)
          pos = entry.find('LH-')
          dict_enter = pd.Series(data={'Subject': list_enter[2], 'Start Time': list_enter[1],
                                       'Start Date': list_enter[0], 'Location': entry[pos:pos + 4]})
          df_updated = df_updated.append(dict_enter, ignore_index=True)
          list_enter.pop()
        list_enter.pop()
    return df_updated

def processUpdatedFile(df_updated):
  df_updated['End Time'] = df_updated['Start Time'] + dt.timedelta(minutes=90)
  print(df_updated.head())
  start_day_upd = [dt.datetime.fromtimestamp(time.mktime(time.strptime(entry, "%d-%b-%y"))).date() for entry in
                   df_updated['Start Date']]
  df_updated['Start Date'] = start_day_upd
  start_time_upd = [entry.time() for entry in df_updated['Start Time']]
  end_time_upd = [entry.time() for entry in df_updated['End Time']]
  df_updated['Start Time'] = start_time_upd
  df_updated['End Time'] = end_time_upd
  return df_updated

def generateEventCSV(list_course, df_updated):
    list_indices = []
    print("list_course is:",list_course)
    col = ['Subject', 'Start Date', 'Start Time', 'End Time', 'Location']
    for entry in list_course:
      list_indices = list_indices + [i for i in df_updated.index if df_updated['Subject'].str.find(entry)[i] != -1]
    return df_updated.iloc[list_indices]

# def getClassmates(df,user_name):
#   file_names = df['Filename'].unique()
#   for file in file_names:
#     file.
