from pymongo import MongoClient
import mongomock
from app.core.config import settings

# Determine whether to use mock DB
USE_MOCK_DB = settings.DEBUG  # or add a specific setting if preferred

if USE_MOCK_DB:
    client = mongomock.MongoClient()
else:
    client = MongoClient(settings.MONGO_URI)

db = client[settings.MONGO_DB_NAME]

# Collections (explicit for clarity)
users_collection = db["users"]
agents_collection = db["agents"]
videos_collection = db["videos"]
metrics_collection = db["metrics"]
campaigns_collection = db["campaigns"]
