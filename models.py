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
    def create_user(cls, username, email, password, location):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password),
                location=location)
        except IntegrityError:
            raise ValueError("User already exists")

    @classmethod
    def login_user(cls, email, password):
        try:
            cls.login(
                email=email,
                password=generate_password_hash(password)
            )
        except IntegrityError:
            raise ValueError("Invalid email/password")

