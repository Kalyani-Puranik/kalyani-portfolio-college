"""Spotify Now Playing integration."""

from fastapi import APIRouter
import httpx
import os
import base64
from datetime import datetime

router = APIRouter()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")

_token_cache = {"token": None, "expires_at": None}


async def get_spotify_token() -> str | None:
    """Get a fresh Spotify access token using refresh token."""
    if not all([SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REFRESH_TOKEN]):
        return None

    # Return cached token if still valid
    if _token_cache["token"] and _token_cache["expires_at"]:
        if (datetime.utcnow() - _token_cache["expires_at"]).seconds < 3500:
            return _token_cache["token"]

    creds = base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()

    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://accounts.spotify.com/api/token",
            headers={"Authorization": f"Basic {creds}", "Content-Type": "application/x-www-form-urlencoded"},
            data={"grant_type": "refresh_token", "refresh_token": SPOTIFY_REFRESH_TOKEN}
        )
        if res.status_code == 200:
            data = res.json()
            _token_cache["token"] = data["access_token"]
            _token_cache["expires_at"] = datetime.utcnow()
            return data["access_token"]
    return None


@router.get("/now-playing")
async def now_playing():
    """Get currently playing Spotify track."""
    token = await get_spotify_token()

    if not token:
        return {
            "is_playing": False,
            "track_name": "Spotify not configured",
            "artist": "Add SPOTIFY_* env vars",
            "album_art": None
        }

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            res = await client.get(
                "https://api.spotify.com/v1/me/player/currently-playing",
                headers={"Authorization": f"Bearer {token}"}
            )

            if res.status_code == 204 or res.status_code == 200 and not res.text:
                # Nothing playing
                return await get_recently_played(token)

            if res.status_code == 200:
                data = res.json()
                item = data.get("item", {})
                artists = item.get("artists", [])
                images = item.get("album", {}).get("images", [])

                return {
                    "is_playing": data.get("is_playing", False),
                    "track_name": item.get("name", "Unknown"),
                    "artist": ", ".join(a["name"] for a in artists),
                    "album": item.get("album", {}).get("name", ""),
                    "album_art": images[0]["url"] if images else None,
                    "spotify_url": item.get("external_urls", {}).get("spotify")
                }
        except Exception as e:
            pass

    return {"is_playing": False, "track_name": "Nothing playing", "artist": "—", "album_art": None}


async def get_recently_played(token: str) -> dict:
    """Fallback: get most recently played track."""
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            res = await client.get(
                "https://api.spotify.com/v1/me/player/recently-played?limit=1",
                headers={"Authorization": f"Bearer {token}"}
            )
            if res.status_code == 200:
                items = res.json().get("items", [])
                if items:
                    track = items[0]["track"]
                    artists = track.get("artists", [])
                    images = track.get("album", {}).get("images", [])
                    return {
                        "is_playing": False,
                        "track_name": track.get("name", "Unknown"),
                        "artist": ", ".join(a["name"] for a in artists),
                        "album_art": images[0]["url"] if images else None,
                        "recently_played": True
                    }
        except Exception:
            pass

    return {"is_playing": False, "track_name": "Nothing right now", "artist": "probably studying 📖", "album_art": None}
