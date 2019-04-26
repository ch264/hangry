# Imports
import os, datetime
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

from peewee import *

# To connect to postgres on heroku
from playhouse.db_url import connect

# Sets DATABASE variable for development
DATABASE = SqliteDatabase('hangry.db')

# Sets DATABASE variable for production
# DATABASE = PostgresqlDatabase('hangry')

# Sets DATABASE variable for deployment on Heroku
# DATABASE = connect(os.environ.get('DATABASE_URL'))


# Creates User class for User table in database
class User(UserMixin, Model):
    # Sets column names and data types
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    location = TextField()
    # image_filename = CharField()
    # image_url = CharField() 
    
    # Sets which database to connect to
    # Sets which table to access
    class Meta:
        database = DATABASE
        db_table = 'user'

    # Function to create an entry in User table
    @classmethod
    # def create_user(cls, username, email, password, location, image_filename, image_url):
    def create_user(cls, username, email, password, location):
        try:
            cls.create(
                # Set column values to parameters passed into method
                username = username,
                email = email,
                password = generate_password_hash(password),
                location = location,
                # image_filename = image_filename,
                # image_url = image_url
                )
        except IntegrityError:
            raise ValueError("create error")


# Creates Recipe class for Recipe table in database
class Recipe(Model):
    # Sets column names and data types
    # Sets timestamp to time when entry is created
    timestamp = DateTimeField(default=datetime.datetime.now())
    category = CharField()
    title = CharField()
    content = TextField()
    ingredient_tag = TextField()
    # Sets user column to expect a foreign key (user id of who created a recipe)
    user = ForeignKeyField(User, backref="recipes")
    # image_filename = CharField()
    # image_url = CharField()

    # Sets which database to connect to
    # Sets which table to access
    class Meta:
        database = DATABASE
        db_table = 'recipe'

    # Defines function create_recipe to create an entry in Recipe table
    @classmethod
    # def create_recipe(cls, category, title, content, ingredient_tag, user, image_filename, image_url):
    def create_recipe(cls, category, title, content, ingredient_tag, user):
        try:
            cls.create(
                category = category,
                title = title,
                content = content,
                ingredient_tag = ingredient_tag,
                user = user,
                # image_filename = image_filename,
                # image_url = image_url
                )
        except IntegrityError:
            raise ValueError("create recipe error")


# Creates SavedRecipe class for SavedRecipes table in database
class SavedRecipes(Model):
    # Sets user column to expect a foreign key (user id of who saved a recipe)

    user = ForeignKeyField(User)
    # Sets recipe column to expect a foreign key (recipe id)
    recipe = ForeignKeyField(Recipe)
    # Sets timestamp column to time when user saves a recipe
    timestamp = DateTimeField(default=datetime.datetime.now())

    # Sets which database to connect to
    # Sets which table to access
    class Meta:
        database = DATABASE
        db_table = 'savedrecipes'
            

# Defines initialize function to connect to database, create empty tables, and close connection
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Recipe, SavedRecipes], safe=True)
    DATABASE.close()

