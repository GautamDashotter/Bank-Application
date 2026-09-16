from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# --- Request models (what the client sends) ---

class CreateAccountRequest(BaseModel):
    userId: Optional[int] = None      # if omitted, a new user is created using name/email below
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    accountType: str = Field(..., description="e.g. SAVINGS or CHECKING")


class DepositRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Deposit amount, must be positive")


class WithdrawRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Withdrawal amount, must be positive")


# --- Response / internal models ---

class User(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    created_at: datetime


class Account(BaseModel):
    account_id: int
    user_id: int
    user_name: str
    balance: float
    account_type: str
    created_at: datetime


class Transaction(BaseModel):
    txn_id: int
    account_id: int
    txn_type: str   # "DEPOSIT" or "WITHDRAW"
    amount: float
    created_at: datetime
