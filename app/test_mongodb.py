import os
from pymongo import MongoClient

uri = os.getenv("MONGO_URI")

if not uri:
    raise RuntimeError("MONGO_URI environment variable is not set")

client = MongoClient(uri)

try:
    client.admin.command("ping")
    print("MongoDB Atlas connected successfully!")

except Exception as e:
    print("Connection failed:")
    print(e)

finally:
    client.close()
