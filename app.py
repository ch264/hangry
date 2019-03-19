import os
from flask import Flask, g
from flask import Flask, request
from flask import render_template, flash, redirect, url_for, session, escape
import models

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

@app.route('/')
def index():

@app.route('/about')
def about():

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













@app.route('/')
def hello_world():
    return render_template('/index.html')


if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)