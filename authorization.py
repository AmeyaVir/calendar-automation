from authlib.client import OAuth2Session
client_id = "550396994206-5o6q7tb3rsrs5ektotost0dkqotfdtmo.apps.googleusercontent.com"
client_secret = "oRO6Fc3u4yx4j7u_SlNc67cM"
scope = 'https://www.googleapis.com/auth/calendar.readonly'
session = OAuth2Session(client_id,client_secret,scope)
uri, state = session.create_authorization_url('http://127.0.0.1:8050/login')


