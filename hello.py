# AS simeple as possbile flask google oAuth 2.0
import time

from flask import Flask, redirect, url_for, session , request, render_template
from authlib.flask.client import OAuth
import os
from datetime import timedelta

# decorator for routes that should be accessible only by logged in users
from auth_decorator import login_required

# dotenv setup
from dotenv import load_dotenv
load_dotenv()


# App config
app = Flask(__name__)
# Session config
app.secret_key = "APP_SECRET_KEY"
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id= "460943878391-90f84gi6ji5630gfbtu7llb57vqf7mfa.apps.googleusercontent.com",
    client_secret="tAZPhWUhHzkF_TbCzeA55kY7",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/calendar/v3',
    client_kwargs={'scope': 'https://www.googleapis.com/auth/calendar'},
)


@app.route('/')
@login_required
def hello_world():
    name = dict(session)['profile']['name']
    return f'Hello, Welcome {name}!'


@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', external=True)
    print(redirect_uri)
    print(google.authorize_redirect(redirect_uri))
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    print(token)
#     resp = google.get('userinfo', token=token)  # userinfo contains stuff u specificed in the scropec
#     user_info = resp.json()
# #    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
#     # Here you use the profile/user data that you got and query your database find/register the user
#     # and set ur own data in the session not the profile from google
#     session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


