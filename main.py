from fastapi import FastAPI, Depends, status
from pymongo.database import Database
from fastapi.middleware.cors import CORSMiddleware

from app.auth import router as auth_router
from app.security import get_current_user
from app.database import get_db

from app.models import (
    CreateAccountRequest,
    DepositRequest,
    WithdrawRequest,
    Account,
    Transaction,
)

from app.service import AccountService


# --------------------------------
# FASTAPI APPLICATION
# --------------------------------

app = FastAPI(
    title="Simple Bank API - JWT Authentication",
    description="REST API backed by MongoDB Atlas with JWT Authentication",
    version="3.0.0",
)


# --------------------------------
# CORS
# --------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------
# AUTHENTICATION ROUTES
# --------------------------------

app.include_router(auth_router)


# --------------------------------
# CREATE ACCOUNT - PROTECTED
# --------------------------------

@app.post(
    "/api/accounts",
    response_model=Account,
    status_code=status.HTTP_201_CREATED
)
def create_account(
    payload: CreateAccountRequest,
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return AccountService.create_account(db, payload)


# --------------------------------
# GET ACCOUNT - PROTECTED
# --------------------------------

@app.get(
    "/api/accounts/{account_id}",
    response_model=Account
)
def get_account(
    account_id: int,
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return AccountService.get_account(db, account_id)


# --------------------------------
# DEPOSIT - PROTECTED
# --------------------------------

@app.post(
    "/api/accounts/{account_id}/deposit",
    response_model=Account
)
def deposit(
    account_id: int,
    payload: DepositRequest,
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return AccountService.deposit(
        db,
        account_id,
        payload.amount
    )


# --------------------------------
# WITHDRAW - PROTECTED
# --------------------------------

@app.post(
    "/api/accounts/{account_id}/withdraw",
    response_model=Account
)
def withdraw(
    account_id: int,
    payload: WithdrawRequest,
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return AccountService.withdraw(
        db,
        account_id,
        payload.amount
    )


# --------------------------------
# TRANSACTION HISTORY - PROTECTED
# --------------------------------

@app.get(
    "/api/accounts/{account_id}/transactions",
    response_model=list[Transaction]
)
def get_transactions(
    account_id: int,
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return AccountService.get_transactions(
        db,
        account_id
    )


# --------------------------------
# HEALTH CHECK - NOT PROTECTED
# --------------------------------

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "Simple Bank API with MongoDB Atlas and JWT Authentication"
    }