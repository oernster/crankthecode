from __future__ import annotations

import re

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.http.deps import get_blog_service, get_templates
from app.services.blog_service import BlogService

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def homepage(
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
            # Keep links in summaries clickable on the homepage.
            "summary_html": p.summary_html,
        }
        for p in blog.list_posts()
    ]
    return templates.TemplateResponse(
        "index.html", {"request": request, "posts": posts}
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
