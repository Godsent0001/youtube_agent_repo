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

    # =========================
    # MONGODB
    # =========================
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "ai_youtube_agent")

    # =========================
    # AI PROVIDERS
    # =========================
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    
    PEXELS_API_KEY: str = os.getenv("PEXELS_API_KEY", "")

    # =========================
    # YOUTUBE API
    # =========================
    YOUTUBE_CLIENT_ID: str = os.getenv("YOUTUBE_CLIENT_ID", "")
    YOUTUBE_CLIENT_SECRET: str = os.getenv("YOUTUBE_CLIENT_SECRET", "")
    YOUTUBE_REFRESH_TOKEN: str = os.getenv("YOUTUBE_REFRESH_TOKEN", "")

    # =========================
    # SECURITY
    # =========================
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecret")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24


settings = Settings()