from __future__ import annotations

"""Books catalogue page route."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.domain.books_catalogue import BOOKS_CATALOGUE
from app.domain.books_compilations import COMPLETE_SERIES_EDITION
from app.http.deps import get_blog_service, get_templates
from app.http.seo import absolute_url, get_site_url
from app.http.view_models.context import build_base_context
from app.http.view_models.sidebar import build_sidebar_categories
from app.services.blog_service import BlogService

router = APIRouter()


@router.get("/books", response_class=HTMLResponse)
async def books_page(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    """Quiet catalogue page for authored books."""

    ctx = build_base_context(request)
    ctx["sidebar_categories"] = build_sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    site_url = get_site_url(request)
    canonical = absolute_url(site_url, "/books")

    ctx.update(
        {
            "is_homepage": False,
            "canonical_url": canonical,
            "page_title": "Books | Crank The Code",
            "og_title": "Books | Crank The Code",
            "og_description": (
                "Authored books on decision architecture and structural design in technical organisations."
            ),
            "meta_description": (
                "Authored books on decision architecture and structural design in technical organisations."
            ),
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Books", "href": "/books"},
            ],
            "books": BOOKS_CATALOGUE,
            "books_by_title": {b.title: b for b in BOOKS_CATALOGUE},
            "complete_series_edition": COMPLETE_SERIES_EDITION,
        }
    )

    return templates.TemplateResponse(request, "books.html", ctx)
