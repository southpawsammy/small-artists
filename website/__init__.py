from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sacc'

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    # Client info
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    REDIRECT_URI = os.getenv('REDIRECT_URI')

    # Spotify API endpoints
    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    TRACKS_ENDPOINT = 'https://api.spotify.com/v1/me/top/tracks'
    ACCOUNT_URL = 'https://api.spotify.com/v1/me'
  

    return app