from flask_login import UserMixin
from lazyAPI import bcrypt
from lazyAPI import mongo

class User(UserMixin):
    def __init__(self, id, phash):
        self.id = id
        self.phash = phash

    @staticmethod
    def load(id):
        userdata = mongo.db['users'].find_one({"_id": id})
        print('test', userdata['_id'])
        print(userdata['phash'])
        return User(id, userdata['phash'])

    def get_id(self):
        return self.id

    def check_password(self, password):
        return bcrypt.check_password_hash(self.phash, password)

    # Class method for getting password hash
    @staticmethod
    def get_phash(password):
        return bcrypt.generate_password_hash(password)

    def is_anonymous(self):
        return False
