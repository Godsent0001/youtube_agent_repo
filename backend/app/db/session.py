from pymongo import MongoClient
import mongomock
from app.core.config import settings

# Determine whether to use mock DB
# We ONLY use mock if DEBUG=True AND MONGO_URI is default or specifically missing
# This ensures that in Render (where MONGO_URI is set) the worker and web talk to the SAME db.
USE_MOCK_DB = settings.DEBUG and ("localhost" in settings.MONGO_URI or not settings.MONGO_URI)

if USE_MOCK_DB:
    print("🍃 MongoDB: Using mongomock (in-memory)")
    client = mongomock.MongoClient()
else:
    # Explicitly use settings.MONGO_URI
    # Mask password for security
    uri_parts = settings.MONGO_URI.split("@")
    masked_uri = uri_parts[-1] if len(uri_parts) > 1 else settings.MONGO_URI
    print(f"🔌 MongoDB: Connecting to real instance at {masked_uri}")
    client = MongoClient(settings.MONGO_URI)

db = client[settings.MONGO_DB_NAME]

# Collections (explicit for clarity)
users_collection = db["users"]
agents_collection = db["agents"]
videos_collection = db["videos"]
metrics_collection = db["metrics"]
campaigns_collection = db["campaigns"]
