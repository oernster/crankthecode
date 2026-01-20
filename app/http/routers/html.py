from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.http.deps import get_blog_service, get_templates
from app.http.seo import (
    DEFAULT_SITE_URL,
    absolute_url,
    build_meta_description,
    canonical_url_for_request,
    get_site_url,
    to_iso_date,
)
from app.services.blog_service import BlogService
from app.adapters.filesystem_posts_repository import FilesystemPostsRepository
from app.adapters.markdown_python_renderer import PythonMarkdownRenderer

router = APIRouter()


def _post_cover_index(blog: BlogService) -> dict[str, str]:
    """Map post slug -> cover_image_url (only when present)."""

    covers: dict[str, str] = {}
    for p in blog.list_posts():
        if p.cover_image_url:
            covers[p.slug] = p.cover_image_url
    return covers


def _post_thumb_index(blog: BlogService) -> dict[str, str]:
    """Map post slug -> thumb_image_url (only when present)."""

    thumbs: dict[str, str] = {}
    for p in blog.list_posts():
        thumb = getattr(p, "thumb_image_url", None)
        if thumb:
            thumbs[p.slug] = thumb
    return thumbs


def _post_blurb_index(blog: BlogService) -> dict[str, str]:
    """Map post slug -> blurb (only when present)."""

    blurbs: dict[str, str] = {}
    for p in blog.list_posts():
        blurb = getattr(p, "blurb", None)
        if blurb:
            blurbs[p.slug] = blurb
    return blurbs


def _sidebar_categories() -> list[dict[str, str]]:
    categories = [
        ("Python Projects", "python"),
        ("Django Projects", "django"),
        ("React Projects", "react"),
        ("3D Printing", "3d|printing|klipper"),
        ("MicroPython", "micropython"),
        ("Machine Learning", "machine learning|computer vision"),
    ]
    return [
        {
            "label": label,
            "query": query,
            "href": f"/posts?q={quote(query, safe='')}",
        }
        for (label, query) in categories
    ]


def _base_context(request: Request) -> dict:
    site_url = get_site_url(request)
    return {
        "request": request,
        "site_url": site_url,
        # Optional override for `<title>` in `base.html`.
        "page_title": None,
        "site_name": "CrankTheCode",
        "robots_meta": "index,follow",
        "canonical_url": canonical_url_for_request(request, site_url=site_url),
        "og_title": "CrankTheCode",
        "og_description": None,
        "og_type": "website",
        "og_image_url": absolute_url(site_url, "/static/images/me.jpg"),
        "jsonld_extra_json": None,
        "meta_description": "CrankTheCode — projects and technical write-ups by Oliver Ernster.",
        "sidebar_categories": _sidebar_categories(),
        "current_q": (request.query_params.get("q") or "").strip(),
        "breadcrumb_items": [
            {"label": "Home", "href": "/"},
        ],
    }


def _category_label_for_query(query: str) -> str | None:
    """Return the friendly sidebar label for an exact category query."""

    if not query:
        return None
    for c in _sidebar_categories():
        if c["query"] == query:
            return c["label"]
    return None


def _load_about_html() -> str:
    """Render the About me markdown into HTML.

    This is intentionally loaded directly from the posts directory so it can be
    used on a dedicated page without appearing in the main post index or RSS.
    """

    try:
        repo = FilesystemPostsRepository(posts_dir=Path("posts"))
        about_post = repo.get_post("about-me")
        if about_post is None:
            return ""
        return PythonMarkdownRenderer().render(about_post.content_markdown)
    except Exception:
        # Fail open: pages should still render if about content can't be loaded.
        return ""


