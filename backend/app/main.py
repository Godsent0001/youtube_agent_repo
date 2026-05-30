from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, video_routes, job_routes, user_routes, agent_routes
from app.core.config import settings
from app.core.logger import logger
import time

app = FastAPI(title="MorphFlow API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://youtube-agent-repo.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - {response.status_code} ({duration:.2f}s)")
    return response

# Include routers
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(video_routes.router, prefix="/videos", tags=["Videos"])
app.include_router(job_routes.router, prefix="/jobs", tags=["Jobs"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(agent_routes.router, prefix="/agents", tags=["Agents"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to MorphFlow API",
        "status": "online",
        "debug_mode": settings.DEBUG
    }

@app.on_event("startup")
async def startup_event():
    logger.info("************************************************")
    logger.info(f" MorphFlow Backend Starting")
    logger.info(f" DEBUG: {settings.DEBUG}")
    logger.info(f" BACKEND_URL: {settings.BACKEND_URL}")
    logger.info(f" FRONTEND_URL: {settings.FRONTEND_URL}")
    logger.info("************************************************")
