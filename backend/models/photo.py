from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime


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
