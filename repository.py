"""
Repository Layer — all direct database access lives here (MongoDB version).

Instead of SQL queries against tables with foreign keys, MongoDB stores
each entity as a flexible JSON-like "document" in a "collection". There's
no built-in relationship enforcement -- we look up related documents
manually where needed (e.g. fetching a user's name when creating an account).
"""
from datetime import datetime, timezone
from pymongo.database import Database

from app.counters import get_next_sequence


class UserRepository:

    @staticmethod
    def get_by_id(db: Database, user_id: int) -> dict | None:
        return db["users"].find_one({"_id": user_id})

    @staticmethod
    def create(db: Database, name: str, email: str) -> dict:
        user_id = get_next_sequence(db, "user_id")
        user_doc = {
            "_id": user_id,
            "name": name,
            "email": email,
            "created_at": datetime.now(timezone.utc),
        }
        db["users"].insert_one(user_doc)
        return user_doc


class AccountRepository:

    @staticmethod
    def get_by_id(db: Database, account_id: int) -> dict | None:
        return db["accounts"].find_one({"_id": account_id})

    @staticmethod
    def create(db: Database, user_id: int, user_name: str, account_type: str) -> dict:
        account_id = get_next_sequence(db, "account_id")
        account_doc = {
            "_id": account_id,
            "user_id": user_id,
            "user_name": user_name,  # denormalized (embedded) so we don't need a join/lookup on every read
            "balance": 0.0,
            "account_type": account_type,
            "created_at": datetime.now(timezone.utc),
        }
        db["accounts"].insert_one(account_doc)
        return account_doc

    @staticmethod
    def update_balance(db: Database, account_id: int, new_balance: float) -> dict:
        db["accounts"].update_one(
            {"_id": account_id},
            {"$set": {"balance": new_balance}},
        )
        return AccountRepository.get_by_id(db, account_id)


class TransactionRepository:

    @staticmethod
    def create(db: Database, account_id: int, txn_type: str, amount: float) -> dict:
        txn_id = get_next_sequence(db, "txn_id")
        txn_doc = {
            "_id": txn_id,
            "account_id": account_id,
            "txn_type": txn_type,
            "amount": amount,
            "created_at": datetime.now(timezone.utc),
        }
        db["transactions"].insert_one(txn_doc)
        return txn_doc

    @staticmethod
    def get_by_account_id(db: Database, account_id: int) -> list[dict]:
        cursor = db["transactions"].find({"account_id": account_id}).sort("created_at", 1)
        return list(cursor)
