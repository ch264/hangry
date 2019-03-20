import os
from flask import Flask, g
from flask import Flask, request

from flask import render_template, flash, redirect, url_for, session, escape

# User login
from flask_login import current_user, login_user

# User logout
from flask_login import logout_user

# Redirect user when not logged in
from werkzeug.urls import url_parse

# import models
import forms


app = Flask(__name__, static_url_path='/static')

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'pickle'

# @app.before_request
# def before_request():
# # Connect to the DB before each request
#   g.db = models.DATABASE
#   g.db.connect()

# @app.after_request
# def after_request(response):
# # Close the database connection after each request
#   g.db.close()
#   return response

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    return render_template('login.html', form=form)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = forms.UserForm()
    return render_template('signup.html', form=form)


<<<<<<< HEAD
###
@app.route('/recipes', methods=['GET', 'POST'])
@app.route('/recipes/<id>', methods=['GET', 'PUT', 'POST', 'DELETE'])

@login_required
def post():
    form = forms.RecipeForm()
    if form.validate_on_submit():
        flash("Recipe Created!", "success") 
        models.Recipe.create(
            user=g.user._get_current_object(), #create new post.
                           content=form.content.data.strip()) 
        
        
        return redirect(url_for('index')) #redirect user
    return render_template('profile.html', form=form)
=======
# @app.route('/logout')
# def logout():


# @app.route('/profile', methods=['GET', 'PUT'])
# @app.route('/profile/<id>', methods=['GET'])
>>>>>>> dbb142e639e2c23428c5d05af598d140fc494469


# @app.route('/recipes', methods=['GET', 'POST'])
# @app.route('/recipes/<id>', methods=['GET', 'PUT', 'POST', 'DELETE'])



if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)