from app import db
from flask import jsonify
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
import datetime
from peewee import *

DATABASE = SqliteDatabase('hangry.db')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    location = TextField(max_length=100)
    class Meta:
        database = DATABASE
        
    @classmethod
    def signup(cls, username, email, password, location):
        try:
            cls.create(
                username = username,
                email = email,
                password = generate_password_hash(password),
                location = location)
        except IntegrityError:
            raise ValueError("User already exists")

    @classmethod
    def login(cls, email, password):
        try:
            cls.select(
                email = email,
                password = generate_password_hash(password)
            )
        except IntegrityError:
            raise ValueError("Invalid email/password")

    @classmethod
    def get_profile(cls, username, email, location):
        try:
            cls.select(
                username=username,
                email=email,
                location = location)
        except IntegrityError:
            raise ValueError("Profile unavailable")

    @classmethod
    def update_profile(cls, username, email, location):
        try:
            cls.update(
                username = username,
                email = email,
                location = location)
        except IntegrityError:
            raise ValueError("Sorry, we can't update your profile!")

class Recipe(Model):
  timestamp = DateTimeField(default=datetime.datetime.now)
  category = CharField()
  title = CharField()
  content = TextField()
  ingredient_tag = TextField()
  user = ForeignKeyField(User, backref="profile")
  
  class Meta:
    database = DATABASE
    order_by = ('-timestamp',)

    @classmethod
    def create_recipe(cls, category, title, content, ingredient_tag, user):
        try:
            cls.create(
                category = category,
                title = title,
                content = content,
                ingredient_tag = ingredient_tag,
                user = user)
        except IntegrityError:
            raise ValueError("Currently can't create recipe. Try again.")

    @classmethod
    def edit_recipe(cls, category, title, content, ingredient_tag,user):
        try:
            cls.update(
                category = category,
                title = title,
                content =content,
                ingredient_tag=ingredient_tag
                user=user)
        except IntegrityError:
            raise ValueError("Currently can't edit recipe. Try again.")
    
    # @classmethod
    # def delete_recipe(cls)
    #     try:
    #         cls.delete()
    #     except IntegrityError:
    #         raise ValueError("Could not delete")

# References User and Recipe
class SavedRecipes(Model):
    user = ForeignKeyField(User)
    recipe = ForeignKeyField(Recipe)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
    database = DATABASE
    order_by = ('-timestamp',)


            
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Recipe], safe=True)
    DATABASE.close()
  
    




if __name__ == 'models':
    db.create_all()