@router.get("/", response_class=HTMLResponse)
async def homepage(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    ctx = _base_context(request)
    cover_index = _post_cover_index(blog)
    thumb_index = _post_thumb_index(blog)
    blurb_index = _post_blurb_index(blog)
    ctx.update(
        {
            "is_homepage": True,
            "og_title": "CrankTheCode",
            "og_description": "Projects and technical write-ups by Oliver Ernster.",
            "breadcrumb_items": [{"label": "Home", "href": "/"}],
            "homepage_projects": {
                "featured": [
                    {"slug": "stellody", "label": "Stellody"},
                    {"slug": "3D-printing-info", "label": "3D Printing Info"},
                    {"slug": "calendifier", "label": "Calendifier"},
                    {"slug": "trainer", "label": "Trainer"},
                    {"slug": "axisdb", "label": "AxisDB"},
                    {"slug": "edcolonizationasst", "label": "EDColonizationAsst"},
                ],
                "backlog": [
                    {"slug": "3D-printer-launcher", "label": "3D Printer Launcher"},
                    {"slug": "audiodeck", "label": "Audio Deck"},
                    {"slug": "elevator", "label": "Elevator"},
                    {"slug": "fancy-clock", "label": "Fancy Clock"},
                    {"slug": "galacticunicorn", "label": "Galactic Unicorn"},
                    {"slug": "numismatism", "label": "Numismatism"},
                    {"slug": "snarkapi", "label": "SnarkAPI"},
                ],
            },
            "homepage_cover_index": cover_index,
            "homepage_thumb_index": thumb_index,
            "homepage_blurb_index": blurb_index,
        }
    )

    # Bonus SEO sauce: SoftwareApplication schema (site-level, for rich previews/search).
    homepage_jsonld = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "CrankTheCode",
        "url": absolute_url(get_site_url(request), "/"),
        "author": {"@type": "Person", "name": "Oliver Ernster"},
    }
    ctx["jsonld_extra_json"] = json.dumps(
        homepage_jsonld, ensure_ascii=False, separators=(",", ":")
    )

    return templates.TemplateResponse(request, "index.html", ctx)


@router.get("/posts", response_class=HTMLResponse)
async def posts_index(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    posts = [
        {
            "slug": p.slug,
            "title": p.title,
            "date": p.date,
            "tags": list(p.tags),
            "blurb": getattr(p, "blurb", None),
            "one_liner": getattr(p, "one_liner", None),
            "cover_image_url": p.cover_image_url,
            "thumb_image_url": getattr(p, "thumb_image_url", None),
            # Keep links in summaries clickable.
            "summary_html": p.summary_html,
        }
        for p in blog.list_posts()
    ]
    ctx = _base_context(request)
    current_q = ctx.get("current_q", "")
    category_label = _category_label_for_query(current_q)
    filtered_href = (
        f"/posts?q={quote(current_q, safe='')}" if current_q else "/posts"
    )
    ctx.update(
        {
            "posts": posts,
            "is_homepage": False,
            "page_title": "Posts | CrankTheCode",
            "og_title": "Posts | CrankTheCode",
            "og_description": "Browse all CrankTheCode posts and project write-ups.",
            "meta_description": "Browse all CrankTheCode posts and project write-ups.",
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Posts", "href": "/posts"},
                *(
                    [
                        {
                            "label": category_label or current_q,
                            "href": filtered_href,
                        }
                    ]
                    if current_q
                    else []
                ),
            ],
        }
    )
    return templates.TemplateResponse(request, "posts.html", ctx)


@router.get("/about", response_class=HTMLResponse)
async def about_page(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
):
    ctx = _base_context(request)
    ctx.update(
        {
            "about_html": _load_about_html(),
            "is_homepage": False,
            "page_title": "About me | CrankTheCode",
            "og_title": "About me | CrankTheCode",
            "og_description": "About Oliver Ernster and the CrankTheCode blog.",
            "meta_description": "About Oliver Ernster and the CrankTheCode blog.",
            "back_link_href": "/",
            "back_link_label": "← Back to posts",
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "About", "href": "/about"},
            ],
        }
    )
    return templates.TemplateResponse(request, "about.html", ctx)


