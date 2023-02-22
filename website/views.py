from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def login():
    return render_template("login.html")

@views.route('/find')
def home():
    return render_template("home.html")


@views.route('/logout')
def logout():
    return '<p>Logout</p>'

@views.route('/callback')
def callback():
    return '<p>Callback page</p>'

@views.route('/account')
def account():
    return render_template("account.html")
