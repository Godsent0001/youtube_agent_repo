import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # =========================
    # GENERAL CONFIG
    # =========================
    APP_NAME: str = "MorphFlow AI Video Creator"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # =========================
    # URLS
    # =========================
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    # =========================
    # DATABASE (MongoDB)
    # =========================
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "morphflow_db")

    # =========================
    # REDIS / QUEUE
    # =========================
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # =========================
    # AI SERVICES (API KEYS)
    # =========================
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    PIXABAY_API_KEY: str = os.getenv("PIXABAY_API_KEY", "")
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")

    # =========================
    # SECURITY
    # =========================
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecret")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    class Config:
        env_file = ".env"


settings = Settings()
