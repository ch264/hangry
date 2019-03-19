import os
from flask import Flask, request
from flask import render_template, flash, redirect, url_for

# User login
from flask_login import current_user, login_user

# User logout
from flask_login import logout_user

# Redirect user when not logged in
from werkzeug.urls import url_parse


app = Flask(__name__, static_url_path='/static')

DEBUG = True
PORT = 8000

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.hangry')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Test route
# @app.route('/')
# def hello_world():
#     return 'Hello World'

@app.route('/')
def index():
    return render_template('landing.html')

# @app.route('/about')
# def about():

# @app.route('/login', methods=['POST'])
# def login():

# @app.route('/signup', methods=['POST'])
# def signup():

# @app.route('/logout')
# def loguout():

# @app.route('/profile', methods=['GET', 'PUT', 'POST'])
# def profile():

# @app.route('/recipes', methods=['GET', 'POST'])
# @app.route('/recipes/<id>', methods=['GET', 'PUT', 'POST'])
# def get_all_recipes():


if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)