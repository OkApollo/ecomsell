from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_login import UserMixin

client = MongoClient("mongodb+srv://fortnitevideocreator:qZVNHnFkg7CjCvH2@cluster0.rzvnawx.mongodb.net/my_database?retryWrites=true&w=majority")
db = client.my_database
product_collection = db.Carts

class Productmodel(UserMixin):
    def __init__(self, variant, productname ,_PID=None ,price = 20):
        #_id can be considered the Cart ID or the id of the person's cart
        self._PID = _PID
        self.productname = productname
        self.price = price
        self.variant = variant
    
    def changeprices(self, _PID ,price):
        pass

    def save_to_db(self):
        user_data = {
            "productname": self.productname,
            "Variant": self.variant,
            "PID" : self.PID,
            "price": self.price
        }
        if self._PID:
            product_collection.update_one({"_PID": ObjectId(self._PID)},{"$set": user_data})
        else:
            self._PID = product_collection.insert_one(user_data).inserted_id

    def delete_from_db(self):
        if self._PID:
            product_collection.delete_one({"_PID":ObjectId(self._PID)})

    def add_to_db(variant, productname ,_PID, price):
        product = Productmodel(variant, productname ,_PID, price)
        product.save_to_db()
        return product