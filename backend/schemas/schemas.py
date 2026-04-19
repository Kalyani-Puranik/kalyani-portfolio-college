"""
Pydantic schemas (request/response shapes) for all API endpoints.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ── BLOG SCHEMAS ───────────────────────────────────────

class BlogCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    slug: str = Field(..., regex=r'^[a-z0-9-]+$')
    excerpt: str = Field(..., min_length=10, max_length=500)
    content: str = Field(..., min_length=20)
    tag: str = "thoughts"
    read_time: str = "5 min read"
    published: bool = False
    featured: bool = False
    cover_image: Optional[str] = None


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    tag: Optional[str] = None
    read_time: Optional[str] = None
    published: Optional[bool] = None
    featured: Optional[bool] = None
    cover_image: Optional[str] = None


class BlogResponse(BaseModel):
    id: str
    title: str
    slug: str
    excerpt: str
    tag: str
    read_time: str
    published: bool
    featured: bool
    cover_image: Optional[str]
    views: int
    created_at: datetime
    updated_at: datetime


# ── PROJECT SCHEMAS ─────────────────────────────────────

class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    slug: str = Field(..., pattern=r'^[a-z0-9-]+$')
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


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    problem: Optional[str] = None
    solution: Optional[str] = None
    impact: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    paper_url: Optional[str] = None
    featured: Optional[bool] = None
    order: Optional[int] = None


class ProjectResponse(BaseModel):
    id: str
    title: str
    slug: str
    description: str
    problem: str
    solution: str
    impact: str
    tech_stack: List[str]
    github_url: Optional[str]
    demo_url: Optional[str]
    paper_url: Optional[str]
    cover_image: Optional[str]
    featured: bool
    year: str
    project_type: str
    created_at: datetime


# ── CONTACT SCHEMAS ─────────────────────────────────────

class ContactCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')
    subject: Optional[str] = "general"
    message: str = Field(..., min_length=10, max_length=2000)


class ContactResponse(BaseModel):
    success: bool
    message: str


# ── AUTH SCHEMAS ────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# ── ANALYTICS SCHEMAS ───────────────────────────────────

class VisitCreate(BaseModel):
    page: str = "/"
    referrer: Optional[str] = None
    timestamp: Optional[str] = None


class AnalyticsResponse(BaseModel):
    total_visits: int
    page_breakdown: dict
    today_visits: int


# ── PHOTO SCHEMAS ────────────────────────────────────────

class PhotoCreate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    url: str
    thumbnail_url: Optional[str] = None
    alt: str = ""
    category: str = "general"
    order: int = 0


class PhotoResponse(BaseModel):
    id: str
    title: Optional[str]
    url: str
    thumbnail_url: Optional[str]
    alt: str
    category: str
    order: int
    created_at: datetime
