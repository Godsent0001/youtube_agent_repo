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

    # Update all agents that don't have status or next_run_time
    result = db["agents"].update_many(
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

    print(f"Migration completed. Modified {result.modified_count} agents.")

if __name__ == "__main__":
    migrate()
