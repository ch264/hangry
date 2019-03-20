import os
from flask import Flask, g
from flask import Flask, request
from flask import render_template, flash, redirect, url_for, session, escape
from flask_bcrypt import check_password_hash
# User login
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
# Redirect user when not logged in
from werkzeug.urls import url_parse

import models
import forms



app = Flask(__name__, static_url_path='/static')

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'pickle'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try: 
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
  g.db = models.DATABASE
  g.db.connect()
  g.user = current_user

@app.after_request
def after_request(response):
  g.db.close()
  return response



@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Email or password not found.  Please sign up!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                ## creates session
                login_user(user)
                flash("You successfully logged in", "success")
                return redirect(url_for('profile', username=user.username))
            else:
                flash("your email or password doesn't match", "error")
    return render_template('login.html', form=form)
#  will change 

@app.route('/signup', methods=('GET', 'POST'))
def register():
    form = forms.SignUpForm()
    if form.validate_on_submit():
        flash('Thank you for signing up', 'success')
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            location=form.location.data
            )
        user = models.User.get(models.User.username == form.username.data)
        login_user(user)
        name = user.username
        return redirect(url_for('profile', username=name))
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out", "success")
    return redirect(url_for('index'))


@app.route('/profile')
@app.route('/profile/<username>', methods=['GET', 'DELETE', 'PUT'])
def profile(username=None):
    if username == None and request.method == 'GET':
        # return repr(models.User.select().get())
        return render_template('profile.html')
    elif username != None and request.method == 'PUT':
        email = request.json['email']
        location = request.json['location']
        user = models.User.select().where(models.User.username == username).get()
        # User can change their email or location
        user.email = email
        user.location = location
        user.save()
        return repr(user)
    elif username != None and request.method == 'GET':
        user = models.User.select().where(models.User.username==username).get()
        return render_template('profile.html', user=user)
        # return repr(models.User.select().where(models.User.username==username).get())
    elif username == None and request.method == 'POST':
        created = models.User.create(
            username = request.json['username'],
            email = request.json['email'],
            password=request.json['password'],
            location = request.json['location']
            )
        user = models.User.select().where(models.User.username == created.username).get()
        return repr(user)
    else: 
        user = models.User.select().where(models.User.username == username).get()
        user.delete_instance()
        return repr(user)
    


@app.route('/recipe', methods=['GET', 'POST'])
@app.route('/recipe/<user>', methods=['GET', 'PUT', 'POST', 'DELETE'])
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


#  will change 
        # else: 
        #     user = models.Recipe.select().where(models.Recipe.title == title).get()
        #     user.delete_instance()
        #     return repr(user)


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
        username='brandon',
        email="brandon@gmail.com",
        password='password',
        location="San Francisco"
        ),
        models.User.create_user(
        username='christina',
        email="christina@gmail.com",
        password='password',
        location="San Francisco"
        ),
        models.User.create_user(
        username='nicolette',
        email="nicolette@gmail.com",
        password='password',
        location="San Francisco"
        ),
        models.User.create_user(
        username='ronni',
        email="ronni@gmail.com",
        password='password',
        location="San Francisco"
        )
    except ValueError:
        pass

app.run(debug=DEBUG, port=PORT)