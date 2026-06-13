from __future__ import annotations

import json
from datetime import timezone
from urllib.parse import urljoin
from datetime import datetime

from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response

from app.http.deps import get_blog_service
from app.http.seo import get_site_url
from app.services.blog_service import BlogService

router = APIRouter(tags=["mmsp"])

_SITE_TITLE = "Crank The Code"
_SITE_DESCRIPTION = (
    "Engineering blog by Oliver Ernster. Principal engineer, Python specialist, "
    "decision architect. Decision Architecture, software craft and open-source tools."
)
_AUTHOR_NAME = "Oliver Ernster"

_EXCLUDED_SLUGS = frozenset({"about-me", "start-here", "portfolio"})
_LEADERSHIP_TAG = "cat:leadership"


def _is_excluded(post: object) -> bool:
    slug = str(getattr(post, "slug", "") or "").strip().lower()
    if slug in _EXCLUDED_SLUGS:
        return True
    tags = getattr(post, "tags", []) or []
    try:
        return any(str(t).strip().lower() == _LEADERSHIP_TAG for t in tags)
    except TypeError:
        return False


def _to_iso_utc(value: str) -> str | None:
    raw = (value or "").strip()
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(raw, fmt)
            if fmt == "%Y-%m-%d":
                dt = dt.replace(hour=12, minute=0, second=0, microsecond=0)
            else:
                dt = dt.replace(second=0, microsecond=0)
            return dt.replace(tzinfo=timezone.utc).isoformat()
        except ValueError:
            continue
    return None


def _absolute(base: str, url: str) -> str:
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return urljoin(base, url)


@router.get("/.well-known/mmsp.json", include_in_schema=False)
async def mmsp_feed(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
) -> Response:
    base_url = get_site_url(request)
    feed_url = urljoin(base_url, ".well-known/mmsp.json")
    about_url = urljoin(base_url, "about")
    icon_url = urljoin(base_url, "static/images/meridian-icon.png")

    posts = [p for p in blog.list_posts() if not _is_excluded(p)]

    items = []
    for post in posts:
        post_url = urljoin(base_url, f"posts/{post.slug}")
        published = _to_iso_utc(post.date)
        if not published:
            continue

        item: dict = {
            "id": f"{post_url}#mmsp-v1",
            "type": "article",
            "title": post.title,
            "url": post_url,
            "published": published,
        }

        blurb = getattr(post, "blurb", None) or getattr(post, "one_liner", None)
        if blurb:
            item["description"] = blurb

        cover = getattr(post, "cover_image_url", None)
        if cover:
            item["thumbnail"] = [{"url": _absolute(base_url, cover)}]

        raw_tags = getattr(post, "tags", []) or []
        clean_tags = [
            str(t)
            for t in raw_tags
            if not str(t).strip().lower().startswith("cat:")
        ]
        if clean_tags:
            item["tags"] = clean_tags

        items.append(item)

    manifest = {
        "mmsp": "1.0",
        "id": feed_url,
        "title": _SITE_TITLE,
        "feed_url": feed_url,
        "description": _SITE_DESCRIPTION,
        "icon": icon_url,
        "language": "en",
        "authors": [
            {
                "name": _AUTHOR_NAME,
                "url": about_url,
            }
        ],
        "tags": ["engineering", "python", "architecture", "software", "open-source"],
        "contact": "oernster@codecrafter.uk",
        "poll": {
            "min_interval_seconds": 300,
            "recommended_interval_seconds": 3600,
        },
        "items": items,
    }

    body = json.dumps(manifest, ensure_ascii=False, indent=2)
    return Response(
        content=body.encode("utf-8"),
        media_type="application/mmsp+json",
        headers={"Content-Type": "application/mmsp+json; charset=utf-8"},
    )
