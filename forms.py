from flask_wtf import FlaskForm as Form
from models import User, Recipe
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Regexp, ValidationError, Length, EqualTo, Email

from flask_wtf.file import FileField, FileRequired

class UploadForm(Form):
    file = FileField(validators=[FileRequired()])

def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("User with this username already exists")

def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("User with this email already exists")

class SignUpForm(Form):
    username = StringField(
        'Username:',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                         "numbers, and underscores only.")),
            name_exists
        ])
    email = StringField(
        'Email:',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password:',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()
        ])
    location = StringField(
        'Location',
        validators=[
            DataRequired()
        ])
   

class LoginForm(Form):
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RecipeForm(Form):
    category = SelectField("Category", choices=[('mexican', 'Mexican'), ('italian', 'Italian'), ('chinese', 'Chinese'), ('asian', 'Asian'), ('indian', 'Indian'), ('southern', 'Southern'), ('other', 'Other')])
    title = StringField("Title")
    content = TextAreaField("Ingredients and Instructions")
    ingredient_tag = StringField("Main Ingredient")

class EditRecipeForm(Form):
    category = SelectField("Category", choices=[('mexican', 'Mexican'), ('italian', 'Italian'), ('chinese', 'Chinese'), ('asian', 'Asian'), ('indian', 'Indian'), ('southern', 'Southern'), ('other', 'Other')])
    title = StringField("Title")
    content = TextAreaField("Content")
    ingredient_tag = StringField("Ingredient_tag")

class EditUserForm(Form):
    username =  StringField("Username")
    email = StringField("Email")
    # password = PasswordField("Password")
    location =  StringField("Location")
    file = FileField(validators=[FileRequired()])
    
