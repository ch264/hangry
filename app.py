import os
from flask import Flask, g, request
from flask import render_template, flash, redirect, url_for, session, escape

# User login
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_bcrypt import check_password_hash

# Image uploader
from flask_uploads import UploadSet, configure_uploads, IMAGES

# For Heroku deployment
# from flask.ext.heroku import Heroku

import models
import forms


app = Flask(__name__, instance_relative_config=True)
# Sets upload destinations for image uploader
app.config.from_pyfile('flask.cfg')
app.secret_key = 'pickle'
# heroku = Heroku(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Sets variable images to uploader
images = UploadSet('images', IMAGES)
configure_uploads(app, images)


@login_manager.user_loader
def load_user(userid):
    try: 
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


# Connects to database and gets current user who is logged in
@app.before_request
def before_request():
  g.db = models.DATABASE
  g.db.connect()
  g.user = current_user

# Closes connection to database after request finishes
@app.after_request
def after_request(response):
  g.db.close()
  return response


# ====================================================================
# =========================  Initial Routes  =========================
# ====================================================================
# Sets landing page
@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/about')
def about():
    return render_template('about.html')


# ====================================================================
# ========================  User Auth Routes  ========================
# ====================================================================
# Route and method to sign up a user
@app.route('/signup', methods=('GET', 'POST'))
def register():
    # Access SignUpForm from forms.py
    form = forms.SignUpForm()

    if form.validate_on_submit():
        # Sets variable filename to image file of uploaded 'profile_image' from form
        filename = images.save(request.files['profile_image'])
        # Sets variable url to change image url to match filename
        url = images.url(filename)

        # Calls method 'create_user' as defined in models.py to create a user in database
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            location=form.location.data,
            image_filename=filename,
            image_url=url)
        
        # Gets newly created user from the database by matching username in the database to username entered in the form
        user = models.User.get(models.User.username == form.username.data)
        # Creates logged in session
        login_user(user)
        flash('Thank you for signing up', 'success')
        # Pass in current/logged in user as parameter to method 'profile' in order to redirect user to profile after signing up
        return redirect(url_for('profile', username=user.username))

    # Initial visit to this page renders the Sign Up template with the SignUpForm passed into it
    return render_template('signup.html', form=form)

# Route and method to login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Access LoginForm from forms.py
    form = forms.LoginForm()

    if form.validate_on_submit():
        try:
            # Find user using email address
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Email or password not found.  Please sign up!", "error")
        else:
            # Check hashed password in database against user's typed password
            if check_password_hash(user.password, form.password.data):
                # Creates logged in session
                login_user(user)
                flash("You successfully logged in", "success")

                # Upon successful login, redirect to user's profile page with user passed in as a parameter to the method 'profile'
                return redirect(url_for('profile', username=user.username))
            else:
                # If passwords don't match, flash error message
                flash("Your email or password doesn't match", "error")
    
    # Initial visit to this page renders the login template with the LoginForm passed into it
    return render_template('login.html', form=form)

# Route and method to logout
@app.route('/logout')
@login_required
def logout():
    # Ends logged in session
    logout_user()
    # Redirects user to 'index' method for landing page
    return redirect(url_for('index'))


# ====================================================================
# =========================  Profile Routes  =========================
# ====================================================================
# Route and method to go to a user's profile
@app.route('/profile/<username>', methods=['GET'])
@login_required
def profile(username=None):
    if username != None:
        # Finds user in database by username passed into url
        user = models.User.select().where(models.User.username==username).get()
        # Finds all recipes in database where the user id stored with a recipe matches the found user above's id
        recipes = models.Recipe.select().where(models.Recipe.user == user.id)
        # Finds all recipes in saved recipe junction table where the user id matches the found user above's id
        saved_recipes = models.SavedRecipes.select().where(models.SavedRecipes.user == user.id)

        # Passes all 3 variables into profile template to make use of database results
        return render_template('profile.html', user=user, recipes=recipes, saved_recipes=saved_recipes)
    
    # [] UNDER WHAT CONDITIONS DOES THIS REDIRECT HAPPEN?
    return redirect(url_for('index'))

# Route and method to edit a user's profile
@app.route('/edit-profile/<username>', methods=['GET', 'POST'])
@login_required
def edit_profile(username=None):
    # Finds user in database by logged in current user's id
    user = models.User.get(g.user.id)
    # Accesses EditUserForm from forms.py
    form = forms.EditUserForm()

    if username != None and request.method == 'POST':
        if form.validate_on_submit():
            # Set user's info in database to new values entered in form
            user.username = form.username.data
            user.email = form.email.data
            user.location = form.location.data
            
            # Save changes to user in database
            user.save()
            flash('Your changes have been saved.', 'success')
            # Redirect to user's profile to reflect changes
            return redirect(url_for('profile', username=user.username))
    
    # Upon initial visit to route, serves up edit profile form
    return render_template('edit-profile.html', form=form, user=user)


# ====================================================================
# ==========================  Recipe Routes  =========================
# ====================================================================
# Routes and methods for all recipes and individual recipes
@app.route('/recipe', methods=['GET'])
@app.route('/recipe/<recipe_id>', methods=['GET'])
@login_required
def recipe(recipe_id=None):
    # If recipe_id is provided as a parameter
    if recipe_id != None:
        # Find single recipe in database using that id number to match the id in the database
        recipe = models.Recipe.select().where(models.Recipe.id == recipe_id).get()
        # Pass found recipe to the individual recipe template
        return render_template('recipe.html', recipe=recipe)
    
    # If no recipe_id is provided as a paramter, select all recipes from the recipe table and limit to 20 results
    recipes = models.Recipe.select().limit(20)
    # Pass those found recipes to the recipes template
    return render_template('recipes.html', recipes=recipes)

