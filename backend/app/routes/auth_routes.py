from fastapi import APIRouter, HTTPException

from app.schemas.user import UserCreate, UserLogin
from app.services.user_service import user_service
from app.core.security import create_access_token, verify_password
from app.core.logger import logger

router = APIRouter(prefix="/auth", tags=["Auth"])


# =========================
# REGISTER USER
# =========================
@router.post("/register")
def register_user(payload: UserCreate):

    existing = user_service.get_by_email(payload.email)

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user_id = user_service.create_user(payload.dict())

    token = create_access_token({"user_id": user_id})

    logger.info(f"User registered: {user_id}")

    return {
        "user_id": user_id,
        "access_token": token,
        "token_type": "bearer"
    }


# =========================
# LOGIN USER
# =========================
@router.post("/login")
def login_user(payload: UserLogin):

    user = user_service.get_by_email(payload.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ✅ FIX: use "id" instead of "_id"
    user_id = user.get("id")

    if not user_id:
        raise HTTPException(status_code=500, detail="User ID missing")

    token = create_access_token({"user_id": user_id})

    return {
        "user_id": user_id,
        "access_token": token,
        "token_type": "bearer"
    }


# =========================
# GET CURRENT USER (ME)
# =========================
@router.get("/me")
def get_me(user_id: str):

    user = user_service.get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# =========================
# OAUTH PLACEHOLDER
# =========================
@router.get("/oauth/google")
def google_oauth():

    return {
        "message": "Google OAuth not implemented yet",
        "status": "placeholder"
    }