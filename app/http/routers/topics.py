"""Decision Architecture Patterns routes.

The former /topics and /decision-architecture surfaces were retired in the
Selected Essays restructure; their URLs 301 to /essays via the redirect
table in `app.http.redirects`.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.domain.tags import humanize_layer_slug
from app.domain.taxonomy import (
    PATTERNS_CAT_TAG,
    PATTERNS_FEATURED_SLUGS,
    PATTERNS_LAYER_EMOJIS,
    PATTERNS_LAYER_LABELS,
    PATTERNS_LAYER_ORDER,
)
from app.http.deps import get_blog_service, get_templates
from app.http.seo import absolute_url, get_site_url
from app.http.view_models.context import build_base_context
from app.http.view_models.leadership import (
    category_posts_grouped_by_layer,
    patterns_posts_for_layer,
    topic_layer_slug_for_route,
)
from app.http.view_models.posts import post_frontmatter_emoji_index
from app.http.view_models.sidebar import build_sidebar_categories
from app.services.blog_service import BlogService

router = APIRouter()

# Repeated verbatim across the Open Graph, meta and body descriptions,
# which is how three copies of one sentence drift apart.
_PATTERNS_DESCRIPTION = (
    "Reusable organisational design patterns derived from Decision "
    "Architecture thinking."
)


@router.get("/patterns", response_class=HTMLResponse)
async def patterns_index(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    """Gateway page for Decision Architecture Patterns."""

    ctx = build_base_context(request)
    ctx["sidebar_categories"] = build_sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    emoji_index = post_frontmatter_emoji_index(blog)
    groups = category_posts_grouped_by_layer(
        blog,
        cat_tag=PATTERNS_CAT_TAG,
        layer_label_overrides=PATTERNS_LAYER_LABELS,
    )

    # "Start here" featured row: resolved in PATTERNS_FEATURED_SLUGS order,
    # skipping any slug that no longer exists so the row degrades quietly.
    by_slug = {str(p.slug or "").strip().lower(): p for p in blog.list_posts()}
    featured = [
        {
            "slug": p.slug,
            "title": p.title,
            "one_liner": getattr(p, "one_liner", None),
            "emoji": getattr(p, "emoji", None),
        }
        for p in (by_slug.get(s.lower()) for s in PATTERNS_FEATURED_SLUGS)
        if p is not None
    ]

    layers = sorted(
        [
            {
                "layer": slug,
                "label": PATTERNS_LAYER_LABELS[slug],
                "emoji": PATTERNS_LAYER_EMOJIS.get(slug, ""),
                "href": f"/patterns/{slug}",
            }
            for slug in PATTERNS_LAYER_ORDER
        ],
        key=lambda d: d["label"].lower(),
    )

    ctx.update(
        {
            "is_homepage": False,
            "page_title": "Decision Architecture Patterns | Crank The Code",
            "og_title": "Decision Architecture Patterns | Crank The Code",
            "og_description": _PATTERNS_DESCRIPTION,
            "meta_description": _PATTERNS_DESCRIPTION,
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Decision Architecture Patterns", "href": "/patterns"},
            ],
            "featured": featured,
            "layers": layers,
            "groups": groups,
            "emoji_index": emoji_index,
        }
    )

    return templates.TemplateResponse(request, "patterns_index.html", ctx)


@router.get("/patterns/{layer_slug}", response_class=HTMLResponse)
async def patterns_layer_page(
    request: Request,
    layer_slug: str,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    cleaned = topic_layer_slug_for_route(layer_slug)
    if cleaned == "general":
        label = "General"
    else:
        label = PATTERNS_LAYER_LABELS.get(cleaned, humanize_layer_slug(cleaned))

    posts = patterns_posts_for_layer(blog, layer_slug=cleaned)

    ctx = build_base_context(request)
    ctx["sidebar_categories"] = build_sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    site_url = get_site_url(request)
    canonical_path = f"/patterns/{cleaned}"
    canonical = absolute_url(site_url, canonical_path)

    ctx.update(
        {
            "is_homepage": False,
            "canonical_url": canonical,
            "page_title": f"{label} | Patterns | Crank The Code",
            "og_title": f"{label} | Patterns | Crank The Code",
            "og_description": f"Posts in {label} (Decision Architecture Patterns).",
            "meta_description": f"Posts in {label} (Decision Architecture Patterns).",
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Decision Architecture Patterns", "href": "/patterns"},
                {"label": label, "href": canonical_path},
            ],
            "hub": {"layer": cleaned, "label": label, "description": ""},
            "layers": sorted(
                [
                    {
                        "layer": slug,
                        "label": PATTERNS_LAYER_LABELS[slug],
                        "emoji": PATTERNS_LAYER_EMOJIS.get(slug, ""),
                        "href": f"/patterns/{slug}",
                    }
                    for slug in PATTERNS_LAYER_ORDER
                ],
                key=lambda d: d["label"].lower(),
            ),
            "current_layer": cleaned,
            "posts": posts,
        }
    )

    return templates.TemplateResponse(request, "patterns_hub.html", ctx)
