"""Blogs router — public GET, protected POST/PUT/DELETE."""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime
from beanie import PydanticObjectId
from models.blog import Blog
from schemas.schemas import BlogCreate, BlogUpdate
from utils.auth import get_current_admin
import re

router = APIRouter()


def to_dict(blog: Blog) -> dict:
    d = blog.model_dump()
    d["id"] = str(blog.id)
    d.pop("_id", None)
    return d


# ── PUBLIC ────────────────────────────────────────────

@router.get("/")
async def get_blogs(
    limit: int = Query(10, ge=1, le=50),
    skip: int = Query(0, ge=0),
    tag: Optional[str] = None,
    published_only: bool = True
):
    """Get all published blogs (paginated)."""
    query = {}
    if published_only:
        query["published"] = True
    if tag:
        query["tag"] = tag

    blogs = await Blog.find(query).sort("-created_at").skip(skip).limit(limit).to_list()
    total = await Blog.find(query).count()

    return {
        "blogs": [to_dict(b) for b in blogs],
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.get("/featured")
async def get_featured_blogs():
    """Get featured blogs."""
    blogs = await Blog.find(Blog.featured == True, Blog.published == True).sort("-created_at").to_list()
    return [to_dict(b) for b in blogs]


@router.get("/{slug}")
async def get_blog(slug: str):
    """Get a single blog by slug — increments view count."""
    blog = await Blog.find_one(Blog.slug == slug, Blog.published == True)
    if not blog:
        raise HTTPException(404, "Blog not found")

    # Increment views
    blog.views += 1
    await blog.save()

    return to_dict(blog)


# ── PROTECTED (Admin only) ──────────────────────────────

@router.post("/", status_code=201)
async def create_blog(payload: BlogCreate, admin=Depends(get_current_admin)):
    """Create a new blog post."""
    existing = await Blog.find_one(Blog.slug == payload.slug)
    if existing:
        raise HTTPException(400, f"Slug '{payload.slug}' already exists")

    blog = Blog(**payload.model_dump())
    await blog.insert()
    return to_dict(blog)


@router.put("/{blog_id}")
async def update_blog(blog_id: str, payload: BlogUpdate, admin=Depends(get_current_admin)):
    """Update a blog post."""
    try:
        oid = PydanticObjectId(blog_id)
    except Exception:
        raise HTTPException(400, "Invalid blog ID")

    blog = await Blog.get(oid)
    if not blog:
        raise HTTPException(404, "Blog not found")

    update_data = payload.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(blog, field, value)

    await blog.save()
    return to_dict(blog)


@router.delete("/{blog_id}", status_code=204)
async def delete_blog(blog_id: str, admin=Depends(get_current_admin)):
    """Delete a blog post."""
    try:
        oid = PydanticObjectId(blog_id)
    except Exception:
        raise HTTPException(400, "Invalid blog ID")

    blog = await Blog.get(oid)
    if not blog:
        raise HTTPException(404, "Blog not found")

    await blog.delete()
    return None
