import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

DEBUG = True
PORT = 8000

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.hangry')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
marshmallow = Marshmallow(app)









@app.route('/')
def hello_world():
    return 'Hello World'


if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)