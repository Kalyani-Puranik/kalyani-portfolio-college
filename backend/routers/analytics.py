"""Analytics router — track visits and clicks."""

from fastapi import APIRouter, Request, Depends
from models.analytics import Analytics
from schemas.schemas import VisitCreate, AnalyticsResponse
from utils.auth import get_current_admin
from datetime import datetime, timedelta
import hashlib

router = APIRouter()


def hash_ip(ip: str) -> str:
    """Hash IP for privacy compliance."""
    return hashlib.sha256(ip.encode()).hexdigest()[:16]


@router.post("/visit", status_code=201)
async def track_visit(payload: VisitCreate, request: Request):
    """Track a page visit."""
    ip = request.client.host if request.client else "unknown"

    visit = Analytics(
        page=payload.page,
        referrer=payload.referrer,
        user_agent=request.headers.get("user-agent"),
        ip_hash=hash_ip(ip),
    )
    await visit.insert()
    return {"tracked": True}


@router.get("/summary", dependencies=[Depends(get_current_admin)])
async def get_analytics_summary():
    """Get analytics summary (admin only)."""
    total = await Analytics.count()

    # Today's visits
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_count = await Analytics.find(Analytics.timestamp >= today_start).count()

    # Page breakdown
    all_visits = await Analytics.find().to_list()
    page_counts = {}
    for v in all_visits:
        page_counts[v.page] = page_counts.get(v.page, 0) + 1

    # Last 7 days
    week_ago = datetime.utcnow() - timedelta(days=7)
    weekly = await Analytics.find(Analytics.timestamp >= week_ago).count()

    return {
        "total_visits": total,
        "today_visits": today_count,
        "weekly_visits": weekly,
        "page_breakdown": dict(sorted(page_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    }
