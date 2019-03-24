from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Regexp, ValidationError, Length, EqualTo, Email
# Imports for file/photo uploader
from flask_wtf.file import FileField, FileRequired, FileAllowed

# Imports User model
from models import User


# Defines function name_exists to check if user exists in database with same username
def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("User with this username already exists")

# Defines function email_exists to check is user exists in database with same email
def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("User with this email already exists")

# Creates a SignUpForm inheriting from Form from flask_wtf
class SignUpForm(Form):
    # Sets names of fields equal to what type of data to receive
    username = StringField(
        # Label for the field
        'Username:',
        validators=[
            # Requires user to enter something
            DataRequired(),
            # Limits characters to alphanumeric
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                         "numbers, and underscores only.")),
            # Calls previously defined function
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
            # Checks that user entered password correctly in both password fields
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
    profile_image = FileField('Profile Image')


# Creates a LoginForm class
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


# Creates an EditUserForm class
class EditUserForm(Form):
    username =  StringField('Username')
    email = StringField('Email')
    location =  StringField('Location')


# Creates a new RecipeForm
class RecipeForm(Form): 
    # SelectField makes a dropdown menu
    category = SelectField(
        'Category',
        # Provides hard-coded options
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
                # [] THIS REGEX DOESN'T WORK
                r'^[a-zA-Z]+$',
                message=('Include only one ingredient'))
        ])
    recipe_image = FileField('Recipe Image')


# Creates an EditRecipeForm class
class EditRecipeForm(Form):
    # Provides same category options as create recipe form
    category = SelectField('Category', choices=[('mexican', 'Mexican'), ('italian', 'Italian'), ('chinese', 'Chinese'), ('asian', 'Asian'), ('indian', 'Indian'), ('southern', 'Southern'), ('other', 'Other')])
    title = StringField('Title')
    content = TextAreaField('Content')
    ingredient_tag = StringField('Main Ingredient')

