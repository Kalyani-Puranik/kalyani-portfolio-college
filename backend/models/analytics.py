from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime


class Analytics(Document):
    page: str = "/"
    referrer: Optional[str] = None
    user_agent: Optional[str] = None
    ip_hash: Optional[str] = None
    country: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "analytics"
        indexes = ["page", "timestamp"]


class Photo(Document):
    title: Optional[str] = None
    description: Optional[str] = None
    url: str
    thumbnail_url: Optional[str] = None
    alt: str = ""
    category: str = "general"
    width: Optional[int] = None
    height: Optional[int] = None
    order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "photos"
        indexes = ["category", "order"]
