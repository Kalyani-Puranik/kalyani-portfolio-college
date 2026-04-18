from beanie import Document
from pydantic import Field
from typing import Optional, List
from datetime import datetime


class Project(Document):
    title: str
    slug: str
    description: str
    problem: str
    solution: str
    impact: str
    tech_stack: List[str] = []
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    paper_url: Optional[str] = None
    cover_image: Optional[str] = None
    images: List[str] = []
    featured: bool = False
    year: str = ""
    project_type: str = ""
    order: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "projects"
        indexes = ["slug", "featured", "order"]
