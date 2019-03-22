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

# foto uploader via form field
from flask import url_for, redirect, render_template
from flask_wtf import Form
from flask_wtf.file import FileField
from werkzeug import secure_filename

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

from flask_wtf.csrf import CSRFProtect

# ////////////////////////////////////////////////////

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



# def allowed_file(filename):
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = forms.UploadForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(str(current_user.username) + '.' + 'jpg' )
        f.save(os.path.join(
            app.instance_path, 'uploads', filename
        ))
        
        # filename = secure_filename(f.filename)
        # form.file.data.save('uploads')
        # return redirect(url_for('upload'))
    return render_template('upload.html', form=form)
    

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


@app.route('/profile/<username>', methods=['GET'])
def profile(username=None):
    if username != None and request.method == 'GET':
        user = models.User.select().where(models.User.username==username).get()
        recipes = models.Recipe.select().where(models.Recipe.user == user.id)

        # saved_recipes = models.SavedRecipes.select().where(models.SavedRecipes.user == user.id)
        Owner = user.alias()
        saved_recipes = (models.SavedRecipes.select(models.SavedRecipes, models.Recipe.title, models.Recipe.id, models.User.username, Owner.username)
        .join(Owner) 
        .switch(models.SavedRecipes)
        .join(models.Recipe)  
        .join(models.User))

        return render_template('profile.html', user=user, recipes=recipes, saved_recipes=saved_recipes)

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
        return redirect(url_for('profile', username=user.username))
    return render_template('edit-profile.html', form=form, user=user)


@app.route('/recipe', methods=['GET'])
<<<<<<< HEAD
@app.route('/recipe/<recipe_id>', methods=['GET', 'PUT'])
def recipe(recipe_id=None):
    if recipe_id != None and request.method == 'GET':
        recipe = models.Recipe.select().where(models.Recipe.id == recipe_id).get()
        return render_template('recipe.html', recipe=recipe)
    recipes = models.Recipe.select().limit(20)
    return render_template('recipes.html', recipes=recipes)

=======
@app.route('/recipe/<recipe_id>', methods=['GET'])
@login_required
def post(recipe_id=None):
    form = forms.RecipeForm()
    if recipe_id != None and request.method == 'GET':
        return render_template('recipe.html')
    # if form.validate_on_submit():
    #     flash("Recipe Created!", "success") 
    #     models.Recipe.create(
    #         user=g.user._get_current_object(), #create new post.
    #         content=form.content.data.strip()) 
        

    #     return redirect(url_for('index')) #redirect user
    return render_template('recipes.html', form=form)
#  will change 
        # else: 
        #     user = models.Recipe.select().where(models.Recipe.title == title).get()
        #     user.delete_instance()
        #     return repr(user)


# [] TEMPORARY ROUTE
>>>>>>> ca401f7908a36e50b7056aa395ba5556f1d64034
@app.route('/create-recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = forms.RecipeForm()
    if request.method == 'POST':
        models.Recipe.create(
            category = form.category.data, #SelectField -use form instead of json
            title = form.title.data,
            content = form.content.data,
            ingredient_tag = form.ingredient_tag.data,
            user = g.user._get_current_object())
<<<<<<< HEAD
        recipe = models.Recipe.get(models.Recipe.title == form.title.data)
        return redirect(url_for('recipe', recipe_id=recipe.id))
    else:
        return render_template('create-recipe.html', form=form)

@app.route('/edit-recipe/<recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id=None):
    recipe = models.Recipe.select().where(models.Recipe.id == recipe_id).get()
    form = forms.EditRecipeForm()
    if form.validate_on_submit():
        recipe.category = form.category.data
        recipe.title = form.title.data
        recipe.content = form.content.data
        recipe.ingredient_tag = form.ingredient_tag.data
        recipe.save()
        flash('Your recipe has been saved.')

        return redirect(url_for('recipe', recipe_id=recipe.id))
    return render_template('edit-recipe.html', form=form, recipe=recipe)

@app.route('/delete-recipe/<recipe_id>', methods=['GET', 'DELETE'])
@login_required
def delete_recipe(recipe_id=None):
    if recipe_id != None:
        deleted_saved_recipe = models.SavedRecipes.delete().where(models.SavedRecipes.recipe == recipe_id)
        deleted_saved_recipe.execute()
        deleted_recipe = models.Recipe.delete().where(models.Recipe.id == recipe_id)
        deleted_recipe.execute()
        return redirect(url_for('recipe'))
    
    return redirect(url_for('recipe', recipe_id=recipe_id))

# create a route to add data to join table
@app.route('/save/<recipe_id>')
def save_to_favorite(recipe_id=None):
    user = g.user._get_current_object()
    recipe = models.Recipe.get(models.Recipe.id == recipe_id)

    models.SavedRecipes.create(user=user.id, recipe=recipe.id)

    return redirect(url_for('recipe'))

@app.route('/remove/<recipe_id>', methods=['GET', 'DELETE'])
@login_required
def remove_favorite(recipe_id=None):
    user = g.user._get_current_object()

    if recipe_id != None:
        removed_recipe = models.SavedRecipes.delete().where(models.SavedRecipes.user == user.id and models.SavedRecipes.recipe == recipe_id)
        removed_recipe.execute()
        return redirect(url_for('profile', username=user.username))
     
    return redirect(url_for('profile', username=user.username))


=======
        return redirect(url_for('profile.html', form=form)
    return redirect(url_for('create-recipe.html', form=form)
        
>>>>>>> ca401f7908a36e50b7056aa395ba5556f1d64034

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
        ingredient_tag="Pork",
        user = 1
        ),
        models.Recipe.create_recipe(
        category='Italian',
        title="Spaghetti",
        content='Yummy Pasta',
<<<<<<< HEAD
        ingredient_tag="Noodles",
=======
        ingredient_tag="Pasta",
>>>>>>> ca401f7908a36e50b7056aa395ba5556f1d64034
        user = 2
        ),
        models.Recipe.create_recipe(
        category='Mexican',
        title="Enchaladas",
        content='Quick and easy',
        ingredient_tag="Meat",
        user = 3
        ),
        models.Recipe.create_recipe(
        category='Chinese',
        title="Orange Chicken",
<<<<<<< HEAD
        content='Fiery. Hot. Nice.',
=======
        content='Crispy Chicken',
>>>>>>> ca401f7908a36e50b7056aa395ba5556f1d64034
        ingredient_tag="Chicken",
        user = 3
        ),
        models.Recipe.create_recipe(
        category='Indian',
        title="Tofu Tikka Marsala",
        content='Taste Authentic',
<<<<<<< HEAD
        ingredient_tag="Sauce",
=======
        ingredient_tag="Tikka Marsala.",
>>>>>>> ca401f7908a36e50b7056aa395ba5556f1d64034
        user = 2
        ),
        models.Recipe.create_recipe(
        category='Southern',
        title="Gumbo",
        content='Simple and Quick',
<<<<<<< HEAD
        ingredient_tag="Seafood",
        user = 4
=======
        ingredient_tag="Meat",
        user = 1
>>>>>>> ca401f7908a36e50b7056aa395ba5556f1d64034
        )

    
    
    
    except ValueError:
        pass

app.run(debug=DEBUG, port=PORT)