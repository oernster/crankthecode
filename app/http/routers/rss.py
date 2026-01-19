from __future__ import annotations

import os
import re
import html
from datetime import datetime
from email.utils import format_datetime
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response

from app.http.deps import get_blog_service
from app.services.blog_service import BlogService


router = APIRouter(tags=["rss"])

_MEDIA_NS = "http://search.yahoo.com/mrss/"
ET.register_namespace("media", _MEDIA_NS)

_CONTENT_NS = "http://purl.org/rss/1.0/modules/content/"
ET.register_namespace("content", _CONTENT_NS)


_CDATA_SECTION_RE = re.compile(r"&lt;!\[CDATA\[(.*?)\]\]&gt;", flags=re.S)


def _wrap_cdata(text: str) -> str:
    """Wrap raw text in a CDATA section.

    ElementTree doesn't support emitting CDATA natively. We embed CDATA markers
    into the element text, then post-process the serialized XML to turn the
    escaped markers back into real CDATA sections.

    Note: `]]>` is not allowed inside a CDATA section; split it safely.
    """

    safe = text.replace("]]>", "]]]]><![CDATA[>")
    return f"<![CDATA[{safe}]]>"


def _unescape_cdata_sections(xml_text: str) -> str:
    """Convert escaped CDATA markers back into real CDATA sections."""

    return _CDATA_SECTION_RE.sub(
        lambda m: "<![CDATA[" + html.unescape(m.group(1)) + "]]>",
        xml_text,
    )


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


def _first_image_src(html: str) -> str | None:
    """Extract the first <img src="..."> from rendered HTML."""

    match = re.search(r"<img[^>]+src=['\"]([^'\"]+)['\"]", html, flags=re.I)
    if not match:
        return None
    return match.group(1)


def _guess_image_mime(url: str) -> str | None:
    lower = url.lower()
    if lower.endswith(".png"):
        return "image/png"
    if lower.endswith(".jpg") or lower.endswith(".jpeg"):
        return "image/jpeg"
    if lower.endswith(".gif"):
        return "image/gif"
    if lower.endswith(".webp"):
        return "image/webp"
    if lower.endswith(".svg"):
        return "image/svg+xml"
    return None


@router.get("/rss.xml", include_in_schema=False)
async def rss_feed(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
):
    posts = list(blog.list_posts())
    posts = posts[:20]

    base_url = _site_url(request)

    # Note: do NOT set `xmlns:media` manually here.
    # We register the namespace globally and ElementTree will include it once
    # when serializing the first `{_MEDIA_NS}...` element.
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

        # Many readers (including Feedly list views) derive thumbnails from the
        # first <img> in the item's HTML body, not from Media RSS alone.
        # Put HTML in CDATA so it's not entity-escaped.
        description_elem = ET.SubElement(item, "description")

        # Feedly and many RSS readers pick up per-item images via Media RSS.
        # We take the first <img> from the full post content (author can add
        # images to markdown, e.g. `![Alt](/static/images/foo.png)`).
        detail = blog.get_post(post.slug)
        if detail is None:
            # Still emit a description; without detail we can't reliably pick an image.
            description_elem.text = _wrap_cdata(post.summary_html)
            continue

        img_src = detail.cover_image_url or _first_image_src(detail.content_html)
        if not img_src:
            description_elem.text = _wrap_cdata(post.summary_html)

            # Still provide full content if available.
            content_elem = ET.SubElement(item, f"{{{_CONTENT_NS}}}encoded")
            content_elem.text = _wrap_cdata(detail.content_html)
            continue

        img_url = img_src
        if not img_url.startswith("http://") and not img_url.startswith("https://"):
            img_url = urljoin(base_url, img_url)

        # Description: keep it short (image + excerpt) so list views can pick it up.
        # Feedly thumbnail heuristics can be very strict: place a "naked" <img>
        # as the very first node in the description (not wrapped in <p>).
        description_html = (
            f'<img src="{html.escape(img_url, quote=True)}" alt="" />'
            + post.summary_html
        )
        description_elem.text = _wrap_cdata(description_html)

        # Full content for readers that use RSS content instead of linking out.
        content_elem = ET.SubElement(item, f"{{{_CONTENT_NS}}}encoded")
        content_html = (
            f'<img src="{html.escape(img_url, quote=True)}" alt="" />'
            + detail.content_html
        )
        content_elem.text = _wrap_cdata(content_html)

        mime = _guess_image_mime(img_url)
        ET.SubElement(
            item,
            f"{{{_MEDIA_NS}}}content",
            {
                "url": img_url,
                "medium": "image",
                **({"type": mime} if mime else {}),
            },
        )

        # Some readers prefer `media:thumbnail` for list views.
        ET.SubElement(
            item,
            f"{{{_MEDIA_NS}}}thumbnail",
            {"url": img_url},
        )

        if mime:
            ET.SubElement(
                item,
                "enclosure",
                {"url": img_url, "type": mime, "length": "0"},
            )

    xml_bytes = ET.tostring(rss, encoding="utf-8", xml_declaration=True)
    xml_text = xml_bytes.decode("utf-8")
    xml_text = _unescape_cdata_sections(xml_text)
    return Response(content=xml_text.encode("utf-8"), media_type="application/rss+xml")

