#!/usr/bin/python3
import os
import requests
import json

from dotenv import load_dotenv
from flask import Flask, make_response, request, redirect, session
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
api_url_base = 'https://api.github.com/'

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
    res = make_response(redirect(f'{authorize_url}?{urlencode(params)}'))
    return res


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('access_token', None)
    return redirect('/')


# When Github redirects the user back here,
# there will be a "code" and "state" parameter in the query string
@app.route('/callback', methods=['GET'])
def callback():
    parsed = urlparse(request.url)

    code = parse_qs(parsed.query)['code'][0]
    state = parse_qs(parsed.query)['state'][0]

    if (not state) or (state != session['state']):
        return redirect('/?error=invalid_state')

    token = requests.post(
        token_url,
        data={
            'grant_type': 'authorization_code',
            'client_id': github_client_id,
            'client_secret': github_client_secret,
            'redirect_url': base_url,
            'code': code
        },
        headers={
            'Accept': 'application/vnd.github.v3+json, application/json',
            'User-Agent': 'https://example-app.com/'
        }
    ).json()

    session['access_token'] = token['access_token']

    return redirect('/callback')


@app.route('/repos', methods=['GET'])
def repos():
    url = api_url_base + 'user/repos?' + urlencode({
        'sort': 'created',
        'direction': 'desc'
    })

    repos = requests.get(
        url,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {session['access_token']}"
        }
    ).json()
    return_str = '<ul>'

    for repo in repos:
        return_str += '<a href="' + repo['html_url'] + '">' + repo['name'] + '</a></li><br>'
    return_str += '</ul>'
    return return_str


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


# def api_request(url:str, body:dict, post:bool=False):
#     headers = {
#         'Accept: application/vnd.github.v3+json, application/json',
#         'User-Agent: https://example-app.com/'
#     }

#     if 'access_token' in session:
#         headers['Authorization'] = f"Bearer {session['access_token']}"

#     if post:
#         response = requests.post(
#             url,
#             data=json.dumps(body),
#             headers=headers
#         )
#     else:
#         response = requests.get(
#             url,
#             headers=headers
#         )

#     return response.json()


if __name__=="__main__":
    app.run(debug=True, port='8000')
