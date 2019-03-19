import os
from flask import Flask, request
from flask import render_template, flash, redirect, url_for


app = Flask(__name__)

DEBUG = True
PORT = 8000



@app.route('/')
def index():

@app.route('/about')
def about():

@app.route('/login', methods=['POST'])
def login():

@app.route('/signup', methods=['POST'])
def signup():

@app.route('/logout')
def loguout():

@app.route('/profile', methods=['GET', 'PUT', 'POST'])
def profile():

@app.route('/recipes', methods=['GET', 'POST'])
@app.route('/recipes/<id>', methods=['GET', 'PUT', 'POST'])
def get_all_recipes():









@app.route('/')
def hello_world():
    return 'Hello World'


if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)