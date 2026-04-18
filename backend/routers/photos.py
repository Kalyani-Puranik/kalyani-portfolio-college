"""Photography gallery router."""

from fastapi import APIRouter, Depends, HTTPException
from beanie import PydanticObjectId
from models.photo import Photo
from schemas.schemas import PhotoCreate
from utils.auth import get_current_admin

router = APIRouter()


def to_dict(photo: Photo) -> dict:
    d = photo.model_dump()
    d["id"] = str(photo.id)
    d.pop("_id", None)
    return d


@router.get("/")
async def get_photos(category: str = None):
    """Get all photos, optionally filtered by category."""
    if category:
        photos = await Photo.find(Photo.category == category).sort("order").to_list()
    else:
        photos = await Photo.find().sort("order").to_list()
    return [to_dict(p) for p in photos]


@router.post("/", status_code=201, dependencies=[Depends(get_current_admin)])
async def add_photo(payload: PhotoCreate):
    """Add a photo (admin only)."""
    photo = Photo(**payload.model_dump())
    await photo.insert()
    return to_dict(photo)


@router.delete("/{photo_id}", status_code=204, dependencies=[Depends(get_current_admin)])
async def delete_photo(photo_id: str):
    """Delete a photo (admin only)."""
    try:
        oid = PydanticObjectId(photo_id)
    except Exception:
        raise HTTPException(400, "Invalid photo ID")
    photo = await Photo.get(oid)
    if not photo:
        raise HTTPException(404, "Photo not found")
    await photo.delete()
    return None
