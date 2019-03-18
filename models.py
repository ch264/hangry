from app import db, marshmallow
from flask import jsonify



if __name__ == 'models':
    db.create_all()
