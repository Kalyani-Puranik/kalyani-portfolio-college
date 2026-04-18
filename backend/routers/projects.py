"""Projects router — public GET, protected POST/PUT/DELETE."""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from datetime import datetime
from beanie import PydanticObjectId
from models.project import Project
from schemas.schemas import ProjectCreate, ProjectUpdate
from utils.auth import get_current_admin

router = APIRouter()


def to_dict(project: Project) -> dict:
    d = project.model_dump()
    d["id"] = str(project.id)
    d.pop("_id", None)
    return d


# ── PUBLIC ────────────────────────────────────────────

@router.get("/")
async def get_projects(featured_only: bool = False):
    """Get all projects, sorted by order."""
    if featured_only:
        projects = await Project.find(Project.featured == True).sort("order").to_list()
    else:
        projects = await Project.find().sort("order").to_list()
    return [to_dict(p) for p in projects]


@router.get("/{slug}")
async def get_project(slug: str):
    """Get a single project by slug."""
    project = await Project.find_one(Project.slug == slug)
    if not project:
        raise HTTPException(404, "Project not found")
    return to_dict(project)


# ── PROTECTED ─────────────────────────────────────────

@router.post("/", status_code=201)
async def create_project(payload: ProjectCreate, admin=Depends(get_current_admin)):
    """Create a new project."""
    existing = await Project.find_one(Project.slug == payload.slug)
    if existing:
        raise HTTPException(400, f"Slug '{payload.slug}' already exists")

    project = Project(**payload.model_dump())
    await project.insert()
    return to_dict(project)


@router.put("/{project_id}")
async def update_project(project_id: str, payload: ProjectUpdate, admin=Depends(get_current_admin)):
    """Update a project."""
    try:
        oid = PydanticObjectId(project_id)
    except Exception:
        raise HTTPException(400, "Invalid project ID")

    project = await Project.get(oid)
    if not project:
        raise HTTPException(404, "Project not found")

    update_data = payload.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(project, field, value)

    await project.save()
    return to_dict(project)


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: str, admin=Depends(get_current_admin)):
    """Delete a project."""
    try:
        oid = PydanticObjectId(project_id)
    except Exception:
        raise HTTPException(400, "Invalid project ID")

    project = await Project.get(oid)
    if not project:
        raise HTTPException(404, "Project not found")

    await project.delete()
    return None
