from __future__ import annotations

import re
from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.http.deps import get_blog_service, get_templates
from app.services.blog_service import BlogService
from app.adapters.filesystem_posts_repository import FilesystemPostsRepository
from app.adapters.markdown_python_renderer import PythonMarkdownRenderer

router = APIRouter()


def _load_about_html() -> str:
    """Render the About Me markdown into HTML.

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
    templates: Jinja2Templates = Depends(get_templates),
):
    return templates.TemplateResponse("index.html", {"request": request})


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
            "cover_image_url": p.cover_image_url,
            # Keep links in summaries clickable.
            "summary_html": p.summary_html,
        }
        for p in blog.list_posts()
    ]
    return templates.TemplateResponse(
        "posts.html", {"request": request, "posts": posts}
    )


@router.get("/about", response_class=HTMLResponse)
async def about_page(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
):
    return templates.TemplateResponse(
        "about.html",
        {
            "request": request,
            "about_html": _load_about_html(),
        },
    )


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
        "cover_image_url": detail.cover_image_url,
        "extra_image_urls": list(getattr(detail, "extra_image_urls", [])),
        "content": detail.content_html,
    }
    return templates.TemplateResponse("post.html", {"request": request, "post": post})
