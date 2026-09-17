"""
Database connection setup (MongoDB via PyMongo).

Reads the connection string from an environment variable so credentials
never get hardcoded/committed. For MongoDB Atlas, this is the connection
string you get from the Atlas dashboard (Connect -> Drivers).
"""
import os
from pymongo import MongoClient
from pymongo.database import Database

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017",  # fallback for local testing only
)
DB_NAME = os.getenv("DB_NAME", "simple_bank")

client = MongoClient(MONGO_URI)
db: Database = client[DB_NAME]

# Collections (Mongo's equivalent of SQL tables)
users_collection = db["users"]
accounts_collection = db["accounts"]
transactions_collection = db["transactions"]
counters_collection = db["counters"]  # used to simulate auto-increment IDs


def get_db() -> Database:
    """FastAPI dependency that provides the database handle."""
    return db
