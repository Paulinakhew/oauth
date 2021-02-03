#!/usr/bin/python3
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session

# get environment variables
load_dotenv()
github_client_id = os.environ.get('GITHUB_CLIENT_ID')
github_client_secret = os.environ.get('GITHUB_CLIENT_SECRET')

# This is the URL we'll send the user to first to get their authorization
authorize_url = 'https://github.com/login/oauth/authorize'

# This is the endpoint our server will request an access token from
token_url = 'https://github.com/login/oauth/access_token'

# This is the Github base URL we can use to make authenticated API requests
api_url_nase = 'https://api.github.com/'

# The URL for this script, used as the redirect URL
base_url = 'http://localhost:8000/callback'

# Start up the Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


# If there is an access token in the session
# the user is already logged in
@app.route('/')
def index():
    if 'access_token' in session:
        return ''''<h3>Logged In</h3>
        <p><a href="?action=repos">View Repos</a></p>
        <p><a href="?action=logout">Log Out</a></p>'''
    else:
        return '''<h3>Not logged in</h3>
        <p><a href="?action=login">Log In</a></p>'''


if __name__=="__main__":
    app.run(debug=True, port='8000')
