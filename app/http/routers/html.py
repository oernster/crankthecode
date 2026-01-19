from __future__ import annotations

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
    # Keep template compatibility: templates expect `post.summary`.
    posts = [
        {
            "slug": p.slug,
            "title": p.title,
            "date": p.date,
            "tags": list(p.tags),
            "summary": p.summary_html,
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
        "content": detail.content_html,
    }
    return templates.TemplateResponse("post.html", {"request": request, "post": post})
