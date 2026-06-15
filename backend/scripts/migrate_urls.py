from pymongo import MongoClient
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.core.config import settings

def migrate_urls():
    print(f"Connecting to MongoDB: {settings.MONGO_DB_NAME}")
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]
    videos_collection = db["videos"]

    # 1. Update video_url to relative paths
    cursor = videos_collection.find({"video_url": {"$regex": "http"}})
    count = 0
    for video in cursor:
        old_url = video["video_url"]
        if "onrender.com" in old_url or "api.aiworkforceinc.com" in old_url or "199.231.187.251" in old_url:
            filename = old_url.split("/")[-1]
            new_path = f"storage/videos/{filename}"
            videos_collection.update_one({"_id": video["_id"]}, {"$set": {"video_url": new_path}})
            count += 1
            print(f"Migrated video {video['_id']}: {old_url} -> {new_path}")

    # 2. Update thumbnail_url to relative paths (if any)
    cursor = videos_collection.find({"thumbnail_url": {"$regex": "http"}})
    for video in cursor:
        old_url = video["thumbnail_url"]
        if "onrender.com" in old_url or "api.aiworkforceinc.com" in old_url or "199.231.187.251" in old_url:
            filename = old_url.split("/")[-1]
            new_path = f"storage/images/{filename}"
            videos_collection.update_one({"_id": video["_id"]}, {"$set": {"thumbnail_url": new_path}})
            count += 1
            print(f"Migrated thumbnail {video['_id']}: {old_url} -> {new_path}")

    print(f"Migration complete. Updated {count} records.")

if __name__ == "__main__":
    migrate_urls()
