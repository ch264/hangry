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
        db_table = 'user'

    # Sign Up POST request
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

 
    
class Recipe(Model):
  timestamp = DateTimeField(default=datetime.datetime.now)
  category = CharField()
  title = CharField()
  content = TextField()
  ingredient_tag = TextField()
  user = ForeignKeyField(User, backref="profile")
  class Meta:
    database = DATABASE
    db_table = 'recipe'
    order_by = ('-timestamp',)

class SavedRecipes(Model):
    user = ForeignKeyField(User)
    recipe = ForeignKeyField(Recipe)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        db_table = 'savedrecipes'
        order_by = ('-timestamp',)
            
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Recipe, SavedRecipes], safe=True)
    DATABASE.close()

if __name__ == 'models':
    db.create_all()
