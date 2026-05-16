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
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

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