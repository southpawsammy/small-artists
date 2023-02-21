from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sacc'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Client info
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')

    # Spotify API endpoints
    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    TOP_ENDPOINT = 'https://api.spotify.com/v1/me/top/tracks'
    

    return app