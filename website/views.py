from flask import (
    abort,
    Blueprint,
    Flask,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
import json
import logging
import os
import requests
import secrets
import string
from urllib.parse import urlencode
import spotipy
from spotipy.oauth2 import SpotifyOAuth

views = Blueprint('views', __name__)

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

# Client info
CLIENT_ID=XXXXXXXXXX
CLIENT_SECRET=XXXXXXXX
REDIRECT_URI='http://127.0.0.1:5000/callback'


# Spotify API endpoints
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
ACCOUNT_URL = 'https://api.spotify.com/v1/me'


@views.route('/')
def login():
   
    
    state = ''.join(
        secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16)
    )

    loginout = 'login'
    # need scope access for playlists, tracks, and other user info
    scope = 'user-read-private playlist-modify-private playlist-modify-public user-library-read'

    if loginout == 'logout':
        payload = {
            'client_id': CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'state': state,
            'scope': scope,
            'show_dialog': True,
        }
    elif loginout == 'login':
        payload = {
            'client_id': CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'state': state,
            'scope': scope,
        }
    else:
        abort(404)

    res = make_response(redirect(f'{AUTH_URL}/?{urlencode(payload)}'))
    res.set_cookie('spotify_auth_state', state)

    return res

@views.route('/callback')
def callback():
    error = request.args.get('error')
    code = request.args.get('code')
    state = request.args.get('state')
    stored_state = request.cookies.get('spotify_auth_state')

    # Check state
    if state is None or state != stored_state:
        views.logger.error('Error message: %s', repr(error))
        views.logger.error('State mismatch: %s != %s', stored_state, state)
        abort(400)

    # Request tokens with code we obtained
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }

    res = requests.post(TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload)
    res_data = res.json()

    if res_data.get('error') or res.status_code != 200:
        views.logger.error(
            'Failed to receive token: %s',
            res_data.get('error', 'No error information received.'),
        )
        abort(res.status_code)

    # Load tokens into session
    session['tokens'] = {
        'access_token': res_data.get('access_token'),
        'refresh_token': res_data.get('refresh_token'),
    }

    return redirect(url_for('views.account'))

@views.route('/refresh')
def refresh():
    '''Refresh access token.'''

    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': session.get('tokens').get('refresh_token'),
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    res = requests.post(
        TOKEN_URL, auth=(CLIENT_ID, CLIENT_SECRET), data=payload, headers=headers
    )
    res_data = res.json()

    # Load new token into session
    session['tokens']['access_token'] = res_data.get('access_token')

    return json.dumps(session['tokens'])

@views.route('/account')
def account():
    '''Get profile info as a API example.'''

    # Check for tokens
    if 'tokens' not in session:
        views.logger.error('No tokens in session.')
        abort(400)

    # Get profile info
    headers = {'Authorization': f"Bearer {session['tokens'].get('access_token')}"}

    res = requests.get(ACCOUNT_URL, headers=headers)
    res_data = res.json()

    if res.status_code != 200:
        views.logger.error(
            'Failed to get profile info: %s',
            res_data.get('error', 'No error message returned.'),
        )
        abort(res.status_code)

    return render_template('account.html', data=res_data, tokens=session.get('tokens'))

@views.route('/find')
def home():
    return render_template("home.html")


@views.route('/mixer')
def mixer():
    return render_template("mixer.html")


