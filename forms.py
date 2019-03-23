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
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ])
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
        )


class EditUserForm(Form):
    username =  StringField('Username')
    email = StringField('Email')
    location =  StringField('Location')
    

class RecipeForm(Form):
    category = SelectField(
        'Category',
        choices=[('mexican', 'Mexican'), ('italian', 'Italian'), ('chinese', 'Chinese'), ('asian', 'Asian'), ('indian', 'Indian'), ('southern', 'Southern'), ('other', 'Other')],
        validators=[DataRequired()]
        )
    title = StringField(
        'Title',
        validators=[DataRequired()]
        )
    content = TextAreaField(
        'Ingredients and Instructions',
        validators=[DataRequired()]
        )
    ingredient_tag = StringField(
        'Main Ingredient',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z]+$',
                message=('Include only one ingredient')),
        ])

class EditRecipeForm(Form):
    category = SelectField('Category', choices=[('mexican', 'Mexican'), ('italian', 'Italian'), ('chinese', 'Chinese'), ('asian', 'Asian'), ('indian', 'Indian'), ('southern', 'Southern'), ('other', 'Other')])
    title = StringField('Title')
    content = TextAreaField(
        'Content',
        validators=[DataRequired()])
    ingredient_tag = StringField(
        'Ingredient_tag',
        validators=[
            Regexp(
                r'^[a-zA-Z]+$',
                message=('Include only one ingredient'))
        ])

