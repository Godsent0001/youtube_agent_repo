from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # =========================
    # GENERAL CONFIG
    # =========================
    APP_NAME: str = "MorphFlow AI Video Creator"
    DEBUG: bool = False

    # =========================
    # URLS
    # =========================
    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:5173"

    # =========================
    # DATABASE (MongoDB)
    # =========================
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "morphflow_db"

    # =========================
    # REDIS / QUEUE
    # =========================
    REDIS_URL: str = "redis://localhost:6379/0"

    # =========================
    # AI SERVICES (API KEYS)
    # =========================
    GEMINI_API_KEY: str = ""
    PIXABAY_API_KEY: str = ""
    ELEVENLABS_API_KEY: str = ""

    # =========================
    # SECURITY
    # =========================
    JWT_SECRET: str = "supersecret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # 👇 IMPORTANT FIX FOR YOUR ERROR
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
