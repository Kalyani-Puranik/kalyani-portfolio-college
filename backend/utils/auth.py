"""JWT Authentication utilities (SHA-256 based)."""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import hashlib

# =========================
# CONFIG
# =========================

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-in-production-please!")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

bearer_scheme = HTTPBearer()

# =========================
# ADMIN CREDENTIALS
# =========================

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "kalyani")

# ⚠️ IMPORTANT: Replace this with your actual hashed password
# Example: hash of "admin123"
ADMIN_PASSWORD_HASH = os.getenv(
    "ADMIN_PASSWORD_HASH",
    "240be518fabd2724ddb6f04eebdf39c5d4d7f7c0b6fdbf9f7e0c3e6c6b0f3d4e"
)

# =========================
# PASSWORD FUNCTIONS (SHA256)
# =========================

def hash_password(password: str) -> str:
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password using SHA-256."""
    return hash_password(plain_password) == hashed_password


# =========================
# JWT FUNCTIONS
# =========================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# =========================
# AUTH DEPENDENCY
# =========================

def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    payload = decode_token(credentials.credentials)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return payload