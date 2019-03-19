import os
from flask import Flask, g
from flask import Flask, request
from flask import render_template, flash, redirect, url_for, session, escape
import models

# User login
from flask_login import current_user, login_user

# User logout
from flask_login import logout_user

# Redirect user when not logged in
from werkzeug.urls import url_parse


app = Flask(__name__, static_url_path='/static')

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'pickle'

@app.before_request
def before_request():
# Connect to the DB before each request
  g.db = models.DATABASE
  g.db.connect()

@app.after_request
def after_request(response):
# Close the database connection after each request
  g.db.close()
  return response
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

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
 

@app.route('/signup', methods=['POST'])
def signup():

@app.route('/logout')
def logout():


@app.route('/profile', methods=['GET', 'PUT'])
@app.route('/profile/<id>', methods=['GET'])


@app.route('/recipes', methods=['GET', 'POST'])
@app.route('/recipes/<id>', methods=['GET', 'PUT', 'POST', 'DELETE'])




# @app.route('/login', methods=['POST'])
# def login():

# @app.route('/signup', methods=['POST'])
# def signup():

# @app.route('/logout')
# def loguout():

# @app.route('/profile', methods=['GET', 'PUT', 'POST'])
# def profile():







@app.route('/')
def hello_world():
    return render_template('/index.html')
# @app.route('/recipes', methods=['GET', 'POST'])
# @app.route('/recipes/<id>', methods=['GET', 'PUT', 'POST'])
# def get_all_recipes():


if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)