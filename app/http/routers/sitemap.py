from __future__ import annotations

import xml.etree.ElementTree as ET

from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response

from app.http.deps import get_blog_service
from app.http.seo import get_site_url, to_iso_date
from app.services.blog_service import BlogService


router = APIRouter(tags=["seo"])


@router.get("/sitemap.xml", include_in_schema=False)
async def sitemap_xml(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
):
    site_url = get_site_url(request)
    base = site_url.rstrip("/")

    urlset = ET.Element(
        "urlset",
        {"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"},
    )

    def _add_url(path: str, lastmod: str | None = None) -> None:
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = f"{base}{path}"
        if lastmod:
            ET.SubElement(url, "lastmod").text = lastmod

    # Main pages.
    _add_url("/")
    _add_url("/posts")
    _add_url("/about")

    # All posts.
    for post in blog.list_posts():
        lastmod = to_iso_date(post.date)
        _add_url(f"/posts/{post.slug}", lastmod=lastmod)

    xml_bytes = ET.tostring(urlset, encoding="utf-8", xml_declaration=True)
    return Response(content=xml_bytes, media_type="application/xml")


@router.get("/robots.txt", include_in_schema=False)
async def robots_txt(request: Request):
    site_url = get_site_url(request)
    sitemap_url = site_url.rstrip("/") + "/sitemap.xml"
    body = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            f"Sitemap: {sitemap_url}",
            "",
        ]
    )
    return Response(content=body, media_type="text/plain; charset=utf-8")

