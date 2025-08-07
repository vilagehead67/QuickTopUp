from bson import ObjectId
from datetime import datetime
from pymongo import ReturnDocument
from database import db

wallets_collection = db["wallets"]

class Wallet:
    @staticmethod
    def create_wallet(user_id):
        """Called after registration to initialize wallet"""
        existing = wallets_collection.find_one({"user_id": ObjectId(user_id)})
        if not existing:
            wallets_collection.insert_one({
                "user_id": ObjectId(user_id),
                "balance": 0.0,
                "created_at": datetime.utcnow()
            })

    @staticmethod
    def get_wallet(user_id):
        return wallets_collection.find_one({"user_id": ObjectId(user_id)})

    @staticmethod
    def get_balance(user_id):
        wallet = Wallet.get_wallet(user_id)
        return wallet["balance"] if wallet else 0.0

    @staticmethod
    def update_balance(user_id, amount, operation="debit"):
        """Debit or credit a user’s wallet"""
        if operation == "debit":
            update = {"$inc": {"balance": -abs(amount)}}
        elif operation == "credit":
            update = {"$inc": {"balance": abs(amount)}}
        else:
            raise ValueError("Invalid operation type. Use 'debit' or 'credit'.")

        updated_wallet = wallets_collection.find_one_and_update(
            {"user_id": ObjectId(user_id)},
            update,
            return_document=ReturnDocument.AFTER
        )
        return updated_wallet

    @staticmethod
    def set_balance(user_id, new_amount):
        """Force set balance to a specific value"""
        return wallets_collection.find_one_and_update(
            {"user_id": ObjectId(user_id)},
            {"$set": {"balance": float(new_amount)}},
            return_document=ReturnDocument.AFTER
        )

    @staticmethod
    def get_all_wallets():
        """Used in the admin dashboard to list all users’ wallets"""
        return list(wallets_collection.find())
