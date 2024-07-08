from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_login import UserMixin

client = MongoClient("mongodb+srv://fortnitevideocreator:qZVNHnFkg7CjCvH2@cluster0.rzvnawx.mongodb.net/my_database?retryWrites=true&w=majority")
db = client.my_database
address_collection = db.Addresses

class addressModel(UserMixin):
    def __init__(self, user_id, country, city, zipcode, notes ,_id=None):
        self.user_id = user_id
        self.country = country
        self.city = city
        self.zipcode = zipcode
        self.notes = notes
        self._id = _id

    @staticmethod
    def find_by_user(u_id):
        addresses = address_collection.find({"user_id": u_id})
        return [addressModel(
            user_id=address["user_id"],
            country=address["country"],
            city=address["city"],
            zipcode=address["zipcode"],
            notes = address["notes"],
            _id=address["_id"]
        ) for address in addresses]

    @staticmethod
    def get_from_id(unique_address_id):
        address = address_collection.find_one({"_id": ObjectId(unique_address_id)})
        if address:
            return addressModel(
                user_id=address["user_id"],
                country=address["country"],
                city=address["city"],
                zipcode=address["zipcode"],
                notes= address["notes"],
                _id=address["_id"]
            )
        return None

    def save_to_db(self):
        user_data = {
            "user_id": self.user_id,
            "country": self.country,
            "city": self.city,
            "zipcode": self.zipcode,
            "notes": self.notes
        }
        if self._id:
            address_collection.update_one(
                {"_id": ObjectId(self._id)},
                {"$set": user_data}
            )
        else:
            self._id = address_collection.insert_one(user_data).inserted_id

    def delete_from_db(self):
        if self._id:
            address_collection.delete_one({"_id": ObjectId(self._id)})

    @staticmethod
    def create_address(user_id, country, city, zipcode, notes):
        address = addressModel(user_id, country, city, zipcode, notes)
        address.save_to_db()
        return address
