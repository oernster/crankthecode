from __future__ import annotations

"""Misc page routes: homepage, about, explore, battlestation, redirects."""

import json

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.domain.books_catalogue import BOOKS_CATALOGUE
from app.domain.books_compilations import COMPLETE_SERIES_EDITION
from app.http.deps import get_blog_service, get_templates
from app.http.jsonld import build_person_jsonld
from app.http.seo import absolute_url, canonical_url_for_request, get_site_url
from app.http.view_models.context import build_base_context, load_about_html
from app.http.view_models.leadership import (
    build_leadership_topic_hubs,
    homepage_leadership_items,
    topic_posts_for_layer,
)
from app.http.view_models.posts import (
    estimate_read_time_from_template,
    estimate_read_time_minutes,
    post_blurb_index,
    post_cover_index,
    post_frontmatter_emoji_index,
    post_thumb_index,
)
from app.http.view_models.sidebar import build_sidebar_categories
from app.services.blog_service import BlogService

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def homepage(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    ctx = build_base_context(request)
    ctx["sidebar_categories"] = build_sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )
    cover_index = post_cover_index(blog)
    thumb_index = post_thumb_index(blog)
    blurb_index = post_blurb_index(blog)
    emoji_index = post_frontmatter_emoji_index(blog)

    site_url = get_site_url(request)
    canonical = canonical_url_for_request(request, site_url=site_url)
    homepage_meta = {
        "is_homepage": True,
        "page_title": "Oliver Ernster - Principal Engineer and Decision Architect",
        "og_title": "Oliver Ernster | Crank The Code",
        "og_description": (
            "Oliver Ernster is a principal engineer and decision architect "
            "writing on structural system design, authority boundaries and backend "
            "engineering."
        ),
        "meta_description": (
            "Oliver Ernster is a principal engineer and decision architect "
            "writing on structural system design, authority boundaries and backend "
            "engineering."
        ),
        "canonical_url": canonical,
        "og_image_url": "",
    }

    ctx.update(
        {
            "breadcrumb_items": [{"label": "Home", "href": "/"}],
            "homepage_projects": {
                "leadership": homepage_leadership_items(blog),
            },
            "homepage_cover_index": cover_index,
            "homepage_thumb_index": thumb_index,
            "homepage_blurb_index": blurb_index,
            "homepage_emoji_index": emoji_index,
            "books": BOOKS_CATALOGUE,
            "complete_series_edition": COMPLETE_SERIES_EDITION,
        }
    )

    home = absolute_url(site_url, "/")
    person_jsonld = build_person_jsonld(site_url=site_url)

    homepage_jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{home}#website",
                "name": "Crank The Code",
                "url": home,
                "author": {"@id": f"{home}#oliver-ernster"},
                "mainEntity": {"@id": f"{home}#oliver-ernster"},
            },
            person_jsonld,
        ],
    }
    ctx["jsonld_json"] = json.dumps(
        homepage_jsonld, ensure_ascii=False, separators=(",", ":")
    )
    ctx["jsonld_extra_json"] = None
    ctx.update(homepage_meta)

    return templates.TemplateResponse(request, "index.html", ctx)


