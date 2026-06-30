import os
from pymongo import MongoClient

# Simple .env loader
if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split("=", 1)
                if len(parts) == 2:
                    key, val = parts
                    os.environ[key] = val

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable is missing!")

# Initialize MongoDB client
client = MongoClient(MONGODB_URI)
# Use 'zoom_clone' database
db = client.get_database("zoom_clone")
users_collection = db.get_collection("users")

# Ensure unique index on email and username
users_collection.create_index("email", unique=True)
users_collection.create_index("username", unique=True)
