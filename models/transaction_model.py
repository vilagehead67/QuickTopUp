from database import transactions_collection
from bson import ObjectId
import datetime

class AirtimeTransaction:
    def __init__(self, phone_number, amount, network, request_id, status, timestamp=None):
        self.phone_number = phone_number
        self.amount = amount
        self.network = network
        self.request_id = request_id
        self.status = status
        self.timestamp = timestamp or datetime.datetime.utcnow()

    def to_dict(self):
        return {
            "phone_number": self.phone_number,
            "amount": self.amount,
            "network": self.network,
            "request_id": self.request_id,
            "status": self.status,
            "timestamp": self.timestamp
        }

    def save(self):
        transactions_collection.insert_one(self.to_dict())

    @staticmethod
    def get_all():
        return list(transactions_collection.find({"plan": {"$exists": False}}))  # only airtime

    @staticmethod
    def get_by_id(transaction_id):
        return transactions_collection.find_one({"_id": ObjectId(transaction_id)})


class DataTransaction:
    def __init__(self, phone_number, amount, network, plan, request_id, status, timestamp=None):
        self.phone_number = phone_number
        self.amount = amount
        self.network = network
        self.plan = plan
        self.request_id = request_id
        self.status = status
        self.timestamp = timestamp or datetime.datetime.utcnow()

    def to_dict(self):
        return {
            "phone_number": self.phone_number,
            "amount": self.amount,
            "network": self.network,
            "plan": self.plan,
            "request_id": self.request_id,
            "status": self.status,
            "timestamp": self.timestamp
        }

    def save(self):
        transactions_collection.insert_one(self.to_dict())

    @staticmethod
    def get_all():
        return list(transactions_collection.find({"plan": {"$exists": True}}))

    @staticmethod
    def get_by_id(transaction_id):
        return transactions_collection.find_one({"_id": ObjectId(transaction_id)})


def record_transaction(user_id, amount, txn_type, status, reference, extra_data=None):
    transaction = {
        "user_id": user_id,
        "amount": amount,
        "type": txn_type,
        "status": status,
        "reference": reference,
        "timestamp": datetime.datetime.utcnow()
    }
    if extra_data and isinstance(extra_data, dict):
        transaction.update(extra_data)

    transactions_collection.insert_one(transaction)


def get_user_transactions(user_id, txn_type=None):
    query = {"user_id": user_id}
    if txn_type:
        query["type"] = txn_type
    return list(transactions_collection.find(query).sort("timestamp", -1))
