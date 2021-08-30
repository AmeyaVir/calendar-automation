# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_auth
from dash.dependencies import Output,Input, State
import plotly.express as px
import pandas as pd
# from flask_oauthlib.provider import OAuth2Provider
import pickle

# from cal_setup import getCalAuth
from processFiles import processExcel,processUpdatedFile,generateEventCSV,generateLabTable, getDataBase
from flask import Flask, redirect, url_for, session , request, render_template


label_key = pd.read_csv('course_list.csv')
label_key.loc[0]['Courses']
scopes = ['https://www.googleapis.com/auth/calendar']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# print(auth)
colors_main = {
    'background': '#000000',
    'text': '#7FDBFF'
}
landing_page = html.Div( children=[
    html.H1(
        children='Calendar Sync App',
        style={
            'textAlign': 'center',
            'color': colors_main['text']
        }
    )
  ])

url_bar_and_content_div = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),
    dcc.Link('Navigate to Login Page', href='/login'),
    html.Br(),
    dcc.Link('Navigate to Calendar Sync', href='/calendar-sync'),
    html.Div(id='page-content'),
])

layout_1 = html.Div( children=[
    html.H1(
        children='Calendar Sync App',
        style={
            'textAlign': 'center',
            'color': colors_main['text']
        }
    ),

    html.B(
      children= "Please select the courses from the dropdown",style={
            'textAlign': 'center',
            'color': colors_main['text']
        },
    ),
    dcc.Dropdown(
        id = "dropdown-courses",
        options= [{'label':label_key.loc[index]['Courses'],'value':label_key.loc[index]['course_key']}
                  for index in label_key.index],
        multi=True,
        style={
            'textAlign': 'center',
            'color': colors_main['text']
        }),

    html.Div(
      id='return-dropdown'
    ),html.Div(children =[html.Button("Click here to download the file", id="btn_txt", type="reset", style={
            'textAlign': 'center',
            'color': colors_main['text']
        }), dcc.Download(id="csv-download"),
    html.P(),
    html.Button("Sync the calendar with GCal", id="google-sign-in", type="reset", style={
            'textAlign': 'center',
            'color': colors_main['text']
        })
    ]),
    html.A("Link to calendar", href='https://plot.ly', target="_blank", id='success-check'),
    html.H1(
        children='Attendance Sheet',
        style={
            'textAlign': 'center',
            'color': colors_main['text']
        }
    ),
    html.Div(id='attendance-analytics',style={},
    children=[
    dcc.Input(id='get-username',placeholder="Type the user email id"),
    html.P(),
    dcc.Input(id='get-password', placeholder= "Type the password",type='password'),
    html.P(),
    html.Button(
        id='signin-button',
        children='Click for sign in',
        type="reset",
        style={
            'textAlign': 'center',
            'color': colors_main['text']
        }
    ),
    dcc.Graph(id='barGraphTotal'),
    dash_table.DataTable(id = 'dataDisplay', filter_action='native', columns= [{
      'name':'Name (Original Name)',
      'id': 'Name (Original Name)'},
      {'name': 'Total Duration (Minutes)',
       'id':'Total Duration (Minutes)'},
      {'name':'Course',
       'id':'Course'},
      {'name':'Filename',
       'id':'Filename'}
    ])
    ])
  ])

login_page = html.Div(style={'backgroundColor': colors_main['background']}, children=[
    html.Title(
      children='Login Page'
    ),
    html.Button(
        id='login-button',
        children='Click for sign in',
        type="reset",
        style={
            'textAlign': 'center',
            'color': colors_main['text']
        }
    ),
    html.H2(id="successAuth")
  ])

# entry_page = html.Div(style={'backgroundColor': colors_main['background']}, children=[
#
#     html.Title(
#       children= 'Login Page'
#     ),
#     html.Button(
#         id = 'login-button',
#         children='Click for sign in',
#         style={
#             'textAlign': 'center',
#             'color': colors_main['text']
#         }
#     ),
#   ])

app.layout = url_bar_and_content_div
app.validation_layout = html.Div([
    url_bar_and_content_div,
    landing_page,
    layout_1,
    login_page
])
server = app.server

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/calendar-sync":
        return layout_1
    elif pathname == "/login":
        return login_page
    else:
        return landing_page


@app.callback(Output('successAuth', 'children'),
              Input('login-button', 'n_clicks'),
              prevent_initial_call = True)
def redirect_url(value):
    auth_handle = cal_setup.getnewCal(app)
    return "Successful"


@app.callback(Output('csv-download','data'),
              Input('btn_txt','n_clicks'),
              Input('dropdown-courses', 'value'),
              prevent_initial_call = True,
            )
def return_output(n_clicks,value):
  df_schedule = processExcel('schedule')
  df_upd = generateLabTable(df_schedule)
  df_update = processUpdatedFile(df_upd)
  print('Number of Clicks =', n_clicks)
  data = generateEventCSV(value,df_update)
  if n_clicks != None:
    return dcc.send_data_frame(data.to_csv,"usercal.csv")

# @app.callback(Output('google-sign-output','children'),
#               Input('google-sign-in','n_clicks'),
#               Input('csv-download','data'),
#               prevent_initial_call = True)
# def updateCal(n_clicks,data):
#   service = getCalAuth()
#   pd.read_csv(data)
#   for events in len(data):
#     event = {'location':data.iloc[events]['Location'],
#              'start':data.iloc[events]['']

# @app.callback(Output("url","pathname"),
#               Input("login-button","n_clicks"))
# def redirect_uri(n_clicks):
#   return "/calendar-sync"

@app.callback(Output('dataDisplay','data'),
              Output('barGraphTotal','figure'),
              Input('signin-button','n_clicks'),
              State('get-username','value'),
              State('get-password','value'),
              prevent_initial_call = True)
def show_analytics(n_clicks,username, password):
    try:
      df = getDataBase(username,password)
      temp_df = df[df['User Email'] == username]
      temp_df = temp_df.drop_duplicates()
      #column_name = [{"name":i, "id":i} for i in temp_df.columns]
      df_graph = temp_df.groupby(['Course']).agg({'Filename':'count'})
      print(df_graph.head())
      list_courses = df_graph.index
      fig = px.bar(df_graph,x=list_courses,y='Filename', labels={'Filename':'Number of classes attended'},
                   text = 'Filename', title='Attendance Chart')
      fig.update_layout(uniformtext_minsize=24, uniformtext_mode='hide')
      return  temp_df.to_dict('records'), fig
    except:
      print('Login Failed')
# @app.callback(Output('success-check','href'),
#               Input("google-sign-in","n_clicks"),
#               Input('dropdown-courses', 'value'),
#               prevent_initial_call=True)
# def redirect_uri(n_clicks,value):
#   if n_clicks != None:
#     df_schedule = processExcel('schedule')
#     df_upd = generateLabTable(df_schedule)
#     df_update = processUpdatedFile(df_upd)
#     data = generateEventCSV(value, df_update)
#     service = getCalAuth(data)
#     return service
#
# @app.callback(Output("page-content","children"),
#               Input("cal-sync-landing-page","n_clicks"))
# def redirect_uri(n_clicks):
#   if n_clicks!=None:
#     return "layout_1"
# @app.callback(Output('barGraphTotal','figure'),
#               Input('storedDf', 'data'))

if __name__ == '__main__':
    app.run_server(debug=True)

