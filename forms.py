from flask_wtf import FlaskForm as Form
from wtforms import TextField, TextAreaField,SubmitField

from models import user

# class UserForm(Form):
#     username = TextField("Username:", validators=[DataRequired()])
#     email = TextField("Email:", validators=[DataRequired])
#     password = TextField("Password:", validators=[DataRequired()])
#     location = TextField("Location")
#     submit = SubmitField("Create Post")

class RecipeForm(Form):
    category = TextAreaField("Category", validators=[DataRequired()])
    title = TextField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    ingredient_tag = TextField("Ingredient_tag")
    user = TextField("By:", validators=[DataRequired()])
    submit = SubmitField("Post")
