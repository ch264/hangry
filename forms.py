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

<<<<<<< HEAD
# class UserForm(Form):
#     username = TextField("Username:", validators=[DataRequired()])
#     email = TextField("Email:", validators=[DataRequired])
#     password = TextField("Password:", validators=[DataRequired()])
#     location = TextField("Location")
#     submit = SubmitField("Create Post")
=======
>>>>>>> dbb142e639e2c23428c5d05af598d140fc494469

class RecipeForm(Form):
    category = TextAreaField("Category", validators=[DataRequired()])
    title = TextField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    ingredient_tag = TextField("Ingredient_tag")
    user = TextField("By:", validators=[DataRequired()])
    submit = SubmitField("Post")
