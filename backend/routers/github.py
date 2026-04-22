from fastapi import APIRouter
import httpx
import os

router = APIRouter()

GITHUB_USERNAME = "Kalyani-Puranik"

@router.get("/stats")
async def get_github_stats():
    token = os.getenv("GITHUB_TOKEN")

    query = """
    {
      user(login: "Kalyani-Puranik") {
        repositories(first: 100, ownerAffiliations: OWNER) {
          nodes {
            stargazerCount
            forkCount
            issues(states: OPEN) {
              totalCount
            }
          }
        }
        followers {
          totalCount
        }
        contributionsCollection {
          contributionCalendar {
            totalContributions
          }
          totalCommitContributions
          totalPullRequestContributions
        }
      }
    }
    """

    headers = {
        "Authorization": f"Bearer {token}"
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://api.github.com/graphql",
            json={"query": query},
            headers=headers
        )

    data = res.json()

    print(data)

    if "data" not in data:
        return {
            "error": "GitHub API failed",
            "details": data
    }
    user = data["data"]["user"]
    repos = user["repositories"]["nodes"]

    total_stars = sum(r["stargazerCount"] for r in repos)
    total_forks = sum(r["forkCount"] for r in repos)
    total_issues = sum(r["issues"]["totalCount"] for r in repos)

    return {
        "public_repos": len(repos),
        "followers": user["followers"]["totalCount"],
        "total_stars": total_stars,
        "total_forks": total_forks,
        "total_issues": total_issues,

        "total_commits": user["contributionsCollection"]["totalCommitContributions"],
        "total_prs": user["contributionsCollection"]["totalPullRequestContributions"],
        "contributions_year": user["contributionsCollection"]["contributionCalendar"]["totalContributions"]
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