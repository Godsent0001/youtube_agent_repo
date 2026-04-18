from pydantic import BaseModel, EmailStr
from typing import Optional, Literal


# =========================
# CREATE USER
# =========================
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None


# =========================
# LOGIN
# =========================
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# =========================
# RESPONSE
# =========================
class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    plan: Literal["free", "pro", "enterprise"]
    is_active: bool