@router.get("/about", response_class=HTMLResponse)
async def about_page(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    ctx = build_base_context(request)
    ctx["sidebar_categories"] = build_sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    site_url = get_site_url(request)
    canonical = absolute_url(site_url, "/about")
    home = absolute_url(site_url, "/")

    about_page_jsonld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "@id": f"{canonical}#webpage",
        "url": canonical,
        "name": "About Oliver Ernster",
        "about": {"@id": f"{home}#oliver-ernster"},
        "isPartOf": {"@id": f"{home}#website"},
    }

    breadcrumb_jsonld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": absolute_url(site_url, "/"),
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "About",
                "item": canonical,
            },
        ],
    }

    about_html = load_about_html()
    ctx.update(
        {
            "about_html": about_html,
            "topic_hubs": build_leadership_topic_hubs(blog),
            "is_homepage": False,
            "page_title": "About Oliver Ernster | Principal Engineer and Decision Architect",
            "og_title": "About Oliver Ernster",
            "og_description": "Oliver Ernster is a principal engineer and decision architect focused on reducing organisational and technical risk through earlier, clearer decisions.",
            "meta_description": "Oliver Ernster is a principal engineer and decision architect focused on reducing organisational and technical risk through earlier, clearer decisions.",
            "back_link_href": "/",
            "back_link_label": "← Back to home",
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "About", "href": "/about"},
            ],
            "show_read_time": True,
            "read_time_minutes": estimate_read_time_minutes(about_html),
        }
    )

    ctx["jsonld_json"] = json.dumps(
        about_page_jsonld, ensure_ascii=False, separators=(",", ":")
    )
    ctx["jsonld_extra_json"] = json.dumps(
        {
            "@context": "https://schema.org",
            "@graph": [
                build_person_jsonld(site_url=site_url),
                breadcrumb_jsonld,
            ],
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return templates.TemplateResponse(request, "about.html", ctx)


@router.get("/about/oliver-ernster", include_in_schema=False)
async def about_oliver_ernster_redirect(request: Request):
    """Alias route to strengthen entity discoverability. Canonical remains `/about`."""
    return RedirectResponse(url="/about", status_code=301)


@router.get("/about-me", include_in_schema=False)
async def about_me_redirect(request: Request):
    """Common URL guess for the about page. Canonical remains `/about`."""
    return RedirectResponse(url="/about", status_code=301)


@router.get("/start-here", include_in_schema=False)
async def start_here_redirect(request: Request):
    """Guessable top-level alias. Canonical lives at `/posts/start-here`."""
    return RedirectResponse(url="/posts/start-here", status_code=301)


@router.get("/governance", include_in_schema=False)
async def governance_redirect(request: Request):
    """Guessable top-level alias for the Governance writing section."""
    return RedirectResponse(url="/posts?view=writing&cat=Governance", status_code=301)


@router.get("/writing", include_in_schema=False)
async def writing_redirect(request: Request):
    """Guessable top-level alias for the Writing section."""
    return RedirectResponse(url="/posts?view=writing", status_code=301)


@router.get("/help", response_class=HTMLResponse)
async def help_page(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    # Legacy route retired: permanently redirect to the Explore surface.
    return RedirectResponse(url="/explore", status_code=301)


@router.get("/explore", response_class=HTMLResponse)
async def explore_page(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    ctx = build_base_context(request)
    ctx["sidebar_categories"] = build_sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    hubs = build_leadership_topic_hubs(blog)
    recommendations: list[dict[str, object]] = []
    for h in hubs:
        layer = str(h.get("layer") or "").strip()
        layer_posts = topic_posts_for_layer(blog, layer_slug=layer)[:3]
        recommendations.append(
            {
                "layer": layer,
                "label": h.get("label"),
                "href": h.get("href"),
                "posts": layer_posts,
            }
        )

    ctx.update(
        {
            "is_homepage": False,
            "page_title": "Explore | Crank The Code",
            "og_title": "Explore | Crank The Code",
            "og_description": "Orientation and themes to explore on Crank The Code.",
            "meta_description": "Explore orientation and themes on Crank The Code.",
            "back_link_href": "/",
            "back_link_label": "← Back to home",
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Explore", "href": "/explore"},
            ],
            "start_here": {
                "author_href": "/about",
                "topics_href": "/topics",
                "topic_hubs": hubs,
                "recommended_by_topic": recommendations,
            },
        }
    )
    return templates.TemplateResponse(request, "explore.html", ctx)


@router.get("/battlestation", include_in_schema=False)
async def battlestation_redirect(request: Request):
    """Legacy URL. Canonical post now lives at /posts/battlestation."""
    return RedirectResponse(url="/posts/battlestation", status_code=301)
