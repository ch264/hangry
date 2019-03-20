from flask_wtf import FlaskForm as Form
from models import User, Recipe
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Regexp, ValidationError, Length, EqualTo, Email

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
            DataRequired(),
        ])

class LoginForm(Form):
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])



class RecipeForm(Form):
    category = TextAreaField("Content")
    title = StringField("Title")
    content = TextAreaField("Content")
    ingredient_tag = StringField("Ingredient_tag")

    # Edit User
    # Edit Recipe
    
