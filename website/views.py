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

views = Blueprint('views', __name__)

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

# Client info
CLIENT_ID='504254a465ad49bc9f6abe15650bf9f0'
CLIENT_SECRET='69b0845682f341cabe3011c7cc51b68c'
REDIRECT_URI='http://127.0.0.1:5000/find'


# Spotify API endpoints
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
ME_URL = 'https://api.spotify.com/v1/me'


@views.route('/')
def login():
   
    # redirect_uri can be guessed, so let's generate
    # a random `state` string to prevent csrf forgery.
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
    #return render_template("login.html")

@views.route('/find')
def home():

    FIND_URL = 'https://api.spotify.com/v1/search'

    return render_template("home.html")

@views.route('/mixer')
def mixer():
    return render_template("mixer.html")

@views.route('/callback')
def callback():
    return '<p>Callback page</p>'

@views.route('/account')
def account():
    return render_template("account.html")
