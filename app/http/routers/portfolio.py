from __future__ import annotations

"""Portfolio page route."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.http.deps import get_blog_service, get_templates
from app.http.seo import absolute_url, get_site_url
from app.http.view_models.context import build_base_context
from app.http.view_models.portfolio import (
    load_portfolio_post,
    portfolio_groups,
    portfolio_label_to_slug,
    render_portfolio_intro_html,
)
from app.http.view_models.sidebar import build_sidebar_categories
from app.services.blog_service import BlogService

router = APIRouter()


@router.get("/portfolio", response_class=HTMLResponse)
async def portfolio_page(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
    section: str | None = None,
):
    ctx = build_base_context(request)
    ctx["sidebar_categories"] = build_sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    md = load_portfolio_post()
    title = str(getattr(md, "title", "Portfolio") if md is not None else "Portfolio")
    emoji = str(getattr(md, "emoji", "") if md is not None else "").strip()
    one_liner = str(getattr(md, "one_liner", "") if md is not None else "").strip()

    all_groups = portfolio_groups(blog)

    if section:
        matched = [g for g in all_groups if portfolio_label_to_slug(str(g.get("label", ""))) == section]
        if not matched:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Portfolio section not found")
        groups = matched
        page_heading = str(matched[0].get("label", title))
        intro_html = None
        flagship = []
    else:
        groups = all_groups
        page_heading = title
        intro_html = render_portfolio_intro_html()
        flagship = []

    meta_description = (
        one_liner
        or "Independent software systems and engineering experiments built outside commercial environments."
    )
    if "software systems and engineering experiments" not in meta_description.lower():
        meta_description = (
            meta_description.strip().removesuffix(".")
            + ". Software systems and engineering experiments."
        )

    ctx.update(
        {
            "is_homepage": False,
            "page_title": f"{page_heading} | Crank The Code",
            "og_title": f"{page_heading} | Crank The Code",
            "og_description": meta_description,
            "meta_description": meta_description,
            "canonical_url": absolute_url(get_site_url(request), "/portfolio"),
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Portfolio", "href": "/portfolio"},
            ],
            "page_heading": page_heading,
            "page_emoji": emoji or "🧩",
            "page_intro_html": intro_html,
            "flagship_entries": flagship,
            "portfolio_groups": groups,
        }
    )

    return templates.TemplateResponse(request, "portfolio.html", ctx)
