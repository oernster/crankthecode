from __future__ import annotations

"""Base request context builder and page-content loaders."""

import datetime as dt
from pathlib import Path

from fastapi import Request

from app.adapters.filesystem_posts_repository import FilesystemPostsRepository
from app.adapters.markdown_python_renderer import PythonMarkdownRenderer
from app.http.seo import (
    absolute_url,
    canonical_url_for_request,
    get_site_url,
)


def build_base_context(request: Request) -> dict:
    site_url = get_site_url(request)
    exclude_blog_raw = (request.query_params.get("exclude_blog") or "").strip().lower()
    exclude_blog = (
        True
        if exclude_blog_raw == ""
        else exclude_blog_raw in {"1", "true", "yes", "y", "on"}
    )
    return {
        "request": request,
        "site_url": site_url,
        "current_year": dt.datetime.now(dt.timezone.utc).year,
        "page_title": "Crank The Code",
        "site_name": "Crank The Code",
        "robots_meta": "index,follow",
        "canonical_url": canonical_url_for_request(request, site_url=site_url),
        "og_title": "Crank The Code",
        "og_description": (
            "Crank The Code - Python engineering blog and technical write-ups by "
            "Oliver Ernster."
        ),
        "og_type": "website",
        "og_image_url": absolute_url(site_url, "/static/images/me.jpg"),
        "jsonld_extra_json": None,
        "meta_description": (
            "Crank The Code - Python engineering blog and technical write-ups by "
            "Oliver Ernster."
        ),
        "sidebar_categories": [],
        "current_q": (request.query_params.get("q") or "").strip(),
        "current_cat": (request.query_params.get("cat") or "").strip(),
        "current_layer": (request.query_params.get("layer") or "").strip(),
        "exclude_blog": exclude_blog,
        "breadcrumb_items": [
            {"label": "Home", "href": "/"},
        ],
        # UI: show read-time pill only on long-form post detail pages.
        "show_read_time": False,
        "read_time_minutes": None,
    }


def load_about_html() -> str:
    """Render the About me markdown into HTML."""
    try:
        repo = FilesystemPostsRepository(posts_dir=Path("posts"))
        about_post = repo.get_post("about-me")
        if about_post is None:
            return ""
        return PythonMarkdownRenderer().render(about_post.content_markdown)
    except Exception:
        return ""
