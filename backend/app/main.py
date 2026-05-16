from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logger import logger

# =========================
# ROUTES IMPORTS
# =========================
from app.routes.auth_routes import router as auth_router
from app.routes.agent_routes import router as agent_router
from app.routes.ads_routes import router as ads_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.settings_routes import router as settings_router
from app.routes.video_routes import router as video_router

# =========================
# WORKER IMPORT
# =========================
from app.workers.worker import worker

# =========================
# DB INIT (MongoDB)
# =========================
from app.db.init_db import init_db


# =========================
# APP INIT
# =========================
app = FastAPI(
    title="AI Video Agent Platform",
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
app.include_router(agent_router)
app.include_router(ads_router)
app.include_router(dashboard_router)
app.include_router(settings_router)
app.include_router(video_router)


# =========================
# STARTUP EVENT
# =========================
@app.on_event("startup")
def startup_event():

    logger.info("Starting AI Video Backend...")

    # Initialize MongoDB
    init_db()

    # Start background worker
    worker.start_background()

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