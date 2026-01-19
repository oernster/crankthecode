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
    # Homepage: keep it lightweight by rendering a short excerpt, not full content.
    # We already have `summary_html` from `blog.list_posts()`.
    def _html_to_text(html: str) -> str:
        # Good-enough tag strip for excerpts; avoids pulling in a full HTML parser.
        text = re.sub(r"<[^>]+>", "", html)
        return " ".join(text.split())

    posts = [
        {
            "slug": p.slug,
            "title": p.title,
            "date": p.date,
            "tags": list(p.tags),
            "cover_image_url": p.cover_image_url,
            "summary_text": _html_to_text(p.summary_html),
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
        "content": detail.content_html,
    }
    return templates.TemplateResponse("post.html", {"request": request, "post": post})
