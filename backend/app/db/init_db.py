from app.core.logger import logger
from app.db.session import users_collection, agents_collection, videos_collection

def init_db():
    """
    Initialize database collections and indexes.
    """
    logger.info("Initializing Database...")

    # Ensure indexes
    try:
        users_collection.create_index("email", unique=True)
        agents_collection.create_index("user_id")
        videos_collection.create_index("user_id")
        videos_collection.create_index("agent_id")

        logger.info("Database indexes created successfully.")
    except Exception as e:
        logger.error(f"Error creating database indexes: {e}")

    logger.info("Database initialization complete.")
