from app import db, marshmallow
from flask import jsonify

# inmport gravatar 
from hashlib import md5

# add this to model user for the gravatar
class User(UserMixin, db.Model):
    # ...
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)



if __name__ == 'models':
    db.create_all()
