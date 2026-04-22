from fastapi import APIRouter
import httpx
import os

router = APIRouter()

@router.get("/now-playing")
async def now_playing():
    api_key = os.getenv("LASTFM_API_KEY")
    username = os.getenv("LASTFM_USERNAME")

    url = "http://ws.audioscrobbler.com/2.0/"

    params = {
        "method": "user.getrecenttracks",
        "user": username,
        "api_key": api_key,
        "format": "json",
        "limit": 1
    }

    async with httpx.AsyncClient() as client:
        res = await client.get(url, params=params)
        data = res.json()

    track = data["recenttracks"]["track"][0]

    return {
        "track_name": track["name"],
        "artist": track["artist"]["#text"],
        "album_art": track["image"][-1]["#text"],
        "is_playing": track.get("@attr", {}).get("nowplaying", False)
    }