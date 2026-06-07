from pydantic import BaseModel, EmailStr
from typing import Optional, Literal


# =========================
# CREATE USER
# =========================
class UserCreate(BaseModel):
    email: EmailStr
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
    tier: Literal["free", "elite", "pro"]
    is_active: bool
