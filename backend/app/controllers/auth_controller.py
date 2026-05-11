from fastapi import HTTPException

from app.services.user_service import user_service
from app.core.security import create_access_token, verify_password
from app.core.logger import logger


class AuthController:
    """
    Handles authentication logic (thin layer over user_service)
    """

    def __init__(self):
        self.logger = logger

    # =========================
    # REGISTER
    # =========================
    def register(self, payload: dict):

        existing = user_service.get_by_email(payload["email"])

        if existing:
            raise HTTPException(status_code=400, detail="User already exists")

        user_id = user_service.create_user(payload)

        token = create_access_token({"user_id": user_id})

        self.logger.info(f"User registered: {user_id}")

        return {
            "user_id": user_id,
            "access_token": token,
            "token_type": "bearer"
        }

    # =========================
    # LOGIN
    # =========================
    def login(self, payload: dict):

        user = user_service.get_by_email(payload["email"])

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(payload["password"], user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # ✅ FIX: use "id" (NOT _id)
        user_id = user.get("id")

        if not user_id:
            raise HTTPException(status_code=500, detail="User ID missing")

        token = create_access_token({"user_id": user_id})

        self.logger.info(f"User logged in: {user_id}")

        return {
            "user_id": user_id,
            "access_token": token,
            "token_type": "bearer"
        }

    # =========================
    # GET CURRENT USER
    # =========================
    def me(self, user_id: str):

        user = user_service.get_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    # =========================
    # OAUTH (PLACEHOLDER)
    # =========================
    def oauth_google(self):

        return {
            "message": "Google OAuth not implemented yet",
            "status": "placeholder"
        }


auth_controller = AuthController()