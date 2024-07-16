from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt
from flask_login import UserMixin

client = MongoClient("mongodb+srv://fortnitevideocreator:qZVNHnFkg7CjCvH2@cluster0.rzvnawx.mongodb.net/my_database?retryWrites=true&w=majority")
db = client.my_database
users_collection = db.new_collection

class userModel(UserMixin):
    def __init__(self, username, email, password_hash, userrole=2 ,_id=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.userrole = userrole
        self._id = _id

    def get_id(self):
        return str(self._id)

    @staticmethod
    def get(user_id):
        user_data = users_collection.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return userModel(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=user_data['password_hash'],
                _id=user_data['_id']
            )
        return None

    @staticmethod
    def find_by_email(email):
        user_data = users_collection.find_one({"email": email})
        if user_data:
            return userModel(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=user_data['password_hash'],
                _id=user_data['_id']
            )
        return None

    def save_to_db(self):
        user_data = {
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash
        }
        if self._id:
            users_collection.update_one({"_id": ObjectId(self._id)}, {"$set": user_data})
        else:
            self._id = users_collection.insert_one(user_data).inserted_id

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

    # def update_name(self,name):
    #     user_data = users_collection.find_one({"_id": ObjectId(self._id)})
    #     users_collection.update_one({"_id": ObjectId(self._id)},{"$username": name}, {"$set": user_data})


    @staticmethod
    def create_user(username, email, password):
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = userModel(username, email, password_hash)
        new_user.save_to_db()
        return new_user
