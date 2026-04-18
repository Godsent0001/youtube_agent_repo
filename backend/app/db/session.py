from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.MONGO_URI)

db = client[settings.MONGO_DB_NAME]

# Collections (explicit for clarity)
users_collection = db["users"]
agents_collection = db["agents"]
videos_collection = db["videos"]
metrics_collection = db["metrics"]
campaigns_collection = db["campaigns"]