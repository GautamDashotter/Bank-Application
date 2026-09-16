from pymongo import MongoClient

uri = "mongodb+srv://gsdashotter_db_user:Q258kBhmI8vDXffY@cluster0.nm9o1qm.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)

try:
    client.admin.command("ping")
    print("MongoDB Atlas connected successfully!")

except Exception as e:
    print("Connection failed:")
    print(e)

finally:
    client.close()