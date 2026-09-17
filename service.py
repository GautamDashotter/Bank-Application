"""
Service Layer — business logic (identical rules to the MySQL version):
- Cannot withdraw more than the current balance
- Deposit/withdraw amounts must be positive
- Every deposit/withdraw creates a transaction record

Only the Repository calls underneath changed -- these business rules
did not need to change at all when switching from MySQL to MongoDB.
"""
from pymongo.database import Database
from fastapi import HTTPException

from app.repository import UserRepository, AccountRepository, TransactionRepository
from app.models import CreateAccountRequest


class AccountService:

    @staticmethod
    def create_account(db: Database, payload: CreateAccountRequest) -> dict:
        if payload.userId is not None:
            user = UserRepository.get_by_id(db, payload.userId)
            if user is None:
                raise HTTPException(status_code=404, detail=f"User {payload.userId} not found")
        else:
            if not payload.name or not payload.email:
                raise HTTPException(
                    status_code=400,
                    detail="name and email are required when userId is not provided",
                )
            user = UserRepository.create(db, payload.name, payload.email)

        account = AccountRepository.create(db, user["_id"], user["name"], payload.accountType)
        return _to_account_response(account)

    @staticmethod
    def get_account(db: Database, account_id: int) -> dict:
        account = AccountRepository.get_by_id(db, account_id)
        if account is None:
            raise HTTPException(status_code=404, detail=f"Account {account_id} not found")
        return _to_account_response(account)

    @staticmethod
    def deposit(db: Database, account_id: int, amount: float) -> dict:
        account = AccountRepository.get_by_id(db, account_id)
        if account is None:
            raise HTTPException(status_code=404, detail=f"Account {account_id} not found")

        if amount <= 0:
            raise HTTPException(status_code=400, detail="Deposit amount must be positive")

        new_balance = account["balance"] + amount
        account = AccountRepository.update_balance(db, account_id, new_balance)

        TransactionRepository.create(db, account_id, "DEPOSIT", amount)
        return _to_account_response(account)

    @staticmethod
    def withdraw(db: Database, account_id: int, amount: float) -> dict:
        account = AccountRepository.get_by_id(db, account_id)
        if account is None:
            raise HTTPException(status_code=404, detail=f"Account {account_id} not found")

        if amount <= 0:
            raise HTTPException(status_code=400, detail="Withdrawal amount must be positive")

        if amount > account["balance"]:
            raise HTTPException(status_code=400, detail="Insufficient balance for this withdrawal")

        new_balance = account["balance"] - amount
        account = AccountRepository.update_balance(db, account_id, new_balance)

        TransactionRepository.create(db, account_id, "WITHDRAW", amount)
        return _to_account_response(account)

    @staticmethod
    def get_transactions(db: Database, account_id: int) -> list[dict]:
        account = AccountRepository.get_by_id(db, account_id)
        if account is None:
            raise HTTPException(status_code=404, detail=f"Account {account_id} not found")

        txns = TransactionRepository.get_by_account_id(db, account_id)
        return [_to_transaction_response(t) for t in txns]


def _to_account_response(doc: dict) -> dict:
    """Maps a Mongo document's `_id` field to `account_id` for the API response."""
    return {
        "account_id": doc["_id"],
        "user_id": doc["user_id"],
        "user_name": doc["user_name"],
        "balance": doc["balance"],
        "account_type": doc["account_type"],
        "created_at": doc["created_at"],
    }


def _to_transaction_response(doc: dict) -> dict:
    return {
        "txn_id": doc["_id"],
        "account_id": doc["account_id"],
        "txn_type": doc["txn_type"],
        "amount": doc["amount"],
        "created_at": doc["created_at"],
    }
