from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# =========================
# PASSWORD HASHING
# =========================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plain password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash
    """
    return pwd_context.verify(plain_password, hashed_password)


# =========================
# JWT TOKEN
# =========================

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create JWT access token
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=60)
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def decode_access_token(token: str):
    """
    Decode JWT token
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload

    except JWTError:
        return None