@router.get("/help", response_class=HTMLResponse)
async def help_page(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
):
    ctx = _base_context(request)
    ctx.update(
        {
            "is_homepage": False,
            "robots_meta": "noindex",
            "page_title": "Help | CrankTheCode",
            "og_title": "Help | CrankTheCode",
            "og_description": "A deliberately unhelpful help page.",
            "meta_description": "Help page for CrankTheCode.",
            "back_link_href": "/",
            "back_link_label": "← Back to home",
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Help", "href": "/help"},
            ],
        }
    )
    return templates.TemplateResponse(request, "help.html", ctx)


@router.get("/posts/{slug}", response_class=HTMLResponse)
async def read_post(
    request: Request,
    slug: str,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    detail = blog.get_post(slug)
    if detail is None:
        return HTMLResponse(content="<h1>404 - Post Not Found</h1>", status_code=404)

    # Keep template compatibility: templates expect `post.content`.
    post = {
        "slug": detail.slug,
        "title": detail.title,
        "date": detail.date,
        "tags": list(detail.tags),
        "blurb": getattr(detail, "blurb", None),
        "one_liner": getattr(detail, "one_liner", None),
        "cover_image_url": detail.cover_image_url,
        "extra_image_urls": list(getattr(detail, "extra_image_urls", [])),
        "content": detail.content_html,
    }
    ctx = _base_context(request)

    # Post-specific SEO.
    site_url = ctx.get("site_url") or DEFAULT_SITE_URL
    canonical = canonical_url_for_request(request, site_url=site_url)
    # SEO meta description: keep it stable and concise; tests expect blurb first.
    description = build_meta_description(
        getattr(detail, "blurb", None),
        fallback=getattr(detail, "one_liner", None),
        default=f"Read {detail.title} on CrankTheCode.",
    )

    # Social previews: one-liner reads better when shared.
    og_description = build_meta_description(
        getattr(detail, "one_liner", None),
        fallback=getattr(detail, "blurb", None),
        default=description,
    )

    subtitle = (getattr(detail, "one_liner", None) or getattr(detail, "blurb", None) or "").strip()
    og_title = f"{detail.title} - {subtitle}" if subtitle else detail.title

    og_image = (
        getattr(detail, "social_image_url", None)
        or detail.cover_image_url
        or absolute_url(site_url, "/static/images/me.jpg")
    )
    og_image = absolute_url(site_url, og_image)

    # Bonus SEO sauce: for project posts, add SoftwareApplication schema.
    is_project = bool(getattr(detail, "one_liner", None) or getattr(detail, "blurb", None))
    if is_project:
        app_jsonld = {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": detail.title,
            "operatingSystem": "Cross-platform",
            "applicationCategory": "Developer Tool",
            "description": og_description,
            "author": {"@type": "Person", "name": "Oliver Ernster"},
            "url": canonical,
        }
        ctx["jsonld_extra_json"] = json.dumps(
            app_jsonld, ensure_ascii=False, separators=(",", ":")
        )

    published_iso = to_iso_date(detail.date)
    jsonld: dict[str, object] = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": detail.title,
        "author": {"@type": "Person", "name": "Oliver Ernster"},
        "mainEntityOfPage": canonical,
    }
    if published_iso:
        jsonld["datePublished"] = published_iso
    if detail.cover_image_url:
        jsonld["image"] = [absolute_url(site_url, detail.cover_image_url)]

    ctx.update(
        {
            "post": post,
            "is_homepage": False,
            "page_title": f"{og_title} | CrankTheCode",
            "canonical_url": canonical,
            "meta_description": description,
            "og_title": og_title,
            "og_description": og_description,
            "og_type": "article",
            "og_image_url": og_image,
            "jsonld_json": json.dumps(jsonld, ensure_ascii=False, separators=(",", ":")),
            "back_link_href": "/posts",
            "back_link_label": "← Back to posts",
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Posts", "href": "/posts"},
                {"label": detail.title, "href": f"/posts/{detail.slug}"},
            ],
        }
    )
    return templates.TemplateResponse(request, "post.html", ctx)
