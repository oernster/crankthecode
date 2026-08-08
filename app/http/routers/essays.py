"""Selected Essays and Build Log routes.

/essays is the curated Decision Architecture essay set (fixed editorial
grouping from `app.domain.essays`). /build-log is everything else with a
date: the running record of applications, tooling and hardware write-ups.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.domain.essays import CRYSTAL_SLUG, ESSAY_GROUPS, ESSAY_SLUGS
from app.http.deps import get_blog_service, get_templates
from app.http.view_models.context import build_base_context
from app.http.view_models.sidebar import build_sidebar_categories
from app.services.blog_service import BlogService

router = APIRouter()

_ESSAYS_DESCRIPTION = (
    "The Decision Architecture thesis, in essay form: structure determines "
    "outcomes, authority is a design material and decision latency is the "
    "performance problem underneath most others."
)

_BUILD_LOG_DESCRIPTION = (
    "A running, dated record of what Oliver Ernster is making: applications, "
    "tooling, 3D printing and this site itself."
)

_HIDDEN_SLUGS = frozenset({"about-me", "about", "start-here", "portfolio"})
_EXCLUDED_CAT_TAGS = frozenset({"cat:leadership", "cat:decision-architecture-patterns"})


def _post_summary(p: object) -> dict[str, object]:
    return {
        "slug": getattr(p, "slug", ""),
        "title": getattr(p, "title", ""),
        "date": str(getattr(p, "date", "") or ""),
        "one_liner": getattr(p, "one_liner", None),
        "blurb": getattr(p, "blurb", None),
        "emoji": getattr(p, "emoji", None),
    }


def essay_groups_with_posts(blog: BlogService) -> list[dict[str, object]]:
    """Resolve the fixed essay grouping against the post repository."""

    by_slug = {str(p.slug or "").strip().lower(): p for p in blog.list_posts()}
    groups: list[dict[str, object]] = []
    for heading, slugs in ESSAY_GROUPS:
        posts = [_post_summary(by_slug[s]) for s in slugs if s in by_slug]
        groups.append({"label": heading, "posts": posts})
    return groups


def build_log_posts(blog: BlogService) -> list[dict[str, object]]:
    """Every dated post that is not an essay, a pattern or a site page."""

    out: list[dict[str, object]] = []
    for p in blog.list_posts():
        slug = str(getattr(p, "slug", "") or "").strip().lower()
        if slug in _HIDDEN_SLUGS:
            continue
        if slug in ESSAY_SLUGS or slug == CRYSTAL_SLUG:
            continue
        tags = {str(t or "").strip().lower() for t in (getattr(p, "tags", None) or [])}
        if tags & _EXCLUDED_CAT_TAGS:
            continue
        out.append(_post_summary(p))

    out.sort(key=lambda i: str(i.get("date", "")), reverse=True)
    return out


@router.get("/essays", response_class=HTMLResponse)
async def essays_page(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    ctx = build_base_context(request)
    ctx["sidebar_categories"] = build_sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )
    ctx.update(
        {
            "is_homepage": False,
            "page_title": "Selected Essays | Crank The Code",
            "og_title": "Selected Essays | Crank The Code",
            "og_description": _ESSAYS_DESCRIPTION,
            "meta_description": _ESSAYS_DESCRIPTION,
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Selected Essays", "href": "/essays"},
            ],
            "groups": essay_groups_with_posts(blog),
        }
    )
    return templates.TemplateResponse(request, "essays.html", ctx)


@router.get("/build-log", response_class=HTMLResponse)
async def build_log_page(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    ctx = build_base_context(request)
    ctx["sidebar_categories"] = build_sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )
    ctx.update(
        {
            "is_homepage": False,
            "page_title": "Build Log | Crank The Code",
            "og_title": "Build Log | Crank The Code",
            "og_description": _BUILD_LOG_DESCRIPTION,
            "meta_description": _BUILD_LOG_DESCRIPTION,
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Build Log", "href": "/build-log"},
            ],
            "posts": build_log_posts(blog),
        }
    )
    return templates.TemplateResponse(request, "build_log.html", ctx)
