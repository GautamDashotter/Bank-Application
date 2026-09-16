"""
Controller Layer — REST API routes (FastAPI), now backed by MongoDB Atlas.

Same endpoints and same request/response contract as before -- only the
underlying data source changed, from an in-memory dict / MySQL to MongoDB.
"""
from fastapi import FastAPI, Depends, status
from pymongo.database import Database
from fastapi.middleware.cors import CORSMiddleware

from app.database import get_db
from app.models import (
    CreateAccountRequest,
    DepositRequest,
    WithdrawRequest,
    Account,
    Transaction,
)
from app.service import AccountService

app = FastAPI(
    title="Simple Bank API (MongoDB Atlas)",
    description="Day 2: REST API backed by MongoDB Atlas",
    version="2.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/accounts", response_model=Account, status_code=status.HTTP_201_CREATED)
def create_account(payload: CreateAccountRequest, db: Database = Depends(get_db)):
    return AccountService.create_account(db, payload)


@app.get("/api/accounts/{account_id}", response_model=Account)
def get_account(account_id: int, db: Database = Depends(get_db)):
    return AccountService.get_account(db, account_id)


@app.post("/api/accounts/{account_id}/deposit", response_model=Account)
def deposit(account_id: int, payload: DepositRequest, db: Database = Depends(get_db)):
    return AccountService.deposit(db, account_id, payload.amount)


@app.post("/api/accounts/{account_id}/withdraw", response_model=Account)
def withdraw(account_id: int, payload: WithdrawRequest, db: Database = Depends(get_db)):
    return AccountService.withdraw(db, account_id, payload.amount)


@app.get("/api/accounts/{account_id}/transactions", response_model=list[Transaction])
def get_transactions(account_id: int, db: Database = Depends(get_db)):
    return AccountService.get_transactions(db, account_id)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Simple Bank API (MongoDB Atlas)"}
