from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_login import UserMixin

client = MongoClient("mongodb+srv://fortnitevideocreator:qZVNHnFkg7CjCvH2@cluster0.rzvnawx.mongodb.net/my_database?retryWrites=true&w=majority")
db = client.my_database
product_collection = db.Products

class productmodel(UserMixin):
    def __init__(self, variant, productname, pictureid , price = 20, _id = None):
        #_id can be considered the Cart ID or the id of the person's cart
        self._id = _id
        self.productname = productname
        self.price = price
        self.variant = variant
        self.pictureid = pictureid
    
    def get_all_products():
        return product_collection.find({})
            
    def get_by_id(_id):
        product = product_collection.find_one({"_id":_id})
    
    def changeprices(self, _id ,price):
        pass

    def save_to_db(self):
        product_data = {
            "productname": self.productname,
            "Variant": self.variant,
            "pictureid":self.pictureid,
            "price": self.price
        }
        if self._id:
            product_collection.update_one({"_id": self._id},{"$set": product_data})
            print("Updated")
        else:
            self._id = product_collection.insert_one(product_data).inserted_id
            print("Saved")

    def delete_from_db(_id):
        if _id:
            product_collection.delete_one({"_id":ObjectId(_id)})

    def add_to_db(variant, productname , pictureid , price):
        product = productmodel(variant, productname , pictureid , price)
        product.save_to_db()
        return product