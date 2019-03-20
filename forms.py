from flask_wtf import FlaskForm as Form
from wtforms import TextField, TextAreaField, SubmitField, StringField, PasswordField

# from models import user

class UserForm(Form):
    username = TextField("Username:")
    email = TextField()
    password = TextField()
    location = TextField("Location")
    # submit = SubmitField("Create Post")

class LoginForm(Form):
    email = StringField('Email')
    password = PasswordField('Password')


class RecipeForm(Form):
    timestamp = TextField("Timestamp")
    category = TextAreaField("Content")
    title = TextField("Title")
    content = TextAreaField("Content")
    ingredient_tag = TextField("Ingredient_tag")
    user = TextField("By:")


class SavedRecipesForm(Form):
    user = TextField("By:")
    recipe = TextAreaField("Content")
    timestamp = TextField("Timestamp")