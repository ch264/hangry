import os
from flask import jsonify
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
import datetime
from peewee import *

# To connect to postgres on heroku
from playhouse.db_url import connect

# Sets DATABASE variable for development
DATABASE = SqliteDatabase('hangry.db')

# Sets DATABASE variable for production
# DATABASE = PostgresqlDatabase('hangry')

# Sets DATABASE variable for deployment on Heroku
# DATABASE = connect(os.environ.get('DATABASE_URL'))


# inmport gravatar 
from hashlib import md5
# add this to model user for the gravatar
# class User(UserMixin, Model):
#     def avatar(self, size):
#         digest = md5(self.email.lower().encode('utf-8')).hexdigest()
#         return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
#             digest, size)

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

    # Sign Up POST request
    @classmethod
    def create_user(cls, username, email, password, location):
        try:
            cls.create(
                username = username,
                email = email,
                password = generate_password_hash(password),
                location = location)
        except IntegrityError:
            raise ValueError("create error")

    @classmethod
    def edit_user(cls, username, email, password, location):
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

    @classmethod
    def create_recipe(cls, category, title, content, ingredient_tag, user):
        try:
            cls.create(
                category = category,
                title = title,
                content = content,
                ingredient_tag = ingredient_tag,
                user = user
                )
        except IntegrityError:
            raise ValueError("create recipe error")

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

