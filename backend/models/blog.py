from beanie import Document
from pydantic import Field
from typing import Optional, List
from datetime import datetime


class Blog(Document):
    title: str
    slug: str
    excerpt: str
    content: str
    tag: str = "thoughts"
    read_time: str = "5 min read"
    published: bool = False
    featured: bool = False
    cover_image: Optional[str] = None
    views: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "blogs"
        indexes = ["slug", "published", "created_at"]
