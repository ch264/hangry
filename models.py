from flask import jsonify
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
import datetime
from peewee import *

DATABASE = SqliteDatabase('hangry.db')

from hashlib import md5


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    location = TextField()
    image_filename = CharField()
    image_url = CharField()
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
    def create_user(cls, username, email, password, location, image_filename, image_url):
        # print(location)
        try:
            cls.create(
                username = username,
                email = email,
                password = generate_password_hash(password),
                location = location,
                image_filename = image_filename,
                image_url = image_url)
        except IntegrityError:
            raise ValueError("create error")

    def edit_user(cls, username, email, password, location):
        # print(location)
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
    image_filename = CharField()
    image_url = CharField()
    class Meta:
        database = DATABASE
        db_table = 'recipe'
        order_by = ('-timestamp',)

    @classmethod
    def create_recipe(cls, category, title, content, ingredient_tag, user, image_filename, image_url):
        # print(location)
        try:
            cls.create(
                category = category,
                title = title,
                content = content,
                ingredient_tag = ingredient_tag,
                user = user,
                image_filename = image_filename,
                image_url = image_url)
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

