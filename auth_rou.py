"""Auth router — admin login only."""

from fastapi import APIRouter, HTTPException, status
from schemas.schemas import LoginRequest, TokenResponse
from utils.auth import verify_password, create_access_token, ADMIN_USERNAME, ADMIN_PASSWORD_HASH
from datetime import timedelta

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """Admin login — returns JWT token."""
    if credentials.username != ADMIN_USERNAME:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(credentials.password, ADMIN_PASSWORD_HASH):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": credentials.username, "role": "admin"},
        expires_delta=timedelta(hours=24)
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=86400
    )


@router.get("/me")
async def get_me():
    """Health check for auth (protected in real usage)."""
    return {"message": "Auth service running"}