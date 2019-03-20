from flask import jsonify
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
import datetime
from peewee import *

DATABASE = SqliteDatabase('hangry.db')
# inmport gravatar 
from hashlib import md5
# add this to model user for the gravatar
class User(UserMixin, Model):
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    location = TextField()
    class Meta:
        database = DATABASE
        db_table = 'user'

         # Get all recipes
    def get_recipes(self):
        return Recipe.select().where(Recipe.user == self)
    # Repr returns object so we can view it
    # def __repr__(self):
    #     return "{}, {}, {}, {}".format(
    #         self.id,
    #         self.username,
    #         self.email,
    #         self.location
    #     )
    # Sign Up POST request
    @classmethod
    def create_user(cls, username, email, password, location='sf'):
        print(location)
        try:
            cls.create(
                username = username,
                email = email,
                password = generate_password_hash(password),
                location = location)
        except IntegrityError:
            raise ValueError("create error")
class Recipe(Model):
  timestamp = DateTimeField(default=datetime.datetime.now())
  category = CharField()
  title = CharField()
  content = TextField()
  ingredient_tag = TextField()
  user = ForeignKeyField(User, backref="recipes")
  class Meta:
    database = DATABASE
    db_table = 'recipe'
    order_by = ('-timestamp',)

class SavedRecipes(Model):
    user = ForeignKeyField(User)
    recipe = ForeignKeyField(Recipe)
    timestamp = DateTimeField(default=datetime.datetime.now())
    class Meta:
        database = DATABASE
        db_table = 'savedrecipes'
        order_by = ('-timestamp',)
            
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Recipe, SavedRecipes], safe=True)
    DATABASE.close()

