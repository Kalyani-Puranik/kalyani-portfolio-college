import json, os
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

DATA_FILE = Path(__file__).parent.parent / "data" / "blogs.json"

def load_blogs() -> list:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

router = APIRouter()


# ── PUBLIC ────────────────────────────────────────────

@router.get("/")
@router.get("/")
async def get_blogs(
    limit: int = Query(10, ge=1, le=50),
    skip: int = Query(0, ge=0),
    tag: Optional[str] = None,
    published_only: bool = True
):
    blogs = load_blogs()
    if published_only:
        blogs = [b for b in blogs if b.get("published", True)]
    if tag:
        blogs = [b for b in blogs if tag in b.get("tags", [])]
    total = len(blogs)
    blogs = sorted(blogs, key=lambda b: b.get("created_at", ""), reverse=True)
    return {"blogs": blogs[skip:skip+limit], "total": total, "skip": skip, "limit": limit}


@router.get("/featured")
async def get_featured_blogs():
    blogs = load_blogs()
    return [b for b in blogs if b.get("featured") and b.get("published", True)]


@router.get("/category/{category}")
async def get_blogs_by_category(category: str):
    valid = {"learning", "photography", "personal"}
    if category not in valid:
        raise HTTPException(400, f"Category must be one of: {valid}")
    blogs = load_blogs()
    return [b for b in blogs if b.get("category") == category and b.get("published", True)]

@router.get("/{slug}")
async def get_blog(slug: str):
    blogs = load_blogs()
    blog = next((b for b in blogs if b["slug"] == slug), None)
    if not blog:
        raise HTTPException(404, "Blog not found")
    return blog
