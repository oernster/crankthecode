from __future__ import annotations

import os
from datetime import datetime
from email.utils import format_datetime
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response

from app.http.deps import get_blog_service
from app.services.blog_service import BlogService


router = APIRouter(tags=["rss"])


def _site_url(request: Request) -> str:
    configured = os.getenv("SITE_URL")
    if configured:
        return configured.rstrip("/") + "/"
    return str(request.base_url)


def _rfc822_date(value: str) -> str:
    """Convert our frontmatter date string into RFC 822 for RSS.

    We currently store dates like: "YYYY-MM-DD HH:MM".
    If parsing fails, return the raw value (better than omitting).
    """

    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(value, fmt)
            return format_datetime(dt)
        except ValueError:
            continue
    return value


@router.get("/rss.xml", include_in_schema=False)
async def rss_feed(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
):
    posts = list(blog.list_posts())
    posts = posts[:20]

    base_url = _site_url(request)

    rss = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(rss, "channel")

    # Minimal channel metadata; kept generic to avoid needing config.
    ET.SubElement(channel, "title").text = "Crankthecode"
    ET.SubElement(channel, "link").text = base_url.rstrip("/")
    ET.SubElement(channel, "description").text = "Blog posts"

    for post in posts:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = post.title
        link = urljoin(base_url, f"posts/{post.slug}")
        ET.SubElement(item, "link").text = link
        guid = ET.SubElement(item, "guid", {"isPermaLink": "true"})
        guid.text = link
        ET.SubElement(item, "pubDate").text = _rfc822_date(post.date)
        ET.SubElement(item, "description").text = post.summary_html

    xml_bytes = ET.tostring(rss, encoding="utf-8", xml_declaration=True)
    return Response(content=xml_bytes, media_type="application/rss+xml")

