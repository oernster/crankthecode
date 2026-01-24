from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

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
    _add_url("/battlestation")

    # All posts.
    for post in blog.list_posts():
        lastmod = to_iso_date(post.date)
        _add_url(f"/posts/{post.slug}", lastmod=lastmod)

    xml_bytes = ET.tostring(urlset, encoding="utf-8", xml_declaration=True)
    return Response(content=xml_bytes, media_type="application/xml")


@router.get("/robots.txt", include_in_schema=False)
async def robots_txt(request: Request):
    """Serve robots.txt based on `static/robots.txt`, with an environment-aware sitemap URL.

    This keeps `robots.txt` editable as a static asset, while ensuring the sitemap
    location reflects `SITE_URL` (or the request base URL) in tests and in prod.
    """

    site_url = get_site_url(request)
    sitemap_url = site_url.rstrip("/") + "/sitemap.xml"

    robots_path = Path("static") / "robots.txt"
    try:
        raw = robots_path.read_text(encoding="utf-8")
    except OSError:
        raw = "".join(
            [
                "User-agent: *\n",
                "Allow: /\n",
                f"Sitemap: {sitemap_url}\n",
            ]
        )

    # Replace any existing Sitemap line so local/test/prod environments always
    # point at the correct base URL.
    out_lines: list[str] = []
    replaced = False
    for line in raw.splitlines():
        if line.strip().lower().startswith("sitemap:"):
            out_lines.append(f"Sitemap: {sitemap_url}")
            replaced = True
        else:
            out_lines.append(line)

    if not replaced:
        if out_lines and out_lines[-1].strip():
            out_lines.append("")
        out_lines.append(f"Sitemap: {sitemap_url}")

    body = "\n".join(out_lines) + "\n"
    return Response(content=body, media_type="text/plain; charset=utf-8")

