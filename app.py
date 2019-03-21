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
app.secret_key = 'pickle'

DEBUG = True
PORT = 8000

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
                flash("Your email or password doesn't match", "error")
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


# @app.route('/profile')
@app.route('/profile/<username>', methods=['GET', 'DELETE'])
@login_required
def profile(username=None):
    if username != None and request.method == 'GET':
        user = models.User.select().where(models.User.username==username).get()
        recipes = models.Recipe.select().where(models.Recipe.user == user.id)
        # saved_recipes = models.SavedRecipes.select().where(models.SavedRecipes.user == user.id)
        return render_template('profile.html', user=user, recipes=recipes)

    return redirect(url_for('index'))


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = models.User.get(current_user.id)
    form = forms.EditUserForm()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        # user.password = form.password.data
        user.location = form.location.data
        user.save()
        flash('Your changes have been saved.')
        return render_template('edit-profile.html', form=form, user=user)
    return render_template('edit-profile.html', form=form, user=user)

    
@app.route('/save/<recipe_id>')
def save_to_favorite(recipe_id=None):
    user = g.user._get_current_object()
    recipe = models.Recipe.get(models.Recipe.id == recipe_id)

    models.SavedRecipes.create(user=user.id, recipe=recipe.id)

    return redirect(url_for('recipe'))


@app.route('/recipe', methods=['GET'])
@app.route('/recipe/<recipe_id>', methods=['GET', 'PUT'])
def recipe(recipe_id=None):
    form = forms.RecipeForm()
    if recipe_id != None and request.method == 'GET':
        recipe = models.Recipe.select().where(models.Recipe.id == recipe_id).get()
        return render_template('recipe.html', recipe=recipe)

    recipes = models.Recipe.select().limit(20)
    return render_template('recipes.html', recipes=recipes)

@app.route('/create-recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = forms.RecipeForm()
    user = g.user._get_current_object()
    if request.method == 'POST':
        models.Recipe.create(
            category = form.category.data, #SelectField -use form instead of json
            title = form.title.data,
            content = form.content.data,
            ingredient_tag = form.ingredient_tag.data,
            user = g.user._get_current_object())
        recipe = models.Recipe.get(models.Recipe.title == form.title.data)
        return redirect(url_for('recipe', recipe_id=recipe.id))
    else:
        return render_template('create-recipe.html', form=form)

# [] TO BE TESTED
@app.route('/edit-recipe/<recipe_id>', methods=['GET', 'PUT'])
def edit_recipe(recipe_id=None):
    form = forms.EditRecipeForm()
    recipe = models.Recipe.select().where(models.Recipe.id==recipe_id).get()
    return render_template('edit-recipe.html', form=form, recipe=recipe)
        

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
        ),
        models.Recipe.create_recipe(
        category='Asian',
        title="Dumplings",
        content='Delicious',
        ingredient_tag="Pork. Cabbage.",
        user = 1
        ),
        models.Recipe.create_recipe(
        category='Italian',
        title="Spaghetti",
        content='Yummy Pasta',
        ingredient_tag="Pasta. Meat. Sauce.",
        user = 2
        ),
        models.Recipe.create_recipe(
        category='Mexican',
        title="Enchaladas",
        content='Quick and easy',
        ingredient_tag="Meat. Cheese. Tortillas",
        user = 3
        ),
        models.Recipe.create_recipe(
        category='Chinese',
        title="Orange Chicken",
        content='Crispy Chicken',
        ingredient_tag="Chicken. Oranges.",
        user = 3
        ),
        models.Recipe.create_recipe(
        category='Indian',
        title="Tofu Tikka Marsala",
        content='Taste Authentic',
        ingredient_tag="Tofu. Sauce.",
        user = 2
        ),
        models.Recipe.create_recipe(
        category='Southern',
        title="Gumbo",
        content='Simple and Quick',
        ingredient_tag="Meat. Seafood. Rice. Veggies.",
        user = 1
        )

    
    
    
    except ValueError:
        pass

app.run(debug=DEBUG, port=PORT)