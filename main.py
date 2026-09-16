"""
Controller Layer — REST API routes (FastAPI).

Endpoints match the project spec exactly:
  POST   /api/accounts                    -> create account
  GET    /api/accounts/{id}                -> get account details
  POST   /api/accounts/{id}/deposit         -> deposit money
  POST   /api/accounts/{id}/withdraw        -> withdraw money
  GET    /api/accounts/{id}/transactions    -> transaction history

Day 1 uses in-memory storage (see app/store.py). Day 2 swaps this for
MySQL via a Repository layer, without changing these routes or the
Service layer's public interface.
"""
from fastapi import FastAPI, status

from app.models import (
    CreateAccountRequest,
    DepositRequest,
    WithdrawRequest,
    Account,
    Transaction,
)
from app.service import AccountService

app = FastAPI(
    title="Simple Bank API (No DB)",
    description="Day 1: REST API using in-memory storage",
    version="1.0.0",
)


@app.post("/api/accounts", response_model=Account, status_code=status.HTTP_201_CREATED)
def create_account(payload: CreateAccountRequest):
    """Create a new account (and a new user, if userId is not supplied)."""
    return AccountService.create_account(payload)


@app.get("/api/accounts/{account_id}", response_model=Account)
def get_account(account_id: int):
    """Get account details by ID."""
    return AccountService.get_account(account_id)


@app.post("/api/accounts/{account_id}/deposit", response_model=Account)
def deposit(account_id: int, payload: DepositRequest):
    """Deposit money into an account."""
    return AccountService.deposit(account_id, payload.amount)


@app.post("/api/accounts/{account_id}/withdraw", response_model=Account)
def withdraw(account_id: int, payload: WithdrawRequest):
    """Withdraw money from an account. Rejects withdrawals exceeding the balance."""
    return AccountService.withdraw(account_id, payload.amount)


@app.get("/api/accounts/{account_id}/transactions", response_model=list[Transaction])
def get_transactions(account_id: int):
    """View transaction history for an account."""
    return AccountService.get_transactions(account_id)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Simple Bank API (No DB)"}
