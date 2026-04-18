from beanie import Document
from pydantic import Field, EmailStr
from typing import Optional
from datetime import datetime


class Contact(Document):
    name: str
    email: str
    subject: Optional[str] = "general"
    message: str
    read: bool = False
    replied: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "contacts"


class Analytics(Document):
    page: str = "/"
    referrer: Optional[str] = None
    user_agent: Optional[str] = None
    ip_hash: Optional[str] = None  # Hashed for privacy
    country: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "analytics"
        indexes = ["page", "timestamp"]
