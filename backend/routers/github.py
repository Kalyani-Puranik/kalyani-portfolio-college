from fastapi import APIRouter
import httpx

router = APIRouter()

GITHUB_USERNAME = "Kalyani-Puranik"


@router.get("/stats")
async def get_github_stats():
    user_url = f"https://api.github.com/users/{GITHUB_USERNAME}"
    repo_url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"

    headers = {
        "Accept": "application/vnd.github+json"
    }

    async with httpx.AsyncClient() as client:
        user_res = await client.get(user_url, headers=headers)
        repo_res = await client.get(repo_url, headers=headers)

    user_data = user_res.json()
    repos = repo_res.json()

    print("USER:", user_data)
    print("REPOS:", repos)

    if "message" in user_data:
        return {
            "public_repos": 0,
            "followers": 0,
            "total_stars": 0,
            "error": user_data["message"]
        }

    if not isinstance(repos, list):
        repos = []

    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)

    return {
        "public_repos": user_data.get("public_repos", 0),
        "followers": user_data.get("followers", 0),
        "total_stars": total_stars,
    }


@router.get("/repos")
async def get_repos():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?sort=updated"

    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        repos = res.json()

    return [
        {
            "name": repo["name"],
            "description": repo["description"],
            "stars": repo["stargazers_count"],
            "url": repo["html_url"],
        }
        for repo in repos[:6]
    ]