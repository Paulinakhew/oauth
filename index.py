#!/usr/bin/python3
import os
import requests
import json

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from urllib.parse import parse_qs, urlencode, urlparse
from urllib import parse

# get environment variables
load_dotenv()

# Fill these out with the values you got from Github
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


# Start the login process by sending the user
# to Github's authorization page
@app.route('/login', methods=['GET'])
def login():
    session.pop('access_token', None)

    # Generate a random hash and store in the session
    session['state'] = os.urandom(16).hex()

    params = {
        'response_type': 'code',
        'client_id': github_client_id,
        'redirect_uri': base_url,
        'scope': 'user public_repo',
        'state': session['state']
    }

    # Redirect the user to GitHub's authorization page
    res = redirect(f'{authorize_url}?{urlencode(params)}')
    return res


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('access_token', None)
    print(session['access_token'])
    return redirect('/')


# When Github redirects the user back here,
# there will be a "code" and "state" parameter in the query string
@app.route('/callback', methods=['GET'])
def callback():
    parsed = urlparse(request.url)

    code = parse_qs(parsed.query)['code'][0]
    state = parse_qs(parsed.query)['state'][0]

    if state and state != session['state']:
        return redirect('/?error=invalid_state')
    params = {
        'grant_type': 'authorization_code',
        'client_id': github_client_id,
        'client_secret': github_client_secret,
        'redirect_url': base_url,
        'code': code
    }

    token = api_request(token_url, params)
    # FIXME: no token['access_token'] to be found
    session['access_token'] = token['access_token']

    return redirect('/')


# If there is an access token in the session
# the user is already logged in
@app.route('/', methods=['GET'])
def index():
    if 'access_token' in session:
        return ''''<h3>Logged In</h3>
        <p><a href="/repos">View Repos</a></p>
        <p><a href="/logout">Log Out</a></p>'''
    else:
        return '''<h3>Not logged in</h3>
        <p><a href="/login">Log In</a></p>'''


def api_request(url:str, body:dict, post:bool=False):
    headers = {
        'Accept: application/vnd.github.v3+json, application/json',
        'User-Agent: https://example-app.com/'
    }

    if session['access_token']:
        headers['Authorization'] = f"Bearer {session['access_token']}"

    if post:
        response = requests.post(
            url,
            data=json.dumps(body),
            headers=headers
        )
    else:
        response = requests.get(
            url,
            headers=headers
        )

    return response.json()


if __name__=="__main__":
    app.run(debug=True, port='8000')
