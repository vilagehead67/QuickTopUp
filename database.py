import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

# Get Mongo URI and DB Name
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

if not MONGO_URI or not MONGO_DB_NAME:
    raise Exception("MONGO_URI or MONGO_DB_NAME is not set in your .env file")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

# Collections
users_collection = db["users"]
wallets_collection = db["wallets"]
transactions_collection = db["transactions"]  # For AirtimeTransaction
