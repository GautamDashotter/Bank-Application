"""
In-memory data store.

This simulates a database using plain Python dictionaries. It will be
swapped out for real persistence (MySQL) on Day 2, without changing the
Service or Controller layers' external behavior.
"""
from itertools import count
from typing import Dict

from models import User, Account, Transaction

users: Dict[int, User] = {}
accounts: Dict[int, Account] = {}
transactions: Dict[int, Transaction] = {}

# Simple auto-incrementing ID generators, mimicking AUTO_INCREMENT columns
_user_id_seq = count(1)
_account_id_seq = count(1)
_txn_id_seq = count(1)


def next_user_id() -> int:
    return next(_user_id_seq)


def next_account_id() -> int:
    return next(_account_id_seq)


def next_txn_id() -> int:
    return next(_txn_id_seq)
