
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# --- Request models (unchanged from Day 1/2 MySQL version) ---

class CreateAccountRequest(BaseModel):
    userId: Optional[int] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    accountType: str = Field(..., description="e.g. SAVINGS or CHECKING")


class DepositRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Deposit amount, must be positive")


class WithdrawRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Withdrawal amount, must be positive")


# --- Response models ---
# Same external shape as before -- MongoDB documents map directly onto
# these dicts, no separate ORM layer needed like SQLAlchemy required.

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
    txn_type: str
    amount: float
    created_at: datetime
