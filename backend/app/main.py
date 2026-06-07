from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logger import logger

# =========================
# ROUTES IMPORTS
# =========================
from app.routes.auth_routes import router as auth_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.settings_routes import router as settings_router
from app.routes.video_routes import router as video_router
from app.routes.job_routes import router as job_router

# =========================
# DB INIT (MongoDB)
# =========================
from app.db.init_db import init_db


# =========================
# APP INIT
# =========================
app = FastAPI(
    title="MorphFlow AI Video Creator",
    version="1.0.0"
)

# =========================
# CORS CONFIGURATION
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://youtube-agent-repo.vercel.app"
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# REGISTER ROUTES
# =========================
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(settings_router)
app.include_router(video_router)
app.include_router(job_router)


# =========================
# STARTUP EVENT
# =========================
@app.on_event("startup")
def startup_event():

    logger.info(f"Starting MorphFlow Backend (DEBUG={settings.DEBUG})...")
    logger.info(f"BACKEND_URL: {settings.BACKEND_URL}")
    logger.info(f"FRONTEND_URL: {settings.FRONTEND_URL}")

    # Initialize MongoDB
    init_db()

    logger.info("System fully initialized 🚀")


# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def root():

    return {
        "message": "AI Video Agent API is running",
        "status": "healthy"
    }