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

    def _prepare_user(self, user: dict):
        if user and "_id" in user:
            user["id"] = str(user.pop("_id"))
        return user

    def get_by_email(self, email: str):
        """Find a user by their email address."""
        user = users_collection.find_one({"email": email})
        return self._prepare_user(user)

    def get_by_id(self, user_id: str):
        """Find a user by their unique MongoDB ID."""
        try:
            user = users_collection.find_one({"_id": ObjectId(user_id)})
            return self._prepare_user(user)
        except Exception as e:
            self.logger.error(f"Error finding user by ID {user_id}: {e}")
            return None

    def create_user(self, data: dict):
        """Create a new user with hashed password."""
        user_doc = data.copy()
        if "password" in user_doc:
            user_doc["password"] = hash_password(user_doc.pop("password"))

        result = users_collection.insert_one(user_doc)
        self.logger.info(f"User created with ID: {result.inserted_id}")
        return str(result.inserted_id)

user_service = UserService()
