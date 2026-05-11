from bson import ObjectId
from app.db.session import users_collection
from app.core.security import hash_password
from app.core.logger import logger


class UserService:
    """
    Service for managing User-related operations.
    """

    def __init__(self):
        self.logger = logger

    # =========================
    # INTERNAL HELPERS
    # =========================
    def _prepare_user(self, user: dict | None):
        """
        Convert MongoDB _id to string id and avoid mutating original object.
        """
        if not user:
            return None

        user_copy = user.copy()

        if "_id" in user_copy:
            user_copy["id"] = str(user_copy.pop("_id"))

        return user_copy

    # =========================
    # GET USER BY EMAIL
    # =========================
    def get_by_email(self, email: str):
        """
        Find a user by their email address.
        """
        user = users_collection.find_one({"email": email})
        return self._prepare_user(user)

    # =========================
    # GET USER BY ID
    # =========================
    def get_by_id(self, user_id: str):
        """
        Find a user by their MongoDB ID.
        """
        try:
            user = users_collection.find_one({"_id": ObjectId(user_id)})
            return self._prepare_user(user)

        except Exception as e:
            self.logger.error(f"Error finding user by ID {user_id}: {e}")
            return None

    # =========================
    # CREATE USER
    # =========================
    def create_user(self, data: dict):
        """
        Create a new user with hashed password.
        """
        try:
            user_doc = data.copy()

            if "password" in user_doc:
                user_doc["password"] = hash_password(user_doc.pop("password"))

            result = users_collection.insert_one(user_doc)

            user_id = str(result.inserted_id)

            self.logger.info(f"User created with ID: {user_id}")

            return user_id

        except Exception as e:
            self.logger.error(f"Error creating user: {e}")
            raise


# Singleton instance
user_service = UserService()