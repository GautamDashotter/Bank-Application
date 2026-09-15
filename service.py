"""
Service Layer — business logic lives here.

This is the layer that enforces the project's business rules:
- Cannot withdraw more than the current balance
- Deposit amount must be positive (also enforced at the request-model level via Field(gt=0))
- Every deposit/withdraw creates a transaction record

Keeping this logic separate from the Controller (API routes) and Repository
(data access) means we can swap the data store (Day 2: real MySQL via a
Repository layer) without touching this business logic at all.
"""
from datetime import datetime, timezone
from fastapi import HTTPException

import store
from models import User, Account, Transaction, CreateAccountRequest


class AccountService:

    @staticmethod
    def create_account(payload: CreateAccountRequest) -> Account:
        # Resolve the user: reuse an existing user_id, or create a new user
        if payload.userId is not None:
            user = store.users.get(payload.userId)
            if user is None:
                raise HTTPException(status_code=404, detail=f"User {payload.userId} not found")
        else:
            if not payload.name or not payload.email:
                raise HTTPException(
                    status_code=400,
                    detail="name and email are required when userId is not provided",
                )
            user = User(
                user_id=store.next_user_id(),
                name=payload.name,
                email=payload.email,
                created_at=datetime.now(timezone.utc),
            )
            store.users[user.user_id] = user

        account = Account(
            account_id=store.next_account_id(),
            user_id=user.user_id,
            user_name=user.name,
            balance=0.0,
            account_type=payload.accountType,
            created_at=datetime.now(timezone.utc),
        )
        store.accounts[account.account_id] = account
        return account

    @staticmethod
    def get_account(account_id: int) -> Account:
        account = store.accounts.get(account_id)
        if account is None:
            raise HTTPException(status_code=404, detail=f"Account {account_id} not found")
        return account

    @staticmethod
    def deposit(account_id: int, amount: float) -> Account:
        account = AccountService.get_account(account_id)

        if amount <= 0:
            raise HTTPException(status_code=400, detail="Deposit amount must be positive")

        account.balance += amount
        store.accounts[account_id] = account

        AccountService._record_transaction(account_id, "DEPOSIT", amount)
        return account

    @staticmethod
    def withdraw(account_id: int, amount: float) -> Account:
        account = AccountService.get_account(account_id)

        if amount <= 0:
            raise HTTPException(status_code=400, detail="Withdrawal amount must be positive")

        if amount > account.balance:
            raise HTTPException(status_code=400, detail="Insufficient balance for this withdrawal")

        account.balance -= amount
        store.accounts[account_id] = account

        AccountService._record_transaction(account_id, "WITHDRAW", amount)
        return account

    @staticmethod
    def get_transactions(account_id: int) -> list[Transaction]:
        # Confirm the account exists first, for a clean 404 rather than an empty list
        AccountService.get_account(account_id)

        return [
            txn for txn in store.transactions.values()
            if txn.account_id == account_id
        ]

    @staticmethod
    def _record_transaction(account_id: int, txn_type: str, amount: float) -> Transaction:
        txn = Transaction(
            txn_id=store.next_txn_id(),
            account_id=account_id,
            txn_type=txn_type,
            amount=amount,
            created_at=datetime.now(timezone.utc),
        )
        store.transactions[txn.txn_id] = txn
        return txn
