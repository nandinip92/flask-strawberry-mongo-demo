from bson.objectid import ObjectId
from database import db

users_collection = db["usersData"]

def get_all_users():
    return list(users_collection.find())

def get_user_by_id(user_id):
    return users_collection.find_one({"_id": ObjectId(user_id)})

def add_user(name, email):
    result = users_collection.insert_one({"name":name, "email":email})
    return users_collection.find_one({"_id": result.inserted_id})

def delete_user(user_id):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count>0