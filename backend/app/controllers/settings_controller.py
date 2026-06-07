from fastapi import HTTPException
from app.core.logger import logger

class SettingsController:
    """
    Controls MorphFlow user settings
    """

    def __init__(self):
        self.logger = logger

    def get_settings(self, user_id: str):
        return {"user_id": user_id, "theme": "light"}

    def update_settings(self, user_id: str, payload: dict):
        self.logger.info(f"Settings updated for user {user_id}")
        return {"message": "Settings updated", "payload": payload}

settings_controller = SettingsController()
