import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Central configuration for the entire backend
    """

    # =========================
    # APP SETTINGS
    # =========================
    APP_NAME: str = "AI YouTube Agent"
    # Default DEBUG to False for production safety
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    BACKEND_URL: str = os.getenv("BACKEND_URL")

    def __init__(self):
        # Default to localhost ONLY if explicitly in DEBUG mode
        if not self.BACKEND_URL:
            if self.DEBUG:
                self.BACKEND_URL = "http://localhost:8000"
            else:
                # In production, we MUST NOT have a localhost fallback.
                self.BACKEND_URL = ""

        # Validate critical settings in production
        if not self.DEBUG:
            if not self.BACKEND_URL or "localhost" in self.BACKEND_URL:
                print("🚨 CRITICAL ERROR: BACKEND_URL is missing or invalid (localhost) in production!")
                print("YouTube OAuth will fail. Ensure BACKEND_URL environment variable is set.")
            if not os.getenv("FRONTEND_URL"):
                print("🚨 WARNING: FRONTEND_URL is not set in production.")

    # =========================
    # MONGODB
    # =========================
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "ai_youtube_agent")

    # =========================
    # AI PROVIDERS
    # =========================
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    ELEVENLABS_VOICE_ID: str = os.getenv("ELEVENLABS_VOICE_ID", "wWWn96OtTHu1sn8SRGEr")
    
    PIXABAY_API_KEY: str = os.getenv("PIXABAY_API_KEY", "")

    # =========================
    # YOUTUBE API
    # =========================
    YOUTUBE_CLIENT_ID: str = os.getenv("YOUTUBE_CLIENT_ID", "")
    YOUTUBE_CLIENT_SECRET: str = os.getenv("YOUTUBE_CLIENT_SECRET", "")

    # =========================
    # SECURITY
    # =========================
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecret")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24


settings = Settings()