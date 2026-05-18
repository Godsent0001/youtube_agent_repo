import os
import sys
from datetime import datetime

# Add the project root to the path
sys.path.append(os.getcwd())

try:
    from backend.app.db.session import db
except ImportError:
    from app.db.session import db

def migrate():
    print("Starting MongoDB migration for agents...")
    now = datetime.utcnow()

    # 1. Ensure all agents have status and next_run_time
    result1 = db["agents"].update_many(
        {
            "$or": [
                {"status": {"$exists": False}},
                {"next_run_time": {"$exists": False}}
            ]
        },
        {
            "$set": {
                "status": "idle",
                "next_run_time": now
            }
        }
    )

    # 2. Ensure all agents have is_active
    result2 = db["agents"].update_many(
        {"is_active": {"$exists": False}},
        {"$set": {"is_active": False}}
    )

    print(f"Migration completed. Modified {result1.modified_count} agents for status/time and {result2.modified_count} for is_active.")

if __name__ == "__main__":
    migrate()
