import os
from flask_login import UserMixin
from bson import ObjectId
from pymongo import MongoClient

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['vtu_portal']  # Replace with your database name
users_collection = db['users']


class User(UserMixin):
    def __init__(self, user_data):
        self._id = user_data['_id']
        self.id = str(user_data['_id'])
        self.email = user_data.get('email')
        self.full_name = user_data.get('full_name')
        self.phone = user_data.get('phone')
        self.role = user_data.get('role', 'user')
        self.profile_pic = user_data.get('profile_pic', 'default.jpg')  # fallback if none


    @property
    def is_admin(self):
        return self.role == "admin"

    def get_id(self):
        return self.id


# Flask-Login required loader
def load_user(user_id):
    try:
        user_data = users_collection.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(user_data)
    except Exception as e:
        print(f"[load_user error] {e}")
    return None


# ✅ Add this function to allow profile fetching
def update_user_profile_pic(user_id, file_path):
    try:
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"profile_pic": file_path}}
        )
    except Exception as e:
        print(f"[update_user_profile_pic error] {e}")

# ✅ Add this missing function
def get_user_by_id(user_id):
    try:
        return users_collection.find_one({"_id": ObjectId(user_id)})
    except Exception as e:
        print(f"[get_user_by_id error] {e}")
        return None

