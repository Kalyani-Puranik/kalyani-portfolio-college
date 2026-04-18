"""GitHub stats proxy — avoids rate limiting from client."""

from fastapi import APIRouter
import httpx
import os
from functools import lru_cache
import asyncio
from datetime import datetime

router = APIRouter()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "kalyani")

# Simple in-memory cache (30 min TTL)
_cache = {}
CACHE_TTL = 1800  # seconds


def get_cached(key: str):
    if key in _cache:
        data, ts = _cache[key]
        if (datetime.utcnow() - ts).seconds < CACHE_TTL:
            return data
    return None


def set_cached(key: str, data):
    _cache[key] = (data, datetime.utcnow())


@router.get("/stats")
async def get_github_stats():
    """Proxy GitHub user stats with caching."""
    cached = get_cached("github_stats")
    if cached:
        return cached

    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            user_res = await client.get(
                f"https://api.github.com/users/{GITHUB_USERNAME}",
                headers=headers
            )
            user_data = user_res.json()

            # Fetch repos for star count
            repos_res = await client.get(
                f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100",
                headers=headers
            )
            repos = repos_res.json()
            total_stars = sum(r.get("stargazers_count", 0) for r in repos if isinstance(r, dict))

            result = {
                "public_repos": user_data.get("public_repos", 0),
                "followers": user_data.get("followers", 0),
                "following": user_data.get("following", 0),
                "total_stars": total_stars,
                "bio": user_data.get("bio", ""),
                "avatar_url": user_data.get("avatar_url", ""),
                "html_url": user_data.get("html_url", ""),
            }

            set_cached("github_stats", result)
            return result

        except Exception as e:
            return {"error": str(e), "public_repos": 0, "followers": 0, "total_stars": 0}