# Route and method for a user to create a recipe
@app.route('/create-recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    # Access the RecipeForm from forms.py
    form = forms.RecipeForm()
    # Sets variable user to current logged in user
    user = g.user._get_current_object()
    
    if request.method == 'POST':
        # Sets variable filename to image file of uploaded 'recipe_image' from form
        filename = images.save(request.files['recipe_image'])
        # Sets variable url to change image url to match filename
        url = images.url(filename)

        models.Recipe.create(
            # User form.field instead of request.json in order to capture the category data since it's a SelectField, rather than a StringField etc.
            # Sets attributes of new recipe in database equal to what was input into the form
            category = form.category.data,
            title = form.title.data,
            content = form.content.data,
            ingredient_tag = form.ingredient_tag.data,
            # Sets user ID in recipe table to logged in user
            user = user,
            image_filename = filename,
            image_url = url)

        # Find newly created recipe in database
        recipe = models.Recipe.get(models.Recipe.title == form.title.data)
        flash('Recipe created!', 'success')
        # Redirect user to the individual recipe page with the found recipe's id passed in as a parameter
        return redirect(url_for('recipe', recipe_id=recipe.id))

    # Render the create-recipe template with the RecipeForm
    # Pass in current user in order to redirect user back to their profile if they choose to cancel creating a recipe
    return render_template('create-recipe.html', form=form, user=user)

# Route and method to edit recipe
@app.route('/edit-recipe/<recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id=None):
    # Accesses EditRecipeForm from forms.py
    form = forms.EditRecipeForm()
    # Find recipe in database that matches the recipe_id parameter
    recipe = models.Recipe.select().where(models.Recipe.id == recipe_id).get()

    # If recipe_id parameter provided and request method is POST (when form is submitted)
    if recipe_id != None and request.method == 'POST':
        if form.validate_on_submit():
            # Sets recipe's column attributes to form data as new values
            recipe.category = form.category.data
            recipe.title = form.title.data
            recipe.content = form.content.data
            recipe.ingredient_tag = form.ingredient_tag.data
            
            # Saves changes in database
            recipe.save()

            flash('Your changes have been saved.', 'success')
            # Redirect user to individual recipe with the recipe id as parameter
            return redirect(url_for('recipe', recipe_id=recipe.id))
    
    # Set the Category field in the edit recipe form to show the recipe's category
    form.category.default = recipe.category
    # [] WHY DOESN'T THIS POPULATE THE CONTENT FIELD?
    # form.content.data = recipe.content

    # Processes form with category populated
    form.process()

    # Render edit-recipe template with the EditRecipe form and pass in found recipe to populate the edit fields with their current value
    return render_template('edit-recipe.html', form=form, recipe=recipe)

# Route and method to delete a recipe
@app.route('/delete-recipe/<recipe_id>', methods=['GET', 'DELETE'])
@login_required
def delete_recipe(recipe_id=None):
    # If recipe_id provided
    if recipe_id != None:
        # Delete recipe in junction table in database that matches the recipe id parameter, so that any user who has the recipe saved will no longer have it
        deleted_saved_recipe = models.SavedRecipes.delete().where(models.SavedRecipes.recipe == recipe_id)
        deleted_saved_recipe.execute()

        # Delete recipe in recipe table in database that matches the recipe id parameter
        deleted_recipe = models.Recipe.delete().where(models.Recipe.id == recipe_id)
        deleted_recipe.execute()

        # Redirect to the all recipes page after deleting
        return redirect(url_for('recipe'))

    # [] UNDER WHAT CONDITIONS DOES THIS REDIRECT HAPPEN?
    return redirect(url_for('recipe'))


# ====================================================================
# ==========================  Saved Recipe Routes  =========================
# ====================================================================
# Route and method to save a recipe and add it to the join table
# [] WHY ISN'T A POST REQUEST METHOD NEEDED HERE?
@app.route('/save/<recipe_id>')
@login_required
def save_to_favorite(recipe_id=None):
    # If recipe_id is provided as a parameter
    if recipe_id != None:
        # Set user variable equal to current logged in user
        user = g.user._get_current_object()
        # Find recipe in database that matches the recipe_id parameter
        recipe = models.Recipe.get(models.Recipe.id == recipe_id)

        # Create an entry in the SavedRecipes join table with user id and recipe id
        models.SavedRecipes.create(user=user.id, recipe=recipe.id)

        # Redirect to current user's profile
        return redirect(url_for('profile', username=user.username))

    # [] UNDER WHAT CONDITIONS DOES THIS REDIRECT HAPPEN?
    return redirect(url_for('recipe'))

# Route and method to remove a saved recipe from a user's favorites
@app.route('/remove/<recipe_id>', methods=['GET', 'DELETE'])
@login_required
def remove_favorite(recipe_id=None):
    # Sets user variable to current logged in user
    user = g.user._get_current_object()

    # If recipe_id parameter given
    if recipe_id != None:
        # Delete recipe in saved recipes join table that matches the current user's id AND the recipe id
        removed_recipe = models.SavedRecipes.delete().where(models.SavedRecipes.user == user.id and models.SavedRecipes.recipe == recipe_id)
        removed_recipe.execute()
        # Redirect to user's profile
        return redirect(url_for('profile', username=user.username))
    
    # [] UNDER WHAT CONDITIONS DOES THIS REDIRECT HAPPEN?
    return redirect(url_for('profile', username=user.username))



# Initialize models when running in Heroku
# if 'ON_HEROKU' in os.environ:
#     print('hitting ')
#     models.initialize()

# Initialize models when running on localhost
if __name__ == '__main__':
    models.initialize()


DEBUG = True
PORT = 8000

app.run(debug=DEBUG, port=PORT)